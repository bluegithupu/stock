# 使用Python官方镜像作为基础镜像
FROM python:3.11-slim as builder

# 设置工作目录
WORKDIR /app

# 设置Python环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 安装系统依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# 安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 第二阶段：最终镜像
FROM python:3.11-slim

WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 从builder阶段复制Python环境
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/

# 复制项目文件
COPY . .

# 收集静态文件
RUN python manage.py collectstatic --noinput

# 设置生产环境配置
ENV DEBUG=0
ENV DJANGO_SETTINGS_MODULE=stock.settings

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["gunicorn", "stock.wsgi:application", "--bind", "0.0.0.0:8000"]