import numpy as np
import csv
import os

# 设置保存路径


current_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = current_dir
os.makedirs(output_dir, exist_ok=True)

# 通用写入函数
def write_csv(filename, y_vals, r_vals):
    filepath = os.path.join(output_dir, filename)
    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        # 写入提示词
        header = []
        for i in range(3):
            header += [f"y{i+1}", f"r{i+1}"]
        writer.writerow(header)
        # 写入数据行
        row = []
        for y, r in zip(y_vals, r_vals):
            row += [y, r]
        writer.writerow(row)
    return filepath

# 示例 1：无噪声
R1, y0_1 = 5.0, 2.0
y_vals1 = [0.0, 2.0, 4.0]
r_vals1 = [2 * np.sqrt(R1**2 - (y - y0_1)**2) for y in y_vals1]
file1 = write_csv("example_no_noise.csv", y_vals1, r_vals1)

# 示例 2：轻微噪声
np.random.seed(0)
R2, y0_2 = 6.0, 1.5
y_vals2 = [1.0, 2.0, 3.0]
r_vals2_true = [2 * np.sqrt(R2**2 - (y - y0_2)**2) for y in y_vals2]
r_vals2_noisy = [r + np.random.normal(0, 0.1) for r in r_vals2_true]
file2 = write_csv("example_light_noise.csv", y_vals2, r_vals2_noisy)

# 示例 3：中等误差 + 非对称
np.random.seed(42)
R3, y0_3 = 4.5, -1.0
y_vals3 = [-2.0, 0.0, 1.5]
r_vals3_true = [2 * np.sqrt(R3**2 - (y - y0_3)**2) for y in y_vals3]
r_vals3_noisy = [r + np.random.normal(0, 0.3) for r in r_vals3_true]
file3 = write_csv("example_medium_noise.csv", y_vals3, r_vals3_noisy)

[file1, file2, file3]
