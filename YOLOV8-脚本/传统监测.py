import cv2
import tkinter as tk
from tkinter import font
import time


class HumanDetectionAlarm:
    def __init__(self):
        # 加载 Haar 级联分类器模型（人脸和全身）
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.body_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_fullbody.xml'
        )

        # 报警相关状态变量
        self.alarm_active = False
        self.last_alarm_time = 0
        self.alarm_cooldown = 10  # 报警冷却时间，单位：秒
        self.alert_window = None  # 用于存储报警弹窗实例

        # 初始化摄像头
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception("无法打开摄像头，请检查设备连接或权限！")

    def show_alert_popup(self):
        """显示报警弹窗，处理弹窗创建和冷却逻辑"""
        current_time = time.time()
        # 检查冷却时间和弹窗是否已存在
        if (current_time - self.last_alarm_time > self.alarm_cooldown) and \
                (self.alert_window is None or not self.alert_window.winfo_exists()):
            self.last_alarm_time = current_time
            # 创建顶级弹窗
            self.alert_window = tk.Toplevel()
            self.alert_window.title("人员检测报警")
            self.alert_window.geometry("400x200")
            self.alert_window.configure(bg="#FFE6E6")
            self.alert_window.attributes("-topmost", True)  # 窗口置顶

            # 设置字体
            alert_font = font.Font(family="SimSun", size=14, weight="bold")

            # 添加报警提示标签
            tk.Label(
                self.alert_window,
                text="⚠️ 检测到人员出现！ ⚠️",
                font=alert_font,
                fg="#D8000C",
                bg="#FFE6E6"
            ).pack(pady=20)

            # 确认按钮，点击关闭弹窗
            def close_popup():
                self.alert_window.destroy()
                self.alert_window = None

            tk.Button(
                self.alert_window,
                text="确认",
                command=close_popup,
                font=alert_font,
                bg="#FFB3B3",
                fg="black"
            ).pack(pady=10)

    def detect_humans(self, frame):
        """检测画面中的人体（人脸或全身），并绘制检测框用于调试"""
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 检测全身
        bodies = self.body_cascade.detectMultiScale(
            gray_frame,
            scaleFactor=1.1,
            minNeighbors=5
        )
        for (x, y, w, h) in bodies:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 检测人脸
        faces = self.face_cascade.detectMultiScale(
            gray_frame,
            scaleFactor=1.1,
            minNeighbors=5
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # 只要检测到人脸或全身其一就返回检测到人员
        return len(bodies) > 0 or len(faces) > 0

    def run_detection(self):
        """运行主循环，处理摄像头读取、检测和显示逻辑"""
        print("开始人员检测监控... 按 'q' 键退出程序")
        # 初始化 Tkinter 主窗口（用于支撑弹窗）
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口，仅用其事件循环

        try:
            while True:
                # 读取摄像头画面
                ret, frame = self.cap.read()
                if not ret:
                    print("无法获取摄像头画面，将退出循环！")
                    break

                # 执行人体检测
                human_detected = self.detect_humans(frame)

                # 检测到人员且满足条件时显示报警弹窗
                if human_detected:
                    self.show_alert_popup()
                    # 在画面上叠加报警文字
                    cv2.putText(
                        frame,
                        "检测到人员！",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 0, 255),
                        2
                    )

                # 显示带检测结果的画面
                cv2.imshow("人员检测监控画面", frame)

                # 处理按键事件，按 'q' 退出
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                # 让 Tkinter 处理潜在的弹窗事件（关键：确保弹窗能正常显示和交互）
                root.update()

        finally:
            # 释放资源
            self.cap.release()
            cv2.destroyAllWindows()
            root.destroy()  # 销毁 Tkinter 主窗口


if __name__ == "__main__":
    try:
        alarm_system = HumanDetectionAlarm()
        alarm_system.run_detection()
    except Exception as e:
        print(f"程序运行出错：{str(e)}")