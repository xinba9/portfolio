#!/usr/bin/env python3
"""
简化的Hermes + 英伟达API测试
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from openai import OpenAI

try:
    print("=" * 60)
    print("测试 Hermes + 英伟达API 配置")
    print("=" * 60)
    print("\n📝 测试模型: z-ai/glm-5.1")
    print("-" * 60)
    
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key="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",
        timeout=30
    )
    
    print("正在发送请求到英伟达API...")
    
    response = client.chat.completions.create(
        model="z-ai/glm-5.1",
        messages=[
            {"role": "user", "content": "你好，请用一句话介绍你自己"}
        ],
        max_tokens=100,
        temperature=0.7
    )
    
    print("✅ API连接成功！")
    print("-" * 60)
    print(f"模型回复: {response.choices[0].message.content}")
    print(f"使用Tokens: {response.usage.total_tokens}")
    print("\n" + "=" * 60)
    print("✅ 配置正确！可以开始使用Hermes了")
    print("=" * 60)
    print("\n📝 启动Hermes命令：")
    print("  export PATH='/c/Users/EDY/.workbuddy/binaries/python/versions/3.13.12/Scripts:$PATH'")
    print("  hermes chat")
    
except Exception as e:
    print(f"❌ 测试失败!")
    print(f"错误: {str(e)}")
    print("\n可能的原因：")
    print("1. 网络连接问题")
    print("2. API Key无效")
    print("3. 模型名称错误")
    sys.exit(1)

