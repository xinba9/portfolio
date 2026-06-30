# Hermes + 英伟达API 使用指南

## ✅ 配置完成

Hermes Agent 已成功安装并配置英伟达API！

---

## 📋 配置信息

| 项目 | 值 |
|------|-----|
| **Hermes版本** | v0.16.0 |
| **API提供商** | 英伟达 NVIDIA NIM |
| **当前模型** | z-ai/glm-5.1 |
| **API端点** | https://integrate.api.nvidia.com/v1 |
| **配置文件** | `~/.hermes/config.yaml` |
| **环境变量** | `~/.hermes/.env` |

---

## 🚀 快速开始

### 方法1：直接启动（推荐）

```bash
# 1. 添加Hermes到PATH（每次新开终端都需要）
export PATH="/c/Users/EDY/.workbuddy/binaries/python/versions/3.13.12/Scripts:$PATH"

# 2. 启动Hermes聊天
hermes chat
```

### 方法2：使用启动脚本

```bash
# 运行启动脚本
bash start_hermes.sh
```

---

## 🔧 常用命令

### 查看配置
```bash
hermes config
```

### 交互式配置模型
```bash
hermes model
```

### 编辑配置文件
```bash
hermes config edit
```

### 检查配置状态
```bash
hermes config check
```

### 查看版本
```bash
hermes --version
```

---

## 🎯 可用模型列表

英伟达NIM平台当前支持的**热门免费模型**：

| 模型名称 | 模型ID | 特点 | 推荐场景 |
|---------|--------|------|---------|
| **GLM 5.1** | `z-ai/glm-5.1` | **当前使用**，中文优秀 | 通用对话、中文任务 |
| MiniMax M3 | `minimaxai/minimax-m3` | 最新多模态 | 图片理解、多模态任务 |
| MiniMax M2.7 | `minimaxai/minimax-m2.7` | 230B参数 | 代码生成、复杂推理 |
| DeepSeek V4 | `deepseek-ai/deepseek-v4-flash` | 快速推理 | 代码任务、快速响应 |
| Kimi K2.6 | `moonshotai/kimi-k2.6` | 1T参数 | 长文本理解、智能体 |
| Qwen 3.5 | `qwen/qwen3.5` | 阿里通义 | 中文任务、代码 |

### 切换模型方法

编辑 `~/.hermes/config.yaml`，修改：
```yaml
model:
  default: "minimaxai/minimax-m3"  # 改成你想用的模型ID
```

然后重启Hermes即可。

---

## 💡 使用技巧

### 1. 永久添加到PATH（推荐）

避免每次都输入完整PATH，可以将以下内容添加到 `~/.bashrc`：

```bash
# Hermes Agent
export PATH="/c/Users/EDY/.workbuddy/binaries/python/versions/3.13.12/Scripts:$PATH"
```

然后运行：
```bash
source ~/.bashrc
```

之后就可以直接使用 `hermes chat` 了！

### 2. Hermes聊天命令

在Hermes聊天中，可以使用以下命令：
- `/exit` - 退出聊天
- `/model` - 切换模型
- `/clear` - 清空对话历史
- `/help` - 显示帮助

### 3. 配置文件说明

**config.yaml** - 主配置文件（非敏感信息）
- 模型选择
- 终端后端
- 显示设置
- 工具开关

**.env** - 环境变量（敏感信息）
- API Keys
- 密码
- Token

---

## 🔍 测试API连接

如果你想测试API是否正常工作，运行：

```bash
cd /c/Users/EDY/WorkBuddy/2026-06-15-16-18-44
C:/Users/EDY/.workbuddy/binaries/python/versions/3.13.12/python.exe simple_test.py
```

---

## ⚠️ 注意事项

1. **API额度**：英伟达提供免费额度，但有使用限制
2. **网络访问**：需要确保能访问 `integrate.api.nvidia.com`
3. **模型生命周期**：某些模型会过期（如glm-4.7已停用），请及时更新配置
4. **API Key安全**：不要分享你的API Key（nvapi-...）

---

## 📚 更多资源

- [Hermes官方文档](https://hermes-agent.nousresearch.com/)
- [英伟达NIM平台](https://build.nvidia.com/models)
- [Hermes GitHub](https://github.com/NousResearch/hermes-agent)

---

## ✅ 测试记录

- [x] Hermes安装成功
- [x] 英伟达API Key配置完成
- [x] API连接测试通过
- [x] GLM-5.1模型测试成功
- [x] 配置文件创建完成

**测试时间**：2026-06-15
**测试结果**：✅ 所有测试通过
