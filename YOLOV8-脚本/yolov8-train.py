from ultralytics import YOLO
if __name__ == '__main__':
    model = YOLO("yolov8n.pt")  # 加载预训练的YOLOv8n基础模型
    results = model.train(
        data = 'bvn.yaml',# 指定配置文件
        epochs=70,#设置训练轮数
        device=0,#设置训练设备
        batch=-1,#设置训练批次
        workers=0,#设置训练线程数
        half=True,#设置半精度训练
    )

