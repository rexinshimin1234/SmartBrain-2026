import streamlit as st
from openai import OpenAI

# 1. 页面标题
st.title("🔥 林氏智能 IoT 监控中心")
st.write("请输入传感器数据，AI 专家将为您诊断风险。")

# 2. 配置 AI (记得换 Key!)
client = OpenAI(
    api_key="sk-4f5a33e749174b61969cea91ed09d4e0", # <--- 换成你的 Key
    base_url="https://api.deepseek.com"
)

# 3. 输入框
user_input = st.text_input("在这里输入数据 (例如: 温度80度, 震动强):")

# 4. 按钮
if st.button("开始分析"):
    if not user_input:
        st.warning("请先输入数据！")
    else:
        # 显示转圈圈动画
        with st.spinner('AI 正在大脑风暴中...'):
            try:
                # 呼叫 AI
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "你是一个严谨的工业安全专家。请分析用户提供的传感器数据，判断风险等级（安全/警告/危险），并给出简短的处理建议。"},
                        {"role": "user", "content": user_input}
                    ],
                    stream=False
                )
                answer = response.choices[0].message.content
                
                # 5. 显示结果
                st.success("分析完成！")
                st.markdown("### 🤖 专家诊断报告：")
                st.write(answer)
                
            except Exception as e:
                st.error(f"出错了: {e}")