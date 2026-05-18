#!/usr/bin/env python3
"""
数学计算大师 v1.0
=================
功能：科学计算、统计分析、方程求解、图形绘制
售价：$13.99
"""

import os
import sys
import math
import json
from datetime import datetime

try:
    import numpy as np
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'numpy'])
    import numpy as np

try:
    import matplotlib.pyplot as plt
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'matplotlib'])
    import matplotlib.pyplot as plt


class MathMaster:
    """数学计算大师"""
    
    def __init__(self):
        self.results = []
    
    def basic_calculate(self, expression: str) -> float:
        """基础计算"""
        try:
            result = eval(expression)
            self.results.append({'expression': expression, 'result': result})
            return result
        except Exception as e:
            return {'error': str(e)}
    
    def factorial(self, n: int) -> int:
        """阶乘"""
        return math.factorial(n)
    
    def fibonacci(self, n: int) -> list:
        """斐波那契数列"""
        fib = [0, 1]
        for i in range(2, n):
            fib.append(fib[i-1] + fib[i-2])
        return fib[:n]
    
    def is_prime(self, n: int) -> bool:
        """判断素数"""
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def primes_up_to(self, n: int) -> list:
        """获取 n 以内的所有素数"""
        return [i for i in range(2, n+1) if self.is_prime(i)]
    
    def gcd(self, a: int, b: int) -> int:
        """最大公约数"""
        return math.gcd(a, b)
    
    def lcm(self, a: int, b: int) -> int:
        """最小公倍数"""
        return abs(a * b) // math.gcd(a, b)
    
    def statistics(self, data: list) -> dict:
        """统计分析"""
        arr = np.array(data)
        return {
            'count': len(data),
            'sum': float(np.sum(arr)),
            'mean': float(np.mean(arr)),
            'median': float(np.median(arr)),
            'std': float(np.std(arr)),
            'var': float(np.var(arr)),
            'min': float(np.min(arr)),
            'max': float(np.max(arr)),
            'range': float(np.ptp(arr)),
        }
    
    def solve_quadratic(self, a: float, b: float, c: float) -> dict:
        """求解一元二次方程 ax² + bx + c = 0"""
        discriminant = b**2 - 4*a*c
        
        if discriminant > 0:
            x1 = (-b + math.sqrt(discriminant)) / (2*a)
            x2 = (-b - math.sqrt(discriminant)) / (2*a)
            return {'x1': x1, 'x2': x2, 'type': 'real_roots'}
        elif discriminant == 0:
            x = -b / (2*a)
            return {'x': x, 'type': 'double_root'}
        else:
            real = -b / (2*a)
            imag = math.sqrt(abs(discriminant)) / (2*a)
            return {'x1': complex(real, imag), 'x2': complex(real, -imag), 'type': 'complex_roots'}
    
    def plot_function(self, func, x_range: tuple = (-10, 10), 
                     title: str = '函数图像', output_file: str = 'function_plot.png') -> str:
        """绘制函数图像"""
        x = np.linspace(x_range[0], x_range[1], 100)
        y = [func(xi) for xi in x]
        
        plt.figure(figsize=(10, 6))
        plt.plot(x, y, 'b-', linewidth=2)
        plt.title(title)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid(True)
        plt.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        plt.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
        plt.savefig(output_file, dpi=150)
        plt.close()
        
        print(f"✅ 函数图像已生成: {output_file}")
        return output_file
    
    def matrix_operations(self, matrix1: list, matrix2: list, operation: str = 'add') -> list:
        """矩阵运算"""
        a = np.array(matrix1)
        b = np.array(matrix2)
        
        if operation == 'add':
            return (a + b).tolist()
        elif operation == 'subtract':
            return (a - b).tolist()
        elif operation == 'multiply':
            return np.dot(a, b).tolist()
        elif operation == 'transpose':
            return a.T.tolist()
        elif operation == 'inverse':
            return np.linalg.inv(a).tolist()
        elif operation == 'determinant':
            return float(np.linalg.det(a))
        else:
            return {'error': f'不支持的运算: {operation}'}
    
    def convert_base(self, number: int, from_base: int = 10, to_base: int = 2) -> str:
        """进制转换"""
        if from_base == 10:
            if to_base == 2:
                return bin(number)[2:]
            elif to_base == 8:
                return oct(number)[2:]
            elif to_base == 16:
                return hex(number)[2:].upper()
        else:
            # 先转为10进制
            decimal = int(str(number), from_base)
            return self.convert_base(decimal, 10, to_base)
    
    def unit_converter(self, value: float, from_unit: str, to_unit: str) -> float:
        """单位转换"""
        conversions = {
            'km_to_miles': 0.621371,
            'miles_to_km': 1.60934,
            'kg_to_lbs': 2.20462,
            'lbs_to_kg': 0.453592,
            'celsius_to_fahrenheit': lambda x: x * 9/5 + 32,
            'fahrenheit_to_celsius': lambda x: (x - 32) * 5/9,
        }
        
        key = f"{from_unit}_to_{to_unit}"
        if key in conversions:
            conv = conversions[key]
            if callable(conv):
                return conv(value)
            return value * conv
        else:
            return {'error': f'不支持的转换: {from_unit} -> {to_unit}'}


def main():
    """主函数"""
    print("=" * 50)
    print("数学计算大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. 基础计算")
    print("  2. 数论函数")
    print("  3. 统计分析")
    print("  4. 方程求解")
    print("  5. 函数绘图")
    print("  6. 矩阵运算")
    print()
    print("使用方法:")
    print("  from math_master import MathMaster")
    print("  master = MathMaster()")
    print("  result = master.basic_calculate('2 + 3 * 4')")
    print("  stats = master.statistics([1, 2, 3, 4, 5])")
    print()
    print("价格: $13.99")


if __name__ == "__main__":
    main()
