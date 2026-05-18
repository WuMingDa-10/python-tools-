#!/usr/bin/env python3
"""
二维码生成大师 v1.0
===================
功能：二维码生成、解码、批量生成、美化
售价：$10.99
"""

import os
import sys
import json
from datetime import datetime

try:
    import qrcode
    from PIL import Image
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'qrcode[pil]'])
    import qrcode
    from PIL import Image


class QRCodeMaster:
    """二维码生成大师"""
    
    def __init__(self):
        self.generated = 0
    
    def generate_qr(self, data: str, output_file: str = 'qrcode.png',
                    size: int = 10, border: int = 4) -> str:
        """生成二维码"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(output_file)
        
        self.generated += 1
        print(f"✅ 二维码已生成: {output_file}")
        return output_file
    
    def generate_qr_with_logo(self, data: str, logo_file: str, 
                              output_file: str = 'qrcode_with_logo.png') -> str:
        """生成带 Logo 的二维码"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        
        # 打开 Logo
        logo = Image.open(logo_file)
        
        # 调整 Logo 大小
        qr_width, qr_height = qr_img.size
        logo_size = int(qr_width * 0.25)
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        
        # 计算 Logo 位置
        logo_pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
        
        # 粘贴 Logo
        qr_img.paste(logo, logo_pos)
        qr_img.save(output_file)
        
        self.generated += 1
        print(f"✅ 带 Logo 的二维码已生成: {output_file}")
        return output_file
    
    def generate_wifi_qr(self, ssid: str, password: str, 
                         security: str = 'WPA', output_file: str = 'wifi_qr.png') -> str:
        """生成 WiFi 二维码"""
        wifi_data = f'WIFI:T:{security};S:{ssid};P:{password};;'
        return self.generate_qr(wifi_data, output_file)
    
    def generate_vcard_qr(self, name: str, phone: str, email: str,
                          output_file: str = 'vcard_qr.png') -> str:
        """生成名片二维码"""
        vcard = f'''BEGIN:VCARD
VERSION:3.0
FN:{name}
TEL:{phone}
EMAIL:{email}
END:VCARD'''
        return self.generate_qr(vcard, output_file)
    
    def generate_url_qr(self, url: str, output_file: str = 'url_qr.png') -> str:
        """生成 URL 二维码"""
        return self.generate_qr(url, output_file)
    
    def generate_text_qr(self, text: str, output_file: str = 'text_qr.png') -> str:
        """生成文本二维码"""
        return self.generate_qr(text, output_file)
    
    def generate_email_qr(self, email: str, subject: str = '', body: str = '',
                          output_file: str = 'email_qr.png') -> str:
        """生成邮件二维码"""
        email_data = f'MAILTO:{email}'
        if subject:
            email_data += f'?SUBJECT={subject}'
        if body:
            email_data += f'&BODY={body}'
        return self.generate_qr(email_data, output_file)
    
    def generate_phone_qr(self, phone: str, output_file: str = 'phone_qr.png') -> str:
        """生成电话二维码"""
        return self.generate_qr(f'TEL:{phone}', output_file)
    
    def generate_sms_qr(self, phone: str, message: str = '',
                        output_file: str = 'sms_qr.png') -> str:
        """生成短信二维码"""
        sms_data = f'SMSTO:{phone}'
        if message:
            sms_data += f':{message}'
        return self.generate_qr(sms_data, output_file)
    
    def batch_generate(self, data_list: list, output_dir: str = 'qrcodes') -> list:
        """批量生成二维码"""
        os.makedirs(output_dir, exist_ok=True)
        output_files = []
        
        for i, data in enumerate(data_list):
            output_file = os.path.join(output_dir, f'qrcode_{i+1}.png')
            self.generate_qr(data, output_file)
            output_files.append(output_file)
        
        print(f"✅ 批量生成完成: {len(output_files)} 个二维码")
        return output_files
    
    def decode_qr(self, image_file: str) -> str:
        """解码二维码"""
        try:
            from pyzbar.pyzbar import decode
            
            img = Image.open(image_file)
            decoded = decode(img)
            
            if decoded:
                return decoded[0].data.decode('utf-8')
            else:
                return {'error': '未检测到二维码'}
        except ImportError:
            print("需要安装 pyzbar: pip install pyzbar")
            return None
    
    def generate_colored_qr(self, data: str, fill_color: str = 'black',
                            back_color: str = 'white', 
                            output_file: str = 'colored_qr.png') -> str:
        """生成彩色二维码"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        img.save(output_file)
        
        self.generated += 1
        print(f"✅ 彩色二维码已生成: {output_file}")
        return output_file


def main():
    """主函数"""
    print("=" * 50)
    print("二维码生成大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. 生成二维码")
    print("  2. 带 Logo 二维码")
    print("  3. WiFi 二维码")
    print("  4. 名片二维码")
    print("  5. 批量生成")
    print("  6. 解码二维码")
    print()
    print("使用方法:")
    print("  from qrcode_master import QRCodeMaster")
    print("  master = QRCodeMaster()")
    print("  master.generate_qr('https://example.com')")
    print("  master.generate_wifi_qr('MyWiFi', 'password123')")
    print()
    print("价格: $10.99")


if __name__ == "__main__":
    main()
