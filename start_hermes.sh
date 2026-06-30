#!/bin/bash
# Hermes 快速启动脚本
# 使用方法：./start_hermes.sh

echo "=================================="
echo "Hermes Agent 启动器"
echo "=================================="
echo ""

# 添加Hermes到PATH
export PATH="/c/Users/EDY/.workbuddy/binaries/python/versions/3.13.12/Scripts:$PATH"

# 显示当前配置
echo "📋 当前配置："
echo "  模型: z-ai/glm-5.1"
echo "  API: 英伟达 NVIDIA NIM"
echo "  配置文件: ~/.hermes/config.yaml"
echo ""

# 启动Hermes聊天
echo "🚀 正在启动Hermes..."
echo "提示：输入 /exit 或按 Ctrl+C 退出"
echo "=================================="
echo ""

hermes chat
