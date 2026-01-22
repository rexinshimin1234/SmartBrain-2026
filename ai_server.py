from fastapi import FastAPI
from openai import OpenAI
app =FastAPI()
client = OpenAI(
    api_key="sk-4f5a33e749174b61969cea91ed09d4e0",
    base_url="https://api.deepseek.com"
)
@app.get("/")
def home():
    return{"message":"AI服务已启动！请访问/ask?q=你的问题 来提问"}
@app.get("/ask")
def ask_ai(q:str):
    print(f"正在思考问题:{q}...")
    try:
        response =client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role":"system","content":"你是一个说话幽默风趣的物联网专家"},
                {"role":"user","content":q}
            ],
            stream=False
        )
        ai_answer =response.choices[0].message.content
        return{
            "status":"success",
            "question":q,
            "answer":ai_answer
        }
    except Exception as e:
        return{"status":"error","message":str(e)}