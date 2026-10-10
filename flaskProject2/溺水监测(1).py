import cv2
import numpy as np
import time
from ultralytics import YOLO
import winsound
import tkinter as tk
from tkinter import font

# 加载YOLOv8姿态模型
model = YOLO('yolov8n-pose.pt')

# 摄像头编号
camera_no = 0

# 打开摄像头
cap = cv2.VideoCapture(camera_no)
if not cap.isOpened():
    print("无法打开摄像头")
    exit()

# 挥手检测参数
threshold = 12
frames = 5  # 挥手检测所需帧数，同时作为轨迹记录帧数
hand_history = []
last_alarm_time = 0
alarm_cooldown = 5

# 轨迹记录参数（与挥手检测帧数保持一致）
wrist_trail = []  # 存储轨迹点

# 关键点配置（只关注手腕）
LEFT_WRIST = 9
RIGHT_WRIST = 10
KEYPOINT_CONF_THRESH = 0.4
HIDE_KEYPOINTS = [i for i in range(17) if i not in (LEFT_WRIST, RIGHT_WRIST)]

# 存储上一次检测到的手腕位置，初始化为屏幕中心
last_known_wrists = [(320, 240)]  # 默认值，假设640x480分辨率的中心

def is_waving(pos_list, threshold, frames):

    d_list = []
    for i in range(1, len(pos_list)):
        dx = abs(pos_list[i][0] - pos_list[i - 1][0])
        dy = abs(pos_list[i][1] - pos_list[i - 1][1])
        d_list.append(np.sqrt(dx*dx + dy*dy))

    cnt = 0
    for d in d_list:
        if d > threshold:
            cnt += 1
            if cnt >= frames:
                return True

    return False

def show_alert(message):
    root = tk.Tk()
    root.title("紧急报警")
    root.attributes("-topmost", True)
    root.geometry("600x300")
    root.configure(bg="#FFE6E6")

    alert_label = tk.Label(
        root, text=message,
        font=font.Font(size=28, weight="bold"),
        fg="#CC0000", bg="#FFE6E6",
        wraplength=550, justify="center"
    )
    alert_label.pack(pady=40)

    tk.Button(
        root, text="确定",
        font=font.Font(size=18),
        fg="#333", bg="#FFCCCC",
        activebackground="#FFB3B3",
        padx=20, pady=5,
        command=root.destroy
    ).pack(pady=10)

    root.mainloop()


while True:
    res, frame = cap.read()
    if not res:
        print("无法获取图像帧，退出")
        break

    # 推理并获取原始结果
    results = model(frame, verbose=False)
    annotated_frame = frame.copy()
    keypoints = results[0].keypoints.data

    current_wrists = []
    if len(keypoints) > 0:
        person = keypoints[0]  # 取第一个人体

        # 绘制左手腕（绿色圆点）
        left = person[LEFT_WRIST]
        if left[2] > KEYPOINT_CONF_THRESH:
            lx, ly = int(left[0]), int(left[1])
            cv2.circle(annotated_frame, (lx, ly), 8, (0, 255, 0), -1)  # 实心绿点
            current_wrists.append((lx, ly))

        # 绘制右手腕（绿色圆点）
        right = person[RIGHT_WRIST]
        if right[2] > KEYPOINT_CONF_THRESH:
            rx, ry = int(right[0]), int(right[1])
            cv2.circle(annotated_frame, (rx, ry), 8, (0, 255, 0), -1)  # 实心绿点
            current_wrists.append((rx, ry))

    # 如果没有检测到手腕，使用上一次已知位置
    if not current_wrists:
        current_wrists = last_known_wrists.copy()
        # 绘制红色圆点表示使用的是固定位置
        for (x, y) in current_wrists:
            cv2.circle(annotated_frame, (x, y), 8, (0, 0, 255), -1)  # 实心红点
    else:
        # 更新上一次已知位置
        last_known_wrists = current_wrists.copy()

    # 计算平均手腕位置并添加到轨迹
    if current_wrists:
        avg_x = int(np.mean([w[0] for w in current_wrists]))
        avg_y = int(np.mean([w[1] for w in current_wrists]))

        # 添加当前平均位置到轨迹，轨迹长度与wave_frames保持一致
        wrist_trail.append((avg_x, avg_y))

        # 保持轨迹长度等于wave_frames
        if len(wrist_trail) > frames:
            wrist_trail.pop(0)

        # 绘制轨迹折线
        if len(wrist_trail) > 1:
            # 将轨迹点转换为适合cv2.polylines的格式
            points = np.array(wrist_trail, np.int32)
            points = points.reshape((-1, 1, 2))
            # 绘制蓝色轨迹线，线宽2
            cv2.polylines(annotated_frame, [points], isClosed=False, color=(255, 0, 0), thickness=2)

        # 更新手腕历史（用于挥手检测）
        hand_history.append((avg_x, avg_y))
        if len(hand_history) > 15:
            hand_history.pop(0)

    # 挥手检测与报警
    wave_detected = is_waving(hand_history, threshold, frames)
    print(wave_detected)
    current_time = time.time()

    if wave_detected and (current_time - last_alarm_time > alarm_cooldown):
        last_alarm_time = current_time
        winsound.Beep(1000, 500)
        show_alert("可能有人溺水，请立即处理！")

        cv2.putText(
            annotated_frame, "报警：检测到挥手动作",
            (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
            1.5, (0, 0, 255), 3
        )

    # 显示画面
    cv2.imshow("YOLOv8-pose 手腕检测与轨迹", annotated_frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
