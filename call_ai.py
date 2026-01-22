from openai import OpenAI

# 1. 配置连接信息
# 就像我们要连接 Wi-Fi 一样，要告诉 Python 地址和密码
client = OpenAI(
    api_key="sk-4f5a33e749174b61969cea91ed09d4e0", # <--- 【这里一定要换成你的 Key，保留双引号！】
    base_url="https://api.deepseek.com"            #这是 DeepSeek 的专用通道，不要改
)

print("正在呼叫 AI，请稍等...")

# 2. 发送请求 (发微信)
try:
    response = client.chat.completions.create(
        model="deepseek-chat",  # 指定我们要用哪个脑子
        messages=[
            {"role": "system", "content": "你是一个资深的程序员导师"}, # 设定人设
            {"role": "user", "content": "我是一个物联网专业的学生，正在学习由 Python 控制 AI。请用一句话鼓励我，要热血一点！"} # 你的问题
        ],
        stream=False
    )

    # 3. 接收回复
    # AI 返回的数据藏得很深，我们要一层层剥开
    ai_answer = response.choices[0].message.content

    print("----------------")
    print("AI 回复说：")
    print(ai_answer)

except Exception as e:
    print("出错了！错误信息如下：")
    print(e)