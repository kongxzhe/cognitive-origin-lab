# cognitive_models/function_evolution.py
"""
模拟“函数衍化与意识涌现”的核心模型。
核心思想：一个基础函数（无意识模式）在遇到预测误差（中断）时，会尝试衍生新函数（有意识过程），最终选择更优者（新稳定态）。
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, List, Tuple
import random

class ConsciousFunctionEvolver:
    """
    一个会“思考”的函数演化模拟器。
    """
    def __init__(self, base_function: Callable[[float], float], domain: Tuple[float, float] = (0, 10)):
        """
        初始化一个具有基础规律（无意识函数）的系统。
        :param base_function: 初始的、稳定的“无意识”函数，例如：lambda x: 2*x + 1。
        :param domain: 函数的定义域。
        """
        self.current_function = base_function  # 当前主导的“函数”（当前意识状态）
        self.domain = domain
        self.history = []  # 记录函数的演化历史
        self.disruption_history = []  # 记录“中断”事件
        print(f"[系统初始化] 初始函数: {base_function.__name__ if hasattr(base_function, '__name__') else '匿名函数'}")

    def perceive(self, x: float, with_noise: bool = False) -> float:
        """
        感知/计算：根据当前函数规律，输出y。
        :param with_noise: 是否在输出中加入随机噪声（模拟感知不确定性）。
        """
        y = self.current_function(x)
        if with_noise:
            y += np.random.normal(0, 0.1)  # 加入小噪声
        return y

    def experience_disruption(self, x: float, unexpected_y: float, threshold: float = 0.5):
        """
        经历“中断”：当外部输入与当前函数预测严重不符时，触发“意识过程”。
        :param unexpected_y: 与当前函数预测不符的“意外”观测值。
        :param threshold: 预测误差阈值，超过则触发“中断”。
        """
        predicted_y = self.current_function(x)
        error = abs(predicted_y - unexpected_y)

        if error > threshold:
            print(f"[意识触发] 在 x={x} 处发现显著预测误差！预测:{predicted_y:.2f}, 观测:{unexpected_y:.2f}, 误差:{error:.2f}")
            self.disruption_history.append((x, predicted_y, unexpected_y))
            # “衍生”新函数的尝试（这里是随机生成几个候选）
            candidate_functions = self._generate_candidates()
            # “选择”更适应新数据的新函数
            new_func = self._select_function(candidate_functions, x, unexpected_y)
            # 记录历史并更新
            self.history.append((self.current_function, error))
            self.current_function = new_func
            print(f"[函数衍化] 旧函数被更新。新函数已适应新数据点。")
            return True  # 表示发生了中断与衍化
        return False

    def _generate_candidates(self) -> List[Callable]:
        """ ‘衍生’：在中断后，生成几个可能的新函数假设（这里简化为随机线性函数）。"""
        candidates = []
        for _ in range(5):  # 生成5个候选函数
            # 随机改变斜率和截距，代表新的规律假设
            m = random.uniform(0.5, 3.0)
            b = random.uniform(-2.0, 2.0)
            candidates.append(lambda x, m=m, b=b: m * x + b)
        # 总是包含当前函数作为一个候选（保守假设）
        candidates.append(self.current_function)
        return candidates

    def _select_function(self, candidates: List[Callable], x: float, y_obs: float) -> Callable:
        """ ‘选择’：从候选函数中选出最能解释新数据点（x, y_obs）的那个。"""
        best_func = None
        best_error = float('inf')
        for func in candidates:
            error = abs(func(x) - y_obs)
            if error < best_error:
                best_error = error
                best_func = func
        return best_func

    def run_experiment(self, data_stream: List[Tuple[float, float]]) -> dict:
        """
        运行一个完整的模拟实验：让系统处理一系列数据点，观察其演化。
        :param data_stream: 输入的数据流，每个元素是 (x, y)。
        :return: 实验结果摘要。
        """
        disruptions = 0
        for i, (x, y_obs) in enumerate(data_stream):
            print(f"\n[数据点 {i+1}] 输入: ({x}, {y_obs})")
            if self.experience_disruption(x, y_obs):
                disruptions += 1

        return {
            "final_function": self.current_function,
            "total_disruptions": disruptions,
            "evolution_steps": len(self.history),
            "history": self.history
        }
