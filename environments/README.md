# 环境版本快照

删除本地 conda / venv 环境**之前**导出的精确包版本清单（2026-10-10）。
以后想还原环境，按这里装，能装出**和当时一模一样**的版本，避免新版库改了 API 导致代码跑不起来。

## 文件说明

| 文件 | 对应环境 | 说明 |
|---|---|---|
| `base-pip.txt` / `conda-base.txt` | Miniconda3 根环境 | |
| `pytorch-pip.txt` / `conda-pytorch.txt` | `envs/pytorch` | PyTorch 训练用 |
| `yolo-pip.txt` / `conda-yolo.txt` | `envs/yolo` | YOLO 训练用 |
| `yolov13-pip.txt` / `conda-yolov13.txt` | `envs/yolov13` | |
| `labelme-pip.txt` / `conda-labelme.txt` | `envs/labelme` | 标注工具 |
| `yolov8-venv-pip.txt` | `F:\python\YOLOV8\venv` | YOLOV8 项目虚拟环境 |
| `python313-pip.txt` | `C:\...\Programs\Python\Python313` | **这个没删**，仅作记录 |

`*-pip.txt` = `pip freeze` 的结果，用 `pip install -r` 还原。
`conda-*.txt` = `conda list --export` 的结果，用 `conda create --file` 还原，能额外捕获非 pip 装的包。

## 怎么还原（以 pytorch 环境为例）

**方式一：conda（推荐，完整）**
```bat
conda create -n pytorch --file conda-pytorch.txt
```

**方式二：纯 pip（快，但可能漏掉 conda 特有的包）**
```bat
conda create -n pytorch python=3.11
conda activate pytorch
pip install -r pytorch-pip.txt
```

> CUDA 版的 PyTorch 装法受驱动版本影响，`torch` 建议单独去 https://pytorch.org 按自己显卡驱动选命令装，再 `pip install -r` 装剩下的。

**YOLOV8 的 venv 环境：**
```bat
cd F:\python\YOLOV8
python -m venv venv
venv\Scripts\activate
pip install -r environments\yolov8-venv-pip.txt
```

## 注意

快照里的版本号是**导出当天**的。如果以后在新机器上按这个装，遇到某些包需要编译、装不上，可以去掉版本号装最新版试试 —— 大版本别跳太多通常没事。
