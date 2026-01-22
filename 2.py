import json

class ChatBot:
    def __init__(self):
        self.history = []

    # 练习：补全 save_memory 函数
    def save_memory(self, filename="memory.json"): # 1. 这里缺两个符号
        
        # 2. 打开文件，写入模式('w')，记得最后有个冒号
        with open(filename, 'w', encoding='utf-8') as f:
            
            # 3. 调用 json 库的 dump 方法
            # 把 self.history 写入到 f 文件里
            json.dump(self.history, f, ensure_ascii=False, indent=4)
            
        print("存档成功")

# --- 测试区 ---
bot = ChatBot()
bot.history.append({"role": "user", "content": "测试"})

# 4. 调用这个方法（记得加括号）
bot.save_memory()