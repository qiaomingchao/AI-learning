# MarsCode

<div align="center">
    <img src="icon.png" alt="MarsCode Logo" width="120" height="120"/>
    <h3>Your AI Coding Assistant</h3>
</div>

## 简介

MarsCode 是一个基于 Streamlit 开发的智能编程助手应用，它提供了直观的界面和强大的 AI 对话能力，帮助开发者更高效地解决编程问题。

## 特性

- 🚀 实时 AI 对话：快速响应您的编程问题
- 💻 代码支持：提供代码补全、解释和优化建议
- 🎨 现代化界面：简洁优雅的用户界面设计
- 🔐 安全配置：支持环境变量和界面配置 API 密钥
- 📝 系统提示词：可自定义的系统提示词
- 💾 会话管理：支持对话历史记录和清除
- 🌐 跨平台支持：可在任何支持 Python 的平台上运行

## 快速开始

### 环境要求

- Python 3.8 或更高版本
- pip 包管理器

### 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/marscode.git
cd marscode
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
创建 `.env` 文件并添加以下配置：
```env
MARSCODE_API_KEY=your-api-key
MARSCODE_MODEL_EP=your-model-endpoint
MARSCODE_ICON_PATH=path/to/your/icon.png  # 可选
```

4. 运行应用：
```bash
streamlit run app.py
```

## 配置说明

### API 配置

支持两种配置方式：
1. 环境变量配置（推荐）：
   - 在 `.env` 文件中设置
   - 作为默认配置和回退选项
   
2. 界面配置：
   - 在应用侧边栏的 API 设置中配置
   - 可随时修改和验证
   - 支持重置为环境变量值

### 系统提示词

可以通过以下方式自定义系统提示词：
1. 在 `prompts.txt` 文件中直接编辑
2. 通过应用界面在系统设置中修改

## 项目结构

```
marscode/
├── app.py              # 主应用文件
├── icon.png           # 应用图标
├── prompts.txt        # 系统提示词配置
├── .env              # 环境变量配置
├── requirements.txt   # 项目依赖
└── README.md         # 项目文档
```

## 依赖列表

```text
streamlit~=1.28.0
python-dotenv~=1.0.0
Pillow~=10.0.0
volcenginesdkarkruntime
```

## 功能说明

### 聊天功能
- 实时对话：支持与 AI 助手进行实时对话
- 代码高亮：自动识别和高亮显示代码块
- 历史记录：保存对话历史，方便回顾

### 系统设置
- API 配置管理：支持 API 密钥和模型端点配置
- 系统提示词：可自定义对话的系统提示词
- 界面主题：提供现代化的界面主题

### 工具栏功能
- 清除对话：一键清除当前会话历史
- 复制内容：快速复制对话内容
- 导出功能：支持导出对话记录
- 设置选项：快速访问系统设置

## 常见问题

1. API 配置无法验证？
   - 检查 API 密钥是否正确
   - 确认网络连接正常
   - 查看控制台错误信息

2. 图标无法显示？
   - 确认 icon.png 文件存在
   - 检查文件权限
   - 可以通过环境变量指定图标路径

3. 如何重置所有设置？
   - 删除 .env 文件并重新配置
   - 删除 prompts.txt 文件将重置系统提示词
   - 使用界面中的重置按钮


## 许可证

本项目基于 MIT 许可证开源 - 查看 [LICENSE](LICENSE) 文件了解更多详情。



## 致谢

- Streamlit 团队提供的出色框架
- 所有项目贡献者
- 使用本项目的开发者们