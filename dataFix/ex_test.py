import os
import csv

# 导入你写的主函数
from main import fit_circle_from_chords

# === 修改此处选择要测试的 CSV 文件 ===
FILENAME = "reality.csv"

# FILENAME = "example_no_noise.csv"
# FILENAME = "example_medium_noise.csv"
# FILENAME = "example_light_noise.csv"
# FILENAME = "reality.csv"

def read_csv_data(filepath):
    """
    读取 CSV 文件中的一组 y_k 和 r_k 数据
    
    返回：y_vals, r_vals
    """
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # 跳过提示行
        row = next(reader)     # 读取数据行
        row = [float(val) for val in row]
        y_vals = [row[i] for i in range(0, 6, 2)]
        r_vals = [row[i] for i in range(1, 6, 2)]
        return y_vals, r_vals

if __name__ == "__main__":
    # 计算 CSV 的绝对路径（位于当前脚本同目录）
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, FILENAME)

    # 读取数据并拟合
    y_vals, r_vals = read_csv_data(csv_path)
    R, y0 = fit_circle_from_chords(y_vals, r_vals, draw=True)

    # 输出拟合结果
    print(f"测试文件：{FILENAME}")
    print(f"拟合结果：\n  半径 R  = {R:.4f}\n  圆心 y0 = {y0:.4f}")
