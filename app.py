import streamlit as st
import requests  # 👈 新朋友：专门负责发 HTTP 请求的

# 1. 基础配置
st.set_page_config(page_title="SmartBrain 2.0", page_icon="🚀")
st.title("🚀 SmartBrain (API版)")

# 2. 初始化 Session State
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "我是 SmartBrain 2.0，我的大脑在云端 (FastAPI)！"}
    ]

# 3. 渲染历史记录
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 4. 处理输入
user_input = st.chat_input("请输入问题...")

if user_input:
    # --- 显示用户输入 ---
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # --- 呼叫后端 API (核心变化) ---
    with st.chat_message("assistant"):
        status_box = st.empty()
        status_box.markdown("📡 **正在连接后端 API...**")

        try:
            # 【重点】这里不再自己算，而是发 POST 请求给 api.py
            # 记得确保你的 uvicorn api:app 还在另一个终端里跑着！
            response = requests.post(
                "http://127.0.0.1:8000/chat", 
                json={"query": user_input}  # 发送的数据格式必须和后端定义的 Pydantic 一样
            )
            
            if response.status_code == 200:
                # 拿到 JSON 结果
                data = response.json()
                answer = data["answer"]
                
                # 更新界面
                status_box.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
                # (可选) 在侧边栏显示查到的参考资料，方便调试
                # (可选) 在侧边栏显示查到的参考资料
                with st.sidebar:
                    st.write("🔍 **本次参考资料：**")
                    # ❌ 删掉这行: st.json(data["source"])
                    # ✅ 改成这行:
                    st.markdown(data["source"])
            else:
                status_box.error(f"❌ 服务器报错: {response.text}")
                
        except Exception as e:
            status_box.error(f"❌ 无法连接后端: {e}")