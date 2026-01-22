import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. 加载保险箱 (这一步会自动把 .env 里的东西读进系统内存)
load_dotenv()

# 2. 从内存里取钥匙 (如果没取到，os.getenv 会返回 None)
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    print("❌ 错误：未找到 API Key，请检查 .env 文件！")
    exit()

# 3. 初始化客户端 (用刚才取到的安全钥匙)
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# 4. 这里的 RAG 核心：先读取你的“私有知识”
try:
    with open("data.txt", "r", encoding="utf-8") as f:
        private_data = f.read()
except FileNotFoundError:
    print("❌ 没找到 data.txt，请确认文件位置！")
    exit()
print("✅ 知识库加载成功！我是你的 SmartBrain，问我关于 data.txt 的问题吧。")
print("(输入 'exit' 或 'q' 退出)")

while True:
    user_input = input("\nUser > ").strip()
    if user_input.lower() in  ["exit","q"]:
        print("👋 Bye!")
        break
    if not user_input:
        continue
    print("SmartBrain > Thinking...")


    system_prompt = f"""
你是一个智能助手。请根据下面的【已知信息】来回答用户的问题。
如果问题无法从已知信息中得到答案，请诚实地回答“我不知道”。

【已知信息】：
    {private_data}
"""
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        print(f"SmartBrain > {response.choices[0].message.content}")
    
    except Exception as e:
        print(f"❌ 出错了: {e}")