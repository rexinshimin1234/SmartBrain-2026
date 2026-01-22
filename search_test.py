import chromadb

# 1. 连接到刚才创建的数据库 (注意路径必须一致！)
print("🔌 正在连接向量数据库...")
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# 2. 获取那个集合
collection = chroma_client.get_collection(name="smartbrain_knowledge")
print(f"✅ 连接成功！当前库中共有 {collection.count()} 条数据。")

# 3. 模拟用户搜索
#    你可以随便换问题，比如 "赛季什么时候结束？" 或者 "怎么获得资格？"
query_text = "新赛季什么时候开始？"

print(f"\n❓ 用户在问: {query_text}")
print("🔍 正在进行向量检索 (Vector Search)...")

# 4. 核心魔法：Query
#    n_results=1 表示只找最相似的那 1 条 (这就是所谓的 Top-K)
# 让它多吐点数据出来
results = collection.query(
    query_texts = ["1月8日"],
    n_results=3
)

# 遍历打印出来看看
for i, doc in enumerate(results['documents'][0]):
    print(f"\n[片段 {i+1}]:")
    print(doc)
    print("-" * 30)