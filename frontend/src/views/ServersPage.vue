<template>
  <div class="servers-page">
    <el-card>
      <div slot="header" class="page-header">
        <h2>服务器管理</h2>
        <el-button type="primary" @click="showAddServerDialog">添加服务器</el-button>
      </div>
      
      <div class="search-bar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索服务器名称、IP或操作系统"
          prefix-icon="el-icon-search"
          style="width: 300px;"
          @input="handleSearch"
        ></el-input>
        <el-select
          v-model="selectedRoom"
          placeholder="选择机房"
          style="width: 200px; margin-left: 10px;"
          @change="handleRoomChange"
        >
          <el-option label="全部机房" value=""></el-option>
          <el-option
            v-for="room in rooms"
            :key="room.id"
            :label="room.name"
            :value="room.id"
          ></el-option>
        </el-select>
      </div>
      
      <el-table
        :data="filteredServers"
        border
        style="width: 100%; margin-top: 20px;"
      >
        <el-table-column
          prop="name"
          label="服务器名称"
          width="150"
        ></el-table-column>
        <el-table-column
          prop="ip_address"
          label="IP地址"
          width="150"
        ></el-table-column>
        <el-table-column
          prop="hostname"
          label="主机名"
          width="180"
        ></el-table-column>
        <el-table-column
          prop="room_name"
          label="所属机房"
          width="150"
        ></el-table-column>
        <el-table-column
          prop="status"
          label="状态"
          width="120"
        >
          <template slot-scope="scope">
            <el-tag
              :type="scope.row.status === 'online' ? 'success' : (scope.row.status === 'offline' ? 'danger' : 'warning')"
            >
              {{ scope.row.status === 'online' ? '在线' : (scope.row.status === 'offline' ? '离线' : '维护中') }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="os"
          label="操作系统"
          width="150"
        ></el-table-column>
        <el-table-column
          prop="cpu"
          label="CPU"
          width="200"
        ></el-table-column>
        <el-table-column
          prop="memory"
          label="内存"
          width="100"
        ></el-table-column>
        <el-table-column
          label="操作"
          width="250"
        >
          <template slot-scope="scope">
            <el-button
              type="text"
              @click="checkServerStatus(scope.row.id)"
            >
              检查状态
            </el-button>
            <el-button
              type="text"
              @click="getServerConfig(scope.row.id)"
            >
              获取配置
            </el-button>
            <el-button
              type="text"
              @click="showEditServerDialog(scope.row)"
            >
              编辑
            </el-button>
            <el-button
              type="text"
              style="color: #f56c6c;"
              @click="handleDeleteServer(scope.row.id)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 50]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="totalServers"
        style="margin-top: 20px; text-align: right;"
      ></el-pagination>
    </el-card>
    
    <!-- 添加/编辑服务器对话框 -->
    <el-dialog
      :title="serverDialogTitle"
      :visible.sync="serverDialogVisible"
      width="600px"
    >
      <el-form
        ref="serverForm"
        :model="serverForm"
        :rules="serverRules"
        label-width="120px"
      >
        <el-form-item label="服务器名称" prop="name">
          <el-input v-model="serverForm.name"></el-input>
        </el-form-item>
        <el-form-item label="IP地址" prop="ip_address">
          <el-input v-model="serverForm.ip_address"></el-input>
        </el-form-item>
        <el-form-item label="主机名" prop="hostname">
          <el-input v-model="serverForm.hostname"></el-input>
        </el-form-item>
        <el-form-item label="所属机房" prop="room">
          <el-select
            v-model="serverForm.room"
            placeholder="请选择机房"
          >
            <el-option
              v-for="room in rooms"
              :key="room.id"
              :label="room.name"
              :value="room.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="serverForm.status">
            <el-option label="在线" value="online"></el-option>
            <el-option label="离线" value="offline"></el-option>
            <el-option label="维护中" value="maintenance"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="操作系统" prop="os">
          <el-input v-model="serverForm.os"></el-input>
        </el-form-item>
        <el-form-item label="CPU" prop="cpu">
          <el-input v-model="serverForm.cpu"></el-input>
        </el-form-item>
        <el-form-item label="内存" prop="memory">
          <el-input v-model="serverForm.memory"></el-input>
        </el-form-item>
        <el-form-item label="磁盘" prop="disk">
          <el-input v-model="serverForm.disk"></el-input>
        </el-form-item>
        <el-form-item label="网络速度" prop="network_speed">
          <el-input v-model="serverForm.network_speed"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="serverDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveServer">保存</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import {
  getServers,
  createServer,
  updateServer,
  deleteServer,
  checkServerStatus,
  getServerConfig,
  getRooms
} from '../services/resourceService'

export default {
  name: 'ServersPage',
  data() {
    return {
      servers: [],
      filteredServers: [],
      rooms: [],
      searchQuery: '',
      selectedRoom: '',
      currentPage: 1,
      pageSize: 10,
      totalServers: 0,
      
      serverDialogVisible: false,
      serverDialogTitle: '添加服务器',
      currentServerId: null,
      serverForm: {
        name: '',
        ip_address: '',
        hostname: '',
        room: '',
        status: 'offline',
        os: '',
        cpu: '',
        memory: '',
        disk: '',
        network_speed: ''
      },
      serverRules: {
        name: [
          { required: true, message: '请输入服务器名称', trigger: 'blur' }
        ],
        ip_address: [
          { required: true, message: '请输入IP地址', trigger: 'blur' },
          { type: 'ip', message: '请输入正确的IP地址', trigger: 'blur' }
        ],
        room: [
          { required: true, message: '请选择所属机房', trigger: 'change' }
        ]
      }
    }
  },
  created() {
    this.loadRooms()
    this.loadServers()
  },
  methods: {
    loadRooms() {
      getRooms().then(response => {
        this.rooms = response.data
      }).catch(error => {
        const errorDetail = error.response && error.response.data && error.response.data.detail;
        this.$message.error('获取机房列表失败: ' + (errorDetail || error.message));
      });
    },
    loadServers() {
      const params = {
        page: this.currentPage,
        page_size: this.pageSize
      }
      if (this.selectedRoom) {
        params.room = this.selectedRoom
      }
      if (this.searchQuery) {
        params.search = this.searchQuery
      }
      
      getServers(params).then(response => {
        this.servers = response.data.results
        this.totalServers = response.data.count
        this.filteredServers = this.servers
      }).catch(error => {
        const errorDetail = error.response && error.response.data && error.response.data.detail;
        this.$message.error('获取服务器列表失败: ' + (errorDetail || error.message));
      });
    },
    handleSearch() {
      this.currentPage = 1
      this.loadServers()
    },
    handleRoomChange() {
      this.currentPage = 1
      this.loadServers()
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.currentPage = 1
      this.loadServers()
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.loadServers()
    },
    showAddServerDialog() {
      this.serverDialogTitle = '添加服务器'
      this.currentServerId = null
      this.serverForm = {
        name: '',
        ip_address: '',
        hostname: '',
        room: '',
        status: 'offline',
        os: '',
        cpu: '',
        memory: '',
        disk: '',
        network_speed: ''
      }
      this.serverDialogVisible = true
    },
    showEditServerDialog(server) {
      this.serverDialogTitle = '编辑服务器'
      this.currentServerId = server.id
      this.serverForm = {
        name: server.name,
        ip_address: server.ip_address,
        hostname: server.hostname,
        room: server.room,
        status: server.status,
        os: server.os,
        cpu: server.cpu,
        memory: server.memory,
        disk: server.disk,
        network_speed: server.network_speed
      }
      this.serverDialogVisible = true
    },
    saveServer() {
      this.$refs.serverForm.validate(valid => {
        if (valid) {
          if (this.currentServerId) {
            updateServer(this.currentServerId, this.serverForm).then(() => {
              this.$message.success('服务器更新成功')
              this.serverDialogVisible = false
              this.loadServers()
            }).catch(error => {
              const errorDetail = error.response && error.response.data && error.response.data.detail;
              this.$message.error('服务器更新失败: ' + (errorDetail || error.message));
            });
          } else {
            createServer(this.serverForm).then(() => {
              this.$message.success('服务器添加成功')
              this.serverDialogVisible = false
              this.loadServers()
            }).catch(error => {
              const errorDetail = error.response && error.response.data && error.response.data.detail;
              this.$message.error('服务器添加失败: ' + (errorDetail || error.message));
            });
          }
        }
      })
    },
    handleDeleteServer(id) {
      this.$confirm('确定要删除这个服务器吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteServer(id).then(() => {
          this.$message.success('删除成功')
          this.loadServers()
        }).catch(error => {
          const errorDetail = error.response && error.response.data && error.response.data.detail;
          this.$message.error('删除失败: ' + (errorDetail || error.message));
        });
      }).catch(() => {
        this.$message.info('已取消删除')
      })
    },
    checkServerStatus(id) {
      const loading = this.$loading({
        lock: true,
        text: '正在检查服务器状态...',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      })
      
      checkServerStatus(id).then(response => {
        loading.close()
        this.$message.success(`服务器状态: ${response.data.status === 'online' ? '在线' : '离线'}`)
        this.loadServers()
      }).catch(error => {
        loading.close()
        const errorDetail = error.response && error.response.data && error.response.data.detail;
        this.$message.error('检查服务器状态失败: ' + (errorDetail || error.message));
      });
    },
    getServerConfig(id) {
      const loading = this.$loading({
        lock: true,
        text: '正在获取服务器配置...',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      })
      
      getServerConfig(id).then(() => {
        loading.close()
        this.$message.success('服务器配置获取成功')
        this.loadServers()
      }).catch(error => {
        loading.close()
        const errorDetail = error.response && error.response.data && error.response.data.detail;
        this.$message.error('获取服务器配置失败: ' + (errorDetail || error.message));
      });
    }
  }
}
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-bar {
  display: flex;
  margin-top: 10px;
}
</style>
    