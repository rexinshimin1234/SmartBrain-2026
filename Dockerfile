# 1. 基础镜像：使用轻量级的 Python 3.10
FROM python:3.10-slim

# 2. 设置工作目录
WORKDIR /app

# 3. 复制依赖清单并安装 (利用 Docker 缓存层，先装依赖再拷代码)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 复制项目代码
COPY . .

# 5. 暴露端口 (FastAPI 和 Streamlit)
EXPOSE 8000
EXPOSE 8501

# 6. 启动脚本：默认启动后端，但也准备好了前端环境
#    (实际部署时，我们通常会用 docker-compose 来分别启动)
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]