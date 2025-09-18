// sc_v1.0/frontend/src/services/environmentService.js
import request from './api'  // 引入配置好的axios实例

// 环境相关API
export function getEnvironments(params) {
  return request({
    url: '/api/environments/',  // 正确的API路径（包含/api前缀）
    method: 'get',
    params  // 分页、搜索等参数
  })
}

export function createEnvironment(data) {
  return request({
    url: '/api/environments/',
    method: 'post',
    data  // 环境信息（name, description, server_ids等）
  })
}

export function updateEnvironment(id, data) {
  return request({
    url: `/api/environments/${id}/`,
    method: 'put',
    data
  })
}

export function deleteEnvironment(id) {
  return request({
    url: `/api/environments/${id}/`,
    method: 'delete'
  })
}