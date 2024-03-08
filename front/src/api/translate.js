import axios from 'axios'

const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:5001',
    // 其他配置项
});

function getCsrfToken() {
    return apiClient.get('/csrf_token').then(res => {
        return res.data
    })
}

function translate(data, fn) {
    let csrf_token = getCsrfToken()
    csrf_token.then(token => {
        // 设置header
        apiClient.defaults.headers.common['X-CSRF-Token'] = token
        fn(apiClient.post('/translate', data))
    })
}

export default {
    translate
}