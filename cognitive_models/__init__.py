# cognitive_models/__init__.py
"""
认知起源实验室 - 核心计算模型包。

此包包含用于模拟认知、意识和函数衍化等核心概念的模型。
"""

# 从子模块中导入核心类/函数，使其在包级别可直接访问
from .function_evolution import ConsciousFunctionEvolver
from .visualization import visualize_evolution

# 定义当用户使用 `from cognitive_models import *` 时会导入的内容
__all__ = [
    'ConsciousFunctionEvolver',
    'visualize_evolution',
]
