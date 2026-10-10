import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QPushButton, QWidget, QLabel, QFileDialog, QSlider, QCheckBox)
from PyQt5.QtGui import QImage, QPixmap, QPainter, QFont, QColor
from PyQt5.QtCore import Qt, QTimer
from ultralytics import YOLO


class VideoRecognitionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YOLOv8 实时视频识别系统")
        self.setGeometry(100, 100, 1200, 800)

        # 初始化变量
        self.model = None
        self.cap = None
        self.timer = QTimer()
        self.is_recording = False
        self.detection_enabled = True
        self.confidence_threshold = 0.5
        self.classes_filter = []

        # 创建UI
        self.init_ui()

        # 连接信号与槽
        self.timer.timeout.connect(self.update_frame)

    def init_ui(self):
        # 主布局
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # 视频显示区域
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setMinimumSize(800, 600)
        self.video_label.setStyleSheet("background-color: #2c3e50; border-radius: 10px;")

        # 控制面板
        control_layout = QHBoxLayout()

        # 左侧控制按钮
        left_control = QVBoxLayout()

        self.load_model_btn = QPushButton("加载YOLOv8模型")
        self.load_model_btn.setStyleSheet(
            "background-color: #3498db; color: white; font-weight: bold; padding: 10px; border-radius: 5px;")
        self.load_model_btn.clicked.connect(self.load_model)

        self.camera_btn = QPushButton("打开摄像头")
        self.camera_btn.setStyleSheet(
            "background-color: #2ecc71; color: white; font-weight: bold; padding: 10px; border-radius: 5px;")
        self.camera_btn.clicked.connect(self.open_camera)

        self.stop_btn = QPushButton("停止")
        self.stop_btn.setStyleSheet(
            "background-color: #e74c3c; color: white; font-weight: bold; padding: 10px; border-radius: 5px;")
        self.stop_btn.clicked.connect(self.stop_camera)
        self.stop_btn.setEnabled(False)

        left_control.addWidget(self.load_model_btn)
        left_control.addWidget(self.camera_btn)
        left_control.addWidget(self.stop_btn)

        # 右侧控制选项
        right_control = QVBoxLayout()

        # 置信度阈值滑块
        confidence_layout = QHBoxLayout()
        confidence_label = QLabel("置信度阈值:")
        confidence_label.setStyleSheet("color: white; font-weight: bold;")
        self.confidence_slider = QSlider(Qt.Horizontal)
        self.confidence_slider.setRange(0, 100)
        self.confidence_slider.setValue(50)
        self.confidence_slider.valueChanged.connect(self.update_confidence)
        self.confidence_value = QLabel("0.50")
        self.confidence_value.setStyleSheet("color: white; font-weight: bold;")

        confidence_layout.addWidget(confidence_label)
        confidence_layout.addWidget(self.confidence_slider)
        confidence_layout.addWidget(self.confidence_value)

        # 检测开关
        self.detection_toggle = QCheckBox("启用目标检测")
        self.detection_toggle.setChecked(True)
        self.detection_toggle.setStyleSheet("color: white; font-weight: bold;")
        self.detection_toggle.stateChanged.connect(self.toggle_detection)

        # 状态信息
        self.status_label = QLabel("状态: 准备就绪")
        self.status_label.setStyleSheet("color: #f39c12; font-weight: bold; font-size: 14px;")
        self.fps_label = QLabel("FPS: 0.0")
        self.fps_label.setStyleSheet("color: #f39c12; font-weight: bold; font-size: 14px;")
        self.objects_label = QLabel("检测对象: 0")
        self.objects_label.setStyleSheet("color: #f39c12; font-weight: bold; font-size: 14px;")

        right_control.addLayout(confidence_layout)
        right_control.addWidget(self.detection_toggle)
        right_control.addWidget(self.status_label)
        right_control.addWidget(self.fps_label)
        right_control.addWidget(self.objects_label)

        # 添加控制面板到主布局
        control_layout.addLayout(left_control)
        control_layout.addLayout(right_control)

        # 添加组件到主布局
        main_layout.addWidget(self.video_label)
        main_layout.addLayout(control_layout)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # 设置样式
        self.setStyleSheet("background-color: #34495e;")

    def load_model(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "选择YOLOv8模型文件", "", "模型文件 (*.pt)")
            if file_path:
                self.model = YOLO(file_path)
                self.status_label.setText(f"状态: 已加载模型 {file_path.split('/')[-1]}")
                self.status_label.setStyleSheet("color: #2ecc71; font-weight: bold; font-size: 14px;")
        except Exception as e:
            self.status_label.setText(f"错误: {str(e)}")
            self.status_label.setStyleSheet("color: #e74c3c; font-weight: bold; font-size: 14px;")

    def open_camera(self):
        if self.model is None:
            self.status_label.setText("错误: 请先加载模型!")
            self.status_label.setStyleSheet("color: #e74c3c; font-weight: bold; font-size: 14px;")
            return

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.status_label.setText("错误: 无法打开摄像头!")
            self.status_label.setStyleSheet("color: #e74c3c; font-weight: bold; font-size: 14px;")
            return

        self.is_recording = True
        self.camera_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_label.setText("状态: 运行中 (摄像头)")
        self.status_label.setStyleSheet("color: #2ecc71; font-weight: bold; font-size: 14px;")

        self.timer.start(30)  # 大约33 FPS

    def stop_camera(self):
        if self.is_recording:
            self.timer.stop()
            self.cap.release()
            self.is_recording = False
            self.camera_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.status_label.setText("状态: 已停止")
            self.status_label.setStyleSheet("color: #f39c12; font-weight: bold; font-size: 14px;")

    def update_confidence(self, value):
        self.confidence_threshold = value / 100
        self.confidence_value.setText(f"{self.confidence_threshold:.2f}")

    def toggle_detection(self, state):
        self.detection_enabled = state == Qt.Checked

    def update_frame(self):
        if not self.is_recording or not self.cap.isOpened():
            return

        ret, frame = self.cap.read()
        if not ret:
            return

        # 计算FPS
        start_time = cv2.getTickCount()

        # 执行目标检测
        detected_frame = frame.copy()
        detected_count = 0

        if self.detection_enabled and self.model:
            # 使用YOLOv8进行检测
            results = self.model.predict(
                frame,
                conf=self.confidence_threshold,
                verbose=False
            )

            # 绘制检测结果
            for result in results:
                boxes = result.boxes.xyxy.cpu().numpy()
                confidences = result.boxes.conf.cpu().numpy()
                class_ids = result.boxes.cls.cpu().numpy().astype(int)

                detected_count = len(boxes)

                for i, box in enumerate(boxes):
                    x1, y1, x2, y2 = map(int, box)
                    confidence = confidences[i]
                    class_id = class_ids[i]
                    class_name = self.model.names[class_id]

                    # 绘制边界框
                    color = self.get_color(class_id)
                    cv2.rectangle(detected_frame, (x1, y1), (x2, y2), color, 2)

                    # 绘制标签背景
                    label = f"{class_name}: {confidence:.2f}"
                    (label_width, label_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
                    cv2.rectangle(detected_frame, (x1, y1 - 20), (x1 + label_width, y1), color, -1)

                    # 绘制标签文本
                    cv2.putText(detected_frame, label, (x1, y1 - 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        else:
            detected_frame = frame

        # 计算FPS
        end_time = cv2.getTickCount()
        fps = cv2.getTickFrequency() / (end_time - start_time)

        # 在帧上显示FPS
        cv2.putText(detected_frame, f"FPS: {fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(detected_frame, f"Objects: {detected_count}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        # 更新UI
        self.fps_label.setText(f"FPS: {fps:.1f}")
        self.objects_label.setText(f"检测对象: {detected_count}")

        # 将OpenCV图像转换为Qt图像
        rgb_image = cv2.cvtColor(detected_frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)

        # 缩放以适应标签大小
        self.video_label.setPixmap(pixmap.scaled(
            self.video_label.width(),
            self.video_label.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        ))

    def get_color(self, class_id):
        # 为不同的类生成不同的颜色
        colors = [
            (255, 0, 0),  # 红色
            (0, 255, 0),  # 绿色
            (0, 0, 255),  # 蓝色
            (255, 255, 0),  # 黄色
            (255, 0, 255),  # 紫色
            (0, 255, 255),  # 青色
            (255, 165, 0),  # 橙色
            (128, 0, 128),  # 深紫色
            (0, 128, 128),  # 青色
            (128, 128, 0)  # 橄榄色
        ]
        return colors[class_id % len(colors)]

    def closeEvent(self, event):
        if self.is_recording:
            self.stop_camera()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoRecognitionApp()
    window.show()
    sys.exit(app.exec_())