import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler


class WaterLevelPredictor:
    def __init__(self, window_size=5, hidden_layer_sizes=(7,),
                 activation='relu', solver='lbfgs', max_iter=5000,
                 learning_rate_init=0.01, alpha=0.001, random_state=42, tol=1e-6):
        """
        初始化水位预测器
        :param window_size: 滑动窗口大小
        :param hidden_layer_sizes: 隐藏层结构
        :param activation: 激活函数
        :param solver: 优化器
        :param max_iter: 最大迭代次数
        :param learning_rate_init: 初始学习率
        :param alpha: L2正则化系数
        :param random_state: 随机种子
        :param tol: 收敛阈值
        """
        self.window_size = window_size
        self.hidden_layer_sizes = hidden_layer_sizes
        self.activation = activation
        self.solver = solver
        self.max_iter = max_iter
        self.learning_rate_init = learning_rate_init
        self.alpha = alpha
        self.random_state = random_state
        self.tol = tol

        # 初始化组件
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.model = None
        self.latest_window = None

    def fit(self, training_data):
        """
        训练模型
        :param training_data: 训练数据（至少需要 window_size + 1 个数据点）
        """
        # 数据标准化
        scaled_data = self.scaler.fit_transform(training_data.reshape(-1, 1)).flatten()

        # 构建训练样本
        X, y = [], []
        for i in range(len(scaled_data) - self.window_size):
            X.append(scaled_data[i:i + self.window_size])
            y.append(scaled_data[i + self.window_size])

        # 初始化并训练模型
        self.model = MLPRegressor(
            hidden_layer_sizes=self.hidden_layer_sizes,
            activation=self.activation,
            solver=self.solver,
            max_iter=self.max_iter,
            learning_rate_init=self.learning_rate_init,
            alpha=self.alpha,
            random_state=self.random_state,
            tol=self.tol
        )
        self.model.fit(X, y)

        # 保存最新窗口数据
        self.latest_window = scaled_data[-self.window_size:]

    def predict(self, future_steps=4, true_values=None):
        """
        执行预测
        :param future_steps: 需要预测的步数
        :param true_values: 真实值（用于计算误差，可选）
        :return: 预测结果字典
        """
        if self.model is None:
            raise ValueError("请先调用fit方法训练模型")

        # 执行多步预测
        predictions = []
        window_data = self.latest_window.copy()

        for _ in range(future_steps):
            next_val = self.model.predict(window_data.reshape(1, -1))
            predictions.append(next_val[0])
            window_data = np.append(window_data[1:], next_val)

        # 逆标准化
        predictions = self.scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()

        # 准备返回结果
        result = {
            "predictions": [round(x, 2) for x in predictions],
            "alert_level": self._get_alert_level(predictions)
        }

        # 如果有真实值则计算误差
        if true_values is not None:
            relative_errors = np.abs(predictions - true_values) / true_values * 100
            result["relative_errors"] = [f"{x:.2f}%" for x in relative_errors]

        return result

    def _get_alert_level(self, predictions):
        """获取预警等级"""
        max_pred = max(predictions)
        if max_pred > 22:
            return "红色预警"
        elif max_pred > 21:
            return "橙色预警"
        elif max_pred > 20:
            return "黄色预警"
        else:
            return "蓝色预警"


# 使用示例
if __name__ == "__main__":
    # 示例数据（假设是时间序列，前16个点为历史数据，后4个为真实值）
    sample_data = np.array([18.2, 18.5, 18.7, 19.0, 19.2, 19.5, 19.7, 20.0,
                            20.2, 20.5, 20.7, 21.0, 21.2, 21.5, 21.7, 22.0,])

    # 初始化预测器
    predictor = WaterLevelPredictor(
        window_size=5,
        hidden_layer_sizes=(10, 5),  # 加深网络结构
        max_iter=10000,
        learning_rate_init=0.005
    )

    # 训练模型（使用前16个数据点）
    predictor.fit(sample_data[:16])

    # 执行预测（使用最后4个真实值计算误差）
    result = predictor.predict(
        future_steps=4,
        true_values=sample_data[-4:]
    )

    # 打印结果
    print("预测水位(cm):", result["predictions"])
    print("预警等级:", result["alert_level"])