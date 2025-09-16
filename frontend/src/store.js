import Vue from 'vue'
import Vuex from 'vuex'
import { login, register, getUserInfo } from './services/authService'
import { getToken, setToken, removeToken } from './utils/auth'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    token: getToken(),
    user: null,
    isAuthenticated: false
  },
  mutations: {
    SET_TOKEN: (state, token) => {
      state.token = token
      state.isAuthenticated = !!token
    },
    SET_USER: (state, user) => {
      state.user = user
    },
    LOGOUT: (state) => {
      state.token = null
      state.user = null
      state.isAuthenticated = false
      removeToken()
    }
  },
  actions: {
    // 登录
    Login({ commit }, userInfo) {
      const { username, password } = userInfo
      return new Promise((resolve, reject) => {
        login(username, password).then(response => {
          // 注意：api.js 已返回 response.data，直接从 response 取数据
          const { access } = response
          setToken(access)
          commit('SET_TOKEN', access)
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 注册（移除空对象参数，解决 no-empty-pattern 错误）
    Register(userInfo) {  // 仅保留 userInfo 参数
      const { username, email, password, password2 } = userInfo
      return new Promise((resolve, reject) => {
        register(username, email, password, password2).then(() => {
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 获取用户信息
    GetUserInfo({ commit }) {
      return new Promise((resolve, reject) => {
        getUserInfo().then(response => {
          commit('SET_USER', response.data)
          resolve(response)
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 退出登录
    Logout({ commit }) {
      return new Promise(resolve => {
        commit('LOGOUT')
        resolve()
      })
    }
  },
  modules: {
  }
})