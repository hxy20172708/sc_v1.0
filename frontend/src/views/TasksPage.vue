<template>
  <div class="tasks-page">
    <el-card>
      <div slot="header" class="page-header">
        <h2>任务管理</h2>
        <el-button type="primary" @click="showAddTaskDialog">添加定时任务</el-button>
      </div>

      <div class="search-bar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索任务名称或命令"
          prefix-icon="el-icon-search"
          style="width: 300px;"
          @input="handleSearch"
        ></el-input>
        <el-select
          v-model="selectedStatus"
          placeholder="选择任务状态"
          style="width: 180px; margin-left: 10px;"
          @change="handleStatusChange"
        >
          <el-option label="全部状态" value=""></el-option>
          <el-option label="待执行" value="pending"></el-option>
          <el-option label="执行中" value="running"></el-option>
          <el-option label="已完成" value="completed"></el-option>
          <el-option label="失败" value="failed"></el-option>
        </el-select>
      </div>

      <el-table
        :data="filteredTasks"
        border
        style="width: 100%; margin-top: 20px;"
      >
        <el-table-column
          prop="name"
          label="任务名称"
          width="180"
        ></el-table-column>
        <el-table-column
          prop="command"
          label="执行命令"
          width="300"
        ></el-table-column>
        <el-table-column
          label="目标服务器"
          width="200"
        >
          <template slot-scope="scope">
            <el-tag v-for="(server, index) in scope.row.server_list" :key="index" type="info" style="margin-right: 5px;">
              {{ server.name }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="schedule"
          label="Cron表达式"
          width="200"
        ></el-table-column>
        <el-table-column
          prop="status"
          label="状态"
          width="120"
        >
          <template slot-scope="scope">
            <el-tag
              :type="scope.row.status === 'completed' ? 'success' : (scope.row.status === 'failed' ? 'danger' : (scope.row.status === 'running' ? 'warning' : 'info'))"
            >
              {{ scope.row.status === 'pending' ? '待执行' : (scope.row.status === 'running' ? '执行中' : (scope.row.status === 'completed' ? '已完成' : '失败')) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="last_execution"
          label="上次执行时间"
          width="180"
        ></el-table-column>
        <el-table-column
          prop="next_execution"
          label="下次执行时间"
          width="180"
        ></el-table-column>
        <el-table-column
          label="操作"
          width="250"
        >
          <template slot-scope="scope">
            <el-button
              type="text"
              @click="executeTaskNow(scope.row.id)"
            >
              立即执行
            </el-button>
            <el-button
              type="text"
              @click="showTaskResults(scope.row.id)"
            >
              执行结果
            </el-button>
            <el-button
              type="text"
              @click="showEditTaskDialog(scope.row)"
            >
              编辑
            </el-button>
            <el-button
              type="text"
              style="color: #f56c6c;"
              @click="handleDeleteTask(scope.row.id)"
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
        :total="totalTasks"
        style="margin-top: 20px; text-align: right;"
      ></el-pagination>
    </el-card>

    <!-- 添加/编辑任务对话框 -->
    <el-dialog
      :title="taskDialogTitle"
      :visible.sync="taskDialogVisible"
      width="700px"
    >
      <el-form
        ref="taskForm"
        :model="taskForm"
        :rules="taskRules"
        label-width="120px"
      >
        <el-form-item label="任务名称" prop="name">
          <el-input v-model="taskForm.name"></el-input>
        </el-form-item>
        <el-form-item label="执行命令" prop="command">
          <el-input type="textarea" v-model="taskForm.command" rows="3"></el-input>
        </el-form-item>
        <el-form-item label="目标服务器" prop="server_ids">
          <el-select
            v-model="taskForm.server_ids"
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
        <el-form-item label="Cron表达式" prop="schedule">
          <el-input
            v-model="taskForm.schedule"
            placeholder="格式：分 时 日 月 周，例如：0 0 * * * 表示每天凌晨执行"
          ></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="taskDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveTask">保存</el-button>
      </div>
    </el-dialog>

    <!-- 任务执行结果对话框 -->
    <el-dialog
      title="任务执行结果"
      :visible.sync="resultDialogVisible"
      width="800px"
    >
      <el-table
        :data="taskResults"
        border
        style="width: 100%;"
      >
        <el-table-column
          prop="server_name"
          label="服务器"
          width="180"
        ></el-table-column>
        <el-table-column
          prop="executed_at"
          label="执行时间"
          width="180"
        ></el-table-column>
        <el-table-column
          prop="exit_code"
          label="退出码"
          width="100"
        >
          <template slot-scope="scope">
            <el-tag :type="scope.row.exit_code === 0 ? 'success' : 'danger'">
              {{ scope.row.exit_code }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="output"
          label="输出结果"
        >
          <template slot-scope="scope">
            <el-button type="text" @click="showOutputDetail(scope.row.output)">查看详情</el-button>
          </template>
        </el-table-column>
        <el-table-column
          prop="error"
          label="错误信息"
        >
          <template slot-scope="scope">
            <el-button
              type="text"
              style="color: #f56c6c;"
              @click="showOutputDetail(scope.row.error, true)"
              v-if="scope.row.error"
            >
              查看错误
            </el-button>
            <span v-else>-</span>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        @size-change="handleResultSizeChange"
        @current-change="handleResultCurrentChange"
        :current-page="resultCurrentPage"
        :page-sizes="[5, 10, 20]"
        :page-size="resultPageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="totalResults"
        style="margin-top: 15px; text-align: right;"
      ></el-pagination>
    </el-dialog>

    <!-- 输出详情对话框 -->
    <el-dialog
      :title="outputDialogTitle"
      :visible.sync="outputDialogVisible"
      width="800px"
      top="5%"
    >
      <el-scrollbar style="height: 500px;">
        <pre style="white-space: pre-wrap; word-break: break-all;">{{ outputContent }}</pre>
      </el-scrollbar>
    </el-dialog>
  </div>
</template>

<script>
import { getTasks, createTask, updateTask, deleteTask, executeTaskNow, getTaskResults } from '../services/taskService'
import { getServers } from '../services/resourceService'

export default {
  name: 'TasksPage',
  data() {
    return {
      tasks: [],
      filteredTasks: [],
      servers: [],
      taskResults: [],
      searchQuery: '',
      selectedStatus: '',
      currentPage: 1,
      pageSize: 10,
      totalTasks: 0,

      resultCurrentPage: 1,
      resultPageSize: 10,
      totalResults: 0,
      currentTaskId: null,

      taskDialogVisible: false,
      taskDialogTitle: '添加定时任务',
      currentTaskIdEdit: null,
      taskForm: {
        name: '',
        command: '',
        server_ids: [],
        schedule: ''
      },
      taskRules: {
        name: [
          { required: true, message: '请输入任务名称', trigger: 'blur' }
        ],
        command: [
          { required: true, message: '请输入执行命令', trigger: 'blur' }
        ],
        server_ids: [
          { required: true, message: '请选择至少一个目标服务器', trigger: 'change' },
          { type: 'array', min: 1, message: '至少选择一个服务器', trigger: 'change' }
        ],
        schedule: [
          { required: true, message: '请输入Cron表达式', trigger: 'blur' }
        ]
      },

      resultDialogVisible: false,
      outputDialogVisible: false,
      outputDialogTitle: '输出详情',
      outputContent: ''
    }
  },
  created() {
    this.loadServers()
    this.loadTasks()
  },
  methods: {
    loadServers() {
      getServers().then(response => {
        this.servers = response.results
      }).catch(error => {
        const errorDetail = error.response && error.response.data && error.response.data.detail;
        this.$message.error('获取服务器列表失败: ' + (errorDetail || error.message));
      });
    },
    loadTasks() {
      const params = {
        page: this.currentPage,
        page_size: this.pageSize
      }
      if (this.searchQuery) {
        params.search = this.searchQuery
      }
      if (this.selectedStatus) {
        params.status = this.selectedStatus
      }

      getTasks(params).then(response => {
        this.tasks = response.results
        this.totalTasks = response.count
        this.filteredTasks = this.tasks
      }).catch(error => {
        const errorDetail = error.response && error.response.data && error.response.data.detail;
        this.$message.error('获取任务列表失败: ' + (errorDetail || error.message));
      });
    },
    handleSearch() {
      this.currentPage = 1
      this.loadTasks()
    },
    handleStatusChange() {
      this.currentPage = 1
      this.loadTasks()
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.currentPage = 1
      this.loadTasks()
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.loadTasks()
    },
    showAddTaskDialog() {
      this.taskDialogTitle = '添加定时任务'
      this.currentTaskIdEdit = null
      this.taskForm = {
        name: '',
        command: '',
        server_ids: [],
        schedule: ''
      }
      this.taskDialogVisible = true
    },
    showEditTaskDialog(task) {
      this.taskDialogTitle = '编辑定时任务'
      this.currentTaskIdEdit = task.id
      const serverIds = task.server_list.map(server => server.id)
      this.taskForm = {
        name: task.name,
        command: task.command,
        server_ids: serverIds,
        schedule: task.schedule
      }
      this.taskDialogVisible = true
    },
    saveTask() {
      this.$refs.taskForm.validate(valid => {
        if (valid) {
          if (this.currentTaskIdEdit) {
            updateTask(this.currentTaskIdEdit, this.taskForm).then(() => {
              this.$message.success('任务更新成功')
              this.taskDialogVisible = false
              this.loadTasks()
            }).catch(error => {
              const errorDetail = error.response && error.response.data && error.response.data.detail;
              this.$message.error('任务更新失败: ' + (errorDetail || error.message));
            });
          } else {
            createTask(this.taskForm).then(() => {
              this.$message.success('任务添加成功')
              this.taskDialogVisible = false
              this.loadTasks()
            }).catch(error => {
              const errorDetail = error.response && error.response.data && error.response.data.detail;
              this.$message.error('任务添加失败: ' + (errorDetail || error.message));
            });
          }
        }
      })
    },
    handleDeleteTask(id) {
      this.$confirm('确定要删除这个任务吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteTask(id).then(() => {
          this.$message.success('删除成功')
          this.loadTasks()
        }).catch(error => {
          const errorDetail = error.response && error.response.data && error.response.data.detail;
          this.$message.error('删除失败: ' + (errorDetail || error.message));
        });
      }).catch(() => {
        this.$message.info('已取消删除')
      })
    },
    executeTaskNow(id) {
      this.$confirm('确定要立即执行这个任务吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'info'
      }).then(() => {
        const loading = this.$loading({
          lock: true,
          text: '任务正在执行中...',
          spinner: 'el-icon-loading',
          background: 'rgba(0, 0, 0, 0.7)'
        })

        executeTaskNow(id).then(() => {
          loading.close()
          this.$message.success('任务执行成功，可查看执行结果')
          this.showTaskResults(id)
        }).catch(error => {
          loading.close()
          const errorDetail = error.response && error.response.data && error.response.data.detail;
          this.$message.error('任务执行失败: ' + (errorDetail || error.message));
        });
      }).catch(() => {
        this.$message.info('已取消执行')
      })
    },
    showTaskResults(taskId) {
      this.currentTaskId = taskId
      this.resultCurrentPage = 1
      this.loadTaskResults()
      this.resultDialogVisible = true
    },
    loadTaskResults() {
      const params = {
        page: this.resultCurrentPage,
        page_size: this.resultPageSize,
        task: this.currentTaskId
      }

      getTaskResults(params).then(response => {
        this.taskResults = response.results
        this.totalResults = response.count
      }).catch(error => {
        const errorDetail = error.response && error.response.data && error.response.data.detail;
        this.$message.error('获取执行结果失败: ' + (errorDetail || error.message));
      });
    },
    handleResultSizeChange(val) {
      this.resultPageSize = val
      this.resultCurrentPage = 1
      this.loadTaskResults()
    },
    handleResultCurrentChange(val) {
      this.resultCurrentPage = val
      this.loadTaskResults()
    },
    showOutputDetail(content, isError = false) {
      this.outputContent = content || '无内容'
      this.outputDialogTitle = isError ? '错误信息详情' : '输出结果详情'
      this.outputDialogVisible = true
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

pre {
  font-family: "Courier New", Courier, monospace;
  color: #333;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 4px;
}
</style>