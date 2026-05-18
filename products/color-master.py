#!/usr/bin/env python3
"""
颜色处理大师 v1.0
=================
功能：颜色转换、调色板生成、颜色分析、渐变生成
售价：$9.99
"""

import os
import sys
import json
import random
from datetime import datetime


class ColorMaster:
    """颜色处理大师"""
    
    def __init__(self):
        self.colors = []
    
    def hex_to_rgb(self, hex_color: str) -> tuple:
        """十六进制转 RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hex(self, r: int, g: int, b: int) -> str:
        """RGB 转十六进制"""
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def rgb_to_hsl(self, r: int, g: int, b: int) -> tuple:
        """RGB 转 HSL"""
        r, g, b = r / 255, g / 255, b / 255
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        l = (max_val + min_val) / 2
        
        if max_val == min_val:
            h = s = 0
        else:
            d = max_val - min_val
            s = d / (2 - max_val - min_val) if l > 0.5 else d / (max_val + min_val)
            
            if max_val == r:
                h = (g - b) / d + (6 if g < b else 0)
            elif max_val == g:
                h = (b - r) / d + 2
            else:
                h = (r - g) / d + 4
            
            h /= 6
        
        return (round(h * 360), round(s * 100), round(l * 100))
    
    def hsl_to_rgb(self, h: int, s: int, l: int) -> tuple:
        """HSL 转 RGB"""
        h, s, l = h / 360, s / 100, l / 100
        
        if s == 0:
            r = g = b = l
        else:
            def hue2rgb(p, q, t):
                if t < 0:
                    t += 1
                if t > 1:
                    t -= 1
                if t < 1/6:
                    return p + (q - p) * 6 * t
                if t < 1/2:
                    return q
                if t < 2/3:
                    return p + (q - p) * (2/3 - t) * 6
                return p
            
            q = l * (1 + s) if l < 0.5 else l + s - l * s
            p = 2 * l - q
            r = hue2rgb(p, q, h + 1/3)
            g = hue2rgb(p, q, h)
            b = hue2rgb(p, q, h - 1/3)
        
        return (round(r * 255), round(g * 255), round(b * 255))
    
    def generate_palette(self, base_color: str, count: int = 5, 
                        scheme: str = 'complementary') -> list:
        """生成调色板"""
        r, g, b = self.hex_to_rgb(base_color)
        h, s, l = self.rgb_to_hsl(r, g, b)
        
        colors = []
        
        if scheme == 'complementary':
            # 互补色
            colors.append(base_color)
            colors.append(self.rgb_to_hex(*self.hsl_to_rgb((h + 180) % 360, s, l)))
        elif scheme == 'analogous':
            # 类似色
            for i in range(count):
                new_h = (h + i * 30) % 360
                colors.append(self.rgb_to_hex(*self.hsl_to_rgb(new_h, s, l)))
        elif scheme == 'triadic':
            # 三色组
            for i in range(3):
                new_h = (h + i * 120) % 360
                colors.append(self.rgb_to_hex(*self.hsl_to_rgb(new_h, s, l)))
        elif scheme == 'random':
            # 随机
            for _ in range(count):
                new_h = random.randint(0, 360)
                colors.append(self.rgb_to_hex(*self.hsl_to_rgb(new_h, s, l)))
        
        return colors
    
    def generate_gradient(self, color1: str, color2: str, steps: int = 10) -> list:
        """生成渐变"""
        r1, g1, b1 = self.hex_to_rgb(color1)
        r2, g2, b2 = self.hex_to_rgb(color2)
        
        gradient = []
        for i in range(steps):
            r = int(r1 + (r2 - r1) * i / (steps - 1))
            g = int(g1 + (g2 - g1) * i / (steps - 1))
            b = int(b1 + (b2 - b1) * i / (steps - 1))
            gradient.append(self.rgb_to_hex(r, g, b))
        
        return gradient
    
    def get_color_info(self, color: str) -> dict:
        """获取颜色信息"""
        r, g, b = self.hex_to_rgb(color)
        h, s, l = self.rgb_to_hsl(r, g, b)
        
        return {
            'hex': color,
            'rgb': (r, g, b),
            'hsl': (h, s, l),
            'luminance': 0.299 * r + 0.587 * g + 0.114 * b,
            'is_dark': (0.299 * r + 0.587 * g + 0.114 * b) < 128,
        }
    
    def random_color(self) -> str:
        """生成随机颜色"""
        return f'#{random.randint(0, 0xFFFFFF):06x}'
    
    def generate_palette_image(self, colors: list, output_file: str = 'palette.png') -> str:
        """生成调色板图片"""
        try:
            from PIL import Image, ImageDraw
            
            width = 100 * len(colors)
            height = 100
            img = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(img)
            
            for i, color in enumerate(colors):
                r, g, b = self.hex_to_rgb(color)
                draw.rectangle([i * 100, 0, (i + 1) * 100, height], fill=(r, g, b))
            
            img.save(output_file)
            print(f"✅ 调色板已生成: {output_file}")
            return output_file
        except ImportError:
            print("需要安装 Pillow: pip install Pillow")
            return None
    
    def export_palette(self, colors: list, output_file: str = 'palette.json') -> str:
        """导出调色板"""
        palette = {
            'timestamp': datetime.now().isoformat(),
            'colors': [],
        }
        
        for color in colors:
            info = self.get_color_info(color)
            palette['colors'].append(info)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(palette, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 调色板已导出: {output_file}")
        return output_file


def main():
    """主函数"""
    print("=" * 50)
    print("颜色处理大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. 颜色转换")
    print("  2. 调色板生成")
    print("  3. 渐变生成")
    print("  4. 颜色分析")
    print("  5. 随机颜色")
    print("  6. 导出调色板")
    print()
    print("使用方法:")
    print("  from color_master import ColorMaster")
    print("  master = ColorMaster()")
    print("  rgb = master.hex_to_rgb('#ff0000')")
    print("  palette = master.generate_palette('#3498db', 5, 'complementary')")
    print()
    print("价格: $9.99")


if __name__ == "__main__":
    main()
