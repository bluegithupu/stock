# 使用Python官方镜像作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置Python环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBUG=0 \
    DJANGO_SETTINGS_MODULE=stock.settings

# 安装系统依赖并安装Python依赖
COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# 复制项目文件并设置静态文件
COPY . .
RUN mkdir -p /app/staticfiles && \
    chmod 755 /app/staticfiles && \
    python manage.py collectstatic --noinput

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["gunicorn", "stock.wsgi:application", "--bind", "0.0.0.0:8000"]