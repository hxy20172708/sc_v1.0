<template>
  <div class="home-container">
    <el-container>
      <el-header class="header">
        <div class="logo">服务器管理系统</div>
        <div class="user-info">
          <span>{{ user && user.username }}</span>
          <el-button type="text" @click="handleLogout">退出登录</el-button>
        </div>
      </el-header>
      <el-container>
        <el-aside width="200px" class="aside">
          <el-menu
            default-active="/servers"
            class="el-menu-vertical-demo"
            router
          >
            <el-menu-item index="/servers">
              <i class="el-icon-server"></i>
              <span slot="title">服务器管理</span>
            </el-menu-item>
            <el-menu-item index="/rooms">
              <i class="el-icon-office-building"></i>
              <span slot="title">机房管理</span>
            </el-menu-item>
            <el-menu-item index="/tasks">
              <i class="el-icon-s-order"></i>
              <span slot="title">任务管理</span>
            </el-menu-item>
            <el-menu-item index="/environments">
              <i class="el-icon-layout"></i>
              <span slot="title">环境管理</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main class="main">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'Home',
  computed: {
    ...mapState(['user'])
  },
  created() {
    this.$store.dispatch('GetUserInfo').catch(() => {
      this.$store.dispatch('Logout').then(() => {
        this.$router.push('/login')
      })
    })
  },
  methods: {
    ...mapActions(['Logout']),
    handleLogout() {
      this.Logout().then(() => {
        this.$router.push('/login')
        this.$message.success('退出登录成功')
      })
    }
  }
}
</script>

<style scoped>
.home-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background-color: #20a0ff;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.logo {
  font-size: 20px;
  font-weight: bold;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-info span {
  margin-right: 10px;
}

.aside {
  background-color: #333744;
}

.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}

.el-menu {
  background-color: #333744;
  color: white;
}

.el-menu-item {
  color: rgba(255, 255, 255, 0.7);
}

.el-menu-item.is-active {
  background-color: #1890ff;
  color: white;
}

.main {
  padding: 20px;
  background-color: #f5f7fa;
  flex: 1;
  overflow-y: auto;
}
</style>