import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def read_data(file_path):
    positions = []
    powers = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        i = 0
        while i < len(lines):
            try:
                # 跳过第一行
                if not lines[i].startswith('当前是第'):
                    i += 1
                    continue
                
                # 提取位置值
                pos_line = lines[i]
                pos = float(pos_line.split('值为：')[1].strip())
                
                # 跳过中间行
                i += 2
                
                # 提取功率值
                if i < len(lines):
                    power_line = lines[i]
                    if 'Total Power' in power_line:
                        power = float(power_line.split(':')[1].split('Watts')[0].strip())
                        power = float(f"{power:.6f}")
                        
                        positions.append(pos)
                        powers.append(power)
                
                i += 1
            except (IndexError, ValueError) as e:
                print(f"跳过处理第{i}行时出现错误: {e}")
                i += 1
                continue
    
    return np.array(positions), np.array(powers)

def fit_function(x, a, b, c):
    # 使用指数函数进行拟合
    return a * np.exp(-((x - b) ** 2) / (2 * c ** 2))

def plot_data(positions, powers):
    plt.figure(figsize=(10, 6))
    
    # 绘制散点图
    plt.scatter(positions, powers, color='blue', alpha=0.5, label='测量数据')
    
    # 函数拟合
    popt, _ = curve_fit(fit_function, positions, powers)
    x_fit = np.linspace(min(positions), max(positions), 100)
    y_fit = fit_function(x_fit, *popt)
    
    # 绘制拟合曲线
    plt.plot(x_fit, y_fit, 'r-', label=f'拟合曲线\ny = {popt[0]:.2e}x² + {popt[1]:.2e}x + {popt[2]:.2e}')
    
    plt.xlabel('Wolter Z 位置')
    plt.ylabel('Total Power (Watts)')
    plt.title('Wolter Z 位置与总功率关系')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # 保存图像
    plt.savefig('power_vs_position.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    positions, powers = read_data('total.txt')
    if len(positions) > 0:
        plot_data(positions, powers)
        print('图像已保存为 power_vs_position.png')
    else:
        print('未能从文件中提取有效数据')

if __name__ == '__main__':
    main()