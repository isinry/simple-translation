# 指定基础镜像
FROM python:3.10.5

# 设置工作目录
WORKDIR /app

# 将当前目录下的文件复制到容器的 /app 目录中
COPY . /app

# 安装依赖项
RUN pip install --no-cache-dir -r requirements.txt

ENV API_URL=https://api.deeplx.org/translate
ENV SITE_PORT=8080

# 暴露应用程序的端口
EXPOSE 5001


# 运行应用程序
CMD [ "python", "app.py" ]
