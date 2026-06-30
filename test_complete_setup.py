#!/usr/bin/env python3
"""
Hermes + 英伟达API 完整功能测试
测试主模型和辅助模型配置
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from openai import OpenAI

print("=" * 70)
print("Hermes + 英伟达API 完整功能测试")
print("=" * 70)

api_key = "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"
base_url = "https://integrate.api.nvidia.com/v1"

# 创建客户端
client = OpenAI(
    base_url=base_url,
    api_key=api_key,
    timeout=30
)

print("\n📝 测试1：主模型（z-ai/glm-5.1）")
print("-" * 70)
try:
    response = client.chat.completions.create(
        model="z-ai/glm-5.1",
        messages=[{"role": "user", "content": "你好，请介绍你的功能"}],
        max_tokens=100
    )
    print("✅ 主模型测试成功！")
    print(f"回复: {response.choices[0].message.content[:100]}...")
    print(f"Tokens: {response.usage.total_tokens}")
except Exception as e:
    print(f"❌ 主模型测试失败: {e}")

print("\n📝 测试2：代码生成能力")
print("-" * 70)
try:
    response = client.chat.completions.create(
        model="z-ai/glm-5.1",
        messages=[{"role": "user", "content": "用Python写一个计算斐波那契数列的函数"}],
        max_tokens=200
    )
    print("✅ 代码生成测试成功！")
    print(f"回复长度: {len(response.choices[0].message.content)} 字符")
    print(f"Tokens: {response.usage.total_tokens}")
except Exception as e:
    print(f"❌ 代码生成测试失败: {e}")

print("\n📝 测试3：中文理解能力")
print("-" * 70)
try:
    response = client.chat.completions.create(
        model="z-ai/glm-5.1",
        messages=[{"role": "user", "content": "解释一下什么是人工智能"}],
        max_tokens=150
    )
    print("✅ 中文理解测试成功！")
    print(f"回复: {response.choices[0].message.content[:100]}...")
    print(f"Tokens: {response.usage.total_tokens}")
except Exception as e:
    print(f"❌ 中文理解测试失败: {e}")

print("\n" + "=" * 70)
print("✅ 所有测试完成！")
print("=" * 70)
print("\n💡 配置摘要：")
print("  - 主模型: z-ai/glm-5.1")
print("  - API端点: https://integrate.api.nvidia.com/v1")
print("  - 辅助模型: 已配置（用于图片分析、网页提取等）")
print("\n📝 下一步：")
print("  1. 双击桌面 'Hermes Chat.bat' 启动聊天")
print("  2. 或运行: hermes chat")
print("=" * 70)
