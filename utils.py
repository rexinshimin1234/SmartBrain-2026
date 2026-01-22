# utils.py

def split_text(text, chunk_size=300):
    """
    功能：把长文本切成小块
    参数：
        text: 原始长文本
        chunk_size: 每块的长度（默认100字）
    返回：
        一个包含所有碎片的列表
    """
    chunks = []
    total_length = len(text)
    
    # 核心算法：用 range 生成步长
    # 比如 range(0, 500, 100) -> 0, 100, 200, 300, 400
    for i in range(0, total_length, chunk_size):
        # 切片操作：从 i 开始，切到 i + chunk_size
        piece = text[i : i + chunk_size]
        chunks.append(piece)
        
    return chunks

# --- 自测代码 (只有直接运行此文件时才会跑) ---
if __name__ == "__main__":
    # 搞个长点的假数据测试一下
    long_data = "A" * 250  # 弄一个 250 个 A 的字符串
    result = split_text(long_data, chunk_size=300)
    
    print(f"切分前长度: {len(long_data)}")
    print(f"切分后块数: {len(result)}")
    print(f"第一块长度: {len(result[0])}")
    print(f"最后一块长度: {len(result[-1])}") # 应该是 50