import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from numpy.linalg import inv

# 设置中文字体
plt.rcParams["font.family"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False


def compute_gradient(theta, f, eps=1e-5):
    """计算目标函数在theta处的梯度（一阶导数）"""
    n = len(theta)
    grad = np.zeros(n)
    for i in range(n):
        # 保存原始值
        original = theta[i]
        # 正向扰动
        theta[i] =  original + eps
        f_plus = f(theta)
        # 反向扰动
        theta[i] = original - eps
        f_minus = f(theta)
        # 恢复原始值
        theta[i] = original
        # 中心差分近似梯度
        grad[i] = (f_plus - f_minus) / (2 * eps)
    return grad


def compute_hessian(theta, f, eps=1e-5):
    """计算目标函数在theta处的Hessian矩阵（二阶导数）"""
    n = len(theta)
    hessian = np.zeros((n, n))
    # 先计算原始梯度
    grad0 = compute_gradient(theta.copy(), f, eps)

    for i in range(n):
        # 保存原始值
        original = theta[i]
        # 正向扰动参数d
        theta[i] = original + eps
        # 计算扰动后的梯度
        grad_plus = compute_gradient(theta.copy(), f, eps)
        # 恢复原始值
        theta[i] = original
        # 用梯度差近似二阶导数
        hessian[:, i] = (grad_plus - grad0) / eps
    return hessian


def FastGD(theta, f):
    grad = compute_hessian(theta,f)
    hessian = compute_gradient(theta,f)
    hessian_inv = inv(hessian)
    theta_new = theta - np.dot(hessian_inv,grad)
    return theta_new
def predict_with_mlp(level_data):
    data = level_data[:16]
    true_values = level_data[-4:]

    scaler = MinMaxScaler(feature_range=(0, 1))
    data_scaled = scaler.fit_transform(data.reshape(-1, 1)).flatten()

    window_size = 5
    X, y = [], []
    for i in range(len(data_scaled) - window_size):
        X.append(data_scaled[i:i + window_size])
        y.append(data_scaled[i + window_size])

    X = np.array(X)
    y = np.array(y)

    # 构建并训练模型
    # 隐含层 #激活函数 #采用优化器 #学习率 #正则化 #随机种子 #终止条件
    model = MLPRegressor(hidden_layer_sizes=(11),
                         activation="relu",
                         solver='lbfgs',
                         learning_rate_init=0.01,
                         alpha=0.001,
                         random_state=42,
                         tol=1e-6,
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

    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

    # 计算精准度（100%减去最大相对误差）
    if len(true_values) == 4:
        relative_errors = np.abs(predictions.flatten() - true_values) / true_values * 100
        max_error = np.max(relative_errors)
        accuracy = 100 - max_error
        # 提取小数点后两位并转为字符串，再截取最后两位
        accuracy_str = f"{accuracy:.2f}%"
        # 只取小数点后两位数字部分，如 99.86% → 86%
        result = accuracy_str.split('.')[1].replace('%', '') + '%'
        print(f"预测准确率{result}")
    else:
        print("无法计算精准度：输入数据中真实值不足4个")

    # 加入预警等级判断阈值说明
    print("该地区的预警等级判断阈值：")
    print("蓝色预警阈值：175m。")
    print("黄色预警阈值：182m。")
    print("橙色预警阈值：188m。")
    print("红色阈值阈值：195m。")
    print("依据水位预测模型的结果得到：")

    # 预警等级判断
    max_pred = np.max(predictions)
    if max_pred > 179:
        print("红色预警")
    elif max_pred > 176:
        print("橙色预警")
    elif max_pred > 173:
        print("黄色预警")
    else:
        print("蓝色预警")

    # 绘制图表
    plt.figure(figsize=(10, 6))
    # 原始数据（前16个点），注意这里x轴刻度要和新的对应上，前16个点对应新刻度的前16个位置
    plt.plot([5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80], data[:16], 'b-o', label='原始数据（1-16）')
    if len(true_values) == 4:
        # 真实值（后4个点），对应新刻度的后4个位置
        plt.plot([85,90,95,100], true_values, 'g-o', label='真实值（17-20）')
    # 预测值（后4个点），对应新刻度的后4个位置
    plt.plot([85,90,95,100], predictions.flatten(), 'r--o', label='预测值（17-20）')

    plt.title('水位预测结果对比')
    plt.xlabel('时间点(min)')
    plt.ylabel('水位(m)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    # 设置新的横坐标刻度
    plt.xticks([5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100])
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    file_path = "C:\\Users\\29120\\Desktop\\shuiweishuj.txt"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            input_str = f.read().strip()
        level_data = np.array([float(x) for x in input_str.split()])
        if len(level_data) < 20:
            raise ValueError(f"数据点不足，需要至少20个，实际有{len(level_data)}个")
        predict_with_mlp(level_data)
    except FileNotFoundError:
        print(f"错误：未找到文件，请检查路径是否正确：\n{file_path}")
    except ValueError as e:
        print(f"数据格式错误：{e}")
    except Exception as e:
        print(f"运行出错：{e}")