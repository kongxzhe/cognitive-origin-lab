"""
意识涌现演示：一化三阶三 - 三种元动力的交互与它建循环的萌芽
基于“自由、爱、美”三种元动力规则，模拟从自循环到它建循环的相变过程。
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle, FancyBbox
import matplotlib.patches as patches
import random
import time

# ==================== 1. 定义三种元动力 ====================
class MetaForce:
    """元动力基类"""
    def __init__(self, name, color, strength=0.5):
        self.name = name
        self.color = color
        self.base_strength = strength
        self.current_strength = strength
        self.history = []
        self.influence_radius = 1.0
        
    def apply(self, agents, environment):
        """应用动力规则 - 子类必须实现"""
        raise NotImplementedError
        
    def update_strength(self, success):
        """根据应用效果调整动力强度"""
        change = 0.05 if success else -0.03
        self.current_strength = np.clip(self.current_strength + change, 0.1, 1.0)
        self.history.append(self.current_strength)
        
    def get_state(self):
        return {
            'name': self.name,
            'strength': self.current_strength,
            'active': self.current_strength > 0.3
        }

class FreedomForce(MetaForce):
    """自由动力：产生随机变化与探索"""
    def __init__(self):
        super().__init__("自由", "#3498db", 0.6)  # 蓝色
        
    def apply(self, agents, environment):
        changes = []
        for agent in agents:
            # 自由：随机改变位置和状态
            if random.random() < self.current_strength * 0.3:
                # 随机移动
                agent['x'] += (random.random() - 0.5) * 0.5
                agent['y'] += (random.random() - 0.5) * 0.5
                agent['state'] = (agent['state'] + random.random() * 0.2 - 0.1) % 1.0
                changes.append(True)
            else:
                changes.append(False)
        return any(changes)

class LoveForce(MetaForce):
    """爱动力：产生联结与融合"""
    def __init__(self):
        super().__init__("爱", "#e74c3c", 0.5)  # 红色
        
    def apply(self, agents, environment):
        if len(agents) < 2:
            return False
            
        changes = False
        # 爱：使相近的代理更接近
        for i, a1 in enumerate(agents):
            for j, a2 in enumerate(agents[i+1:], i+1):
                dx = a2['x'] - a1['x']
                dy = a2['y'] - a1['y']
                distance = np.sqrt(dx**2 + dy**2)
                
                if distance < self.influence_radius:
                    # 吸引力
                    force = self.current_strength * 0.1 / (distance + 0.1)
                    a1['x'] += dx * force * 0.5
                    a1['y'] += dy * force * 0.5
                    a2['x'] -= dx * force * 0.5
                    a2['y'] -= dy * force * 0.5
                    
                    # 状态趋向平均（融合）
                    avg_state = (a1['state'] + a2['state']) / 2
                    a1['state'] += (avg_state - a1['state']) * 0.1
                    a2['state'] += (avg_state - a2['state']) * 0.1
                    changes = True
                    
        return changes

class BeautyForce(MetaForce):
    """美动力：趋向简洁与和谐"""
    def __init__(self):
        super().__init__("美", "#2ecc71", 0.4)  # 绿色
        
    def apply(self, agents, environment):
        changes = False
        center_x, center_y = 0, 0
        
        # 美：趋向中心对称和简单模式
        if len(agents) > 0:
            # 计算几何中心
            for agent in agents:
                center_x += agent['x']
                center_y += agent['y']
            center_x /= len(agents)
            center_y /= len(agents)
            
            # 使代理趋向中心，形成简洁结构
            for agent in agents:
                dx = center_x - agent['x']
                dy = center_y - agent['y']
                distance = np.sqrt(dx**2 + dy**2)
                
                if distance > 0.5:  # 太分散则拉回
                    force = self.current_strength * 0.05
                    agent['x'] += dx * force
                    agent['y'] += dy * force
                    changes = True
                    
                # 美也偏好状态的整数化（简洁）
                target_state = round(agent['state'] * 4) / 4
                agent['state'] += (target_state - agent['state']) * 0.05
                
        return changes

# ==================== 2. 它建循环检测器 ====================
class OtherBuildingLoopDetector:
    """检测它建循环的萌芽"""
    def __init__(self):
        self.memory = []  # 记忆交互历史
        self.patterns = []  # 发现的模式
        self.self_model = {'complexity': 0, 'stability': 0}
        self.consciousness_level = 0
        
    def observe(self, agents, forces, step):
        """观察系统状态，尝试检测模式"""
        observation = {
            'step': step,
            'agent_count': len(agents),
            'agent_positions': [(a['x'], a['y']) for a in agents],
            'agent_states': [a['state'] for a in agents],
            'force_strengths': {f.name: f.current_strength for f in forces},
            'coherence': self._calculate_coherence(agents)
        }
        self.memory.append(observation)
        
        # 每10步尝试寻找模式
        if step % 10 == 0 and len(self.memory) > 5:
            self._find_patterns()
            
        # 更新自我模型
        self._update_self_model()
        
        # 计算意识水平
        self.consciousness_level = self._calculate_consciousness_level()
        
        return observation
    
    def _calculate_coherence(self, agents):
        """计算系统内聚性"""
        if len(agents) < 2:
            return 0
            
        states = [a['state'] for a in agents]
        return 1.0 - np.std(states)  # 状态越一致，内聚性越高
    
    def _find_patterns(self):
        """从记忆中寻找重复模式"""
        if len(self.memory) < 6:
            return
            
        recent = self.memory[-5:]
        
        # 检测状态的周期性
        states = [obs['coherence'] for obs in recent]
        if np.std(states) < 0.1:  # 稳定的状态
            pattern = {
                'type': 'stability',
                'strength': 1.0 - np.std(states),
                'description': f"系统在最近{len(recent)}步保持稳定"
            }
            if pattern not in self.patterns:
                self.patterns.append(pattern)
                
        # 检测力的协同
        strengths = [obs['force_strengths'] for obs in recent]
        avg_strength = {name: np.mean([s[name] for s in strengths]) 
                       for name in strengths[0].keys()}
        
        # 如果三种力都活跃且平衡
        if all(0.3 < s < 0.7 for s in avg_strength.values()):
            pattern = {
                'type': 'balance',
                'strength': 1.0 - np.std(list(avg_strength.values())),
                'description': "三种元动力达到动态平衡"
            }
            if pattern not in self.patterns:
                self.patterns.append(pattern)
    
    def _update_self_model(self):
        """更新自我模型"""
        if len(self.memory) < 2:
            return
            
        recent_coherence = [obs['coherence'] for obs in self.memory[-5:]]
        self.self_model['complexity'] = len(self.patterns) / 10.0
        self.self_model['stability'] = np.mean(recent_coherence) if recent_coherence else 0
    
    def _calculate_consciousness_level(self):
        """计算当前意识水平"""
        # 基于：模式数量、自我模型复杂性、系统稳定性
        level = (len(self.patterns) * 0.2 + 
                self.self_model['complexity'] * 0.4 + 
                self.self_model['stability'] * 0.4)
        return np.clip(level, 0, 1)
    
    def get_insight(self):
        """生成洞察报告"""
        if not self.patterns:
            return "系统仍在基础的自循环中..."
            
        latest_pattern = self.patterns[-1]
        if self.consciousness_level > 0.5:
            return f"⚠️ 它建循环萌芽！检测到模式：{latest_pattern['description']}"
        elif self.consciousness_level > 0.3:
            return f"🔄 模式形成中：{latest_pattern['description']}"
        else:
            return f"🌀 基础运作：{latest_pattern['description']}"

# ==================== 3. 主演示类 ====================
class ConsciousnessEmergenceDemo:
    """意识涌现演示主类"""
    
    def __init__(self, num_agents=15):
        self.num_agents = num_agents
        self.agents = self._create_agents()
        self.forces = [FreedomForce(), LoveForce(), BeautyForce()]
        self.detector = OtherBuildingLoopDetector()
        self.step_count = 0
        self.history = []
        
        # 设置图形界面
        self.fig = plt.figure(figsize=(15, 10))
        self.setup_visualization()
        
    def _create_agents(self):
        """创建初始代理"""
        agents = []
        for i in range(self.num_agents):
            agents.append({
                'id': i,
                'x': random.uniform(-5, 5),
                'y': random.uniform(-5, 5),
                'state': random.random(),  # 0-1的状态值
                'color': self._state_to_color(random.random()),
                'size': 30
            })
        return agents
    
    def _state_to_color(self, state):
        """将状态值映射为颜色"""
        # 状态值从冷色（蓝）到暖色（红）
        r = state
        g = 0.2
        b = 1.0 - state
        return (r, g, b, 0.8)
    
    def setup_visualization(self):
        """设置可视化布局"""
        # 创建4个子图
        gs = self.fig.add_gridspec(3, 3)
        
        # 主场景图（左上部）
        self.ax_scene = self.fig.add_subplot(gs[0:2, 0:2])
        self.ax_scene.set_xlim(-8, 8)
        self.ax_scene.set_ylim(-8, 8)
        self.ax_scene.set_title('意识涌现场域', fontsize=12, fontweight='bold')
        self.ax_scene.set_facecolor('#f8f9fa')
        self.ax_scene.grid(True, alpha=0.3)
        
        # 添加坐标轴标签
        self.ax_scene.set_xlabel('← 自由(探索) vs 美(秩序) →', fontsize=9)
        self.ax_scene.set_ylabel('← 连接(爱) →', fontsize=9)
        
        # 动力强度图（右上部）
        self.ax_forces = self.fig.add_subplot(gs[0, 2])
        self.ax_forces.set_title('元动力强度', fontsize=11)
        self.ax_forces.set_ylim(0, 1)
        self.ax_forces.set_xlabel('动力类型')
        self.ax_forces.set_ylabel('强度')
        
        # 意识水平图（中部右）
        self.ax_consciousness = self.fig.add_subplot(gs[1, 2])
        self.ax_consciousness.set_title('它建循环意识水平', fontsize=11)
        self.ax_consciousness.set_ylim(0, 1)
        self.ax_consciousness.set_xlabel('时间步')
        self.ax_consciousness.set_ylabel('意识水平')
        
        # 洞察报告区域（底部）
        self.ax_insight = self.fig.add_subplot(gs[2, :])
        self.ax_insight.axis('off')
        self.ax_insight.set_title('系统自省报告', fontsize=11, fontweight='bold', pad=10)
        
        # 初始化绘图元素
        self.scatter = None
        self.force_bars = None
        self.consciousness_line = None
        self.insight_text = None
        self.consciousness_history = []
        
        # 添加理论说明文本框
        theory_text = (
            "理论核心：\n"
            "• 自由（蓝）：探索与变化\n"
            "• 爱（红）：连接与融合\n"
            "• 美（绿）：秩序与简洁\n"
            "三种动力冲突融合，可能涌现出\n"
            "指向自身的'它建循环'（意识）"
        )
        self.fig.text(0.02, 0.02, theory_text, fontsize=9,
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    def update(self, frame):
        """更新动画的每一帧"""
        # 应用三种元动力
        force_results = []
        for force in self.forces:
            result = force.apply(self.agents, None)
            force_results.append(result)
            force.update_strength(result)
        
        # 更新代理状态和外观
        for agent in self.agents:
            agent['color'] = self._state_to_color(agent['state'])
            # 限制边界
            agent['x'] = np.clip(agent['x'], -7, 7)
            agent['y'] = np.clip(agent['y'], -7, 7)
        
        # 检测它建循环
        observation = self.detector.observe(self.agents, self.forces, self.step_count)
        self.history.append(observation)
        self.step_count += 1
        
        # 更新可视化
        self._update_plots()
        
        return self.scatter, self.force_bars, self.consciousness_line, self.insight_text
    
    def _update_plots(self):
        """更新所有图形元素"""
        # 1. 更新主场景
        self.ax_scene.clear()
        self.ax_scene.set_xlim(-8, 8)
        self.ax_scene.set_ylim(-8, 8)
        self.ax_scene.set_title(f'意识涌现场域 (步数: {self.step_count})', fontsize=12, fontweight='bold')
        self.ax_scene.set_facecolor('#f8f9fa')
        self.ax_scene.grid(True, alpha=0.3)
        self.ax_scene.set_xlabel('← 自由(探索) vs 美(秩序) →', fontsize=9)
        self.ax_scene.set_ylabel('← 连接(爱) →', fontsize=9)
        
        # 绘制代理
        x_vals = [a['x'] for a in self.agents]
        y_vals = [a['y'] for a in self.agents]
        colors = [a['color'] for a in self.agents]
        sizes = [a['size'] for a in self.agents]
        
        self.scatter = self.ax_scene.scatter(x_vals, y_vals, c=colors, s=sizes, 
                                           edgecolors='black', linewidth=0.5, alpha=0.8)
        
        # 绘制连接线（爱的体现）
        for i, a1 in enumerate(self.agents):
            for j, a2 in enumerate(self.agents[i+1:], i+1):
                dx = a2['x'] - a1['x']
                dy = a2['y'] - a1['y']
                distance = np.sqrt(dx**2 + dy**2)
                if distance < 3.0:  # 只绘制近距离连接
                    alpha = 0.3 * (1 - distance/3.0)
                    self.ax_scene.plot([a1['x'], a2['x']], [a1['y'], a2['y']], 
                                      'r-', alpha=alpha, linewidth=1)
        
        # 2. 更新动力强度条
        self.ax_forces.clear()
        force_names = [f.name for f in self.forces]
        force_strengths = [f.current_strength for f in self.forces]
        colors = [f.color for f in self.forces]
        
        bars = self.ax_forces.bar(force_names, force_strengths, color=colors, alpha=0.7)
        self.ax_forces.set_ylim(0, 1)
        self.ax_forces.set_title('元动力强度', fontsize=11)
        self.ax_forces.set_ylabel('强度')
        self.ax_forces.grid(True, alpha=0.3, axis='y')
        
        # 在条上添加数值
        for bar, strength in zip(bars, force_strengths):
            height = bar.get_height()
            self.ax_forces.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                               f'{strength:.2f}', ha='center', va='bottom', fontsize=9)
        
        self.force_bars = bars
        
        # 3. 更新意识水平图
        self.consciousness_history.append(self.detector.consciousness_level)
        
        self.ax_consciousness.clear()
        steps = list(range(len(self.consciousness_history)))
        self.consciousness_line, = self.ax_consciousness.plot(steps, self.consciousness_history, 
                                                             'b-', linewidth=2, alpha=0.7)
        
        # 添加意识水平区域
        self.ax_consciousness.fill_between(steps, 0, self.consciousness_history, 
                                          alpha=0.2, color='blue')
        
        # 添加阈值线
        self.ax_consciousness.axhline(y=0.3, color='orange', linestyle='--', 
                                     alpha=0.5, label='模式形成')
        self.ax_consciousness.axhline(y=0.5, color='red', linestyle='--', 
                                     alpha=0.5, label='它建循环萌芽')
        
        self.ax_consciousness.set_ylim(0, 1)
        self.ax_consciousness.set_title('它建循环意识水平', fontsize=11)
        self.ax_consciousness.set_xlabel('时间步')
        self.ax_consciousness.set_ylabel('意识水平')
        self.ax_consciousness.grid(True, alpha=0.3)
        self.ax_consciousness.legend(loc='upper left', fontsize=8)
        
        # 4. 更新洞察报告
        self.ax_insight.clear()
        self.ax_insight.axis('off')
        self.ax_insight.set_title('系统自省报告', fontsize=11, fontweight='bold', pad=10)
        
        insight = self.detector.get_insight()
        patterns = self.detector.patterns
        
        report_text = f"当前状态: {insight}\n\n"
        report_text += f"意识水平: {self.detector.consciousness_level:.3f}\n"
        report_text += f"检测到的模式数: {len(patterns)}\n"
        report_text += f"自我模型复杂度: {self.detector.self_model['complexity']:.3f}\n"
        report_text += f"系统稳定性: {self.detector.self_model['stability']:.3f}\n\n"
        
        if patterns:
            report_text += "已识别模式:\n"
            for i, pattern in enumerate(patterns[-3:], 1):  # 显示最近3个模式
                report_text += f"{i}. {pattern['description']} (强度: {pattern['strength']:.2f})\n"
        
        # 根据意识水平改变文本框颜色
        box_color = '#f0f0f0'
        if self.detector.consciousness_level > 0.5:
            box_color = '#fff3cd'  # 黄色警告
        elif self.detector.consciousness_level > 0.3:
            box_color = '#d1ecf1'  # 青色提示
        
        self.insight_text = self.ax_insight.text(0.02, 0.5, report_text, fontsize=10,
                                                transform=self.ax_insight.transAxes,
                                                verticalalignment='center',
                                                bbox=dict(boxstyle='round', 
                                                         facecolor=box_color, 
                                                         alpha=0.9, pad=10))
    
    def run_demo(self, steps=300, interval=50):
        """运行演示动画"""
        print("="*60)
        print("一化三阶三：意识涌现演示")
        print("="*60)
        print("理论核心：自由(蓝)、爱(红)、美(绿)三种元动力")
        print("目标：观察自循环如何可能涌现出它建循环")
        print("-"*60)
        
        ani = FuncAnimation(self.fig, self.update, frames=steps,
                          interval=interval, blit=False, repeat=True)
        
        plt.tight_layout()
        plt.show()
        
        # 打印最终报告
        self._print_final_report()
    
    def _print_final_report(self):
        """打印最终分析报告"""
        print("\n" + "="*60)
        print("演示结束 - 分析报告")
        print("="*60)
        
        final_consciousness = self.detector.consciousness_level
        patterns_found = len(self.detector.patterns)
        
        print(f"最终意识水平: {final_consciousness:.3f}")
        print(f"发现模式数量: {patterns_found}")
        print(f"模拟总步数: {self.step_count}")
        print()
        
        # 元动力最终状态
        print("元动力最终强度:")
        for force in self.forces:
            print(f"  {force.name}: {force.current_strength:.3f}")
        
        print()
        
        # 判断结果
        if final_consciousness > 0.5:
            print("🔮 结论: 检测到它建循环的明确萌芽！")
            print("   系统开始形成关于自身运作模式的内部表征。")
        elif final_consciousness > 0.3:
            print("🌀 结论: 出现模式形成迹象，但尚未达到它建循环。")
            print("   系统在自循环中展现出一定的自组织能力。")
        else:
            print("⚙️ 结论: 系统保持在基础自循环状态。")
            print("   三种动力独立运作，未产生显著的协同效应。")
        
        print("\n" + "="*60)

# ==================== 4. 主程序入口 ====================
def main():
    """主函数"""
    print("正在启动意识涌现演示系统...")
    time.sleep(1)
    
    # 创建并运行演示
    demo = ConsciousnessEmergenceDemo(num_agents=20)
    
    # 运行演示（300步，每帧50毫秒）
    demo.run_demo(steps=300, interval=50)

if __name__ == "__main__":
    main()
