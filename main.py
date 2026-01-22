# 1. 引入 fastapi
from fastapi import FastAPI

# 2. 创建一个 APP 实例 (这就是你的网站本体)
app = FastAPI()

# --- 这是一个普通的函数 ---
# 还是刚才那个逻辑，稍微改了一点点，让它返回字典
def analyze_temps(data_list):
    current_max = 0
    is_danger = False
    
    for t in data_list:
        if t > 30:
            is_danger = True
        if t > current_max:
            current_max = t
            
    # 返回一个字典，这样网页端能直接看懂
    return {
        "status": "success",
        "is_danger": is_danger,
        "max_temp": current_max,
        "message": "检测完成"
    }

# --- 见证奇迹的地方：装饰器 (Decorator) ---
# @app.get("/") 意思是：当有人访问你网站的首页时，执行下面这个函数
@app.get("/")
def home():
    return {"message": "你好！这是林老师带你做的第一个AI服务后台！"}

# @app.get("/check_iot") 意思是：当有人访问 /check_iot 这个网址时...
@app.get("/check_iot")
def check_iot_data():
    # 模拟一组数据（后面我们会让它真的去读）
    fake_data = [22, 23, 55, 24] 
    
    # 调用上面的工具函数
    result = analyze_temps(fake_data)
    
    # 把结果扔给网页
    return result