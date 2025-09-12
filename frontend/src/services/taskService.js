import request from './api'  // 引入配置好的axios实例

// 任务相关API
export function getTasks(params) {
  return request({
    url: '/tasks/',  // 后端任务列表接口
    method: 'get',
    params  // 分页、搜索、状态筛选等参数
  })
}

export function createTask(data) {
  return request({
    url: '/tasks/',  // 后端创建任务接口
    method: 'post',
    data  // 任务信息（name, command, server_ids, schedule等）
  })
}

export function updateTask(id, data) {
  return request({
    url: `/tasks/${id}/`,  // 后端更新任务接口
    method: 'put',
    data  // 要更新的任务信息
  })
}

export function deleteTask(id) {
  return request({
    url: `/tasks/${id}/`,  // 后端删除任务接口
    method: 'delete'
  })
}

export function executeTaskNow(id) {
  return request({
    url: `/tasks/${id}/execute/`,  // 后端立即执行任务接口
    method: 'post'
  })
}

export function getTaskResults(params) {
  return request({
    url: '/task-results/',  // 后端任务执行结果接口
    method: 'get',
    params  // 任务ID、分页等参数
  })
}
