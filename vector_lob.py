from sentence_transformers import SentenceTransformer, util

# 1. 加载模型 (注意：这次我们换成了支持中文的多语言模型)
# 第一次运行会下载约 400MB 的数据，可能需要一点时间，请耐心等待
print("正在加载多语言 Embedding 模型...")
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2') 

# 2. 准备词汇
words = ["apple", "pear", "car", "苹果", "香蕉", "卡车"]
print(f"测试词汇: {words}")

# 3. 转化为向量
embeddings = model.encode(words)

# 4. 重新测试相似度
print("\n--- 🤖 AI 的认知测试 (多语言版) ---")

# 英文测试
score_1 = util.cos_sim(embeddings[0], embeddings[1]) # apple vs pear
score_2 = util.cos_sim(embeddings[0], embeddings[2]) # apple vs car
print(f"1. 'apple' vs 'pear': {score_1.item():.4f}")
print(f"2. 'apple' vs 'car' : {score_2.item():.4f}")

print("\n--- 中文测试 (见证时刻) ---")
# 这次应该能区分开了
score_3 = util.cos_sim(embeddings[3], embeddings[4]) # 苹果 vs 香蕉
score_4 = util.cos_sim(embeddings[3], embeddings[5]) # 苹果 vs 卡车

print(f"3. '苹果' vs '香蕉': {score_3.item():.4f} (预期: 高)")
print(f"4. '苹果' vs '卡车': {score_4.item():.4f} (预期: 低)")