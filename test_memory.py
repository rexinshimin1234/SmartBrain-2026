import requests
import time

# 目标地址
url = "http://127.0.0.1:8000/chat"

print("🔥 开始多轮对话记忆测试...")

# 第一轮：告诉它信息
history = [{"role": "user", "content": "你好，我叫于清华，我的工号是 9527。"}]
print(f"\n[1] 发送: {history[-1]['content']}")

resp1 = requests.post(url, json={"messages": history}).json()
print(f"🤖 AI 回复: {resp1['answer']}")

# 把 AI 的回复加进历史
history.append({"role": "assistant", "content": resp1['answer']})

# 第二轮：考考它
history.append({"role": "user", "content": "我刚才告诉你我的工号是多少？"})
print(f"\n[2] 发送: {history[-1]['content']}")

resp2 = requests.post(url, json={"messages": history}).json()
print(f"🤖 AI 回复: {resp2['answer']}")

# 验证逻辑
if "9527" in resp2['answer']:
    print("\n✅ 测试通过！它记住了！")
else:
    print("\n❌ 测试失败，它是个金鱼脑子。")