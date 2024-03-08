from flask import Flask, request, render_template, abort, session, Response
from flask_cors import CORS
import requests
import json
import os
import hmac
import hashlib
import secrets


# 创建Flask应用程序实例
app = Flask(__name__)
CORS(app)
# 设置session的密钥
app.secret_key = secrets.token_hex(16)

# 翻译接口
api_url = os.getenv('API_URL', 'https://api.deeplx.org/translate')
print(f'当前API_URL地址: {api_url}')

# 前端站点端口
site_domain = os.getenv('SITE_DOMAIN', 'http://front')

@app.before_request
def check_origin():
    allowed_origins = ['http://translation.isinry.cn', 'http://localhost:8080']
    origin = request.headers.get('Origin')
    print(f'当前请求的Origin: {origin}')
    # if origin not in allowed_origins:
    #     abort(403)  # 返回 403 Forbidden 错误


# 生成csrf_token
def generate_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
    return session['csrf_token']

# 验证csrf
def check_csrf_token():
    print(111)
    token = request.headers.get('X-CSRF-Token')
    csrf_token = session.get('csrf_token')
    print('token对比：', token, csrf_token)
    if not token or token != csrf_token:
        abort(403)

# 获取csrf
@app.route('/csrf_token', methods=['GET'])
def get_token():
    csrf_token = generate_csrf_token()
    return csrf_token


# 定义路由和视图函数
@app.route('/translate', methods=['POST'])
def translate():
    check_csrf_token()
    text = request.json.get('text')
    target_lang = request.json.get('target_lang')

    payload = json.dumps({
        "text": text,
        "source_lang": "auto",
        "target_lang": target_lang
    })
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    response = requests.request("POST", api_url, headers=headers, data=payload)
    print("翻译结果：" + response.text)
    return response.json()


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'OPTION'])
def proxy(path):
    # site_domain = 'http://localhost:8080'
    target_url = site_domain + '/' + path  # 设置目标服务器的 URL
    print(target_url)

    # 获取请求的方法、头部和主体
    method = request.method
    body = request.get_data()

    # 发送请求到目标服务器
    response = requests.request(method, target_url, headers=request.headers, data=body)
    
    # 构建响应对象
    return Response(response.content, content_type=response.headers['Content-Type'], status=response.status_code)

# 启动应用程序
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
