# 1. 导入必要的工具箱
import json  # 用于把数据存进硬盘(序列化)和读出来(反序列化)
from openai import OpenAI
# 2. 定义 ChatBot 类
# 它是我们的核心控制器，不用继承任何东西，所以括号里是空的(或者不写)
class ChatBot:
    
    # --- 构造函数 (初始化) ---
    # 这里的 self 是固定写法，代表"这个机器人自己"
    def __init__(self):
        # 定义一个列表，用来装所有的聊天记录
        # 这就是机器人的"海马体"
        self.history = [] 
        
        # 机器人一出生，立刻执行"读取记忆"的操作
        # 注意：调用自己内部的方法，必须加 self.
        self.load_memory()
        self.client = OpenAI(
            api_key="sk-4f5a33e749174b61969cea91ed09d4e0", # 🔴 替换这里！
            base_url="https://api.deepseek.com"    # 🔴 如果用 OpenAI，删掉这就行
        )
    # --- 功能：添加消息 ---
    # role: 谁说的？(user/assistant/system)
    # content: 说了啥？
    def add_message(self, role, content):
        # 这里的 {} 代表创建一个字典 (Dictionary)
        # 我们直接把数据包装成 API 喜欢的格式
        data = {
            "role": role,
            "content": content
        }
        
        # append 是列表的方法，意思是"追加到末尾"
        # 把打包好的字典 data，扔进 self.history 列表里
        self.history.append(data)

    # --- 功能：存档 (存入硬盘) ---
    # filename="memory.json" 是默认参数
    # 如果你调用时不传文件名，它就默认存到 memory.json
    def save_memory(self, filename="memory.json"):
        # with open 是 Python 打开文件的标准姿势
        # 'w' = Write (写入模式，会覆盖旧内容)
        # encoding='utf-8' = 防止中文变成乱码
        # as f = 给打开的文件起个临时名字叫 f
        with open(filename, 'w', encoding='utf-8') as f:
            
            # json.dump 是保存指令
            # 参数1 (self.history): 要存的数据
            # 参数2 (f): 存到哪个文件里
            # ensure_ascii=False: 允许直接写入汉字
            # indent=4: 自动缩进4格，让文件好看
            json.dump(self.history, f, ensure_ascii=False, indent=4)
            
        print(f"💾 存档成功！")

    # --- 功能：读档 (从硬盘读取) ---
    def load_memory(self, filename="memory.json"):
        # try 是"尝试执行"，为了防止报错崩溃
        try:
            # 'r' = Read (只读模式)
            with open(filename, 'r', encoding='utf-8') as f:
                # json.load 是读取指令
                # 它会把文件里的字符串，变回 Python 的列表
                self.history = json.load(f)
                
            # len(...) 用来统计列表里有多少个元素
            print(f"✅ 记忆已恢复，共 {len(self.history)} 条。")
            
        # except 捕获错误：如果文件找不到 (FileNotFoundError)
        except FileNotFoundError:
            print("⚠️ 没找到记忆文件，初始化新大脑。")
            # 既然没文件，那就把历史设为一个空列表
            self.history = []

    # --- 功能：获取上下文 ---
    # 下午接 API 时，我们会用到这个方法
    def get_context(self):
        # 直接返回列表即可，因为列表里已经是字典了
        # return 是"把结果递出去"，不是打印在屏幕上
        return self.history
    def ask_ai(self):
        """
        功能：把当前所有的对话记录发给 AI，并获取回复
        """
        print("🤔 SmartBrain 正在思考...")

        # try-except 再次登场，防止断网或 Key 错误导致程序崩溃
        try:
            # 1. 发起请求 (Call API)
            # 这就像是把写好的信 (messages) 寄出去
            response = self.client.chat.completions.create(
                model="deepseek-chat", # 指定用哪个脑子 (如果是 OpenAI 用 gpt-3.5-turbo)
                messages=self.history.pop(5)  # 把我们攒的列表传过去！
            )

            # 2. 解析回复 (Extract)
            # API 返回的是一个超复杂的对象，我们只要里面的"内容"
            # 路径是固定的：choices[0] -> message -> content
            reply_text = response.choices[0].message.content

            # 3. 存入记忆 (Save)
            # AI 说的话，也要记在小本本上，不然下一轮它就忘了
            self.add_message("assistant", reply_text)
            
            # 4. 顺手存个盘 (Auto-Save)
            self.save_memory()

            return reply_text

        except Exception as e:
            print(f"❌ 发生错误: {e}")
            return "我脑子短路了，请检查网络或 Key。"
# =========================================
#  SmartBrain 启动程序 (Main Loop)
# =========================================
if __name__ == "__main__":
    # 1. 唤醒机器人
    bot = ChatBot()
    print("---------------------------------------------")
    print("🤖 SmartBrain 已上线！(输入 'exit' 或 'q' 退出)")
    print("---------------------------------------------")

    # 2. 进入死循环 (对话模式)
    while True:
        # A. 获取用户输入
        user_input = input("\n👤 你: ")
        
        # B. 判断是否退出
        if user_input.lower() in ["exit", "q", "quit"]:
            print("👋 SmartBrain 下线。再见！")
            break # 打破循环，程序结束
            
        # C. 这里的判空处理很关键！防止用户手滑直接回车
        if not user_input.strip():
            print("⚠️ 哪怕发个句号也行，别发空消息啊。")
            continue # 跳过本次循环，重新开始

        # D. 存入用户消息
        bot.add_message("user", user_input)

        # E. 呼叫 AI (并把回复打印出来！)
        # 这里的 print 是为了确保你一定能看到 AI 说了啥
        ai_reply = bot.ask_ai()
        print(f"🤖 AI: {ai_reply}")