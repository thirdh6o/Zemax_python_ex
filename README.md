# Zemax 与示波器自动化项目

## 概述

该项目包含一系列 Python 脚本，用于自动化 Zemax OpticStudio 的光学仿真、控制示波器进行数据采集，以及对采集到的数据进行处理和分析。


## 脚本与使用说明

### 1. `main.py` (Zemax 仿真)

- **功能**: 通过 ZOS-API 连接并控制 Zemax OpticStudio，执行非序列光线追迹仿真。
- **核心流程**:
    1. 初始化与 ZOS-API 的连接。
    2. 循环移动场景中两个物体（Object 2 和 Object 3）的 X 坐标。
    3. 每次移动后，执行一次光线追迹。
    4. 获取探测器上的总功率（Total Power）。
    5. 将每次循环的物体坐标和对应的功率值保存到带时间戳的 CSV 文件中。
- **配置**: 
    - `STEP_SIZE_OBJECT2`: 物体2每次移动的步长。
    - `STEP_SIZE_OBJECT3`: 物体3每次移动的步长。
    - `TOTAL_RUNS`: 总的循环仿真次数。
- **使用方法**:
    ```bash
    python main.py
    ```
- **输出**: 在项目根目录生成 `YYYYMMDD_HHMMSS_data.csv` 文件，记录了物体位置和探测器功率。

### 2. `autoclick/main.py` (示波器自动化)

- **功能**: 提供一个图形用户界面（GUI），用于连接和控制示波器，实现自动化测量和截图。
- **核心流程**:
    1. 通过 `pyvisa` 连接到指定 VISA 地址的示波器。
    2. GUI 界面可以选择目标通道（CHANnel1-4）。
    3. **执行测量**: 测量选定通道的幅值（VAMP）和面积（MARea），并将结果追加到 CSV 文件中。
    4. **波形截图**: 捕获当前示波器屏幕并保存为 PNG 图片。
- **使用方法**:
    ```bash
    python autoclick/main.py
    ```
- **输出**:
    - `measurements_YYYYMMDD_HHMMSS.csv`: 记录测量次数、通道、幅值和面积。
    - `screenshot_X.png`: 保存的示波器截图。

### 3. `dataFix/main.py` (圆形拟合分析)

- **功能**: 根据给定的三组弦长和其对应的 y 轴位置，拟合出最佳的圆，并计算其半径和圆心位置。
- **核心流程**:
    1. 在代码中手动输入三组 `y` 坐标和对应的弦长 `r`。
    2. 使用 `scipy.optimize.minimize` 进行最小二乘法拟合，计算出最佳的圆半径 `R` 和圆心 `y0`。
    3. 使用 `matplotlib` 绘制拟合结果，包括三条弦、拟合的圆和圆心。
- **使用方法**: 
    1. 修改脚本中 `y_samples` 和 `r_samples` 的数据。
    2. 运行脚本：
    ```bash
    python dataFix/main.py
    ```
- **输出**: 在 `dataFix/results/` 目录下生成 `circle_fit_YYYYMMDD_HHMMSS.png` 图像文件。

## 依赖

确保已安装以下 Python 库：

- `pyvisa`
- `matplotlib`
- `numpy`
- `scipy`
- `pythonnet` (用于 `clr`)

此外，系统需要安装 Zemax OpticStudio 和相应的 VISA 驱动（如 NI-VISA）。