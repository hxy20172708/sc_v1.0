<template>
  <div class="environments-page">
    <el-card>
      <div slot="header" class="page-header">
        <h2>环境管理</h2>
        <el-button type="primary" @click="showAddEnvironmentDialog">添加环境</el-button>
      </div>

      <div class="search-bar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索环境名称或描述"
          prefix-icon="el-icon-search"
          style="width: 300px;"
          @input="handleSearch"
        ></el-input>
      </div>

      <el-table
        :data="filteredEnvironments"
        border
        style="width: 100%; margin-top: 20px;"
      >
        <el-table-column
          prop="name"
          label="环境名称"
          width="180"
        ></el-table-column>
        <el-table-column
          prop="description"
          label="描述"
        ></el-table-column>
        <el-table-column
          prop="created_at"
          label="创建时间"
          width="180"
        ></el-table-column>
        <el-table-column
          label="服务器数量"
          width="120"
        >
          <template slot-scope="scope">
            <el-button
              type="text"
              @click="showEnvironmentServers(scope.row.id)"
            >
              {{ scope.row.servers.length }}台
            </el-button>
          </template>
        </el-table-column>
        <el-table-column
          label="操作"
          width="200"
        >
          <template slot-scope="scope">
            <el-button
              type="text"
              @click="showEditEnvironmentDialog(scope.row)"
            >
              编辑
            </el-button>
            <el-button
              type="text"
              style="color: #f56c6c;"
              @click="handleDeleteEnvironment(scope.row.id)"
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
        :total="totalEnvironments"
        style="margin-top: 20px; text-align: right;"
      ></el-pagination>
    </el-card>

    <!-- 添加/编辑环境对话框 -->
    <el-dialog
      :title="environmentDialogTitle"
      :visible.sync="environmentDialogVisible"
      width="500px"
    >
      <el-form
        ref="environmentForm"
        :model="environmentForm"
        :rules="environmentRules"
        label-width="100px"
      >
        <el-form-item label="环境名称" prop="name">
          <el-input v-model="environmentForm.name"></el-input>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input type="textarea" v-model="environmentForm.description" rows="4"></el-input>
        </el-form-item>
        <el-form-item label="关联服务器" prop="server_ids">
          <el-select
            v-model="environmentForm.server_ids"
            multiple
            placeholder="请选择服务器"
            style="width: 100%;"
          >
            <el-option
              v-for="server in servers"
              :key="server.id"
              :label="server.name + ' (' + server.ip_address + ')'"
              :value="server.id"
            ></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="environmentDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveEnvironment">保存</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getEnvironments, createEnvironment, updateEnvironment, deleteEnvironment } from '../services/environmentService'
import { getServers } from '../services/resourceService'

export default {
  name: 'EnvironmentsPage',
  data() {
    return {
      environments: [],
      filteredEnvironments: [],
      servers: [],
      searchQuery: '',
      currentPage: 1,
      pageSize: 10,
      totalEnvironments: 0,

      environmentDialogVisible: false,
      environmentDialogTitle: '添加环境',
      currentEnvironmentId: null,
      environmentForm: {
        name: '',
        description: '',
        server_ids: []
      },
      environmentRules: {
        name: [
          { required: true, message: '请输入环境名称', trigger: 'blur' }
        ],
        server_ids: [
          { type: 'array', min: 1, message: '至少选择一台服务器', trigger: 'change' }
        ]
      }
    }
  },
  created() {
    this.loadEnvironments()
    this.loadServers()
  },
  methods: {
    loadEnvironments() {
      const params = {
        page: this.currentPage,
        page_size: this.pageSize
      }
      if (this.searchQuery) {
        params.search = this.searchQuery
      }

      getEnvironments(params).then(response => {
        this.environments = response.results
        this.totalEnvironments = response.count
        this.filteredEnvironments = this.environments
      }).catch(error => {
        const errorDetail = error.response && error.response.data && error.response.data.detail;
        this.$message.error('获取环境列表失败: ' + (errorDetail || error.message));
      });
    },

    loadServers() {
      getServers().then(response => {
        this.servers = response.data.results
      }).catch(error => {
        const errorDetail = error.response && error.response.data && error.response.data.detail;
        this.$message.error('获取服务器列表失败: ' + (errorDetail || error.message));
      });
    },

    handleSearch() {
      this.currentPage = 1
      this.loadEnvironments()
    },

    handleSizeChange(val) {
      this.pageSize = val
      this.currentPage = 1
      this.loadEnvironments()
    },

    handleCurrentChange(val) {
      this.currentPage = val
      this.loadEnvironments()
    },

    showAddEnvironmentDialog() {
      this.environmentDialogTitle = '添加环境'
      this.currentEnvironmentId = null
      this.environmentForm = {
        name: '',
        description: '',
        server_ids: []
      }
      this.environmentDialogVisible = true
    },

    showEditEnvironmentDialog(environment) {
      this.environmentDialogTitle = '编辑环境'
      this.currentEnvironmentId = environment.id
      this.environmentForm = {
        name: environment.name,
        description: environment.description,
        server_ids: environment.servers.map(server => server.id)
      }
      this.environmentDialogVisible = true
    },

    saveEnvironment() {
      this.$refs.environmentForm.validate(valid => {
        if (valid) {
          if (this.currentEnvironmentId) {
            updateEnvironment(this.currentEnvironmentId, this.environmentForm).then(() => {
              this.$message.success('环境更新成功')
              this.environmentDialogVisible = false
              this.loadEnvironments()
            }).catch(error => {
              const errorDetail = error.response && error.response.data && error.response.data.detail;
              this.$message.error('环境更新失败: ' + (errorDetail || error.message));
            });
          } else {
            createEnvironment(this.environmentForm).then(() => {
              this.$message.success('环境添加成功')
              this.environmentDialogVisible = false
              this.loadEnvironments()
            }).catch(error => {
              const errorDetail = error.response && error.response.data && error.response.data.detail;
              this.$message.error('环境添加失败: ' + (errorDetail || error.message));
            });
          }
        }
      })
    },

    handleDeleteEnvironment(id) {
      this.$confirm('确定要删除这个环境吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteEnvironment(id).then(() => {
          this.$message.success('删除成功')
          this.loadEnvironments()
        }).catch(error => {
          const errorDetail = error.response && error.response.data && error.response.data.detail;
          this.$message.error('删除失败: ' + (errorDetail || error.message));
        });
      }).catch(() => {
        this.$message.info('已取消删除')
      })
    },

    showEnvironmentServers(environmentId) {
      this.$router.push({
        path: '/servers',
        query: { environment_id: environmentId }
      })
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
  margin-top: 10px;
}
</style>