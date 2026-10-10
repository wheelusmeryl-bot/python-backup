import numpy as np
from flask import Flask, render_template, Response, jsonify, request
import cv2
import time
import threading
from flask_cors import CORS
from ultralytics import YOLO  # 修改1: 导入YOLOv8的YOLO类
from water_level_predictor import WaterLevelPredictor
import pygame
from threading import Lock

result_name = "None"

def is_waving(hand_history, threshold, frames):
    if len(hand_history) < 2:  # 至少需要2个点才能计算距离
        return False
    # 计算每帧之间的移动距离
    d_list = []
    for i in range(1, len(hand_history)):
        dx = abs(hand_history[i][0] - hand_history[i - 1][0])
        dy = abs(hand_history[i][1] - hand_history[i - 1][1])
        d_list.append(np.sqrt(dx * dx + dy * dy))

    # 统计超过阈值的帧数
    cnt = 0
    for d in d_list:
        if d > threshold:
            cnt += 1
            if cnt > frames:
                return True
    return False

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.model = YOLO('F:/python/flaskProject2/static/yolov8n-pose.pt')
        self.conf_thres = 0.5
        # 初始化一个默认的黑色帧，用于摄像头读取失败时
        self.default_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(self.default_frame, "Camera Error", (100, 240),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        # 挥手检测参数
        self.threshold = 24
        self.frames = 5
        self.hand_history = []
        self.last_alarm_time = 0
        self.alarm_cooldown = 5
        self.wrist_trail = []
        self.last_known_wrists = [(320, 240)]
        self.result_name = "None"
        self.lock = Lock()

        # 初始化音频
        pygame.mixer.init()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        global result_name
        success, frame = self.video.read()
        if not success:
            frame = self.default_frame.copy()

        # 创建两个图像副本：一个用于检测，一个用于显示
        detection_frame = frame.copy()
        display_frame = frame.copy()

        # YOLOv8推理
        results = self.model.predict(
            source=detection_frame,
            conf=self.conf_thres,
            verbose=False
        )[0]

        # 关键点配置
        LEFT_WRIST = 9
        RIGHT_WRIST = 10
        KEYPOINT_CONF_THRESH = 0.5

        # 处理关键点
        keypoints = results.keypoints
        current_wrists = []

        if keypoints is not None and len(keypoints.data) > 0:
            person = keypoints.data[0]  # 取第一个人体

            # 处理左手腕
            left = person[LEFT_WRIST]
            if left[2] > KEYPOINT_CONF_THRESH:
                lx, ly = int(left[0]), int(left[1])
                cv2.circle(display_frame, (lx, ly), 8, (0, 255, 0), -1)
                current_wrists.append((lx, ly))

            # 处理右手腕
            right = person[RIGHT_WRIST]
            if right[2] > KEYPOINT_CONF_THRESH:
                rx, ry = int(right[0]), int(right[1])
                cv2.circle(display_frame, (rx, ry), 8, (0, 255, 0), -1)
                current_wrists.append((rx, ry))

        # 如果没有检测到手腕，使用上一次已知位置
        if not current_wrists:
            current_wrists = self.last_known_wrists.copy()
            for (x, y) in current_wrists:
                cv2.circle(display_frame, (x, y), 8, (0, 0, 255), -1)
        else:
            self.last_known_wrists = current_wrists.copy()

        # 计算平均手腕位置并添加到轨迹
        if current_wrists:
            avg_x = int(np.mean([w[0] for w in current_wrists]))
            avg_y = int(np.mean([w[1] for w in current_wrists]))

            # 更新轨迹
            self.wrist_trail.append((avg_x, avg_y))
            if len(self.wrist_trail) > self.frames:
                self.wrist_trail.pop(0)

            # 绘制轨迹
            if len(self.wrist_trail) > 1:
                points = np.array(self.wrist_trail, np.int32)
                points = points.reshape((-1, 1, 2))
                cv2.polylines(display_frame, [points], isClosed=False, color=(255, 0, 0), thickness=2)

            # 更新手腕历史
            self.hand_history.append((avg_x, avg_y))
            if len(self.hand_history) > 15:
                self.hand_history.pop(0)

            # 挥手检测与报警
            wave_detected = is_waving(self.hand_history, self.threshold, self.frames)
            #print(wave_detected)
            current_time = time.time()
            result_name = "None"
            if wave_detected and (current_time - self.last_alarm_time > self.alarm_cooldown):
                result_name = "hand"
                    # 在非主线程中播放音频
                def play_alarm():
                    try:
                        pygame.mixer.music.load('F:/python/flaskProject2/static/warning.mp3')
                        pygame.mixer.music.play()
                        time.sleep(2)
                    except Exception as e:
                        print(f"音频播放失败: {e}")

                alarm_thread = threading.Thread(target=play_alarm)
                alarm_thread.daemon = True
                alarm_thread.start()

        # 添加状态文本
        cv2.putText(display_frame, f"Status: {self.result_name}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(display_frame, "Wrist Tracking", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        # 编码为JPEG
        _, jpeg = cv2.imencode('.jpg', display_frame)
        return jpeg.tobytes()


app = Flask(__name__)
CORS(app)  # 允许所有来源的跨域请求


@app.after_request
def add_cors_headers(response):
    # 允许所有来源
    response.headers['Access-Control-Allow-Origin'] = '*'
    # 允许的请求方法
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    # 允许的请求头
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


# 启用CORS，允许所有域名访问（生产环境建议指定域名）

@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    global result_name
    while True:
        start_t = time.time()
        frame = camera.get_frame()
        print(f"time: {time.time() - start_t:.3f}s")
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    def generate(camera):
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    return Response(generate(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


collected_data = []  # 数据收集器
predictor = None  # 预测器实例
predictorData = 0


@app.route('/predict', methods=['POST'])
def data_predict():
    global collected_data, predictor, predictorData

    # 1. 接收并处理数据
    int_str = request.json
    collected_data.append(int(int_str))
    # print(collected_data)
    # 2. 数据不足时返回收集状态
    if len(collected_data) < 16:
        return jsonify({
            "status": "collecting",
            "received": len(collected_data),
            "needed": 16 - len(collected_data)
        })
    del collected_data[0]
    # 3. 使用最新16个数据
    historical_data = np.array(collected_data[-16:])
    # print(historical_data)

    # 4. 初始化预测器（仅首次）
    if predictor is None:
        predictor = WaterLevelPredictor(
            window_size=5,
            hidden_layer_sizes=(10, 5),
            max_iter=10000,
            learning_rate_init=0.005
        )

    # 5. 训练并预测
    predictor.fit(historical_data)
    predictions = predictor.predict(future_steps=4)
    # print(predictions["predictions"])
    predictions_array = np.array(predictions["predictions"])
    print(predictions["predictions"])
    combined_data = np.concatenate([historical_data, predictions_array])
    predictorData = predictions_array[0]
    # 6. 直接返回预测结果数组（保持原始格式）
    return predictions["predictions"]


@app.route('/getdata')
def data():
    return str(predictorData)

@app.route('/predict_result')
def result():
    print(result_name)
    return str(result_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
