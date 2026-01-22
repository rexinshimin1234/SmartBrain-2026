import requests  # 引入请求工具（必须加在文件第一行）

# 1. 订单对象（不需要改，保持原样）
class QueryRequest:
    def __init__(self, messages):
        self.messages = messages

# 2. 机器对象（大升级）
class DeepSeekClient:
    def __init__(self, api_key):
        self.api_key = api_key
        # DeepSeek 的官方 API 地址（相当于工厂地址）
        self.api_url = "https://api.deepseek.com/chat/completions"
        print(f"✅ 客户端就绪，API Key 尾号：{self.api_key[-4:]}")

    def send_chat(self, request_obj):
        """
        这个方法负责：拆开包裹 -> 组装参数 -> 发送请求 -> 拿到结果
        """
        # A. 准备身份证明 (Headers)
        # 这里用到了 self.api_key（机器自带的刀片）
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # B. 准备请求数据 (Payload)
        # 这里用到了 request_obj.messages（你临时塞进来的橙子）
        data = {
            "model": "deepseek-chat",
            "messages": request_obj.messages,
            "stream": False  # 先关掉流式输出，简单点
        }

        print("📡 正在向 DeepSeek 发送请求，请稍候...")
        
        # C. 发送网络请求 (requests.post)
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            
            # D. 处理结果
            if response.status_code == 200:
                # 成功！返回 JSON 数据里的回复内容
                # 下面这行稍微有点长，是 DeepSeek 返回数据的固定格式
                return response.json()['choices'][0]['message']['content']
            else:
                return f"❌ 请求失败：{response.status_code} - {response.text}"
                
        except Exception as e:
            return f"❌ 发生错误：{e}"

# ==========================================
# 🚀 实战测试区 (Main)
# ==========================================

# 1. 准备你的 API Key (请填入你真实的 key)
my_key = "sk-4f5a33e749174b61969cea91ed09d4e0" 

# 2. 创建机器
client = DeepSeekClient(my_key)

# 3. 准备问题（打包橙子）
# 我们问个稍微难点的，测试它是不是真的 AI
user_question = [{"role": "user", "content": "用Python写一个冒泡排序，只给我代码。"}]
order = QueryRequest(user_question)

# 4. 开机榨汁！
result = client.send_chat(order)

# 5. 打印最终结果
print("-" * 30)
print("🤖 DeepSeek 回复：")
print(result)
print("-" * 30)
# ... 上面是你刚才运行过的代码 ...

print("\n" + "="*30 + "\n") # 打印个分割线方便看

# === 第二次测试：机器还在热着，直接用！===

# 1. 打包第二个订单（这次我们要解释一下代码）
# 注意：我们不需要重新 new 一个 DeepSeekClient，直接用上面的 client！
order_2 = QueryRequest([{"role": "user", "content": "请给上面的冒泡排序代码加上详细的中文注释"}])

# 2. 直接发货
result_2 = client.send_chat(order_2)

# 3. 看结果
print("🤖 DeepSeek 的补充解释：")
print(result_2)