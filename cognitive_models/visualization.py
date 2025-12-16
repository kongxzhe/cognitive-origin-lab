"""
visualization.py

认知起源实验室 - 可视化模块
用于可视化函数衍化、意识涌现等过程的图表工具。
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional, Any, Dict
import matplotlib.cm as cm
from .function_evolution import ConsciousFunctionEvolver


def visualize_evolution(
    evolver: ConsciousFunctionEvolver,
    data_stream: List[Tuple[float, float]],
    save_path: Optional[str] = None,
    show_plot: bool = True,
    figsize: Tuple[int, int] = (14, 8)
) -> plt.Figure:
    """
    可视化函数衍化的完整过程，包括函数变化、数据点和中断事件。
    
    参数:
        evolver: 已完成实验的函数衍化器实例
        data_stream: 输入的数据流，每个元素为 (x, y)
        save_path: 图片保存路径，如果为None则不保存
        show_plot: 是否显示图表
        figsize: 图表大小
        
    返回:
        matplotlib图表对象
    """
    fig = plt.figure(figsize=figsize)
    
    # 1. 主图：函数衍化与数据点
    ax1 = plt.subplot(2, 2, (1, 2))  # 占据第一行的两列
    
    # 生成定义域内的x值
    domain_min, domain_max = evolver.domain
    x_vals = np.linspace(domain_min, domain_max, 300)
    
    # 绘制初始函数（如果有历史）
    if evolver.history:
        initial_func = evolver.history[0][0]
        ax1.plot(x_vals, [initial_func(x) for x in x_vals], 
                'k--', alpha=0.5, linewidth=1.5, label='初始函数（稳定态/无意识）')
    
    # 绘制最终函数
    ax1.plot(x_vals, [evolver.current_function(x) for x in x_vals], 
            'b-', linewidth=2.5, label='最终函数（新稳定态）')
    
    # 绘制中间状态函数（如果有的话）
    for i, (func, error) in enumerate(evolver.history[1:], 1):
        ax1.plot(x_vals, [func(x) for x in x_vals], 
                'g-', alpha=0.3, linewidth=0.8, label=f'中间状态 {i}' if i == 1 else "")
    
    # 绘制数据点，并根据是否引起中断进行颜色区分
    disruption_xs = [d[0] for d in evolver.disruption_history] if hasattr(evolver, 'disruption_history') else []
    
    regular_xs, regular_ys = [], []
    disruption_xs_plot, disruption_ys_plot = [], []
    
    for x, y in data_stream:
        # 判断这个点是否引起了中断
        is_disruption = any(abs(x - dx) < 1e-6 for dx in disruption_xs)
        if is_disruption:
            disruption_xs_plot.append(x)
            disruption_ys_plot.append(y)
        else:
            regular_xs.append(x)
            regular_ys.append(y)
    
    # 绘制常规数据点
    if regular_xs:
        ax1.scatter(regular_xs, regular_ys, c='gray', s=40, alpha=0.6, 
                   label='常规数据（符合预期）', edgecolors='black', linewidth=0.5)
    
    # 绘制引起中断的数据点
    if disruption_xs_plot:
        ax1.scatter(disruption_xs_plot, disruption_ys_plot, c='red', s=100, alpha=0.8,
                   label='中断触发点（预测误差）', edgecolors='darkred', linewidth=1.5,
                   zorder=5)  # 确保中断点在最上层
    
    # 添加中断区域的阴影
    if disruption_xs_plot:
        min_disruption_x = min(disruption_xs_plot)
        max_disruption_x = max(disruption_xs_plot)
        ax1.axvspan(min_disruption_x, max_disruption_x, alpha=0.1, color='red',
                   label='中断发生区域')
    
    ax1.set_xlabel('输入 x（现象/刺激）', fontsize=11)
    ax1.set_ylabel('输出 y（响应/预测）', fontsize=11)
    ax1.set_title('函数衍化：从稳定态到新稳定态', fontsize=13, fontweight='bold')
    ax1.legend(loc='best', fontsize=9)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.set_xlim([domain_min, domain_max])
    
    # 2. 子图2：预测误差与中断事件
    ax2 = plt.subplot(2, 2, 3)
    
    if evolver.history:
        errors = [step[1] for step in evolver.history]
        evolution_steps = range(1, len(errors) + 1)
        
        # 创建颜色渐变，根据误差大小
        colors = cm.Reds(np.linspace(0.3, 0.9, len(errors)))
        
        bars = ax2.bar(evolution_steps, errors, color=colors, edgecolor='darkred', alpha=0.7)
        
        # 添加误差值标签
        for bar, error in zip(bars, errors):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{error:.2f}', ha='center', va='bottom', fontsize=8)
        
        ax2.set_xlabel('函数衍化步骤', fontsize=10)
        ax2.set_ylabel('预测误差', fontsize=10)
        ax2.set_title('中断事件与预测误差', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.2, axis='y')
        ax2.set_xticks(evolution_steps)
    else:
        ax2.text(0.5, 0.5, '无中断事件发生\n系统保持稳定', 
                ha='center', va='center', fontsize=12, transform=ax2.transAxes)
        ax2.set_title('中断事件与预测误差', fontsize=12, fontweight='bold')
    
    # 3. 子图3：系统状态变化示意图
    ax3 = plt.subplot(2, 2, 4)
    
    # 创建简化的状态机示意图
    states = ['稳定态\n（函数F₀）']
    transitions = []
    
    if evolver.history:
        for i, (func, error) in enumerate(evolver.history):
            if i < len(evolver.history) - 1:
                states.append(f'中断态\n（误差:{error:.2f}）')
                states.append(f'过渡态\n（函数F_{i+1}）')
    
    states.append(f'新稳定态\n（函数F_{len(evolver.history)}）')
    
    # 绘制状态节点
    for i, state in enumerate(states):
        y_pos = 0.5
        x_pos = i / (len(states) - 1) if len(states) > 1 else 0.5
        
        # 根据状态类型设置颜色
        if '稳定态' in state:
            color = 'lightblue'
            edge_color = 'blue'
        elif '中断态' in state:
            color = 'lightcoral'
            edge_color = 'red'
        else:  # 过渡态
            color = 'lightgreen'
            edge_color = 'green'
        
        circle = plt.Circle((x_pos, y_pos), 0.08, color=color, 
                          ec=edge_color, lw=2, zorder=2)
        ax3.add_patch(circle)
        ax3.text(x_pos, y_pos, state, ha='center', va='center', 
                fontsize=8, fontweight='bold')
        
        # 绘制状态间的箭头
        if i < len(states) - 1:
            next_x = (i + 1) / (len(states) - 1) if len(states) > 1 else 0.5
            ax3.arrow(x_pos + 0.08, y_pos, next_x - x_pos - 0.16, 0,
                     head_width=0.05, head_length=0.03, fc='black', ec='black', 
                     length_includes_head=True, alpha=0.7, zorder=1)
    
    ax3.set_xlim([-0.1, 1.1])
    ax3.set_ylim([0.3, 0.7])
    ax3.set_title('系统状态转变示意图', fontsize=12, fontweight='bold')
    ax3.axis('off')
    
    # 4. 添加整体标题
    plt.suptitle('意识作为"函数衍化"的计算模拟', fontsize=16, fontweight='bold', y=0.98)
    
    # 添加哲学解释文本框
    text_content = (
        "哲学框架解读：\n"
        "• 稳定函数 → 无意识/自动处理\n"
        "• 预测误差 → 意识中断触发\n"
        "• 函数衍化 → 有意识适应过程\n"
        "• 新稳定态 → 整合后的新认知模式"
    )
    
    fig.text(0.02, 0.02, text_content, fontsize=9, 
             bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", alpha=0.7),
             verticalalignment='bottom')
    
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])  # 为底部文本框留出空间
    
    # 保存图片
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"图表已保存至: {save_path}")
    
    # 显示图表
    if show_plot:
        plt.show()
    
    return fig


def plot_function_comparison(
    functions: List[Any],
    labels: List[str],
    domain: Tuple[float, float] = (0, 10),
    title: str = "函数比较",
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    比较多个函数的可视化工具。
    
    参数:
        functions: 函数对象列表
        labels: 每个函数的标签
        domain: 定义域
        title: 图表标题
        save_path: 保存路径
        
    返回:
        matplotlib图表对象
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x_vals = np.linspace(domain[0], domain[1], 300)
    
    colors = plt.cm.Set1(np.linspace(0, 1, len(functions)))
    
    for i, (func, label, color) in enumerate(zip(functions, labels, colors)):
        y_vals = [func(x) for x in x_vals]
        ax.plot(x_vals, y_vals, color=color, linewidth=2, label=label, alpha=0.8)
    
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('f(x)', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    return fig


def create_interactive_visualization(
    evolver: ConsciousFunctionEvolver,
    data_stream: List[Tuple[float, float]]
) -> Dict[str, Any]:
    """
    创建交互式可视化所需的数据结构（为未来Web应用做准备）。
    
    参数:
        evolver: 函数衍化器实例
        data_stream: 数据流
        
    返回:
        包含可视化数据的字典
    """
    # 提取数据用于交互式可视化
    domain_min, domain_max = evolver.domain
    x_vals = np.linspace(domain_min, domain_max, 100).tolist()
    
    # 初始函数数据
    initial_func_data = []
    if evolver.history:
        initial_func = evolver.history[0][0]
        initial_func_data = [initial_func(x) for x in x_vals]
    
    # 最终函数数据
    final_func_data = [evolver.current_function(x) for x in x_vals]
    
    # 数据点分类
    disruption_xs = [d[0] for d in evolver.disruption_history] if hasattr(evolver, 'disruption_history') else []
    
    regular_points = []
    disruption_points = []
    
    for x, y in data_stream:
        is_disruption = any(abs(x - dx) < 1e-6 for dx in disruption_xs)
        if is_disruption:
            disruption_points.append({"x": x, "y": y})
        else:
            regular_points.append({"x": x, "y": y})
    
    # 构建结果字典
    result = {
        "x_values": x_vals,
        "initial_function": initial_func_data,
        "final_function": final_func_data,
        "regular_points": regular_points,
        "disruption_points": disruption_points,
        "evolution_steps": len(evolver.history) if evolver.history else 0,
        "total_disruptions": len(disruption_points),
        "domain": [domain_min, domain_max]
    }
    
    # 添加中断事件详情
    if evolver.history:
        result["disruption_details"] = [
            {
                "step": i + 1,
                "error": error,
                "description": f"第{i+1}次中断，误差: {error:.4f}"
            }
            for i, (_, error) in enumerate(evolver.history)
        ]
    
    return result


def export_visualization_data(
    evolver: ConsciousFunctionEvolver,
    data_stream: List[Tuple[float, float]],
    output_format: str = "json"
) -> str:
    """
    导出可视化数据为指定格式。
    
    参数:
        evolver: 函数衍化器实例
        data_stream: 数据流
        output_format: 输出格式，支持"json"或"csv"
        
    返回:
        格式化后的数据字符串
    """
    import json
    import csv
    import io
    
    # 创建交互式数据
    data = create_interactive_visualization(evolver, data_stream)
    
    if output_format.lower() == "json":
        return json.dumps(data, indent=2)
    
    elif output_format.lower() == "csv":
        # 创建CSV格式的数据
        output = io.StringIO()
        writer = csv.writer(output)
        
        # 写入标题
        writer.writerow(["数据类型", "x", "y", "标签"])
        
        # 写入函数数据
        for i, (x, y) in enumerate(zip(data["x_values"], data["final_function"])):
            writer.writerow(["最终函数", x, y, f"最终函数点{i+1}"])
        
        # 写入常规点
        for point in data["regular_points"]:
            writer.writerow(["常规数据点", point["x"], point["y"], "常规点"])
        
        # 写入中断点
        for point in data["disruption_points"]:
            writer.writerow(["中断数据点", point["x"], point["y"], "中断点"])
        
        return output.getvalue()
    
    else:
        raise ValueError(f"不支持的输出格式: {output_format}")


# 如果直接运行此文件，提供一个简单的演示
if __name__ == "__main__":
    print("运行 visualization.py 演示...")
    
    # 创建一个简单的演示函数
    from function_evolution import ConsciousFunctionEvolver
    
    # 创建模拟数据
    base_func = lambda x: 2 * x + 1
    system = ConsciousFunctionEvolver(base_func, domain=(0, 10))
    
    # 创建模拟数据流
    data_stream = []
    for i in range(20):
        x = i * 0.5
        if 4 < x < 7:  # 在某个区间制造"意外"
            y = 1.5 * x + 3
        else:
            y = base_func(x)
        y += np.random.normal(0, 0.2)
        data_stream.append((x, y))
    
    # 运行实验
    system.run_experiment(data_stream)
    
    # 可视化
    fig = visualize_evolution(system, data_stream, save_path=None, show_plot=True)
    
    print("演示完成!")
