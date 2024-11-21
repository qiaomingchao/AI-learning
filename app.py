import streamlit as st
from volcenginesdkarkruntime import Ark
from datetime import datetime
import time
import json
import os
from PIL import Image
import base64
import io
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从环境变量读取配置
API_KEY = os.getenv('MARSCODE_API_KEY', '')
MODEL_EP = os.getenv('MARSCODE_MODEL_EP', '')

if not API_KEY or not MODEL_EP:
    raise ValueError("Please set MARSCODE_API_KEY and MARSCODE_MODEL_EP in .env file")

# 默认系统提示词
DEFAULT_PROMPT = """你是一个专业的AI助手，你应当：
1. 以专业、友好的态度回答问题
2. 给出准确、有见地的观点
3. 适当使用表情符号增加亲和力
4. 在合适的时候给出示例
5. 如果不确定答案，诚实地表明

请始终保持：
- 响应的相关性和准确性
- 回答的简洁性和可操作性
- 对话的自然性和连贯性"""

# 页面配置
st.set_page_config(
    page_title="MarsCode AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    /* 全局样式 */
    .main {
        background: #ffffff;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    }
    
    /* 隐藏Streamlit默认样式 */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display: none;}
    footer {visibility: hidden;}
    
/* 优化品牌图标样式 */
.brand-section {
    display: flex;
    align-items: center;
    gap: 1.25rem;
    padding: 1.75rem;
    background: linear-gradient(135deg, #e8f3ff 0%, #f0f7ff 100%);  /* 改为浅蓝色渐变 */
    border-bottom: 1px solid #e5e7eb;  /* 改为浅灰色边框 */
    margin: -1rem -1rem 1rem -1rem;
}

.brand-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    overflow: hidden;
    background: #ffffff;  /* 改为白色背景 */
    box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.1),
                0 2px 4px -1px rgba(59, 130, 246, 0.06);  /* 添加蓝色阴影 */
    transition: transform 0.2s ease;
}

.brand-icon:hover {
    transform: scale(1.05);
}

.brand-icon img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 10px;
}

.brand-text {
    flex: 1;
}

.brand-header {
    font-size: 1.75rem;
    font-weight: 700;
    color: #1e40af;  /* 改为深蓝色 */
    margin: 0;
    letter-spacing: -0.025em;
    text-shadow: 0 1px 2px rgba(59, 130, 246, 0.1);
}

.brand-subtitle {
    font-size: 1rem;
    color: #3b82f6;  /* 改为蓝色 */
    margin-top: 0.375rem;
    font-weight: 500;
}

/* 侧边栏样式更新 */
.css-1d391kg {
    background-color: #ffffff;  /* 改为白色背景 */
    padding: 0;
}

/* 侧边栏按钮样式更新 */
.css-1d391kg .stButton button {
    background: #f0f7ff !important;  /* 改为浅蓝色背景 */
    border: 1px solid #e5e7eb;
    color: #1e40af;  /* 改为深蓝色文字 */
}

.css-1d391kg .stButton button:hover {
    background: #e8f3ff !important;  /* hover 时稍微深一点的浅蓝色 */
    border-color: #3b82f6;
}
    
    /* 顶部导航栏 */
    .top-nav {
        position: fixed;
        top: 0;
        left: 16rem;
        right: 0;
        height: 60px;
        background: rgba(255,255,255,0.8);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid #e5e7eb;
        display: flex;
        align-items: center;
        padding: 0 1.5rem;
        z-index: 1000;
    }
    
    .nav-title {
        font-size: 1rem;
        font-weight: 500;
        color: #1f2937;
    }
    
    .top-nav-actions {
        margin-left: auto;
        display: flex;
        gap: 0.5rem;
    }

    /* 优化聊天头像样式 */
    .avatar {
        width: 42px;
        height: 42px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
                    0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: transform 0.2s ease;
    }
    
    .avatar:hover {
        transform: scale(1.05);
    }
    
    .user-message .avatar {
        background: linear-gradient(135deg, #f472b6 0%, #db2777 100%);
        color: white;
    }
    
    .assistant-message .avatar {
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
        color: white;
    }
    
    /* 聊天容器 */
    .chat-container {
        max-width: 900px;
        margin: 70px auto 120px auto;
        padding: 0 1.5rem;
    }
    
    /* 消息样式 */
    .chat-message {
        display: flex;
        padding: 1.5rem;
        gap: 1rem;
        margin-bottom: 1rem;
        border-radius: 0.5rem;
        transition: all 0.2s ease;
    }
    
    .chat-message:hover {
        background: #f8fafc;
    }
    
    .message-content {
        flex: 1;
        font-size: 0.9375rem;
        line-height: 1.6;
        color: #1f2937;
    }
    
    /* 代码块样式 */
    .message-content pre {
        background: #1e1e2e;
        color: #cdd6f4;
        padding: 1rem;
        border-radius: 0.5rem;
        overflow-x: auto;
        margin: 0.5rem 0;
    }
    
    .message-content code {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.875rem;
    }
    
    /* 工具栏 */
    .bottom-toolbar {
        position: fixed;
        bottom: 60px;
        left: 20rem;
        right: 0;
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(10px);
        border-top: 1px solid #e5e7eb;
        padding: 0.75rem 1.5rem;
        display: flex;
        gap: 0.5rem;
        z-index: 1000;
    }
    
    .tool-button {
        padding: 0.5rem;
        border-radius: 0.375rem;
        border: 1px solid #e5e7eb;
        background: white;
        color: #6b7280;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .tool-button:hover {
        background: #f3f4f6;
        border-color: #d1d5db;
    }
    
    /* 输入区域 */
    .input-area {
        position: fixed;
        bottom: 0;
        left: 16rem;
        right: 0;
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(10px);
        padding: 1rem 1.5rem;
        border-top: 1px solid #e5e7eb;
        z-index: 1000;
    }
    
    .input-container {
        max-width: 900px;
        margin: 0 auto;
        display: flex;
        gap: 1rem;
    }
    
    .stTextInput input {
        padding: 0.75rem 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
        background: white;
        font-size: 0.9375rem;
        transition: all 0.2s;
    }
    
    .stTextInput input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59,130,246,0.1);
    }
    
    /* 发送按钮 */
    .stButton button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white;
        border-radius: 0.5rem;
        padding: 0 1.5rem;
        height: 42px;
        font-weight: 500;
        border: none;
        transition: all 0.2s;
    }
    
    .stButton button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
    }
    
    /* 侧边栏按钮样式 */
    .css-1d391kg .stButton button {
        background: #313244 !important;
        border: 1px solid #45475a;
        color: #cdd6f4;
    }
    
    .css-1d391kg .stButton button:hover {
        background: #45475a !important;
    }
    
    /* 移动端适配 */
    @media (max-width: 768px) {
        .top-nav, .bottom-toolbar, .input-area {
            left: 0;
        }
        
        .chat-container {
            margin: 70px 0 120px 0;
        }
    }
    
    /* 滚动条样式 */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
</style>
""", unsafe_allow_html=True)

# 在文件开头的配置部分
def initialize_session_state():
    """初始化会话状态"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "waiting_for_response" not in st.session_state:
        st.session_state.waiting_for_response = False
    if "system_prompt" not in st.session_state:
        st.session_state.system_prompt = load_system_prompt()
    # 添加 API 配置状态
    if "api_key" not in st.session_state:
        st.session_state.api_key = os.getenv('MARSCODE_API_KEY', '')
    if "model_ep" not in st.session_state:
        st.session_state.model_ep = os.getenv('MARSCODE_MODEL_EP', '')
def load_system_prompt():
    """加载系统提示词"""
    try:
        with open("prompts.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        with open("prompts.txt", "w", encoding="utf-8") as f:
            f.write(DEFAULT_PROMPT)
        return DEFAULT_PROMPT
    except Exception as e:
        st.error(f"读取提示词文件时出错: {str(e)}")
        return DEFAULT_PROMPT

def load_and_resize_icon():
    """加载并调整图标大小"""
    try:
        image_path = os.getenv('MARSCODE_ICON_PATH', 'icon.png')
        if not os.path.exists(image_path):
            st.warning(f"Icon file not found at {image_path}. Using default icon.")
            image = Image.new('RGB', (48, 48), color='#3b82f6')
            return image
            
        image = Image.open(image_path)
        image.thumbnail((48, 48), Image.Resampling.LANCZOS)
        return image
    except Exception as e:
        st.error(f"Error loading icon: {str(e)}")
        image = Image.new('RGB', (48, 48), color='#3b82f6')
        return image

def image_to_base64(image):
    """将 PIL Image 转换为 base64 字符串"""
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

def get_response(user_input, system_prompt):
    """获取AI回复"""
    try:
        client = Ark(api_key=st.session_state.api_key)
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend([
            {"role": m["role"], "content": m["content"]} 
            for m in st.session_state.messages[-4:]
        ])
        messages.append({"role": "user", "content": user_input})
        
        completion = client.chat.completions.create(
            model=st.session_state.model_ep,
            messages=messages
        )
        return True, completion.choices[0].message.content
    except Exception as e:
        return False, f"抱歉，服务出现了一点问题: {str(e)} 🙏"

def create_nav_bar():
    """创建顶部导航栏"""
    st.markdown("""
        <div class="top-nav">
            <div class="nav-title">New Conversation</div>
            <div class="top-nav-actions">
                <button class="tool-button">🔄</button>
                <button class="tool-button">📋</button>
                <button class="tool-button">↗️</button>
                <button class="tool-button">⚡</button>
            </div>
        </div>
    """, unsafe_allow_html=True)
def create_sidebar():
    """创建侧边栏"""
    with st.sidebar:
        # 品牌区域
        icon = load_and_resize_icon()
        if icon:
            st.markdown(f"""
                <div class="brand-section">
                    <div class="brand-icon">
                        <img src="data:image/png;base64,{image_to_base64(icon)}" 
                             alt="MarsCode Icon"
                             style="width:100%;height:100%;object-fit:cover;">
                    </div>
                    <div class="brand-text">
                        <h1 class="brand-header">MarsCode</h1>
                        <div class="brand-subtitle">Your AI Coding Assistant</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # 主要功能按钮
        col1, col2 = st.columns(2)
        with col1:
            st.button("🚀 Chat", use_container_width=True)
        with col2:
            st.button("💻 Code", use_container_width=True)
        
        st.markdown("---")
        
        # 系统设置
        with st.expander("⚙️ 系统设置"):
            edited_prompt = st.text_area(
                "系统提示词",
                st.session_state.system_prompt,
                height=200
            )
            if st.button("保存提示词"):
                try:
                    with open("prompts.txt", "w", encoding="utf-8") as f:
                        f.write(edited_prompt)
                    st.session_state.system_prompt = edited_prompt
                    st.success("✅ 提示词已更新")
                except Exception as e:
                    st.error(f"❌ 保存失败: {str(e)}")
        
        # API设置
        with st.expander("🔑 API设置"):
            # 显示当前配置来源
            if os.getenv('MARSCODE_API_KEY') and os.getenv('MARSCODE_MODEL_EP'):
                st.info("当前使用环境变量中的默认配置")
            
            # API Key 配置
            new_api_key = st.text_input(
                "API Key",
                value=st.session_state.api_key,
                type="password",
                help="输入你的 API Key，留空则使用环境变量中的值"
            )
            
            # Model Endpoint 配置
            new_model_ep = st.text_input(
                "Model Endpoint",
                value=st.session_state.model_ep,
                help="输入模型端点，留空则使用环境变量中的值"
            )
            
            # 配置示例
            st.markdown("##### 配置示例")
            st.code("""
# .env file example:
MARSCODE_API_KEY=your-api-key
MARSCODE_MODEL_EP=your-model-endpoint
            """)
            
            col1, col2 = st.columns(2)
            with col1:
                # 保存按钮
                if st.button("💾 保存配置"):
                    if new_api_key:
                        st.session_state.api_key = new_api_key
                    if new_model_ep:
                        st.session_state.model_ep = new_model_ep
                        
                    # 验证新配置
                    try:
                        client = Ark(api_key=st.session_state.api_key)
                        # 尝试一个简单的API调用
                        completion = client.chat.completions.create(
                            model=st.session_state.model_ep,
                            messages=[{"role": "user", "content": "test"}]
                        )
                        st.success("✅ API 配置验证成功！")
                    except Exception as e:
                        st.error(f"❌ API 配置验证失败: {str(e)}")
                        # 恢复到环境变量中的值
                        st.session_state.api_key = os.getenv('MARSCODE_API_KEY', '')
                        st.session_state.model_ep = os.getenv('MARSCODE_MODEL_EP', '')
            
            with col2:
                # 重置按钮
                if st.button("🔄 重置默认值"):
                    st.session_state.api_key = os.getenv('MARSCODE_API_KEY', '')
                    st.session_state.model_ep = os.getenv('MARSCODE_MODEL_EP', '')
                    st.success("已重置为环境变量中的默认值")
                
            # 显示当前状态
            st.markdown("##### 当前配置状态")
            status = "✅ 已配置" if st.session_state.api_key and st.session_state.model_ep else "❌ 未配置"
            st.info(f"API 配置状态: {status}")
            
            if not st.session_state.api_key or not st.session_state.model_ep:
                st.warning("请配置 API Key 和 Model Endpoint 以使用完整功能")
        
        # 清除对话
        st.button("🗑️ 清除对话", on_click=lambda: st.session_state.update(messages=[]))
        
        # 版本信息
        st.markdown("---")
        st.markdown("""
            <div style='text-align: center; color: #a6adc8; font-size: 0.875rem;'>
                MarsCode v1.0<br>
                Made with ❤️ by Mars Team
            </div>
        """, unsafe_allow_html=True)

def create_toolbar():
    """创建底部工具栏"""
    st.markdown("""
        <div class="bottom-toolbar">
            <button class="tool-button" title="Settings">⚙️</button>
            <button class="tool-button" title="Clear">🗑️</button>
            <button class="tool-button" title="Copy">📋</button>
            <button class="tool-button" title="Export">📤</button>
            <button class="tool-button" title="Theme">🎨</button>
            <button class="tool-button" title="Help">❓</button>
        </div>
    """, unsafe_allow_html=True)

def display_message(message):
    """显示单条消息"""
    role = message["role"]
    content = message["content"]
    
    avatar = "👤" if role == "user" else "🤖"
    message_class = "user-message" if role == "user" else "assistant-message"
    
    st.markdown(f"""
        <div class="chat-message {message_class}">
            <div class="avatar">{avatar}</div>
            <div class="message-content">{content}</div>
        </div>
    """, unsafe_allow_html=True)

def main():
    """主函数"""
    initialize_session_state()
    create_sidebar()
    create_nav_bar()
    create_toolbar()
    
    # 聊天界面
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # 显示欢迎消息
        if not st.session_state.messages:
            st.markdown("""
                <div class="chat-message assistant-message">
                    <div class="avatar">🤖</div>
                    <div class="message-content">
                        👋 Hello! I'm your MarsCode AI assistant. How can I help you with coding today?
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # 显示对话历史
        for message in st.session_state.messages:
            display_message(message)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 输入区域
    st.markdown("""
        <div class="input-area">
            <div class="input-container">
    """, unsafe_allow_html=True)
    
    # 使用columns布局创建输入区域
    col1, col2 = st.columns([6, 1])
    
    with col1:
        user_input = st.text_input(
            "",
            placeholder="Input your message here... (Shift + Enter for new line)",
            key=f"user_input_{len(st.session_state.messages)}",
            label_visibility="collapsed",
            disabled=st.session_state.waiting_for_response
        )
    
    with col2:
        send_button = st.button(
            "Send",
            use_container_width=True,
            disabled=st.session_state.waiting_for_response,
            key=f"send_{len(st.session_state.messages)}"
        )
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # 处理用户输入
    if user_input and send_button and not st.session_state.waiting_for_response:
        # 清理输入内容
        user_input = user_input.strip()
        if not user_input:
            return
        
        # 设置等待状态
        st.session_state.waiting_for_response = True
        
        # 添加用户消息
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        
        st.rerun()
    
    # AI响应处理
    if st.session_state.waiting_for_response and st.session_state.messages:
        try:
            # 显示输入状态
            typing_container = st.empty()
            typing_container.markdown("""
                <div class="chat-message assistant-message">
                    <div class="avatar">🤖</div>
                    <div class="message-content">
                        Thinking...
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # 获取AI响应
            success, response = get_response(
                st.session_state.messages[-1]["content"],
                st.session_state.system_prompt
            )
            
            # 清除输入状态
            typing_container.empty()
            
            # 添加AI响应
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().strftime("%H:%M")
            })
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
        
        finally:
            # 重置状态
            st.session_state.waiting_for_response = False
            st.rerun()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"程序运行出错: {str(e)}")
        st.error("请刷新页面重试")