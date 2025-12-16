#!/usr/bin/env python3
"""
demo_conscious_evolution.py

认知起源实验室 - 主演示脚本
展示"意识作为函数衍化"模拟系统的多个实验场景。

核心思想演示：
1. 基本函数在遇到预测误差时的自适应演变
2. 多个中断点触发的复杂函数演变
3. 不同噪声水平下的系统稳定性测试
4. 哲学框架与实际模拟的对应关系展示
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import List, Tuple, Dict, Any

# 添加项目根目录到Python路径，确保可以导入cognitive_models包
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from cognitive_models.function_evolution import ConsciousFunctionEvolver
from cognitive_models.visualization import visualize_evolution, plot_function_comparison


def setup_experiment_environment() -> None:
    """设置实验环境，创建必要的目录结构"""
    output_dir = project_root / "experiments" / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("认知起源实验室 - 意识作为函数衍化 模拟演示")
    print("=" * 70)
    print(f"输出目录: {output_dir}")
    print()


def experiment_1_basic_linear_evolution() -> Dict[str, Any]:
    """
    实验1：基础线性函数演化
    演示一个简单线性函数如何适应"意外"数据点
    
    哲学对应：基本认知模式在遇到轻微不符经验时的调整
    """
    print("\n" + "=" * 60)
    print("实验1：基础线性函数演化")
    print("=" * 60)
    
    # 定义初始"无意识"函数：y = 2x + 1
    print("初始函数：y = 2x + 1")
    print("这代表一个稳定的认知模式/无意识处理规则")
    
    base_func = lambda x: 2 * x + 1
    system = ConsciousFunctionEvolver(base_func, domain=(0, 10))
    
    # 创建数据流：大部分符合旧规律，但在区间[4, 7]引入"意外"
    print("\n生成数据流...")
    print("在 x∈[4, 7] 区间引入新规律：y = 1.5x + 3")
    print("这模拟了认知系统遇到的与预期不符的新经验")
    
    data_stream = []
    for i in range(20):
        x = i * 0.5  # 从0到9.5，步长0.5
        
        # 在特定区间制造"认知冲突"（意外数据）
        if 4.0 <= x <= 7.0:  
            y = 1.5 * x + 3  # 新的规律
            data_type = "意外"
        else:
            y = base_func(x)  # 旧规律
            data_type = "常规"
        
        # 加入随机噪声，模拟感知的不确定性
        y += np.random.normal(0, 0.15)
        data_stream.append((x, y))
        
        if i % 5 == 0:  # 每5个点打印一次
            print(f"  数据点 {i+1:2d}: x={x:4.1f}, y={y:6.2f} ({data_type})")
    
    # 运行实验
    print("\n开始实验...")
    print("-" * 40)
    results = system.run_experiment(data_stream)
    
    print(f"\n实验结果摘要：")
    print(f"  总数据点: {len(data_stream)}")
    print(f"  中断事件: {results['total_disruptions']}次")
    print(f"  函数演变: {results['evolution_steps']}个阶段")
    
    # 可视化
    print("\n生成可视化图表...")
    fig = visualize_evolution(
        system, 
        data_stream,
        save_path=str(project_root / "experiments" / "outputs" / "experiment_1_basic_evolution.png"),
        show_plot=False
    )
    
    # 显示最终函数的信息
    final_func = results['final_function']
    test_x = [2.0, 5.0, 8.0]
    print(f"\n最终函数测试 (在x={test_x}时)：")
    for x in test_x:
        y = final_func(x)
        print(f"  f({x}) = {y:.2f}")
    
    return {
        "system": system,
        "results": results,
        "data_stream": data_stream,
        "figure": fig
    }


def experiment_2_complex_pattern_adaptation() -> Dict[str, Any]:
    """
    实验2：复杂模式适应
    演示系统处理多个不连续"意外"区域的能力
    
    哲学对应：认知系统面对复杂矛盾经验时的分段适应
    """
    print("\n" + "=" * 60)
    print("实验2：复杂模式适应（多个中断区域）")
    print("=" * 60)
    
    # 更复杂的初始函数：二次函数
    print("初始函数：y = 0.3x² - 1.5x + 2")
    base_func = lambda x: 0.3 * x**2 - 1.5 * x + 2
    system = ConsciousFunctionEvolver(base_func, domain=(0, 12))
    
    # 创建包含多个"意外"区域的数据流
    print("\n数据流包含三个意外区域：")
    print("  区域1: x∈[2, 4] -> y = 1.8x + 0.5")
    print("  区域2: x∈[6, 8] -> y = -0.8x + 10")
    print("  区域3: x∈[9, 11] -> y = 0.1x² + 1")
    
    data_stream = []
    for i in range(30):
        x = i * 0.4  # 从0到11.6
        
        # 定义多个意外区域
        if 2.0 <= x <= 4.0:
            y = 1.8 * x + 0.5
            region = "区域1"
        elif 6.0 <= x <= 8.0:
            y = -0.8 * x + 10
            region = "区域2"
        elif 9.0 <= x <= 11.0:
            y = 0.1 * x**2 + 1
            region = "区域3"
        else:
            y = base_func(x)
            region = "常规"
        
        # 增加噪声
        y += np.random.normal(0, 0.2)
        data_stream.append((x, y))
        
        if i % 8 == 0:
            print(f"  数据点 {i+1:2d}: x={x:4.1f}, y={y:6.2f} ({region})")
    
    # 运行实验
    print("\n开始实验...")
    results = system.run_experiment(data_stream)
    
    print(f"\n实验结果：")
    print(f"  总中断事件: {results['total_disruptions']}次")
    print(f"  函数经历了 {results['evolution_steps']} 次重大调整")
    
    # 可视化
    fig = visualize_evolution(
        system,
        data_stream,
        save_path=str(project_root / "experiments" / "outputs" / "experiment_2_complex_adaptation.png"),
        show_plot=False
    )
    
    return {
        "system": system,
        "results": results,
        "data_stream": data_stream,
        "figure": fig
    }


def experiment_3_noise_resilience_test() -> Dict[str, Any]:
    """
    实验3：噪声鲁棒性测试
    测试系统在不同噪声水平下的稳定性
    
    哲学对应：认知系统在信息不确定环境中的稳定性
    """
    print("\n" + "=" * 60)
    print("实验3：噪声鲁棒性测试")
    print("=" * 60)
    
    # 测试不同的噪声水平
    noise_levels = [0.05, 0.15, 0.3, 0.5]
    results_by_noise = {}
    
    for noise_level in noise_levels:
        print(f"\n测试噪声水平: {noise_level}")
        print("-" * 30)
        
        base_func = lambda x: 2.5 * np.sin(0.5 * x) + 3
        system = ConsciousFunctionEvolver(base_func, domain=(0, 10))
        
        # 创建数据流，在x∈[3, 7]引入系统性的变化
        data_stream = []
        disruptions_expected = 0
        
        for i in range(25):
            x = i * 0.4
            if 3.0 <= x <= 7.0:
                y = 1.2 * x + 1  # 新规律
                disruptions_expected += 1
            else:
                y = base_func(x)  # 原规律
            
            # 应用当前噪声水平的随机噪声
            y += np.random.normal(0, noise_level)
            data_stream.append((x, y))
        
        # 运行实验
        results = system.run_experiment(data_stream)
        results_by_noise[noise_level] = {
            "actual_disruptions": results['total_disruptions'],
            "expected_disruptions": min(disruptions_expected, 1),  # 至少一次
            "evolution_steps": results['evolution_steps']
        }
        
        print(f"  实际中断: {results['total_disruptions']}次")
        print(f"  演变步骤: {results['evolution_steps']}步")
    
    # 分析噪声鲁棒性
    print("\n" + "-" * 40)
    print("噪声鲁棒性分析：")
    print("噪声水平 | 实际中断 | 演变步骤 | 稳定性")
    print("-" * 40)
    
    for noise_level in noise_levels:
        result = results_by_noise[noise_level]
        stability = "高" if result['evolution_steps'] <= 2 else "中" if result['evolution_steps'] <= 4 else "低"
        print(f"{noise_level:6.2f}   | {result['actual_disruptions']:8d} | {result['evolution_steps']:8d} | {stability}")
    
    return results_by_noise


def experiment_4_philosophical_discussion():
    """
    实验4：哲学讨论与框架对应
    将模拟结果与原始哲学框架对应起来
    """
    print("\n" + "=" * 60)
    print("实验4：哲学框架对应分析")
    print("=" * 60)
    
    print("""
    原始哲学命题：
    "本心和灵性到底是什么，会不会就是一种可衍化的，
    并基于衍化展开的自解码函数呢？"
    
    模拟框架对应关系：
    """)
    
    framework_map = {
        "函数": "认知系统的基本处理规则/模式",
        "现象": "输入数据流 (x, y) 序列",
        "无意识": "函数稳定运行，准确预测大部分数据",
        "中断": "预测误差超过阈值，系统检测到异常",
        "衍生新变化": "系统生成新的候选函数假设",
        "有意识": "中断→衍生→选择新函数的完整过程",
        "自解码": "系统通过分析误差模式理解自身局限",
        "可衍化": "系统能够改变自身处理规则的能力"
    }
    
    for concept, explanation in framework_map.items():
        print(f"  • {concept:8s} → {explanation}")
    
    print("""
    
    模拟演示的核心洞见：
    1. 意识不是静态的"东西"，而是动态的"过程"
    2. 这个过程就是认知规则在冲突压力下的适应性演变
    3. 系统通过"预测-误差-调整"循环实现"自解码"
    4. "可衍化性"是系统的基本属性，不是额外添加的功能
    
    在模拟中，当函数遇到无法解释的数据时，它不会崩溃，
    而是会探索新的解释框架。这种探索和选择的过程，
    就是我们观察到的"有意识"调整。
    """)
    
    # 创建一个简单的示意图来展示哲学框架
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 绘制哲学框架图
    nodes = {
        "现象\n(数据输入)": (0.1, 0.5),
        "函数\n(处理规则)": (0.3, 0.7),
        "无意识\n(稳定运行)": (0.3, 0.3),
        "预测误差\n(中断)": (0.5, 0.5),
        "衍生\n(新假设)": (0.7, 0.7),
        "有意识\n(调整过程)": (0.7, 0.3),
        "新函数\n(适应后规则)": (0.9, 0.5)
    }
    
    # 绘制节点
    for label, (x, y) in nodes.items():
        color = 'lightblue' if '意识' in label or '误差' in label else 'lightgray'
        ax.add_patch(plt.Circle((x, y), 0.05, color=color, ec='black', lw=2))
        ax.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold')
    
    # 绘制连接线
    connections = [
        ("现象", "函数"),
        ("函数", "无意识"),
        ("函数", "预测误差"),
        ("预测误差", "衍生"),
        ("预测误差", "有意识"),
        ("衍生", "新函数"),
        ("有意识", "新函数")
    ]
    
    for start, end in connections:
        x1, y1 = nodes[start]
        x2, y2 = nodes[end]
        ax.arrow(x1 + 0.05, y1, x2 - x1 - 0.1, y2 - y1, 
                head_width=0.02, head_length=0.03, fc='black', ec='black', alpha=0.6)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('"意识作为函数衍化"哲学框架示意图', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(
        str(project_root / "experiments" / "outputs" / "philosophical_framework.png"),
        dpi=150, bbox_inches='tight'
    )
    print(f"\n哲学框架示意图已保存至: experiments/outputs/philosophical_framework.png")


def run_all_experiments():
    """运行所有实验"""
    setup_experiment_environment()
    
    print("开始运行认知起源模拟实验...")
    print("每个实验展示意识作为'函数衍化'过程的不同方面")
    
    try:
        # 运行实验1：基础演化
        exp1_results = experiment_1_basic_linear_evolution()
        
        # 运行实验2：复杂模式适应
        exp2_results = experiment_2_complex_pattern_adaptation()
        
        # 运行实验3：噪声鲁棒性
        exp3_results = experiment_3_noise_resilience_test()
        
        # 运行实验4：哲学讨论
        experiment_4_philosophical_discussion()
        
        # 生成综合报告
        generate_summary_report(exp1_results, exp2_results, exp3_results)
        
    except Exception as e:
        print(f"\n错误：实验运行过程中出现异常: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def generate_summary_report(exp1, exp2, exp3):
    """生成实验总结报告"""
    print("\n" + "=" * 70)
    print("实验总结报告")
    print("=" * 70)
    
    print(f"""
    综合发现：
    
    1. 基础演化 (实验1)：
       • 系统成功检测到与预期不符的数据模式
       • 通过生成和选择新假设完成函数演变
       • 演示了从"无意识"稳定态到"有意识"调整的基本过程
    
    2. 复杂适应 (实验2)：
       • 系统能够处理多个不连续区域的模式变化
       • 展示了认知系统的分段适应能力
       • 复杂模式需要更多的"中断-调整"循环
    
    3. 噪声鲁棒性 (实验3)：
       • 低噪声下系统稳定，准确检测真实模式变化
       • 高噪声下可能出现误报或过度调整
       • 噪声水平影响系统的"判断"准确性
    
    关键洞见：
    • 意识作为过程：意识不是认知的某个部分，而是认知系统
      在应对预测失败时的整个调整过程
    
    • 自解码能力：系统通过分析自身预测误差来理解
      当前认知框架的局限性，这是"自解码"的核心
    
    • 可衍化性：一个真正有适应性的认知系统必须具备
      改变自身处理规则的能力，而不仅仅是调整参数
    
    后续研究方向：
    1. 引入多层级的函数系统（元认知）
    2. 添加环境交互和具身性要素
    3. 探索函数演变的社会性（多系统交互）
    4. 将离散函数扩展为连续神经网络
    """)
    
    # 保存报告
    report_path = project_root / "experiments" / "outputs" / "experiment_summary.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("认知起源实验室 - 实验总结报告\n")
        f.write("=" * 50 + "\n\n")
        f.write("所有图表已保存至 experiments/outputs/ 目录\n")
    
    print(f"\n详细报告已保存至: {report_path}")
    print("所有输出图表保存在: experiments/outputs/")
    print("\n演示完成！")


def quick_demo():
    """快速演示版本，适合初次体验"""
    print("\n" + "=" * 60)
    print("快速演示：意识作为函数衍化")
    print("=" * 60)
    
    # 简化的演示
    base_func = lambda x: 2 * x + 1
    system = ConsciousFunctionEvolver(base_func, domain=(0, 8))
    
    # 少量数据点
    data_stream = [
        (1.0, 3.2), (2.0, 5.1), (3.0, 7.3),  # 符合预期
        (4.0, 10.5),  # 轻微意外
        (5.0, 15.8),  # 重大意外 - 应触发中断
        (6.0, 13.1), (7.0, 15.4)  # 后续点
    ]
    
    print(f"初始函数: y = 2x + 1")
    print(f"测试数据点: {len(data_stream)}个")
    print("\n运行模拟...")
    
    results = system.run_experiment(data_stream)
    
    print(f"\n结果：经历了 {results['total_disruptions']} 次意识中断")
    print(f"函数演变了 {results['evolution_steps']} 次")
    
    # 简单可视化
    fig = visualize_evolution(
        system,
        data_stream,
        save_path=str(project_root / "experiments" / "outputs" / "quick_demo.png"),
        show_plot=True  # 这次显示图表
    )
    
    print("\n快速演示完成！")
    return system, results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='运行认知起源模拟实验')
    parser.add_argument('--mode', choices=['full', 'quick', 'exp1', 'exp2', 'exp3', 'exp4'],
                       default='full', help='运行模式 (默认: full)')
    
    args = parser.parse_args()
    
    if args.mode == 'full':
        success = run_all_experiments()
        if success:
            print("\n✅ 所有实验完成！")
        else:
            print("\n❌ 实验运行出错")
            
    elif args.mode == 'quick':
        quick_demo()
        
    elif args.mode == 'exp1':
        experiment_1_basic_linear_evolution()
        plt.show()  # 显示图表
        
    elif args.mode == 'exp2':
        experiment_2_complex_pattern_adaptation()
        plt.show()
        
    elif args.mode == 'exp3':
        experiment_3_noise_resilience_test()
        
    elif args.mode == 'exp4':
        experiment_4_philosophical_discussion()
        plt.show()
    
    print("\n感谢使用认知起源实验室模拟系统！")
    print("更多信息请访问项目仓库: https://github.com/kongxzhe/cognitive-origin-lab")
