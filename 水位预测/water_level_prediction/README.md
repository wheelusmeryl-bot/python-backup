# 水位预测Web应用

这是一个基于BP神经网络的水位预测系统，提供Web界面进行交互。

## 项目结构

- `app.py`: Flask后端API
- `index.html`: 前端网页
- `BPnetwork.py`: 原始Python脚本
- `requirements.txt`: 项目依赖

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行应用

1. 启动后端服务:
   ```bash
   python app.py
   ```

2. 打开前端网页:
   在浏览器中打开 `index.html` 文件

3. 使用应用:
   - 在输入框中输入至少16个水位数据（用空格分隔）
   - 点击"开始预测"按钮
   - 查看预测结果、图表和预警信息

## API接口

### 预测接口

- **URL**: `http://localhost:5000/predict`
- **方法**: POST
- **数据格式**: JSON
- **请求示例**:
  ```json
  {
    "data": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
  }
  ```
- **响应示例**:
  ```json
  {
    "predictions": [17.23, 18.12, 19.05, 20.01],
    "relative_errors": [1.23, 0.89, 1.56, 0.67],
    "warning": "蓝色预警",
    "max_prediction": 20.01,
    "plot": "iVBORw0KGgoAAAANSUhEUgAA..."
  }
  ```