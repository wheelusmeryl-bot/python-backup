import matplotlib
matplotlib.use('Agg')  # 设置matplotlib使用非交互式后端
from flask import Flask, request, jsonify, send_file, render_template
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 获取输入数据
        data = request.json.get('data')
        level_data = np.array(data[:16])
        true_values = np.array(data[-4:]) if len(data) >= 20 else None
        
        # 数据标准化
        scaler = MinMaxScaler(feature_range=(0, 1))
        data_scaled = scaler.fit_transform(level_data.reshape(-1, 1)).flatten()
        
        # 构造训练数据
        window_size = 5
        X, y = [], []
        for i in range(len(data_scaled) - window_size):
            X.append(data_scaled[i:i+window_size])
            y.append(data_scaled[i+window_size])
        
        X = np.array(X)
        y = np.array(y)
        
        # 训练模型
        model = MLPRegressor(
            hidden_layer_sizes=(7,),
            activation='relu',
            solver='lbfgs',
            max_iter=5000,
            learning_rate_init=0.01,
            alpha=0.001,
            random_state=42,
            tol=1e-6
        )
        model.fit(X, y)
        
        # 预测未来4个点
        predictions = []
        future_points = 4
        window_data = data_scaled[-window_size:].copy()
        
        for _ in range(future_points):
            next_val = model.predict(window_data.reshape(1, -1))
            predictions.append(next_val[0])
            window_data = np.append(window_data[1:], next_val)
        
        # 逆标准化
        predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()
        
        # 计算相对误差（如果有真实值）
        relative_errors = []
        if true_values is not None:
            relative_errors = (np.abs(predictions - true_values) / true_values * 100).tolist()
        
        # 确定预警等级
        max_pred = np.max(predictions)
        if max_pred > 22:
            warning = "红色预警"
        elif max_pred > 21:
            warning = "橙色预警"
        elif max_pred > 20:
            warning = "黄色预警"
        else:
            warning = "蓝色预警"
        
        # 生成图表
        img = io.BytesIO()
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, 17), level_data, 'b-o', label='Original points')
        if true_values is not None:
            plt.plot(range(17, 21), true_values, 'g-o', label='Real points')
        plt.plot(range(17, 21), predictions, 'r--o', label='Prediction points')
        plt.title('Machine Learning Prediction Result')
        plt.xlabel('time')
        plt.ylabel('value')
        plt.legend()
        plt.grid(True)
        plt.xticks(range(1, 21))
        plt.tight_layout()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        
        return jsonify({
            'predictions': [round(float(x), 2) for x in predictions],
            'relative_errors': [round(float(x), 2) for x in relative_errors],
            'warning': warning,
            'max_prediction': round(float(max_pred), 2),
            'plot': plot_url
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/')
def index():
    return send_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)