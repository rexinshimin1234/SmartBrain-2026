import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
import os
import glob
import shutil
import httpx  # ✅ 引入异步 HTTP 客户端
from typing import List, Dict, Optional

# --- 1. 配置区域 ---
API_KEY = "sk-4f5a33e749174b61969cea91ed09d4e0"
BASE_URL = "https://api.deepseek.com/chat/completions" # 注意：httpx 需要完整的 URL endpoints
DATA_DIR = "./data"

# --- 2. 核心类定义 (OOP 封装) ---

class KnowledgeBase:
    """
    知识库管理类：负责文件读取、向量化、检索
    """
    def __init__(self, data_dir: str, model_path: str = './local_model'):
        self.data_dir = data_dir
        self.model = SentenceTransformer(model_path)
        self.documents = []   # 存文本
        self.sources = []     # 存文件名
        self.embeddings = None
        
        # 初始化时加载
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        self.reload()

    def reload(self):
        """重新扫描并计算向量"""
        print(f"🔄 [KnowledgeBase] 正在扫描: {self.data_dir}")
        temp_docs = []
        temp_sources = []
        
        # 扫描 TXT
        for file_path in glob.glob(os.path.join(self.data_dir, "*.txt")):
            with open(file_path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
                temp_docs.extend(lines)
                temp_sources.extend([os.path.basename(file_path)] * len(lines))
        
        # 这里为了演示简洁，暂时省略 PDF 逻辑，你把之前的 PDF 逻辑粘回来即可
        
        self.documents = temp_docs
        self.sources = temp_sources
        
        if self.documents:
            print("⚡ [KnowledgeBase] 正在计算向量...")
            self.embeddings = self.model.encode(self.documents)
        else:
            self.embeddings = None
            
        print(f"✅ [KnowledgeBase] 加载完毕，共 {len(self.documents)} 条知识")

    def search(self, query: str, top_k: int = 3):
        """检索最相关的文档"""
        if not self.documents or self.embeddings is None:
            return None, None, 0.0

        query_vec = self.model.encode([query])
        hits = util.semantic_search(query_vec, self.embeddings, top_k=top_k)
        
        best = hits[0][0]
        idx = best['corpus_id']
        return self.documents[idx], self.sources[idx], best['score']

class DeepSeekClient:
    """
    AI 客户端类：负责与 LLM 进行异步通信
    """
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    async def chat_async(self, messages: List[Dict]):
        """
        ✅ 异步发送聊天请求
        """
        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            "stream": False
        }
        
        # 使用异步上下文管理器，不会阻塞主线程
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                resp = await client.post(self.base_url, headers=self.headers, json=payload)
                resp.raise_for_status() # 如果 4xx/5xx 会报错
                return resp.json()['choices'][0]['message']['content']
            except Exception as e:
                print(f"❌ API 请求失败: {e}")
                return "AI 思考时断线了..."

# --- 3. 实例化全局对象 (单例模式) ---
# 这些对象在应用启动时只创建一次
kb = KnowledgeBase(DATA_DIR)
ai_client = DeepSeekClient(API_KEY, BASE_URL)

app = FastAPI()

class QueryRequest(BaseModel):
    # 标准的 OpenAI 格式: [{"role": "user", "content": "..."}]
    messages: List[Dict[str, str]]

# --- 4. 接口实现 ---

@app.post("/chat")
async def chat_endpoint(request: QueryRequest):
    # 1. 获取用户最新的问题
    if not request.messages:
        raise HTTPException(status_code=400, detail="消息列表为空")
    
    user_query = request.messages[-1]["content"]
    
    # 2. 检索知识库 (RAG)
    # 简单策略：直接用最新问题去搜。
    # 进阶策略(你之前的): 用上下文去搜。这里先保持简单，确保代码跑通。
    retrieved_text, source_file, score = kb.search(user_query)
    
    # 3. 构建 Prompt
    # 技巧：我们将“参考资料”放入 System Prompt，这样 AI 会记得更牢，而且不破坏 messages 结构
    system_prompt = "你是一个专业的工业助手。回答问题时请参考以下资料。如果资料中没有答案，请诚实告知。"
    if retrieved_text and score > 0.35:
        system_prompt += f"\n\n【参考资料】(来源: {source_file}):\n{retrieved_text}"
    else:
        system_prompt += "\n\n(暂无相关参考资料，请凭常识回答)"

    # 4. 组装最终的消息列表
    # 结构：[System(带资料), User, Assistant, User...]
    full_messages = [{"role": "system", "content": system_prompt}] + request.messages

    # 5. ✅ 异步调用 AI
    print(f"📨 发送请求给 DeepSeek... (包含 {len(full_messages)} 条历史)")
    answer = await ai_client.chat_async(full_messages)
    
    return {
        "answer": answer,
        "source": source_file if score > 0.35 else "无",
        "score": float(score)
    }

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(DATA_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 调用对象的方法热更新
    kb.reload()
    
    return {"message": f"文件 {file.filename} 上传成功，知识库已刷新。"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)