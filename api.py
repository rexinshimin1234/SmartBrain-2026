import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict  # ✅ 新增：用于定义列表和字典类型
import chromadb
from openai import OpenAI
from dotenv import load_dotenv

# 1. 加载环境变量
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# 2. 初始化核心组件
app = FastAPI()
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_or_create_collection(name="smartbrain_docs")

# 3. ✅ 升级请求模型 (这是关键！)
class ChatRequest(BaseModel):
    query: str
    # 新增 history 字段，它是一个列表，里面装着字典 (role, content)
    # 默认值为空列表 []，防止报错
    history: List[Dict[str, str]] = [] 

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    # 1. 先去数据库查资料 (只查最新的问题)
    results = collection.query(
        query_texts=[request.query],
        n_results=1
    )
    
    if not results['documents'][0]:
        context = "没有找到相关资料，请尝试用通用知识回答。"
    else:
        context = results['documents'][0][0]

    # 2. ✅ 构建完整的对话历史
    # 第一条：系统提示词 (包含最新的参考资料)
    messages = [
        {
            "role": "system", 
            "content": f"你是一个智能助手 SmartBrain。请根据以下参考资料回答用户问题：\n\n【参考资料】\n{context}"
        }
    ]
    
    # 中间：把前端传过来的历史记录插进去 (让 AI 知道上下文)
    # 我们只取最近的 4 轮对话，防止 Token 爆炸
    messages.extend(request.history[-8:]) 
    
    # 最后：加上用户最新的问题
    messages.append({"role": "user", "content": request.query})

    # 3. 呼叫 DeepSeek
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=False
        )
        return {
            "answer": response.choices[0].message.content,
            "source": context
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)