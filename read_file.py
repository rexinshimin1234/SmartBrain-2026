# 1. 定义文件名
file_name = "data.txt"

# 2. 打开文件 (注意 encoding='utf-8' 是必须的，否则中文会乱码)
#    with open(...) as f:  意思就是“在这个缩进里，f 就是打开的文件，出缩进自动关闭”
with open(file_name, "r", encoding="utf-8") as f:
    
    # 3. 一次性把所有内容读成一个巨大的字符串
    content = f.read()

# 4. 打印看看
print("=== 读取到的内容 ===")
print(content)
print("==================")

# 5. 验证一下是不是字符串
print(f"数据类型: {type(content)}")
print(f"总字数: {len(content)}")