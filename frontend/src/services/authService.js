import request from './api'

// 登录接口
export function login(username, password) {
  return request({
    url: '/api/accounts/login/',
    method: 'post',
    data: { username, password }
  })
}

// 注册接口
export function register(username, email, password, password2) {
  return request({
    url: '/api/accounts/register/',
    method: 'post',
    data: { username, email, password, password2 }
  })
}

// 获取用户信息接口（修复路径）
export function getUserInfo() {
  return request({
    url: '/api/accounts/me/',  // 已修复为正确路径
    method: 'get'
  })
}