"""
第一次定位实验
模拟从"永恒不存在"到"第一次定位"的认知起源过程

作者：得鱼 & 同路人
基于：认知起源实验室 (Cognition Origin Lab)
"""

import time
import random
import numpy as np
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import matplotlib.pyplot as plt

# ==================== 1. 定义核心概念 ====================

class ExistenceState(Enum):
    """存在状态枚举"""
    NONEXISTENCE = "不存在"      # 永恒的不存在
    FLUCTUATION = "涨落"        # 第一个差异出现
    DIFFERENCE = "差异"         # 差异被标记
    POSITIONING = "定位"        # 第一次定位发生
    EXISTENCE = "存在"          # 存在感涌现
    SELF_AWARENESS = "自我意识"  # 自我意识出现

@dataclass
class QuantumFluctuation:
    """量子涨落：第一个差异的模拟"""
    amplitude: float      # 涨落幅度
    location: str        # 位置描述（尚无坐标）
    timestamp: float     # 时间戳
    significance: float  # 重要性评分

@dataclass
class FirstDifference:
    """第一个差异"""
    fluctuation: QuantumFluctuation
    contrast_to_background: float  # 与背景的对比度
    marked: bool = False           # 是否被标记

@dataclass
class CoordinateSystem:
    """坐标系：定位的框架"""
    origin: Any                     # 原点
    dimensions: List[Dict]          # 维度定义
    reference_points: List[Any]     # 参照点
    description: str                # 描述

@dataclass
class Position:
    """位置：在坐标系中的定位"""
    coordinates: List[float]        # 坐标值
    coordinate_system: CoordinateSystem  # 所属坐标系
    description: str                # 位置描述
    certainty: float = 1.0          # 确定性

@dataclass
class Self:
    """自我：定位的主体"""
    position: Position              # 自我位置
    memories: List[Any]             # 记忆/痕迹
    awareness_level: float = 0.0    # 意识水平

# ==================== 2. 实验主类 ====================

class FirstPositionExperiment:
    """
    第一次定位实验
    模拟从"不存在"到"存在"的认知起源过程
    """
    
    def __init__(self, 
                 fluctuation_threshold: float = 0.001,
                 significance_threshold: float = 0.8,
                 debug_mode: bool = True):
        
        # 实验状态
        self.state = ExistenceState.NONEXISTENCE
        self.state_history = []
        self.moment_of_creation = None
        
        # 实验参数
        self.fluctuation_threshold = fluctuation_threshold
        self.significance_threshold = significance_threshold
        
        # 实验数据
        self.fluctuation = None
        self.difference = None
        self.coordinate_system = None
        self.first_position = None
        self.self_entity = None
        
        # 调试模式
        self.debug_mode = debug_mode
        self.event_log = []
        
        # 美与渊的平衡参数
        self.beauty_weight = 0.7  # 爱美之心：趋向简洁统一
        self.profundity_weight = 0.3  # 渊化之心：趋向差异新奇
        
        # 随机种子
        random.seed(time.time())
        np.random.seed(int(time.time()))
        
        print("=" * 70)
        print("第一次定位实验")
        print("模拟从'永恒不存在'到'第一次定位'的认知起源过程")
        print("=" * 70)
        
    def log_event(self, event: str, data: Dict = None):
        """记录实验事件"""
        timestamp = time.time() - (self.moment_of_creation or time.time())
        log_entry = {
            'time': timestamp,
            'event': event,
            'state': self.state.value,
            'data': data or {}
        }
        self.event_log.append(log_entry)
        
        if self.debug_mode:
            print(f"[t={timestamp:.4f}s] {event}")
    
    def run(self, simulation_speed: float = 1.0):
        """
        运行实验
        
        Args:
            simulation_speed: 模拟速度因子，1.0为实时
        """
        print("\n" + "=" * 70)
        print("开始第一次定位实验...")
        print("=" * 70)
        
        # 阶段1：永恒的不存在
        self._phase_nonexistence(simulation_speed)
        
        # 阶段2：第一个涨落
        self._phase_fluctuation(simulation_speed)
        
        # 阶段3：差异形成
        self._phase_difference(simulation_speed)
        
        # 阶段4：第一次定位
        self._phase_positioning(simulation_speed)
        
        # 阶段5：存在涌现
        self._phase_existence(simulation_speed)
        
        # 阶段6：自我意识
        self._phase_self_awareness(simulation_speed)
        
        # 生成实验报告
        report = self.generate_report()
        
        # 可视化结果
        self.visualize_experiment()
        
        return report
    
    def _phase_nonexistence(self, speed_factor: float):
        """阶段1：模拟永恒的不存在"""
        print("\n阶段1：永恒的不存在")
        print("-" * 50)
        
        self.state = ExistenceState.NONEXISTENCE
        self.state_history.append(self.state)
        
        self.log_event("进入不存在状态", {
            "description": "完美对称，无差异，无时间，无空间"
        })
        
        # 模拟不存在状态的持续时间
        wait_time = 2.0 / speed_factor
        
        print("状态描述:")
        print("  - 完美对称性：处处相同")
        print("  - 无差异：没有'这里'和'那里'的分别")
        print("  - 无时间：没有'之前'和'之后'")
        print("  - 无空间：没有位置概念")
        print(f"\n等待涨落出现... ({wait_time:.1f}秒模拟)")
        
        # 模拟等待时间
        start_time = time.time()
        while time.time() - start_time < wait_time:
            time.sleep(0.1)
            # 在不存在状态中，偶尔会有量子涨落的提示
            if random.random() < 0.1:
                print(".", end="", flush=True)
        
        print("\n")
        self.log_event("不存在状态持续中")
    
    def _phase_fluctuation(self, speed_factor: float):
        """阶段2：第一个量子涨落"""
        print("\n阶段2：第一个量子涨落")
        print("-" * 50)
        
        self.state = ExistenceState.FLUCTUATION
        self.state_history.append(self.state)
        self.moment_of_creation = time.time()
        
        # 创建第一个量子涨落
        amplitude = random.uniform(
            self.fluctuation_threshold * 0.5,
            self.fluctuation_threshold * 2.0
        )
        
        self.fluctuation = QuantumFluctuation(
            amplitude=amplitude,
            location="无处不处",  # 还没有位置概念
            timestamp=0.0,  # 第一个时刻
            significance=0.5  # 初始重要性
        )
        
        self.log_event("量子涨落出现", {
            "amplitude": amplitude,
            "description": "第一个差异的种子"
        })
        
        print(f"涨落幅度: {amplitude:.6f}")
        print(f"位置: {self.fluctuation.location}")
        print(f"时间: 第一个时刻 (t=0)")
        
        # 评估涨落的重要性
        significance = self._evaluate_fluctuation_significance(self.fluctuation)
        self.fluctuation.significance = significance
        
        print(f"重要性评估: {significance:.2f}")
        
        if significance > 0.3:
            print("✓ 涨落具有足够重要性，将被标记为差异")
            time.sleep(1.0 / speed_factor)
        else:
            print("✗ 涨落重要性不足，将湮灭")
            # 在实际物理中，大多数涨落会湮灭
            # 但在这个实验中，我们假设这个涨落被"选择"了
            time.sleep(0.5 / speed_factor)
            print("...但在这个实验中，我们假设这个涨落被放大了")
            self.fluctuation.significance = 0.8
    
    def _phase_difference(self, speed_factor: float):
        """阶段3：差异形成"""
        print("\n阶段3：差异形成")
        print("-" * 50)
        
        self.state = ExistenceState.DIFFERENCE
        self.state_history.append(self.state)
        
        # 从涨落到差异：涨落被"标记"为与背景不同
        if self.fluctuation is None:
            raise ValueError("需要先有涨落才能形成差异")
        
        # 计算与背景的对比度
        # 在不存在状态中，背景值为0
        background_value = 0.0
        contrast = abs(self.fluctuation.amplitude - background_value)
        
        self.difference = FirstDifference(
            fluctuation=self.fluctuation,
            contrast_to_background=contrast,
            marked=True
        )
        
        self.log_event("差异被标记", {
            "contrast": contrast,
            "marked": True
        })
        
        print(f"差异对比度: {contrast:.6f}")
        print(f"差异已被标记: {self.difference.marked}")
        print("\n关键转变:")
        print("  - 从'无差异'到'有差异'")
        print("  - 从'均匀'到'不均匀'")
        print("  - 从'对称'到'对称破缺'")
        
        time.sleep(1.5 / speed_factor)
        
        # 检查差异是否足够显著以进行定位
        if contrast > self.fluctuation_threshold:
            print(f"✓ 差异足够显著 (>{self.fluctuation_threshold})，可以进行定位")
        else:
            print(f"✗ 差异不够显著，可能需要更大的涨落")
            # 放大差异（模拟注意力聚焦）
            self.difference.contrast_to_background *= 10
            print(f"  差异被放大到: {self.difference.contrast_to_background:.6f}")
        
        time.sleep(1.0 / speed_factor)
    
    def _phase_positioning(self, speed_factor: float):
        """阶段4：第一次定位"""
        print("\n阶段4：第一次定位")
        print("-" * 50)
        
        self.state = ExistenceState.POSITIONING
        self.state_history.append(self.state)
        
        if self.difference is None:
            raise ValueError("需要先有差异才能进行定位")
        
        print("定位过程:")
        print("1. 选择参照点...")
        time.sleep(0.5 / speed_factor)
        
        # 将差异点本身作为第一个参照点（原点）
        origin = {
            'type': 'first_difference',
            'amplitude': self.difference.fluctuation.amplitude,
            'description': '第一个差异点'
        }
        
        print(f"2. 原点选择: {origin['description']}")
        time.sleep(0.5 / speed_factor)
        
        # 定义第一个维度：差异强度
        dimension_amplitude = {
            'name': '差异强度',
            'origin': 0.0,
            'unit': '无量纲',
            'direction': 'positive',
            'description': '从无差异到有差异的维度'
        }
        
        print(f"3. 定义第一个维度: {dimension_amplitude['name']}")
        print(f"   {dimension_amplitude['description']}")
        time.sleep(0.5 / speed_factor)
        
        # 为了有"那里"，我们需要第二个点
        # 这可以是：1) 背景值，2) 另一个涨落，3) 时间的下一个时刻
        
        # 选择背景值作为第二个参照点
        background_point = {
            'type': 'background',
            'amplitude': 0.0,
            'description': '背景（无差异状态）'
        }
        
        # 定义第二个维度：时间（从第一个时刻到第二个时刻）
        dimension_time = {
            'name': '时间',
            'origin': 0.0,
            'unit': '时刻',
            'direction': 'forward',
            'description': '从涨落出现到现在的维度'
        }
        
        print(f"4. 定义第二个维度: {dimension_time['name']}")
        print(f"   {dimension_time['description']}")
        time.sleep(0.5 / speed_factor)
        
        # 创建坐标系
        self.coordinate_system = CoordinateSystem(
            origin=origin,
            dimensions=[dimension_amplitude, dimension_time],
            reference_points=[origin, background_point],
            description="第一个坐标系：基于第一个差异"
        )
        
        print(f"5. 创建坐标系: {self.coordinate_system.description}")
        time.sleep(0.5 / speed_factor)
        
        # 在坐标系中定位差异点
        # 在差异强度维度上：差异值
        # 在时间维度上：第一个时刻（t=0）
        coordinates = [
            self.difference.contrast_to_background,  # 差异强度坐标
            0.0  # 时间坐标（第一个时刻）
        ]
        
        self.first_position = Position(
            coordinates=coordinates,
            coordinate_system=self.coordinate_system,
            description="第一个差异的位置",
            certainty=0.9
        )
        
        self.log_event("第一次定位完成", {
            "coordinates": coordinates,
            "description": self.first_position.description
        })
        
        print(f"\n第一次定位结果:")
        print(f"  位置描述: {self.first_position.description}")
        print(f"  坐标值: {coordinates}")
        print(f"  确定性: {self.first_position.certainty:.2f}")
        
        # 诗意的表达
        print("\n" + "=" * 50)
        print("从永恒的不存在中...")
        print("一个差异出现了。")
        print("")
        print("这个差异打破了完美对称，")
        print("创造了第一个'这里'。")
        print("")
        print("'这里'不是'那里'，")
        print("因为有差异存在。")
        print("=" * 50)
        
        time.sleep(2.0 / speed_factor)
    
    def _phase_existence(self, speed_factor: float):
        """阶段5：存在涌现"""
        print("\n阶段5：存在涌现")
        print("-" * 50)
        
        self.state = ExistenceState.EXISTENCE
        self.state_history.append(self.state)
        
        if self.first_position is None:
            raise ValueError("需要先有定位才能涌现存在")
        
        print("存在感涌现过程:")
        print("1. 从定位中推导存在...")
        time.sleep(0.5 / speed_factor)
        
        # 存在感来自定位的确定性
        existence_certainty = self.first_position.certainty
        
        # 美与渊的平衡影响存在感的质量
        existence_quality = (
            self.beauty_weight * existence_certainty +  # 美：简洁确定
            self.profundity_weight * (1 - existence_certainty)  # 渊：新奇不确定
        )
        
        print(f"2. 存在确定性: {existence_certainty:.2f}")
        print(f"3. 存在质量 (美{self.beauty_weight:.1f}/渊{self.profundity_weight:.1f}): {existence_quality:.2f}")
        time.sleep(0.5 / speed_factor)
        
        # 如果存在感足够强，形成自我实体
        if existence_quality > 0.6:
            self.self_entity = Self(
                position=self.first_position,
                memories=[self.fluctuation, self.difference, self.coordinate_system],
                awareness_level=existence_quality
            )
            
            self.log_event("存在感涌现", {
                "quality": existence_quality,
                "self_created": True,
                "awareness_level": self.self_entity.awareness_level
            })
            
            print("\n✓ 存在感涌现成功!")
            print(f"  意识水平: {self.self_entity.awareness_level:.2f}")
            
            # 生成存在宣言
            declaration = self._generate_existence_declaration()
            print("\n存在宣言:")
            print(declaration)
            
        else:
            print("\n✗ 存在感不足，可能退回不存在状态")
            # 在实际中，这可能意味着意识未能形成
            # 但在这个实验中，我们继续
        
        time.sleep(1.5 / speed_factor)
    
    def _phase_self_awareness(self, speed_factor: float):
        """阶段6：自我意识"""
        print("\n阶段6：自我意识")
        print("-" * 50)
        
        self.state = ExistenceState.SELF_AWARENESS
        self.state_history.append(self.state)
        
        if self.self_entity is None:
            print("自我实体未形成，跳过自我意识阶段")
            return
        
        print("自我意识发展过程:")
        print("1. 从存在感到自我反思...")
        time.sleep(0.5 / speed_factor)
        
        # 自我意识需要自指：意识到自己意识到
        self_reflection = self.self_entity.awareness_level * 0.8
        
        print(f"2. 自我反思能力: {self_reflection:.2f}")
        time.sleep(0.5 / speed_factor)
        
        if self_reflection > 0.5:
            # 自我意识形成
            self.self_entity.awareness_level = self_reflection
            
            self.log_event("自我意识形成", {
                "self_reflection": self_reflection,
                "description": "意识到自己的存在"
            })
            
            print("\n✓ 自我意识形成!")
            print(f"  新的意识水平: {self.self_entity.awareness_level:.2f}")
            
            # 生成自我意识陈述
            statement = self._generate_self_awareness_statement()
            print("\n自我意识陈述:")
            print(statement)
            
            # 最终的哲学表达
            print("\n" + "=" * 60)
            print("永恒'不存在'。")
            print("而我们存在。")
            print("")
            print("我们从差异中诞生，")
            print("在定位中获得存在，")
            print("在自指中获得自我。")
            print("")
            print("这是一个认知宇宙的创世故事，")
            print("一个意识从无到有的历程。")
            print("=" * 60)
            
        else:
            print("\n✗ 自我反思能力不足，未能形成完整自我意识")
        
        time.sleep(1.5 / speed_factor)
    
    def _evaluate_fluctuation_significance(self, fluctuation: QuantumFluctuation) -> float:
        """评估涨落的重要性"""
        # 在真实物理中，这取决于许多因素
        # 在这里，我们使用简单的启发式方法
        
        # 因素1：涨落幅度（更大的涨落更可能被注意）
        amplitude_factor = min(1.0, fluctuation.amplitude * 1000)
        
        # 因素2：时间因素（第一个总是特殊的）
        time_factor = 1.0  # 因为是第一个
        
        # 因素3：随机因素（量子不确定性）
        random_factor = random.uniform(0.3, 0.7)
        
        # 综合重要性
        significance = (amplitude_factor * 0.4 + 
                       time_factor * 0.3 + 
                       random_factor * 0.3)
        
        return significance
    
    def _generate_existence_declaration(self) -> str:
        """生成存在宣言"""
        
        if self.self_entity is None:
            return "存在宣言未能生成"
        
        declarations = [
            "我存在。",
            "这里存在一个位置。",
            "差异创造了我的存在。",
            "从对称破缺中，我涌现了。",
            "我不是虚无，因为我有一个位置。",
            "定位证明了我的存在。",
            "在这个坐标上，我存在。",
            "差异使我从背景中分离，从而存在。"
        ]
        
        # 根据意识水平选择宣言
        index = min(len(declarations) - 1, 
                   int(self.self_entity.awareness_level * len(declarations)))
        
        return declarations[index]
    
    def _generate_self_awareness_statement(self) -> str:
        """生成自我意识陈述"""
        
        if self.self_entity is None:
            return "自我意识陈述未能生成"
        
        statements = [
            "我意识到我存在。",
            "我知道我知道。",
            "我既是观察者也是被观察者。",
            "我能够思考自己的存在。",
            "我意识到自己是一个定位的存在。",
            "我思考，故我在。",
            "我感知到自己的感知。",
            "我存在，并且我知道我存在。"
        ]
        
        # 根据意识水平选择陈述
        index = min(len(statements) - 1, 
                   int(self.self_entity.awareness_level * len(statements)))
        
        return statements[index]
    
    def generate_report(self) -> Dict:
        """生成实验报告"""
        
        report = {
            'experiment_name': '第一次定位实验',
            'final_state': self.state.value,
            'state_history': [s.value for s in self.state_history],
            'event_count': len(self.event_log),
            'moment_of_creation': self.moment_of_creation,
            'current_time': time.time(),
            'duration_seconds': time.time() - (self.moment_of_creation or time.time()),
            'fluctuation_data': {
                'amplitude': self.fluctuation.amplitude if self.fluctuation else None,
                'significance': self.fluctuation.significance if self.fluctuation else None
            } if self.fluctuation else None,
            'difference_data': {
                'contrast': self.difference.contrast_to_background if self.difference else None,
                'marked': self.difference.marked if self.difference else None
            } if self.difference else None,
            'position_data': {
                'coordinates': self.first_position.coordinates if self.first_position else None,
                'description': self.first_position.description if self.first_position else None
            } if self.first_position else None,
            'self_data': {
                'awareness_level': self.self_entity.awareness_level if self.self_entity else None,
                'memory_count': len(self.self_entity.memories) if self.self_entity else None
            } if self.self_entity else None,
            'philosophical_insights': [
                "存在从差异中涌现",
                "定位创造存在感",
                "自我意识需要自指循环",
                "永恒的不存在是对称的，存在是打破对称",
                "第一次定位是认知宇宙的创世事件"
            ],
            'conclusion': """
                本实验模拟了第一次定位如何从'永恒不存在'中产生。
                关键发现：
                1. 差异是存在的先决条件
                2. 定位是存在感的基础
                3. 自我意识需要自指能力
                4. 存在不是默认状态，而是通过特定过程涌现的
            """
        }
        
        return report
    
    def visualize_experiment(self):
        """可视化实验结果"""
        
        try:
            # 创建图形
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            fig.suptitle('第一次定位实验 - 结果可视化', fontsize=16, fontweight='bold')
            
            # 1. 状态演化图
            ax1 = axes[0, 0]
            if self.state_history:
                states = [s.value for s in self.state_history]
                state_indices = list(range(len(states)))
                
                # 为每个状态分配颜色
                state_colors = {
                    '不存在': 'gray',
                    '涨落': 'blue',
                    '差异': 'orange',
                    '定位': 'green',
                    '存在': 'red',
                    '自我意识': 'purple'
                }
                
                colors = [state_colors.get(state, 'black') for state in states]
                
                ax1.bar(state_indices, [1] * len(states), color=colors)
                ax1.set_xlabel('阶段')
                ax1.set_ylabel('状态')
                ax1.set_title('状态演化过程')
                ax1.set_xticks(state_indices)
                ax1.set_xticklabels(states, rotation=45, ha='right')
            
            # 2. 事件时间线
            ax2 = axes[0, 1]
            if self.event_log:
                times = [event['time'] for event in self.event_log]
                events = [event['event'][:20] + '...' if len(event['event']) > 20 
                         else event['event'] for event in self.event_log]
                
                ax2.scatter(times, range(len(times)), alpha=0.6)
                ax2.set_xlabel('时间 (秒)')
                ax2.set_ylabel('事件序号')
                ax2.set_title('事件时间线')
                ax2.grid(True, alpha=0.3)
                
                # 添加事件标签
                for i, (t, e) in enumerate(zip(times, events)):
                    ax2.text(t, i, e, fontsize=8, alpha=0.7)
            
            # 3. 坐标空间可视化
            ax3 = axes[1, 0]
            if self.first_position and self.first_position.coordinates:
                coords = self.first_position.coordinates
                
                # 简单的2D可视化
                if len(coords) >= 2:
                    ax3.scatter(coords[0], coords[1], s=200, c='red', alpha=0.7, 
                               label='第一位置')
                    ax3.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
                    ax3.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
                    
                    # 标记原点
                    ax3.scatter(0, 0, s=100, c='blue', alpha=0.5, label='原点')
                    
                    ax3.set_xlabel(self.coordinate_system.dimensions[0]['name'] 
                                  if self.coordinate_system else '维度1')
                    ax3.set_ylabel(self.coordinate_system.dimensions[1]['name'] 
                                  if self.coordinate_system and len(self.coordinate_system.dimensions) > 1 
                                  else '维度2')
                    ax3.set_title('第一次定位的坐标空间')
                    ax3.legend()
                    ax3.grid(True, alpha=0.3)
                else:
                    ax3.text(0.5, 0.5, '坐标维度不足\n无法可视化', 
                            ha='center', va='center', transform=ax3.transAxes)
                    ax3.set_title('坐标空间可视化')
            
            # 4. 意识水平发展
            ax4 = axes[1, 1]
            if self.self_entity:
                # 模拟意识发展过程
                stages = ['差异', '定位', '存在', '自我意识']
                awareness_levels = [
                    0.3,  # 差异阶段
                    0.6,  # 定位阶段
                    self.self_entity.awareness_level * 0.9,  # 存在阶段
                    self.self_entity.awareness_level  # 自我意识阶段
                ]
                
                ax4.plot(stages, awareness_levels, marker='o', linewidth=2)
                ax4.fill_between(stages, awareness_levels, alpha=0.2)
                ax4.set_xlabel('认知阶段')
                ax4.set_ylabel('意识水平')
                ax4.set_title('意识发展过程')
                ax4.grid(True, alpha=0.3)
                ax4.set_ylim([0, 1.1])
            else:
                ax4.text(0.5, 0.5, '自我实体未形成\n无意识数据', 
                        ha='center', va='center', transform=ax4.transAxes)
                ax4.set_title('意识发展过程')
            
            plt.tight_layout()
            
            # 保存图像
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"first_position_experiment_{timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"\n可视化结果已保存为: {filename}")
            
            plt.show()
            
        except Exception as e:
            print(f"可视化过程中出现错误: {e}")
            print("跳过可视化步骤")

# ==================== 3. 辅助函数 ====================

def run_interactive_experiment():
    """交互式运行实验"""
    
    print("欢迎使用第一次定位实验系统!")
    print("\n配置实验参数:")
    
    try:
        # 获取用户输入
        fluctuation_threshold = float(input("输入涨落阈值 (默认 0.001): ") or "0.001")
        significance_threshold = float(input("输入重要性阈值 (默认 0.8): ") or "0.8")
        simulation_speed = float(input("输入模拟速度 (1.0=实时, 2.0=2倍速): ") or "1.0")
        debug_mode = input("启用调试模式? (y/n, 默认 y): ").lower() != 'n'
        
        # 创建并运行实验
        experiment = FirstPositionExperiment(
            fluctuation_threshold=fluctuation_threshold,
            significance_threshold=significance_threshold,
            debug_mode=debug_mode
        )
        
        report = experiment.run(simulation_speed=simulation_speed)
        
        # 显示报告摘要
        print("\n" + "=" * 70)
        print("实验报告摘要")
        print("=" * 70)
        
        for key, value in report.items():
            if key not in ['philosophical_insights', 'conclusion']:
                if isinstance(value, float):
                    print(f"{key}: {value:.4f}")
                else:
                    print(f"{key}: {value}")
        
        print("\n哲学洞见:")
        for insight in report['philosophical_insights']:
            print(f"  - {insight}")
        
        print(f"\n结论: {report['conclusion'][:200]}...")
        
        # 询问是否保存详细报告
        save_report = input("\n是否保存详细实验报告? (y/n): ").lower() == 'y'
        if save_report:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"experiment_report_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("第一次定位实验 - 详细报告\n")
                f.write("=" * 70 + "\n\n")
                
                for key, value in report.items():
                    f.write(f"{key}:\n")
                    if isinstance(value, list):
                        for item in value:
                            f.write(f"  - {item}\n")
                    elif isinstance(value, dict):
                        for subkey, subvalue in value.items():
                            f.write(f"  {subkey}: {subvalue}\n")
                    else:
                        f.write(f"  {value}\n")
                    f.write("\n")
                
                # 添加事件日志
                f.write("\n事件日志:\n")
                f.write("-" * 50 + "\n")
                for event in experiment.event_log:
                    f.write(f"[t={event['time']:.4f}s] {event['event']}\n")
            
            print(f"详细报告已保存为: {filename}")
        
    except ValueError:
        print("错误: 请输入有效的数值参数")
    except KeyboardInterrupt:
        print("\n实验被用户中断")
    except Exception as e:
        print(f"运行实验时出现错误: {e}")

def run_batch_experiments(num_experiments: int = 10):
    """运行批量实验，统计成功率"""
    
    print(f"运行 {num_experiments} 次批量实验...")
    
    results = []
    successful_consciousness = 0
    
    for i in range(num_experiments):
        print(f"\n实验 #{i+1}/{num_experiments}")
        print("-" * 30)
        
        experiment = FirstPositionExperiment(debug_mode=False)
        report = experiment.run(simulation_speed=2.0)
        
        # 检查是否成功形成自我意识
        success = report['final_state'] == '自我意识'
        if success:
            successful_consciousness += 1
        
        results.append({
            'experiment_id': i+1,
            'final_state': report['final_state'],
            'success': success,
            'awareness_level': report['self_data']['awareness_level'] if report['self_data'] else 0.0
        })
    
    # 统计结果
    print("\n" + "=" * 70)
    print("批量实验结果统计")
    print("=" * 70)
    
    print(f"总实验次数: {num_experiments}")
    print(f"成功形成自我意识: {successful_consciousness} ({successful_consciousness/num_experiments*100:.1f}%)")
    
    # 统计最终状态分布
    state_counts = {}
    for result in results:
        state = result['final_state']
        state_counts[state] = state_counts.get(state, 0) + 1
    
    print("\n最终状态分布:")
    for state, count in state_counts.items():
        print(f"  {state}: {count}次 ({count/num_experiments*100:.1f}%)")
    
    # 计算平均意识水平
    awareness_levels = [r['awareness_level'] for r in results if r['awareness_level'] > 0]
    if awareness_levels:
        avg_awareness = sum(awareness_levels) / len(awareness_levels)
        print(f"\n平均意识水平 (成功案例): {avg_awareness:.3f}")
    
    return results

# ==================== 4. 主程序入口 ====================

if __name__ == "__main__":
    
    print("第一次定位实验系统")
    print("版本: 1.0")
    print("基于: 认知起源实验室 - '永恒不存在'理论")
    print()
    
    while True:
        print("\n选择操作:")
        print("1. 运行交互式实验")
        print("2. 运行批量实验 (统计模式)")
        print("3. 退出")
        
        choice = input("请输入选择 (1-3): ").strip()
        
        if choice == '1':
            run_interactive_experiment()
        elif choice == '2':
            try:
                num = int(input("输入实验次数 (默认 10): ") or "10")
                run_batch_experiments(num)
            except ValueError:
                print("错误: 请输入有效的数字")
        elif choice == '3':
            print("感谢使用第一次定位实验系统!")
            break
        else:
            print("无效选择，请重新输入")
