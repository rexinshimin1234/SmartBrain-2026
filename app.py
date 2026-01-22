import streamlit as st
import requests
import json

st.title("🚀 SmartBrain Pro (记忆版)")

# --- 核心逻辑：初始化消息历史 ---
# st.session_state 是 Streamlit 的全局缓存
if "messages" not in st.session_state:
    st.session_state.messages = []
    # 可以在这里加一个开场白
    st.session_state.messages.append({
        "role": "assistant",
        "content": "我是 SmartBrain，有什么可以帮你的吗？"
    })
# --- 核心逻辑：把历史聊天记录画出来 ---
for msg in st.session_state.messages:
    # st.chat_message 能够自动区分 "user" (右边) 和 "assistant" (左边)
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
# --- 核心逻辑：处理用户输入 ---
# st.chat_input 是专门的聊天输入框，比 st.text_input 更像微信
if prompt := st.chat_input("请问关于 2026 赛季的问题..."):
    
    # 1. 处理用户消息
    # 存入历史
    st.session_state.messages.append({"role": "user", "content": prompt})
    # 立刻显示在界面上
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. 呼叫后端 API
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            try:
                # 发送请求给 FastAPI
                history_to_send = [
                    {"role": m["role"], "content": m["content"]} 
                    for m in st.session_state.messages[:-1]
                ]

                # 发送请求给 FastAPI
                response = requests.post(
                    "http://127.0.0.1:8000/chat", 
                    json={
                        "query": prompt,
                        "history": history_to_send  # ✅ 这里把历史带上！
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    # ... (在获取到 data 之后) ...
                    answer = data["answer"]
                    source = data.get("source", "")
                    
                    full_response = answer
                    
                    # ✅ 优化逻辑：只有当 source 有效时，才加小尾巴
                    # 假设后端返回的空提示是 "没有找到相关资料..."
                    if source and "没有找到相关资料" not in source:
                        full_response += f"\n\n---\n**📚 参考资料**: {source}"
                    
                    st.markdown(full_response)
                    
                    # 3. 存入 AI 的回复到历史
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": full_response
                    })
                else:
                    st.error(f"后端报错: {response.status_code}")
                    
            except Exception as e:
                st.error(f"连接失败: {str(e)}")