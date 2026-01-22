import os
import chromadb
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

# 1. 初始化环境 (和之前一样)
load_dotenv()
app = FastAPI(title="SmartBrain API", description="专业的 RAG 知识库接口")

# 2. 准备连接 (全局变量，启动时只连一次)
#    注意：这里不需要 @st.cache_resource 了，因为 API 服务是一直开着的
print("正在初始化 SmartBrain 后端引擎...")
try:
    # 连电话
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"), 
        base_url="https://api.deepseek.com"
    )
    # 连书架
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_collection(name="smartbrain_knowledge")
    print("✅ 引擎启动成功！")
except Exception as e:
    print(f"❌ 启动失败: {e}")

# 3. 定义“安检标准” (Data Model)
#    用户发来的数据必须长这样：{"query": "你的问题"}
class ChatRequest(BaseModel):
    query: str

# 4. 核心接口：聊天 (POST)
@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    """
    接收用户的问题，进行 RAG 搜索，返回 AI 的回答
    """
    user_query = request.query
    
    # --- RAG 逻辑 (完全复用昨天的代码) ---
    print(f"收到问题: {user_query}")
    
    # A. 搜库
    results = collection.query(query_texts=[user_query], n_results=3)
    retrieved_text = "\n\n".join(results['documents'][0])
    
    if not retrieved_text:
        context_str = "（无已知信息）"
    else:
        context_str = retrieved_text

    # B. 拼 Prompt
    system_prompt = f"""
    你是一个专业的峡谷之巅客服助手。请根据【参考资料】回答。
    【参考资料】：
    {context_str}
    """

    # C. 问 AI
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]
    )
    
    answer = response.choices[0].message.content
    
    # 5. 返回标准 JSON
    return {
        "query": user_query,
        "answer": answer,
        "source": context_str # 把查到的资料也返回去，方便调试
    }