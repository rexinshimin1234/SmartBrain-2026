# main_process.py
import os
from utils import split_text  # 👈 看这里！我们要调用你刚才写的工具箱

def load_and_process(filename):
    # 1. 检查文件是否存在
    if not os.path.exists(filename):
        print(f"❌ 错误：找不到文件 {filename}")
        return []

    # 2. 读取文件 (The Reader)
    print(f"📄 正在读取 {filename}...")
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read() 
    # 3. 清洗数据 (升级版)
    #    原版: clean_content = content.strip() 
    
    # --- 新版逻辑 ---
    # 1. 先把每一行切开
    lines = content.splitlines()
    # 2. 只有当这一行不是空的时候，才保留 (去除空行)
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    # 3. 再把它们拼回去，用换行符连接
    clean_content = "\n".join(non_empty_lines)
    
    print(f"📊 清洗后字数: {len(clean_content)}")
    
    print(f"📊 原始字数: {len(clean_content)}")

    # 4. 调用手术刀进行切片 (The Chunker)
    #    我们设定每块 100 字
    chunks = split_text(clean_content, chunk_size=300)
    
    print(f"🔪 切分完成！共切成 {len(chunks)} 块。")
    return chunks

# --- 主程序 ---
if __name__ == "__main__":
    # 假设你的数据文件叫 data.txt
    file_path = "data.txt"
    
    # 跑流程
    knowledge_base = load_and_process(file_path)

    # 5. 抽查一下 (看看切出来的第一块长什么样)
    if knowledge_base:
        print("\n--- 预览第一块数据 (Chunk 0) ---")
        print(knowledge_base[0])
        print("-------------------------------")
        
        print("\n--- 预览最后一块数据 ---")
        print(knowledge_base[-1])
        print("-------------------------------")