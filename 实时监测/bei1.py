import cv2
import numpy as np
import time


from ultralytics import YOLO
import winsound
import tkinter as tk
from tkinter import font, ttk

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
KEYPOINT_CONF_THRESH = 0.5
HIDE_KEYPOINTS = [i for i in range(17) if i not in (LEFT_WRIST, RIGHT_WRIST)]

# 存储上一次检测到的手腕位置，初始化为屏幕中心
last_known_wrists = [(320, 240)]  # 默认值，假设640x480   分辨率的中心
def is_waving(pos_list, threshold, frames):
    d_list = []
    for i in range(1, len(pos_list)):
        d_list =  []
        dx = abs(pos_list[i][0] - pos_list[i - 1][0])
        dy = abs(pos_list[i][1] - pos_list[i - 1][1])
        d_list.append(np.sqrt(dx * dx + dy * dy))

    cnt = 0
    for d in d_list:
        if d > threshold:
            cnt += 1
            if cnt > frames:
                return True
    return False
def show_alert(message):
    root = tk.Tk()
    root.title("WARNING MESSAGE")
    root.attributes("-topmost", True)
    # 核心修改：缩小弹窗尺寸（从500x600改为400x450）
    root.geometry("400x450")
    root.configure(bg="#f5f5f5")
    root.resizable(False, False)

    # 顶部标题栏（缩小高度）
    top_frame = tk.Frame(root, bg="#333333", height=40)
    top_frame.pack(fill="x")
    # 缩小标题字体
    tk.Label(
        top_frame, text="WARNING MESSAGE",
        font=font.Font(size=14, weight="bold", family="Arial"),
        fg="white", bg="#333333"
    ).pack(side="left", padx=12, pady=10)
    # 模拟mac窗口按钮（缩小按钮尺寸）
    button_frame = tk.Frame(top_frame, bg="#333333")
    button_frame.pack(side="right", padx=8, pady=8)
    tk.Canvas(button_frame, width=10, height=10, bg="#ffcc00", highlightthickness=0, relief="raised", bd=1).pack(side="left", padx=2)
    tk.Canvas(button_frame, width=10, height=10, bg="#33cc33", highlightthickness=0, relief="raised", bd=1).pack(side="left", padx=2)
    tk.Canvas(button_frame, width=10, height=10, bg="#ff3333", highlightthickness=0, relief="raised", bd=1).pack(side="left", padx=2)

    # 红色警示区（缩小图标和文字）
    warning_frame = tk.Frame(root, bg="#ff3333")
    warning_frame.pack(fill="x", pady=0)
    # 缩小警示图标尺寸
    icon_canvas = tk.Canvas(warning_frame, width=80, height=80, bg="#ff3333", highlightthickness=0)
    icon_canvas.create_polygon(40, 8, 75, 75, 5, 75, fill="#ffcc00", outline="#ffcc00")
    icon_canvas.create_line(40, 20, 40, 55, width=6, fill="#333333")
    icon_canvas.create_oval(35, 60, 45, 70, fill="#333333")
    icon_canvas.pack(side="top", pady=15)
    # 缩小WARNING文字
    tk.Label(
        warning_frame, text="WARNING",
        font=font.Font(size=28, weight="bold", family="Arial"),
        fg="white", bg="#ff3333"
    ).pack(pady=8)

    # 内容区（缩小边距和字体）
    content_frame = tk.Frame(root, bg="white")
    content_frame.pack(fill="both", expand=True, padx=15, pady=15)
    tk.Label(
        content_frame, text=message,
        font=font.Font(family="微软雅黑", size=16, weight="bold"),
        fg="#333333", bg="white",
        wraplength=350, justify="center"
    ).pack(anchor="center", pady=15)

    # 按钮区（缩小按钮尺寸和边距）
    btn_frame = tk.Frame(root, bg="white")
    btn_frame.pack(fill="x", padx=15, pady=25)
    style = ttk.Style()
    style.configure("Warning.TButton",
                    font=font.Font(size=16, weight="bold", family="Arial"),
                    foreground="red",
                    background="#ff3333",
                    padding=12,
                    borderwidth=2,
                    relief="raised")
    style.map("Warning.TButton",
              background=[("active", "#cc0000"), ("pressed", "#990000")])
    ttk.Button(
        btn_frame, text="CANCEL",
        style="Warning.TButton",
        command=root.destroy
    ).pack(anchor="center", pady=8)

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


    def is_Waving(pos_list, threshold, frames):
        d_list = []  # 定义列表d_list用于存储挥手位移
        for i in range(1, len(pos_list)):  # 遍历手部位置
            dx = abs(pos_list[i][0] - pos_list[i - 1][0])  # 计算两帧间X轴方向手部位移
            dy = abs(pos_list[i][1] - pos_list[i - 1][1])  # 同样的，计算Y轴方向手部位移
            d_list.append(np.sqrt(dx * dx + dy * dy))  # 根据欧式距离计算公式得到手部位移

        cnt = 0  # 定义cnt记录挥手次数
        for d in d_list:  # 遍历挥手位移列表d_list
            if d > threshold:  # 当挥手位移超过阈值时
                cnt += 1  # 判定为一次挥手动作
                if cnt > frames:  # 当挥手动作超过指定次数时。
                    return True  # 判定人员溺水
        return False
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
    wave_detected = is_Waving(hand_history, threshold, frames)
    #print(wave_detected)
    current_time = time.time()

    if wave_detected and (current_time - last_alarm_time > alarm_cooldown):
        last_alarm_time = current_time
        # 增强报警音效（双频交替蜂鸣）
        winsound.Beep(1500, 300)
        winsound.Beep(2000, 300)
        winsound.Beep(1500, 300)
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