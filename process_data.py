import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def read_data(file_path):
    positions = []
    powers = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        i = 0
        while i < len(lines):
            try:
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

def export_csv(positions, powers, output_file):
    df = pd.DataFrame({
        'Position': positions,
        'Total_Power': powers
    })
    df.to_csv(output_file, index=False)

def exponential_func(x, a, b, c):
    return a * np.exp(b * x) + c

def fit_and_plot(positions, powers):
    # 筛选5.9-6.3范围内的数据
    mask = (positions >= 5.9) & (positions <= 6.3)
    x_data = positions[mask]
    y_data = powers[mask]
    
    # 计算更好的初始参数估计
    y_min = np.min(y_data)
    y_max = np.max(y_data)
    x_min = np.min(x_data)
    x_max = np.max(x_data)
    
    # 估计初始参数
    c = y_min  # 基线
    a = y_max - y_min  # 振幅
    b = -1.0  # 衰减率初始估计
    
    p0 = [a, b, c]  # 初始参数
    bounds = (
        [0, -10, 0],     # 下界
        [np.inf, 0, 0.2]  # 上界
    )
    
    try:
        # 增加最大迭代次数
        popt, _ = curve_fit(exponential_func, x_data, y_data, 
                           p0=p0, 
                           bounds=bounds, 
                           maxfev=10000)  # 增加最大函数评估次数
        
        # 生成拟合曲线的点
        x_fit = np.linspace(min(x_data), max(x_data), 100)
        y_fit = exponential_func(x_fit, *popt)
        
        # 绘图
        plt.figure(figsize=(10, 6))
        plt.scatter(x_data, y_data, color='blue', alpha=0.5, label='测量数据')
        plt.plot(x_fit, y_fit, 'r-', label=f'指数拟合\ny = {popt[0]:.2e}·exp({popt[1]:.2e}x) + {popt[2]:.2e}')
        
        plt.xlabel('Wolter Z 位置')
        plt.ylabel('Total Power (Watts)')
        plt.title('Wolter Z 位置与总功率关系 (5.9-6.3范围)')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # 保存图像
        plt.savefig('power_vs_position_exp_fit.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        return popt
    except RuntimeError as e:
        print(f"拟合失败：{str(e)}")
        print("尝试的初始参数：", p0)
        print("数据范围：", x_min, x_max, y_min, y_max)
        return None

def main():
    # 读取数据
    positions, powers = read_data('total.txt')
    
    # 导出CSV
    export_csv(positions, powers, 'power_data.csv')
    print('数据已导出到 power_data.csv')
    
 

if __name__ == '__main__':
    main()