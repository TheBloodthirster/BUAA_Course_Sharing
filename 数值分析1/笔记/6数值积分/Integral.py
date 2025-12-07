import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

plt.rcParams["font.family"] = ["Microsoft YaHei"]
plt.rcParams['axes.unicode_minus'] = False

# 复化梯形求积公式
def composite_trapezoidal(f, a, b, n):
    h = (b - a) / n  # 步长
    result = 0.5 * (f(a) + f(b))  # 端点项
    
    # 累加中间节点（乘以2）
    for k in range(1, n):
        x = a + k * h
        result += f(x)
    
    return result * h  # 乘以步长h


# 复化Simpson求积公式
def composite_simpson(f, a, b, n):
    h = (b - a) / (2 * n)  # 步长
    result = f(a) + f(b)  # 端点项
    
    # 累加奇数节点（乘以4）
    for i in range(1, n + 1):
        x = a + (2 * i - 1) * h
        result += 4 * f(x)
    
    # 累加偶数节点（乘以2）
    for i in range(1, n):
        x = a + 2 * i * h
        result += 2 * f(x)
    
    return result * h / 3  # 乘以步长h/3


# 可视化函数
def visualize_integration(f, a, b, n):
    # 创建画布
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(f'复化求积法可视化 (n={n})', fontsize=16)
    
    # 生成高精度x值用于绘制函数曲线
    x_fine = np.linspace(a, b, 1000)
    y_fine = f(x_fine)
    
    # 复化梯形法可视化
    ax1.plot(x_fine, y_fine, 'b-', linewidth=2, label=f'f(x) = x²')
    h_trap = (b - a) / n
    x_trap = np.linspace(a, b, n+1)
    y_trap = f(x_trap)
    
    # 绘制梯形区域
    for i in range(n):
        x = [x_trap[i], x_trap[i], x_trap[i+1], x_trap[i+1]]
        y = [0, y_trap[i], y_trap[i+1], 0]
        poly = Polygon(np.column_stack([x, y]), facecolor='lightblue', edgecolor='blue', alpha=0.4)
        ax1.add_patch(poly)
    
    ax1.plot(x_trap, y_trap, 'ro-', markersize=5)
    # ax1.fill_between(x_fine, y_fine, alpha=0.2, color='green')
    ax1.set_xlabel('x')
    ax1.set_ylabel('f(x)')
    ax1.set_title(f'复化梯形法 (结果: {composite_trapezoidal(f, a, b, n):.6f})')
    ax1.grid(True)
    ax1.legend()
    
    # 复化Simpson法可视化（修正版）
    ax2.plot(x_fine, y_fine, 'b-', linewidth=2, label=f'f(x) = x²')
    h_simp = (b - a) / (2 * n)
    x_simp = np.linspace(a, b, 2*n + 1)
    y_simp = f(x_simp)
    
    # 绘制Simpson抛物线区域（正确拟合抛物线）
    for i in range(n):
        # 每个区间取三个点：左端点、中点、右端点
        x0, x1, x2 = x_simp[2*i], x_simp[2*i+1], x_simp[2*i+2]
        y0, y1, y2 = y_simp[2*i], y_simp[2*i+1], y_simp[2*i+2]
        
        # 构造过这三个点的抛物线（二次多项式）
        A = np.array([[x0**2, x0, 1],
                      [x1**2, x1, 1],
                      [x2**2, x2, 1]])
        B = np.array([y0, y1, y2])
        a_parab, b_parab, c_parab = np.linalg.solve(A, B)
        
        # 生成区间内的精细点并计算抛物线值
        x_parab = np.linspace(x0, x2, 100)
        y_parab = a_parab * x_parab**2 + b_parab * x_parab + c_parab
        
        # 填充抛物线下方区域（与x轴围成的面积）
        ax2.fill_between(x_parab, y_parab, alpha=0.4, color='orange')
        ax2.plot(x_parab, y_parab, 'r--', linewidth=1)
    
    ax2.plot(x_simp, y_simp, 'go-', markersize=5)
    # ax2.fill_between(x_fine, y_fine, alpha=0.2, color='green')
    ax2.set_xlabel('x')
    ax2.set_ylabel('f(x)')
    ax2.set_title(f'复化Simpson法 (结果: {composite_simpson(f, a, b, n):.6f})')
    ax2.grid(True)
    ax2.legend()
    
    # 显示精确值
    plt.figtext(0.5, 0.01, f'精确值: {1-np.cos(10):.6f}', ha='center', fontsize=12)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()


# 主程序
if __name__ == "__main__":
    # 测试函数：f(x) = x^2，积分区间[0, 2]，精确值为8/3 ≈ 2.6667
    def f(x):
        return np.sin(x)
    
    a, b = 0, 10
    n = 5  # 区间等分数（Simpson法实际分为2n个小区间）
    
    # 计算结果
    trap_result = composite_trapezoidal(f, a, b, n)
    simp_result = composite_simpson(f, a, b, n)
    
    # 打印数值结果
    print(f"复化梯形法结果 (n={n}): {trap_result:.6f}")
    print(f"复化Simpson法结果 (n={n}): {simp_result:.6f}")
    print(f"精确值: {1-np.cos(10):.6f}")
    
    # 可视化
    visualize_integration(f, a, b, n)