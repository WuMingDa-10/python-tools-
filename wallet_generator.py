#!/usr/bin/env python3
"""
加密货币钱包生成器
==================
不需要任何账号注册，直接生成钱包
"""

import secrets
import hashlib
import json
from datetime import datetime

def generate_ethereum_wallet():
    """生成以太坊钱包"""
    # 生成私钥
    private_key = secrets.token_hex(32)
    
    # 生成地址（简化版，实际需要用椭圆曲线算法）
    address = '0x' + hashlib.sha256(private_key.encode()).hexdigest()[:40]
    
    return {
        'private_key': private_key,
        'address': address,
        'created': datetime.now().isoformat()
    }

def generate_bitcoin_wallet():
    """生成比特币钱包"""
    # 生成私钥
    private_key = secrets.token_hex(32)
    
    # 生成地址（简化版）
    address = '1' + hashlib.sha256(private_key.encode()).hexdigest()[:33]
    
    return {
        'private_key': private_key,
        'address': address,
        'created': datetime.now().isoformat()
    }

def main():
    print("=" * 50)
    print("加密货币钱包生成器")
    print("=" * 50)
    
    # 生成以太坊钱包
    eth_wallet = generate_ethereum_wallet()
    print(f"\n以太坊钱包:")
    print(f"  地址: {eth_wallet['address']}")
    print(f"  私钥: {eth_wallet['private_key'][:16]}...")
    
    # 生成比特币钱包
    btc_wallet = generate_bitcoin_wallet()
    print(f"\n比特币钱包:")
    print(f"  地址: {btc_wallet['address']}")
    print(f"  私钥: {btc_wallet['private_key'][:16]}...")
    
    # 保存钱包信息
    wallets = {
        'ethereum': eth_wallet,
        'bitcoin': btc_wallet,
        'created': datetime.now().isoformat()
    }
    
    with open('wallets.json', 'w') as f:
        json.dump(wallets, f, indent=2)
    
    print("\n钱包已保存到 wallets.json")
    print("\n" + "=" * 50)
    print("下一步:")
    print("1. 访问 https://faucet.ethereum.org 获取测试币")
    print("2. 访问 https://coinfaucet.io 获取免费币")
    print("3. 参加空投活动获取免费代币")
    print("=" * 50)

if __name__ == "__main__":
    main()
