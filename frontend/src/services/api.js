import axios from 'axios';

// 创建axios实例
const request = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL || '/',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    // 从本地存储获取token
    const token = localStorage.getItem('token');
    // 如果token存在，添加到请求头
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    // 处理请求错误
    console.error('请求错误:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    // 直接返回响应数据部分
    return response.data;
  },
  (error) => {
    // 处理响应错误
    console.error('响应错误:', error);

    // 未授权，可能是token过期
    if (error.response && error.response.status === 401) {
      // 清除本地存储的token
      localStorage.removeItem('token');
      // 跳转到登录页
      window.location.href = '/login';
    }

    return Promise.reject(error);
  }
);

// 账户相关API
export const login = (credentials) => {
  return request.post('/accounts/login/', credentials);
};

export const getCurrentUser = () => {
  return request.get('/accounts/me/');
};

// 服务器相关API
export const getServers = (params) => {
  return request.get('/resources/servers/', { params });
};

export const getServer = (id) => {
  return request.get(`/resources/servers/${id}/`);
};

export const createServer = (data) => {
  return request.post('/resources/servers/', data);
};

export const updateServer = (id, data) => {
  return request.put(`/resources/servers/${id}/`, data);
};

export const deleteServer = (id) => {
  return request.delete(`/resources/servers/${id}/`);
};

// 机房相关API
export const getRooms = (params) => {
  return request.get('/resources/rooms/', { params });
};

export const getRoom = (id) => {
  return request.get(`/resources/rooms/${id}/`);
};

export const createRoom = (data) => {
  return request.post('/resources/rooms/', data);
};

export const updateRoom = (id, data) => {
  return request.put(`/resources/rooms/${id}/`, data);
};

export const deleteRoom = (id) => {
  return request.delete(`/resources/rooms/${id}/`);
};

// 任务相关API
export const getTasks = (params) => {
  return request.get('/tasks/', { params });
};

export const createTask = (data) => {
  return request.post('/tasks/', data);
};

export const cancelTask = (id) => {
  return request.post(`/tasks/${id}/cancel/`);
};

// 环境相关API
export const getEnvironments = (params) => {
  return request.get('/environments/', { params });
};

export const createEnvironment = (data) => {
  return request.post('/environments/', data);
};

export const updateEnvironment = (id, data) => {
  return request.put(`/environments/${id}/`, data);
};

export const deleteEnvironment = (id) => {
  return request.delete(`/environments/${id}/`);
};

export default request;
