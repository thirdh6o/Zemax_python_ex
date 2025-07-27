import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import os
from datetime import datetime

def fit_circle_from_chords(y_vals, r_vals, draw=True):
    """
    根据三组 (y_k, r_k) 拟合圆的 (R, y0)，可选绘图展示拟合结果
    """
    y_vals = np.array(y_vals)
    r_vals = np.array(r_vals)

    def residual(params):
        R, y0 = params
        if R <= 0:
            return 1e10
        predicted_r = 2 * np.sqrt(np.maximum(R**2 - (y_vals - y0)**2, 0))
        return np.sum((predicted_r - r_vals)**2)

    # 初始猜测
    R_init = np.max(r_vals) / 2
    y0_init = np.mean(y_vals)

    result = minimize(residual, x0=[R_init, y0_init], method='L-BFGS-B', bounds=[(1e-5, None), (None, None)])

    if not result.success:
        raise RuntimeError("拟合失败: " + result.message)

    R_opt, y0_opt = result.x

    if draw:
        draw_fit_result(y_vals, r_vals, R_opt, y0_opt)

    return R_opt, y0_opt

def draw_fit_result(y_vals, r_vals, R, y0):
    """
    绘制三条测量线、测得截线、拟合圆、圆心位置
    """
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # 1. 绘制三条横线与截线
    for i in range(len(y_vals)):
        y = y_vals[i]
        r = r_vals[i]
        x_left = -r / 2
        x_right = r / 2
        ax.plot([x_left, x_right], [y, y], 'b-', lw=2, label='Chord' if i == 0 else "")

    # 2. Draw fitted circle
    theta = np.linspace(0, 2 * np.pi, 200)
    x_circle = R * np.cos(theta)
    y_circle = R * np.sin(theta) + y0
    ax.plot(x_circle, y_circle, 'r-', label='Fitted Circle', lw=2)

    # 3. Mark circle center
    ax.plot(0, y0, 'ro', label='Center')

    # Axis settings
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    ax.set_title("Circle Fitting Visualization")

    # 创建results文件夹（如果不存在）
    results_dir = os.path.join(os.path.dirname(__file__), 'results')
    os.makedirs(results_dir, exist_ok=True)

    # 生成当前时间字符串作为文件名
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    save_path = os.path.join(results_dir, f'circle_fit_{current_time}.png')
    
    # 保存图像
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()

# 主程序示例
if __name__ == "__main__":

    ##############################################################################
    # 数据修改就在这里
    y_samples = [1.0, 2.8, 3.0]
    r_samples = [3.0, 4.4, 3.5]

    R_result, y0_result = fit_circle_from_chords(y_samples, r_samples, draw=True)
    print(f"拟合结果：\n半径 R = {R_result:.4f}\n纵向中心 y0 = {y0_result:.4f}")
    ##############################################################################