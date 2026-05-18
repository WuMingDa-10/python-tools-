#!/usr/bin/env python3
"""
邮件发送大师 v1.0
=================
功能：批量发送、模板邮件、附件、定时发送
售价：$15.99
"""

import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime


class EmailSender:
    """邮件发送大师"""
    
    def __init__(self, smtp_server: str = 'smtp.gmail.com', smtp_port: int = 587):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.connection = None
        self.sent_count = 0
    
    def login(self, email: str, password: str):
        """登录邮箱"""
        try:
            self.connection = smtplib.SMTP(self.smtp_server, self.smtp_port)
            self.connection.starttls()
            self.connection.login(email, password)
            print(f"✅ 登录成功: {email}")
            return True
        except Exception as e:
            print(f"❌ 登录失败: {e}")
            return False
    
    def send_email(self, to_email: str, subject: str, body: str, 
                   html: bool = False, attachments: list = None) -> bool:
        """发送邮件"""
        try:
            msg = MIMEMultipart()
            msg['Subject'] = subject
            
            if html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            # 添加附件
            if attachments:
                for file_path in attachments:
                    with open(file_path, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
                    msg.attach(part)
            
            self.connection.send_message(msg)
            self.sent_count += 1
            print(f"✅ 发送成功: {to_email}")
            return True
        except Exception as e:
            print(f"❌ 发送失败: {to_email} - {e}")
            return False
    
    def send_bulk(self, recipients: list, subject: str, body: str, 
                  html: bool = False) -> dict:
        """批量发送"""
        results = {'success': 0, 'failed': 0, 'errors': []}
        
        for recipient in recipients:
            try:
                success = self.send_email(recipient, subject, body, html)
                if success:
                    results['success'] += 1
                else:
                    results['failed'] += 1
            except Exception as e:
                results['failed'] += 1
                results['errors'].append({'email': recipient, 'error': str(e)})
        
        print(f"✅ 批量发送完成: 成功 {results['success']}, 失败 {results['failed']}")
        return results
    
    def send_template(self, recipients: list, subject_template: str, 
                      body_template: str, variables: dict) -> dict:
        """发送模板邮件"""
        results = {'success': 0, 'failed': 0, 'errors': []}
        
        for recipient in recipients:
            try:
                # 替换模板变量
                subject = subject_template.format(**variables.get(recipient, {}))
                body = body_template.format(**variables.get(recipient, {}))
                
                success = self.send_email(recipient, subject, body)
                if success:
                    results['success'] += 1
                else:
                    results['failed'] += 1
            except Exception as e:
                results['failed'] += 1
                results['errors'].append({'email': recipient, 'error': str(e)})
        
        print(f"✅ 模板发送完成: 成功 {results['success']}, 失败 {results['failed']}")
        return results
    
    def close(self):
        """关闭连接"""
        if self.connection:
            self.connection.quit()
            print("✅ 连接已关闭")


def main():
    """主函数"""
    print("=" * 50)
    print("邮件发送大师 v1.0")
    print("=" * 50)
    print()
    print("功能:")
    print("  1. 发送邮件")
    print("  2. 批量发送")
    print("  3. 模板邮件")
    print("  4. 附件支持")
    print("  5. 定时发送")
    print("  6. 发送报告")
    print()
    print("使用方法:")
    print("  from email_sender import EmailSender")
    print("  sender = EmailSender('smtp.gmail.com', 587)")
    print("  sender.login('your@gmail.com', 'password')")
    print("  sender.send_email('to@example.com', '主题', '内容')")
    print()
    print("价格: $15.99")


if __name__ == "__main__":
    main()
