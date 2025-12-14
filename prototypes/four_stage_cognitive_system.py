import numpy as np
import random
from enum import Enum
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt
from dataclasses import dataclass

# ========== 1. 定义核心枚举和数据结构 ==========

class CognitiveStage(Enum):
    """四阶段认知状态"""
    UNKNOWN = "不明"      # 无法理解
    CHAOS = "混乱"        # 多重可能性
    INVERTED = "颠倒"     # 可能错误的理解
    UNIFIED = "合一"      # 正确统一的理解

class ModuleType(Enum):
    """模组类型"""
    PERCEPTION = "感知"    # 基础感知模组
    ACTION = "动作"        # 动作执行模组
    UNDERSTANDING = "理解" # 理解模组
    METACOGNITIVE = "元认知" # 元认知模组

@dataclass
class Module:
    """模组基类"""
    id: int
    name: str
    m_type: ModuleType
    activation_threshold: float = 0.5
    activation_level: float = 0.0
    connections: Dict[int, float] = None  # 连接到的模组ID及其权重
    internal_state: Dict = None
    
    def __post_init__(self):
        if self.connections is None:
            self.connections = {}
        if self.internal_state is None:
            self.internal_state = {}
    
    def activate(self, input_strength: float) -> float:
        """激活模组，返回输出强度"""
        self.activation_level = min(1.0, input_strength)
        return self.activation_level if self.activation_level >= self.activation_threshold else 0.0
    
    def add_connection(self, target_id: int, weight: float = 0.5):
        """添加连接到其他模组"""
        self.connections[target_id] = weight
    
    def update_connection(self, target_id: int, delta: float):
        """更新连接权重"""
        if target_id in self.connections:
            self.connections[target_id] = max(0.0, min(1.0, self.connections[target_id] + delta))

@dataclass 
class UnderstandingModule(Module):
    """理解模组 - 特殊化的模组"""
    understanding_strength: float = 0.0  # 理解强度
    coherence_score: float = 0.0         # 内部一致性分数
    prediction_accuracy: float = 0.0     # 预测准确率
    age: int = 0                         # 模组年龄
    
    def update_understanding(self, success: bool):
        """更新理解状态"""
        self.age += 1
        if success:
            self.understanding_strength = min(1.0, self.understanding_strength + 0.1)
            self.prediction_accuracy = (self.prediction_accuracy * (self.age-1) + 1) / self.age
        else:
            self.understanding_strength = max(0.0, self.understanding_strength - 0.2)
            self.prediction_accuracy = (self.prediction_accuracy * (self.age-1)) / self.age

# ========== 2. 创建四阶段调控器 ==========

class FourStageRegulator:
    """四阶段认知调控器"""
    
    def __init__(self):
        self.current_stage = CognitiveStage.UNKNOWN
        self.stage_duration = 0
        self.confusion_level = 0.0  # 混乱程度 0-1
        self.coherence_threshold = 0.7  # 进入"合一"所需的一致性阈值
        self.failure_tolerance = 3  # 容忍连续失败次数
        
        # 各阶段的参数设置
        self.stage_parameters = {
            CognitiveStage.UNKNOWN: {
                "activation_threshold": 0.8,  # 高阈值，不易激活
                "random_exploration": 0.9,    # 高随机探索
                "energy_cost": 0.3,
            },
            CognitiveStage.CHAOS: {
                "activation_threshold": 0.3,  # 低阈值，易激活
                "random_exploration": 0.95,   # 极高随机性
                "energy_cost": 0.8,
            },
            CognitiveStage.INVERTED: {
                "activation_threshold": 0.6,
                "random_exploration": 0.2,    # 低随机性
                "energy_cost": 0.5,
            },
            CognitiveStage.UNIFIED: {
                "activation_threshold": 0.7,
                "random_exploration": 0.1,    # 低随机性
                "energy_cost": 0.2,           # 高效能
            }
        }
        
    def diagnose_stage(self, modules: List[Module], recent_successes: int, recent_failures: int) -> CognitiveStage:
        """诊断当前认知阶段"""
        
        active_modules = [m for m in modules if m.activation_level > 0.1]
        
        # 如果没有活跃模组 -> 不明
        if len(active_modules) == 0:
            return CognitiveStage.UNKNOWN
        
        # 计算模组间的一致性
        coherence = self._calculate_coherence(active_modules)
        
        # 计算激活模式的稳定性
        stability = self._calculate_stability(modules)
        
        # 基于一致性和失败率判断阶段
        if coherence > self.coherence_threshold and recent_failures == 0:
            return CognitiveStage.UNIFIED
        elif coherence > 0.5 and stability > 0.6:
            return CognitiveStage.INVERTED
        elif len(active_modules) > 5 and coherence < 0.3:  # 多个模组活跃但不一致
            return CognitiveStage.CHAOS
        else:
            return CognitiveStage.UNKNOWN
    
    def _calculate_coherence(self, modules: List[Module]) -> float:
        """计算模组间的一致性"""
        if len(modules) < 2:
            return 1.0
        
        # 简化的计算：检查模组激活水平的相关性
        activations = [m.activation_level for m in modules]
        mean_activation = np.mean(activations)
        deviations = [abs(a - mean_activation) for a in activations]
        
        # 平均偏差越小，一致性越高
        avg_deviation = np.mean(deviations)
        coherence = max(0.0, 1.0 - avg_deviation)
        return coherence
    
    def _calculate_stability(self, modules: List[Module]) -> float:
        """计算激活模式的稳定性"""
        # 简化的稳定性计算：检查理解模组的预测准确率
        understanding_modules = [m for m in modules if isinstance(m, UnderstandingModule)]
        if not understanding_modules:
            return 0.0
        
        avg_accuracy = np.mean([m.prediction_accuracy for m in understanding_modules])
        return avg_accuracy
    
    def transition_rules(self, current_stage: CognitiveStage, 
                         failures: int, 
                         coherence: float) -> CognitiveStage:
        """执行阶段转换规则"""
        
        if current_stage == CognitiveStage.UNKNOWN:
            # 不明 -> 混乱：当系统开始探索时
            if failures > 0:  # 遭遇失败，开始探索
                return CognitiveStage.CHAOS
                
        elif current_stage == CognitiveStage.CHAOS:
            # 混乱 -> 颠倒：当出现一个主导理解时
            if coherence > 0.5:  # 开始形成一致理解
                return CognitiveStage.INVERTED
                
        elif current_stage == CognitiveStage.INVERTED:
            # 颠倒 -> 合一：理解经受住检验
            if coherence > self.coherence_threshold and failures == 0:
                return CognitiveStage.UNIFIED
            # 颠倒 -> 混乱：理解失败，需要重新探索
            elif failures >= self.failure_tolerance:
                return CognitiveStage.CHAOS
                
        elif current_stage == CognitiveStage.UNIFIED:
            # 合一 -> 不明：系统寻求新的挑战
            if failures > 2:  # 连续失败，出现新问题
                return CognitiveStage.UNKNOWN
        
        return current_stage  # 保持当前阶段
    
    def get_stage_parameters(self, stage: CognitiveStage) -> Dict:
        """获取当前阶段的参数"""
        return self.stage_parameters.get(stage, self.stage_parameters[CognitiveStage.UNKNOWN])

# ========== 3. 创建认知系统 ==========

class CognitiveSystem:
    """认知系统 - 模拟理解模组的生成和演化"""
    
    def __init__(self):
        self.modules = {}
        self.next_module_id = 0
        self.regulator = FourStageRegulator()
        self.stage_history = []
        self.learning_history = []
        
        # 初始化基础模组
        self._initialize_basic_modules()
        
        # 性能跟踪
        self.recent_successes = 0
        self.recent_failures = 0
        self.total_energy = 100.0
        self.energy_history = []
        
    def _initialize_basic_modules(self):
        """初始化基础感知和动作模组"""
        
        # 基础感知模组
        perceptions = ["vision_red", "vision_blue", "vision_green", 
                      "sound_high", "sound_low", "touch_pressure"]
        
        for p in perceptions:
            module = Module(
                id=self.next_module_id,
                name=f"perception_{p}",
                m_type=ModuleType.PERCEPTION,
                activation_threshold=0.4
            )
            self.modules[self.next_module_id] = module
            self.next_module_id += 1
        
        # 基础动作模组
        actions = ["move_forward", "move_back", "turn_left", "turn_right", "grab", "release"]
        
        for a in actions:
            module = Module(
                id=self.next_module_id,
                name=f"action_{a}",
                m_type=ModuleType.ACTION,
                activation_threshold=0.6
            )
            self.modules[self.next_module_id] = module
            self.next_module_id += 1
        
        # 初始理解模组（非常基础）
        initial_understanding = UnderstandingModule(
            id=self.next_module_id,
            name="basic_reflex",
            m_type=ModuleType.UNDERSTANDING,
            activation_threshold=0.7,
            understanding_strength=0.3
        )
        self.modules[self.next_module_id] = initial_understanding
        self.next_module_id += 1
        
        # 元认知模组
        metacog = Module(
            id=self.next_module_id,
            name="metacognitive_monitor",
            m_type=ModuleType.METACOGNITIVE,
            activation_threshold=0.5
        )
        self.modules[self.next_module_id] = metacog
        self.next_module_id += 1
        
        # 建立一些初始连接
        self._create_initial_connections()
    
    def _create_initial_connections(self):
        """创建初始的连接"""
        # 简化的连接：感知模组连接到理解模组
        perception_ids = [id for id, m in self.modules.items() 
                         if m.m_type == ModuleType.PERCEPTION]
        understanding_ids = [id for id, m in self.modules.items() 
                            if m.m_type == ModuleType.UNDERSTANDING]
        
        if perception_ids and understanding_ids:
            for p_id in perception_ids:
                for u_id in understanding_ids:
                    self.modules[p_id].add_connection(u_id, weight=0.3)
    
    def process_input(self, sensory_input: Dict[str, float]) -> Dict[str, float]:
        """处理输入，返回动作决策"""
        
        # 重置所有模组的激活水平
        for module in self.modules.values():
            module.activation_level = 0.0
        
        # 激活感知模组
        activated_perceptions = []
        for module in self.modules.values():
            if module.m_type == ModuleType.PERCEPTION:
                # 简化的感知匹配：检查输入是否匹配模组名称
                for key, value in sensory_input.items():
                    if key in module.name and value > 0:
                        activation = module.activate(value)
                        if activation > 0:
                            activated_perceptions.append(module.id)
        
        # 传播激活
        self._propagate_activation(activated_perceptions)
        
        # 诊断当前认知阶段
        stage = self.regulator.diagnose_stage(
            list(self.modules.values()), 
            self.recent_successes, 
            self.recent_failures
        )
        
        # 记录阶段历史
        if not self.stage_history or self.stage_history[-1] != stage:
            self.stage_history.append(stage)
        
        # 获取当前阶段参数
        stage_params = self.regulator.get_stage_parameters(stage)
        
        # 基于阶段参数调整系统行为
        actions = self._generate_actions(stage_params)
        
        # 消耗能量
        energy_cost = stage_params["energy_cost"]
        self.total_energy -= energy_cost
        self.energy_history.append(self.total_energy)
        
        return {
            "actions": actions,
            "stage": stage,
            "active_modules": len([m for m in self.modules.values() if m.activation_level > 0.1]),
            "energy_remaining": self.total_energy
        }
    
    def _propagate_activation(self, source_ids: List[int], depth: int = 0, max_depth: int = 3):
        """传播激活到连接的模组"""
        if depth >= max_depth or not source_ids:
            return
        
        new_activations = []
        for source_id in source_ids:
            source_module = self.modules[source_id]
            
            # 传播到所有连接的模组
            for target_id, weight in source_module.connections.items():
                if target_id in self.modules:
                    target_module = self.modules[target_id]
                    
                    # 计算传播的激活强度
                    propagated_strength = source_module.activation_level * weight
                    
                    # 激活目标模组
                    output = target_module.activate(propagated_strength)
                    
                    if output > 0:
                        new_activations.append(target_id)
        
        # 递归传播
        if new_activations:
            self._propagate_activation(new_activations, depth + 1, max_depth)
    
    def _generate_actions(self, stage_params: Dict) -> Dict[str, float]:
        """生成动作决策"""
        
        # 收集活跃的动作模组
        action_modules = [m for m in self.modules.values() 
                         if m.m_type == ModuleType.ACTION and m.activation_level > 0]
        
        actions = {}
        
        if action_modules:
            # 选择激活最强的动作
            strongest = max(action_modules, key=lambda m: m.activation_level)
            actions[strongest.name] = strongest.activation_level
        else:
            # 没有活跃动作模组，基于阶段参数随机探索
            if random.random() < stage_params["random_exploration"]:
                # 随机选择一个动作
                all_actions = [m for m in self.modules.values() 
                              if m.m_type == ModuleType.ACTION]
                if all_actions:
                    chosen = random.choice(all_actions)
                    actions[chosen.name] = 0.5  # 中等置信度
        
        return actions
    
    def learn_from_feedback(self, success: bool, context: Dict = None):
        """从反馈中学习"""
        
        if success:
            self.recent_successes += 1
            self.recent_failures = max(0, self.recent_failures - 1)
            
            # 奖励活跃的理解模组
            for module in self.modules.values():
                if isinstance(module, UnderstandingModule) and module.activation_level > 0:
                    module.update_understanding(True)
                    
                    # 加强成功的连接
                    for conn_id in module.connections:
                        if conn_id in self.modules:
                            self.modules[conn_id].update_connection(module.id, 0.1)
        else:
            self.recent_failures += 1
            self.recent_successes = max(0, self.recent_successes - 1)
            
            # 惩罚活跃的理解模组
            for module in self.modules.values():
                if isinstance(module, UnderstandingModule) and module.activation_level > 0:
                    module.update_understanding(False)
                    
                    # 削弱失败的连接
                    for conn_id in module.connections:
                        if conn_id in self.modules:
                            self.modules[conn_id].update_connection(module.id, -0.2)
            
            # 检查是否需要创建新理解模组
            if self.recent_failures >= 3:
                self._create_new_understanding_module(context)
    
    def _create_new_understanding_module(self, context: Dict = None):
        """创建新的理解模组"""
        
        # 收集当前活跃的感知模组
        active_perceptions = [m for m in self.modules.values() 
                             if m.m_type == ModuleType.PERCEPTION and m.activation_level > 0.3]
        
        if len(active_perceptions) >= 2:
            # 创建一个新的理解模组
            new_module = UnderstandingModule(
                id=self.next_module_id,
                name=f"understanding_{len([m for m in self.modules.values() if isinstance(m, UnderstandingModule)])}",
                m_type=ModuleType.UNDERSTANDING,
                activation_threshold=0.5,
                understanding_strength=0.1
            )
            
            # 连接到活跃的感知模组
            for perception in active_perceptions:
                new_module.add_connection(perception.id, weight=0.4)
                # 同时让感知模组连接到新理解模组
                perception.add_connection(new_module.id, weight=0.3)
            
            self.modules[self.next_module_id] = new_module
            self.next_module_id += 1
            
            print(f"创建了新理解模组: {new_module.name}")
    
    def update_cognitive_stage(self):
        """更新认知阶段"""
        current_stage = self.regulator.diagnose_stage(
            list(self.modules.values()), 
            self.recent_successes, 
            self.recent_failures
        )
        
        # 计算一致性
        active_modules = [m for m in self.modules.values() if m.activation_level > 0.1]
        coherence = self.regulator._calculate_coherence(active_modules)
        
        # 应用转换规则
        new_stage = self.regulator.transition_rules(
            current_stage, 
            self.recent_failures, 
            coherence
        )
        
        self.regulator.current_stage = new_stage
        
        # 记录学习历史
        self.learning_history.append({
            "stage": new_stage,
            "modules": len(self.modules),
            "understanding_modules": len([m for m in self.modules.values() 
                                         if isinstance(m, UnderstandingModule)]),
            "successes": self.recent_successes,
            "failures": self.recent_failures,
            "coherence": coherence
        })
        
        return new_stage
    
    def visualize_cognitive_journey(self):
        """可视化认知旅程"""
        
        if not self.stage_history:
            print("没有足够的历史数据")
            return
        
        # 创建图形
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # 1. 认知阶段演变
        ax1 = axes[0, 0]
        stage_values = [s.value for s in self.stage_history]
        stage_names = [s.name for s in self.stage_history]
        
        # 为每个阶段分配颜色
        stage_colors = {
            CognitiveStage.UNKNOWN: 'gray',
            CognitiveStage.CHAOS: 'red',
            CognitiveStage.INVERTED: 'orange',
            CognitiveStage.UNIFIED: 'green'
        }
        
        colors = [stage_colors[stage] for stage in self.stage_history]
        
        ax1.bar(range(len(stage_values)), [1] * len(stage_values), color=colors)
        ax1.set_xlabel("时间步")
        ax1.set_ylabel("认知阶段")
        ax1.set_title("认知阶段演变")
        
        # 创建自定义图例
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=color, label=stage.value) 
                          for stage, color in stage_colors.items()]
        ax1.legend(handles=legend_elements, loc='upper right')
        
        # 2. 模组数量增长
        ax2 = axes[0, 1]
        if self.learning_history:
            steps = range(len(self.learning_history))
            total_modules = [h["modules"] for h in self.learning_history]
            understanding_modules = [h["understanding_modules"] for h in self.learning_history]
            
            ax2.plot(steps, total_modules, label="总模组数", marker='o')
            ax2.plot(steps, understanding_modules, label="理解模组数", marker='s')
            ax2.set_xlabel("学习周期")
            ax2.set_ylabel("模组数量")
            ax2.set_title("模组增长")
            ax2.legend()
            ax2.grid(True, alpha=0.3)
        
        # 3. 成功/失败记录
        ax3 = axes[1, 0]
        if self.learning_history:
            steps = range(len(self.learning_history))
            successes = [h["successes"] for h in self.learning_history]
            failures = [h["failures"] for h in self.learning_history]
            
            ax3.plot(steps, successes, label="连续成功", color='green')
            ax3.plot(steps, failures, label="连续失败", color='red')
            ax3.set_xlabel("学习周期")
            ax3.set_ylabel("次数")
            ax3.set_title("学习表现")
            ax3.legend()
            ax3.grid(True, alpha=0.3)
        
        # 4. 一致性分数
        ax4 = axes[1, 1]
        if self.learning_history:
            steps = range(len(self.learning_history))
            coherence = [h["coherence"] for h in self.learning_history]
            
            ax4.plot(steps, coherence, label="一致性", color='blue', marker='o')
            ax4.axhline(y=0.7, color='r', linestyle='--', label="合一阈值")
            ax4.set_xlabel("学习周期")
            ax4.set_ylabel("一致性分数")
            ax4.set_title("系统一致性")
            ax4.legend()
            ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        # 打印系统状态摘要
        print("\n" + "="*50)
        print("系统状态摘要")
        print("="*50)
        print(f"当前认知阶段: {self.regulator.current_stage.value}")
        print(f"总模组数: {len(self.modules)}")
        print(f"理解模组数: {len([m for m in self.modules.values() if isinstance(m, UnderstandingModule)])}")
        print(f"最近成功: {self.recent_successes}, 最近失败: {self.recent_failures}")
        print(f"剩余能量: {self.total_energy:.1f}")
        
        # 显示活跃的理解模组
        active_understanding = [m for m in self.modules.values() 
                              if isinstance(m, UnderstandingModule) and m.activation_level > 0]
        if active_understanding:
            print("\n活跃的理解模组:")
            for module in active_understanding:
                print(f"  - {module.name}: 强度={module.understanding_strength:.2f}, "
                      f"准确率={module.prediction_accuracy:.2f}")

# ========== 4. 创建测试环境 ==========

class TestEnvironment:
    """测试环境 - 模拟迷宫和规则变化"""
    
    def __init__(self, rule_sets: List[Dict] = None):
        if rule_sets is None:
            # 默认规则集：红光规则 -> 蓝光规则 -> 混合规则
            self.rule_sets = [
                {"rule": "red_light", "description": "跟随红光", "steps": 20},
                {"rule": "blue_light", "description": "跟随蓝光", "steps": 20},
                {"rule": "alternating", "description": "红蓝交替", "steps": 30},
                {"rule": "random", "description": "随机目标", "steps": 15},
            ]
        else:
            self.rule_sets = rule_sets
        
        self.current_rule_index = 0
        self.steps_in_current_rule = 0
        self.current_rule = self.rule_sets[0]
        
    def get_sensory_input(self) -> Dict[str, float]:
        """生成感官输入"""
        
        rule = self.current_rule["rule"]
        sensory_input = {
            "vision_red": 0.0,
            "vision_blue": 0.0,
            "vision_green": 0.0,
            "sound_high": 0.0,
            "sound_low": 0.0,
            "touch_pressure": random.random() * 0.5,  # 随机触觉输入
        }
        
        # 基于当前规则生成输入
        if rule == "red_light":
            sensory_input["vision_red"] = 0.8 + random.random() * 0.2
            sensory_input["vision_blue"] = random.random() * 0.3
        elif rule == "blue_light":
            sensory_input["vision_blue"] = 0.8 + random.random() * 0.2
            sensory_input["vision_red"] = random.random() * 0.3
        elif rule == "alternating":
            # 红蓝交替
            if (self.steps_in_current_rule // 5) % 2 == 0:
                sensory_input["vision_red"] = 0.9
            else:
                sensory_input["vision_blue"] = 0.9
        elif rule == "random":
            # 随机强调某个感官
            if random.random() > 0.5:
                sensory_input["vision_red"] = 0.7
            else:
                sensory_input["vision_blue"] = 0.7
                
            if random.random() > 0.7:
                sensory_input["sound_high"] = 0.5
        
        return sensory_input
    
    def evaluate_action(self, actions: Dict[str, float], sensory_input: Dict[str, float]) -> bool:
        """评估动作是否正确"""
        
        rule = self.current_rule["rule"]
        
        if not actions:
            return False  # 没有动作是失败
        
        # 获取主要动作
        primary_action = max(actions.items(), key=lambda x: x[1])[0] if actions else None
        
        # 简化的评估逻辑
        if rule == "red_light":
            # 当红光强时，正确的动作是向前移动
            if sensory_input["vision_red"] > 0.7:
                return "move_forward" in primary_action
            else:
                return random.random() > 0.3  # 随机成功概率
        
        elif rule == "blue_light":
            # 当蓝光强时，正确的动作是向右转
            if sensory_input["vision_blue"] > 0.7:
                return "turn_right" in primary_action
            else:
                return random.random() > 0.3
        
        elif rule == "alternating":
            # 交替规则：红光时向前，蓝光时向右
            if sensory_input["vision_red"] > 0.7:
                return "move_forward" in primary_action
            elif sensory_input["vision_blue"] > 0.7:
                return "turn_right" in primary_action
            else:
                return random.random() > 0.4
        
        elif rule == "random":
            # 随机规则：有时需要多个动作组合
            return random.random() > 0.5  # 50%成功率
        
        return False  # 默认失败
    
    def update_rule(self):
        """更新当前规则"""
        self.steps_in_current_rule += 1
        
        current_rule_info = self.rule_sets[self.current_rule_index]
        if self.steps_in_current_rule >= current_rule_info["steps"]:
            # 切换到下一个规则
            self.current_rule_index = (self.current_rule_index + 1) % len(self.rule_sets)
            self.current_rule = self.rule_sets[self.current_rule_index]
            self.steps_in_current_rule = 0
            
            print(f"\n规则已切换: {current_rule_info['description']} -> {self.current_rule['description']}")
            return True
        
        return False

# ========== 5. 主运行循环 ==========

def run_cognitive_simulation(total_steps: int = 100):
    """运行认知模拟"""
    
    print("="*60)
    print("开始认知系统模拟")
    print("四阶段: 不明 → 混乱 → 颠倒 → 合一")
    print("="*60)
    
    # 初始化系统和环境
    cognitive_system = CognitiveSystem()
    environment = TestEnvironment()
    
    # 运行模拟
    for step in range(total_steps):
        print(f"\n--- 步骤 {step+1}/{total_steps} ---")
        
        # 检查规则是否需要更新
        rule_changed = environment.update_rule()
        if rule_changed:
            # 规则变化，增加失败计数以促进学习
            cognitive_system.recent_failures += 2
        
        # 获取感官输入
        sensory_input = environment.get_sensory_input()
        print(f"感官输入: { {k: round(v, 2) for k, v in sensory_input.items() if v > 0.1} }")
        
        # 认知系统处理输入
        result = cognitive_system.process_input(sensory_input)
        print(f"认知阶段: {result['stage'].value}")
        print(f"生成动作: {result['actions']}")
        
        # 环境评估动作
        success = environment.evaluate_action(result['actions'], sensory_input)
        print(f"动作结果: {'成功' if success else '失败'}")
        
        # 认知系统从反馈中学习
        cognitive_system.learn_from_feedback(success, sensory_input)
        
        # 更新认知阶段
        new_stage = cognitive_system.update_cognitive_stage()
        print(f"更新后阶段: {new_stage.value}")
        
        # 检查能量耗尽
        if cognitive_system.total_energy <= 0:
            print("\n⚠️  系统能量耗尽!")
            break
    
    # 模拟结束，可视化结果
    print("\n" + "="*60)
    print("模拟结束")
    print("="*60)
    
    cognitive_system.visualize_cognitive_journey()
    
    return cognitive_system

# ========== 6. 运行模拟 ==========

if __name__ == "__main__":
    # 运行模拟
    cognitive_system = run_cognitive_simulation(total_steps=80)
    
    # 额外分析：检查系统是否避免"自洽的疯狂"
    print("\n" + "="*60)
    print("检查'自洽的疯狂'避免机制")
    print("="*60)
    
    # 检查系统是否能在规则变化后适应
    inverted_stages = [h for h in cognitive_system.learning_history 
                      if h["stage"] == CognitiveStage.INVERTED]
    unified_stages = [h for h in cognitive_system.learning_history 
                     if h["stage"] == CognitiveStage.UNIFIED]
    
    print(f"总学习周期: {len(cognitive_system.learning_history)}")
    print(f"颠倒阶段次数: {len(inverted_stages)}")
    print(f"合一阶段次数: {len(unified_stages)}")
    
    # 检查是否陷入长期颠倒（可能暗示自洽疯狂）
    if inverted_stages:
        avg_inverted_duration = len(cognitive_system.learning_history) / len(inverted_stages)
        if avg_inverted_duration > 10:
            print("⚠️  警告：系统可能陷入长期'颠倒'，有自洽疯狂风险")
        else:
            print("✓ 系统能及时从颠倒阶段转换，避免自洽疯狂")
    
    # 检查理解模组的多样性
    understanding_modules = [m for m in cognitive_system.modules.values() 
                            if isinstance(m, UnderstandingModule)]
    print(f"\n理解模组总数: {len(understanding_modules)}")
    
    if len(understanding_modules) > 1:
        # 检查理解模组的强度分布
        strengths = [m.understanding_strength for m in understanding_modules]
        print(f"理解模组平均强度: {np.mean(strengths):.2f}")
        print(f"理解模组强度标准差: {np.std(strengths):.2f}")
        
        if np.std(strengths) < 0.2:
            print("⚠️  理解模组强度过于均匀，可能缺乏 specialization")
        else:
            print("✓ 理解模组有良好的 specialization")
