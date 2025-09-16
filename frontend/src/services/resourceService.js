import request from './api'  // 引入配置好的axios实例

// 机房相关API
export function getRooms(params) {
  return request({
    url: '/api/resources/rooms/',  // 后端机房列表接口
    method: 'get',
    params  // 分页、搜索参数
  })
}

export function createRoom(data) {
  return request({
    url: '/api/resources/rooms/',  // 后端创建机房接口
    method: 'post',
    data  // 机房信息（name, location, description等）
  })
}

export function updateRoom(id, data) {
  return request({
    url: `/api/resources/rooms/${id}/`,  // 后端更新机房接口
    method: 'put',
    data  // 要更新的机房信息
  })
}

export function deleteRoom(id) {
  return request({
    url: `/api/resources/rooms/${id}/`,  // 后端删除机房接口
    method: 'delete'
  })
}

// 服务器相关API
export function getServers(params) {
  return request({
    url: '/api/resources/servers/',  // 后端服务器列表接口
    method: 'get',
    params  // 分页、搜索、机房筛选等参数
  })
}

export function createServer(data) {
  return request({
    url: '/api/resources/servers/',  // 后端创建服务器接口
    method: 'post',
    data  // 服务器信息（name, ip_address, room等）
  })
}

export function updateServer(id, data) {
  return request({
    url: `/api/resources/servers/${id}/`,  // 后端更新服务器接口
    method: 'put',
    data  // 要更新的服务器信息
  })
}

export function deleteServer(id) {
  return request({
    url: `/api/resources/servers/${id}/`,  // 后端删除服务器接口
    method: 'delete'
  })
}

export function checkServerStatus(id) {
  return request({
    url: `/api/resources/servers/${id}/check_status/`,  // 后端检查服务器状态接口
    method: 'get'
  })
}

export function getServerConfig(id) {
  return request({
    url: `/api/resources/servers/${id}/config/`,  // 后端获取服务器配置接口
    method: 'get'
  })
}
