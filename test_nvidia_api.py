#!/usr/bin/env python3
"""
测试英伟达NVIDIA NIM API连接
"""
import os
import sys

# 设置控制台输出编码为UTF-8（Windows兼容）
sys.stdout.reconfigure(encoding='utf-8')

from openai import OpenAI

# 从环境变量读取API Key
api_key = "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"

# 创建OpenAI客户端（使用英伟达API端点）
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)

print("正在测试英伟达API连接...")
print(f"API端点: https://integrate.api.nvidia.com/v1")
print(f"模型: z-ai/glm-5.1")
print("-" * 50)

try:
    # 发送测试请求
    response = client.chat.completions.create(
        model="z-ai/glm-5.1",
        messages=[
            {"role": "user", "content": "你好，请用一句话介绍你自己"}
        ],
        max_tokens=100,
        temperature=0.7
    )
    
    print("✅ API连接成功！")
    print("-" * 50)
    print("模型回复：")
    print(response.choices[0].message.content)
    print("-" * 50)
    print(f"使用的tokens: {response.usage.total_tokens}")
    
except Exception as e:
    print("❌ API连接失败！")
    print(f"错误信息: {str(e)}")
    print("\n可能的原因：")
    print("1. API Key不正确或已过期")
    print("2. 网络无法访问英伟达API（可能需要代理）")
    print("3. 模型名称不正确")
    print("4. API额度已用完")
