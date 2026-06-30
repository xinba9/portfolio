#!/usr/bin/env python3
"""
使用Hermes配置测试英伟达API（非交互式测试）
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from openai import OpenAI
import os

# 读取API Key
api_key = "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"

# 测试多个模型
models_to_test = [
    "z-ai/glm-5.1",
    "minimaxai/minimax-m3",
    "minimaxai/minimax-m2.7",
    "deepseek-ai/deepseek-v4-flash",
]

print("=" * 60)
print("Hermes + 英伟达API 配置测试")
print("=" * 60)

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)

for model in models_to_test:
    print(f"\n📝 测试模型: {model}")
    print("-" * 60)
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "用一句话介绍你自己，包括你的名称和特点"}
            ],
            max_tokens=150,
            temperature=0.7,
            timeout=30  # 添加超时设置
        )
        
        print(f"✅ 成功！")
        print(f"回复: {response.choices[0].message.content}")
        print(f"Tokens使用: {response.usage.total_tokens}")
        
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg or "not found" in error_msg.lower():
            print(f"❌ 模型不存在或不可用")
        elif "401" in error_msg or "unauthorized" in error_msg.lower():
            print(f"❌ API Key认证失败")
        elif "429" in error_msg or "rate" in error_msg.lower():
            print(f"⚠️ 速率限制，请稍后再试")
        else:
            print(f"❌ 错误: {error_msg[:200]}")

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)
print("\n💡 使用建议：")
print("1. GLM-5.1: 中文表现优秀，推荐使用")
print("2. MiniMax M3: 最新多模态模型，支持图片理解")
print("3. MiniMax M2.7: 代码生成能力强")
print("\n📝 启动Hermes聊天：")
print("   export PATH='/c/Users/EDY/.workbuddy/binaries/python/versions/3.13.12/Scripts:$PATH'")
print("   hermes chat")

