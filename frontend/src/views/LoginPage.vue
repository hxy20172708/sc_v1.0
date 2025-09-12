<template>
  <div class="login-container">
    <el-card class="login-card">
      <div slot="header" class="login-header">
        <h2>服务器管理系统</h2>
      </div>
      <el-tabs v-model="activeTab" type="card">
        <el-tab-pane label="登录" name="login">
          <el-form ref="loginForm" :model="loginForm" :rules="loginRules" label-width="80px" class="login-form">
            <el-form-item label="用户名" prop="username">
              <el-input v-model="loginForm.username" placeholder="请输入用户名"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input type="password" v-model="loginForm.password" placeholder="请输入密码"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleLogin" class="login-btn">登录</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="注册" name="register">
          <el-form ref="registerForm" :model="registerForm" :rules="registerRules" label-width="80px" class="register-form">
            <el-form-item label="用户名" prop="username">
              <el-input v-model="registerForm.username" placeholder="请输入用户名"></el-input>
            </el-form-item>
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="registerForm.email" placeholder="请输入邮箱"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input type="password" v-model="registerForm.password" placeholder="请输入密码"></el-input>
            </el-form-item>
            <el-form-item label="确认密码" prop="password2">
              <el-input type="password" v-model="registerForm.password2" placeholder="请再次输入密码"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleRegister" class="register-btn">注册</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'LoginPage',
  data() {
    const validatePassword2 = (rule, value, callback) => {
      if (value !== this.registerForm.password) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    }
    return {
      activeTab: 'login',
      loginForm: {
        username: '',
        password: ''
      },
      registerForm: {
        username: '',
        email: '',
        password: '',
        password2: ''
      },
      loginRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      },
      registerRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱格式', trigger: ['blur', 'change'] }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
        ],
        password2: [
          { required: true, message: '请再次输入密码', trigger: 'blur' },
          { validator: validatePassword2, trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    ...mapActions(['Login', 'Register']),
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.Login(this.loginForm).then(() => {
            this.$router.push('/servers')
            this.$message.success('登录成功')
          }).catch(error => {
            let errorMsg = '登录失败';
            if (error.response) {
              if (error.response.data) {
                if (error.response.data.detail) {
                  errorMsg = error.response.data.detail;
                } else {
                  for (const key in error.response.data) {
                    errorMsg = error.response.data[key].join(', ');
                    break;
                  }
                }
              }
            }
            this.$message.error(errorMsg);
          })
        }
      })
    },
    handleRegister() {
      this.$refs.registerForm.validate(valid => {
        if (valid) {
          this.Register(this.registerForm).then(() => {
            this.$message.success('注册成功，请登录')
            this.activeTab = 'login'
          }).catch(error => {
            let errorMsg = '注册失败';
            if (error.response && error.response.data) {
              for (const key in error.response.data) {
                errorMsg = error.response.data[key].join(', ');
                break;
              }
            }
            this.$message.error(errorMsg);
          })
        }
      })
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f7fa;
}

.login-card {
  width: 400px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.login-header {
  text-align: center;
}

.login-form, .register-form {
  margin-top: 20px;
}

.login-btn, .register-btn {
  width: 100%;
}
</style>
    