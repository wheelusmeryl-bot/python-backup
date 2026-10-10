import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler

# 示例数据（假设是时间序列，16个点）
random_interfere = np.random.uniform(-0.025, 0.025, size=16)

data = np.arange(1, 17, 1) * (1 + random_interfere)  # 生成1到16的等差数列
# data = np.array([x**2 for x in range(1,17)]) * (1 + random_interfere)

# 数据标准化
scaler = MinMaxScaler(feature_range=(0, 1))
data_scaled = scaler.fit_transform(data.reshape(-1, 1)).flatten()

# 用滑动窗口构造训练数据（用前4个点预测第5个点）
window_size = 5  # 滑动窗口大小（可调整）
X, y = [], []
for i in range(len(data_scaled) - window_size):
    X.append(data_scaled[i:i + window_size])
    y.append(data_scaled[i + window_size])

X = np.array(X)
y = np.array(y)

# 训练BP神经网络
model = MLPRegressor(
    hidden_layer_sizes=(11),  #yinhancen
    activation='relu',  # xunzheyaishiyongde activation
    solver='lbfgs',  # xunzheyouhuaqi
    max_iter=5000,  # zuidadecishui
    learning_rate_init=0.01,  # 提高初始学习率
    alpha=0.001,  # 增加L2正则化
    early_stopping=True,  # 启用早停
    validation_fraction=0.2,  # 验证集比例
    n_iter_no_change=50,  # 早停耐心值
    random_state=42,#设置随机数种子
    tol=1e-6  # 更严格的收敛阈值
)

# 进行拟合
model.fit(X, y)

# 预测未来4个点[17 18 19 20]
predictions = []
future_points = 4
window_data = data_scaled[-window_size:].copy()  # 初始窗口数据

for _ in range(future_points):
    # 预测并保存结果
    next_val = model.predict(window_data.reshape(1, -1))
    predictions.append(next_val[0])

    # 更新窗口数据
    window_data = np.append(window_data[1:], next_val)

# 逆标准化打印预测结果
predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
print("\n[17:20]预测值:", [f"{x:.2f}" for x in predictions.flatten()])

# 假设真实值（17-20点）
true_values = np.array([17, 18, 19, 20])  # y = x
# true_values = np.arange(17,21)**2  # y = x ** 2

# 计算相对误差
relative_errors = np.abs(predictions.flatten() - true_values) / true_values * 100
print("\n[17:20]相对误差:", [f"{x:.2f}%" for x in relative_errors.flatten()])

# 绘制对比图
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.plot(range(1, 17), data[:16], 'b-o', label='Original points')
plt.plot(range(17, 21), true_values, 'g-o', label='Real points')
plt.plot(range(17, 21), predictions.flatten(), 'r--o', label='Prediction points')

# 添加图例和标签
plt.title('BPnetwork result')
plt.xlabel('time')
plt.ylabel('value')
plt.legend()
plt.grid(True)
plt.xticks(range(1, 21))
plt.tight_layout()
plt.show()

