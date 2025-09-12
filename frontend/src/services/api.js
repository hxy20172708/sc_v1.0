import axios from 'axios'
import { getToken, removeToken } from '../utils/auth'
import router from '../router'

const service = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json;charset=utf-8'
  }
})

service.interceptors.request.use(
  (config) => {
    const token = getToken()
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    console.error('【请求发送失败】', error.message || '未知请求错误')
    return Promise.reject(error)
  }
)

service.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    const errorResponse = error.response;
    const errorDetail = errorResponse && errorResponse.data && errorResponse.data.detail;
    const errorMsg = errorDetail || error.message || '未知响应错误';

    if (errorResponse && errorResponse.status === 401) {
      removeToken()
      router.push({
        path: '/login',
        query: { redirect: router.currentRoute.fullPath }
      })
      window.alert('登录已过期或未登录，请重新登录')
    }

    const statusCode = errorResponse && errorResponse.status;
    console.error(`【响应错误】[${statusCode || '无状态码'}]`, errorMsg)
    return Promise.reject({
      status: statusCode,
      message: errorMsg
    })
  }
)

export default service
    