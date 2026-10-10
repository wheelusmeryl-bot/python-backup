# python 代码备份

从本地 `F:\python` 整理出来的个人 Python 代码（整理日期 2026-10-10）。

## 目录

| 目录 | 文件数 | 内容 |
|---|---|---|
| `代码/` | 76 | CTF 密码学 / 逆向脚本：RSA 各种攻击、DES、AES、MD5 爆破、base 系列编码、栅栏密码、capstone 逆向等 |
| `水位预测/` | 25 | 调用 Dify 大模型的洪水预警问答 + BP 神经网络水位预测（`water_level_prediction/`，含 Vercel 部署） |
| `实时监测/` | 12 | 基于 YOLOv8-pose 的溺水监测（PyQt5 界面 + OpenCV + winsound 告警） |
| `flaskProject2/` | 14 | Flask 版溺水监测 Web 服务（含水位预测页面） |
| `YOLOV8-脚本/` | 6 | 从 YOLOV8 工程里单独挑出的自写训练 / 监测脚本和数据集配置 `bvn.yaml` |

## 故意的没放进来

- **模型权重**（`*.pt` / `*.pth` / `*.onnx`）
  `best.pt` 单个 130 MB，超过 GitHub 单文件 100 MB 硬上限。需要时重新下载：
  ```bat
  pip install ultralytics
  ```
  首次运行会自动拉 `yolov8n-pose.pt`；`best.pt` 需自己重新训练或另存网盘。
- **数据集 / 训练产物**（`datasets/`、`runs/`、`my_model/`）：体积大、可重新生成。
- **虚拟环境**（`venv/`、conda 环境）：按下面依赖重新装即可。
- **缓存 / IDE 配置**（`__pycache__/`、`.idea/`）。

## 运行前要配的环境变量

`水位预测/` 里的脚本要调 Dify 大模型。**API Key 已经从代码里拿掉**，改成读环境变量：

| 变量 | 用在哪 | 说明 |
|---|---|---|
| `DIFY_API_KEY` | `LLM.py`、`LLM_request.py` | Dify 云端 Key，在 Dify 后台「应用 → 访问 API」里重新生成 |
| `DIFY_LOCAL_API_KEY` | `reload.py` | 内网 Dify（192.168.10.251）的 Key |
| `DIFY_LOCAL_URL` | `reload.py` | 内网地址，默认 `http://192.168.10.251:82/v1/chat-messages` |

```bat
:: Windows CMD
set DIFY_API_KEY=app-你的key
python 水位预测\LLM_request.py
```

```powershell
# PowerShell
$env:DIFY_API_KEY="app-你的key"
python .\水位预测\LLM_request.py
```

> 原来写死在代码里的两个 Key 已经泄露过，建议去 Dify 后台**作废重新生成**。

## 依赖

```bat
pip install requests flask flask-cors ultralytics opencv-python PyQt5 numpy ^
            pandas openpyxl scikit-learn gmpy2 sympy pycryptodome ^
            capstone scapy tqdm libnum networkx pygame flask-socketio
```

> `代码/` 里用的是 `from Crypto...`，对应的是 **`pycryptodome`**，不是老的 `pycrypto`。

## 备注

- `代码/.vscode/共模.py` 是一个藏在 `.vscode` 目录里的脚本，很容易被当成配置一起删掉，特意保留了。
- `实时监测/yolov8n-pose.pt`、`flaskProject2/static/*.pt` 按上面的规则没进库，跑之前要自己放回去。
- `flaskProject2/static/warning.mp3` 是告警音，体积小（21 KB），保留。
