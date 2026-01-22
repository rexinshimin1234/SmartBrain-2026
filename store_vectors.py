import chromadb
# 从我们刚才写的脚本里导入处理函数
from main_process import load_and_process 

# 1. 初始化数据库
#    get_or_create: 如果有了就读取，没有就新建
#    path="./chroma_db": 数据会保存在你当前文件夹下的 chroma_db 文件夹里
print("🔄 正在初始化向量数据库...")
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# 2. 创建一个“集合” (Collection)
#    相当于 SQL 里的“表”
#    collection_name 可以随便起，比如 "smartbrain_knowledge"
collection = chroma_client.get_or_create_collection(name="smartbrain_knowledge")

# 3. 准备数据
file_path = "data.txt"
chunks = load_and_process(file_path)

if not chunks:
    print("❌ 没有数据，程序退出")
    exit()

print(f"📦 准备存入 {len(chunks)} 个碎片...")

# 4. 开始存入 (Chroma 会自动帮我们做 Embedding，不需要手写向量化代码)
#    我们需要给每个块一个唯一的 ID，就用 "chunk_0", "chunk_1"...
ids = [f"chunk_{i}" for i in range(len(chunks))]

collection.add(
    documents=chunks, # 文本内容
    ids=ids           # 每个文本的身份证号
)

print(f"✅ 成功存入 {collection.count()} 条数据！")
print("🎉 你的私有知识库已经建立完成。")