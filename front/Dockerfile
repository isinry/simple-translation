# 指定基础镜像
FROM node:14.17.0 as build-stage

# 设置工作目录
WORKDIR /app

# 复制 package.json 和 yarn.lock 到容器中
COPY package*.json yarn.lock ./

# 安装依赖项
RUN yarn install

# 复制所有文件到容器中
COPY . .

# 执行 Vue 项目的打包命令
RUN yarn build

# 构建生产环境镜像
FROM nginx:1.21.1

# 将打包生成的静态文件复制到 Nginx 的默认静态文件目录
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 暴露 Nginx 默认的 HTTP 端口
EXPOSE 80

# 启动 Nginx 服务器
CMD ["nginx", "-g", "daemon off;"]
