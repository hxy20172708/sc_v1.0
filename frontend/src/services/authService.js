// src/services/authService.js
import request from './api'  // 这行必须正确，指向刚创建的 api.js

// 以下是原本的认证 API 逻辑（保持不变）
export function login(username, password) {
  return request({
    url: '/api/accounts/login/',
    method: 'post',
    data: { username, password }
  })
}

export function register(username, email, password, password2) {
  return request({
    url: '/api/accounts/register/',
    method: 'post',
    data: { username, email, password, password2 }
  })
}

export function getUserInfo() {
  return request({
    url: '/api/accounts/me/',
    method: 'get'
  })
}