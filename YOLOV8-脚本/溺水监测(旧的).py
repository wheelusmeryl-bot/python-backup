import cv2
import numpy as np
import time
from ultralytics import YOLO
import winsound
import tkinter as tk
from tkinter import font

# 加载YOLOv8模型
model = YOLO('yolov8n.pt')

# 摄像头编号
camera_no = 0

# 打开摄像头
cap = cv2.VideoCapture(camera_no)

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("无法打开摄像头")
    exit()

# 挥手检测参数
wave_threshold = 15  # 挥手动作的位移阈值
wave_frames = 5  # 连续检测到挥手动作的帧数
hand_history = []  # 存储手部位置历史
wave_detected = False
alarm_triggered = False
alarm_cooldown = 5  # 报警冷却时间(秒)
last_alarm_time = 0


def is_waving(history, threshold, required_frames):
    """判断是否有挥手动作"""
    if len(history) < required_frames * 2:
        return False

    # 计算连续帧之间的手部位移
    movements = []
    for i in range(1, len(history)):
        dx = abs(history[i][0] - history[i - 1][0])
        dy = abs(history[i][1] - history[i - 1][1])
        movements.append(np.sqrt(dx * dx + dy * dy))

    # 检查是否有连续的明显位移
    consecutive_movements = 0
    for movement in movements:
        if movement > threshold:
            consecutive_movements += 1
            if consecutive_movements >= required_frames:
                return True
        else:
            consecutive_movements = 0

    return False


def show_alert(message):
    """优化后的美观报警弹窗"""
    root = tk.Tk()
    root.title("紧急报警")
    # 强制置顶，确保弹窗在最上层
    root.attributes("-topmost", True)
    # 调整弹窗尺寸，比例更协调
    root.geometry("600x300")
    # 设置背景色为浅红色，增强紧急感
    root.configure(bg="#FFE6E6")

    # 配置标签：字体大小适中、加粗，颜色搭配协调
    alert_label = tk.Label(
        root,
        text=message,
        font=font.Font(size=28, weight="bold"),
        fg="#CC0000",  # 深红色字体
        bg="#FFE6E6",  # 浅红色背景
        wraplength=550,
        justify="center"
    )
    alert_label.pack(pady=40)

    # 确认按钮：样式优化，增加交互反馈
    ok_btn = tk.Button(
        root,
        text="确定",
        font=font.Font(size=18),
        fg="#333333",  # 深灰色文字
        bg="#FFCCCC",  # 稍深的红色背景
        activebackground="#FFB3B3",  # 鼠标悬停时的背景色
        padx=20,
        pady=5,
        command=root.destroy
    )
    ok_btn.pack(pady=10)

    root.mainloop()


while True:
    # 获取图像帧
    res, frame = cap.read()

    # 如果读取失败，退出循环
    if not res:
        print("无法获取图像帧，退出程序")
        break

    # 正向推理
    results = model(frame)

    # 绘制结果
    annotated_frame = results[0].plot()

    # 检测人体和手部
    persons = results[0].boxes.data[results[0].boxes.cls == 0]  # 0 是 person 类别的索引

    current_hand_positions = []

    for person in persons:
        x1, y1, x2, y2, conf, cls = person
        if conf > 0.5:  # 置信度过滤
            # 大致估算手部位置（假设在身体上部两侧）
            left_hand_x = int(x1 + (x2 - x1) * 0.1)
            left_hand_y = int(y1 + (y2 - y1) * 0.4)
            right_hand_x = int(x2 - (x2 - x1) * 0.1)
            right_hand_y = int(y1 + (y2 - y1) * 0.4)

            current_hand_positions.append((left_hand_x, left_hand_y))
            current_hand_positions.append((right_hand_x, right_hand_y))

            # 绘制手部位置
            cv2.circle(annotated_frame, (left_hand_x, left_hand_y), 10, (0, 255, 0), -1)
            cv2.circle(annotated_frame, (right_hand_x, right_hand_y), 10, (0, 255, 0), -1)

    # 更新手部历史位置
    if current_hand_positions:
        # 取平均位置作为手部参考点
        avg_x = int(np.mean([pos[0] for pos in current_hand_positions]))
        avg_y = int(np.mean([pos[1] for pos in current_hand_positions]))
        hand_history.append((avg_x, avg_y))

        # 限制历史记录长度
        if len(hand_history) > 30:
            hand_history.pop(0)

        # 检测挥手动作
        wave_detected = is_waving(hand_history, wave_threshold, wave_frames)

    # 报警逻辑
    current_time = time.time()
    if wave_detected and (current_time - last_alarm_time > alarm_cooldown):
        alarm_triggered = True
        last_alarm_time = current_time

        # 播放报警声音
        winsound.Beep(1000, 500)  # 1000Hz 频率，持续 500ms

        # 显示自定义弹窗
        show_alert("有人溺水！请立即处理！")

        # 在图像上显示报警信息
        cv2.putText(
            annotated_frame,
            "挥手检测到！报警！",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,  # 调整字体大小
            (0, 0, 255),
            3  # 线条粗细
        )
    else:
        alarm_triggered = False

    # 显示带检测结果的图像
    cv2.imshow("YOLOv8 挥手检测报警系统", annotated_frame)

    # 按 ESC 键退出程序
    if cv2.waitKey(1) == 27:
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()
