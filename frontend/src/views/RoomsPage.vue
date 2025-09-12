<template>
  <div class="rooms-page">
    <el-card>
      <div slot="header" class="page-header">
        <h2>机房管理</h2>
        <el-button type="primary" @click="showAddRoomDialog">添加机房</el-button>
      </div>
      
      <div class="search-bar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索机房名称或位置"
          prefix-icon="el-icon-search"
          style="width: 300px;"
          @input="handleSearch"
        ></el-input>
      </div>
      
      <el-table
        :data="filteredRooms"
        border
        style="width: 100%; margin-top: 20px;"
      >
        <el-table-column
          prop="name"
          label="机房名称"
          width="180"
        ></el-table-column>
        <el-table-column
          prop="location"
          label="位置"
          width="200"
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
          label="操作"
          width="200"
        >
          <template slot-scope="scope">
            <el-button
              type="text"
              @click="showEditRoomDialog(scope.row)"
            >
              编辑
            </el-button>
            <el-button
              type="text"
              style="color: #f56c6c;"
              @click="handleDeleteRoom(scope.row.id)"
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
        :total="totalRooms"
        style="margin-top: 20px; text-align: right;"
      ></el-pagination>
    </el-card>
    
    <!-- 添加/编辑机房对话框 -->
    <el-dialog
      :title="roomDialogTitle"
      :visible.sync="roomDialogVisible"
      width="500px"
    >
      <el-form
        ref="roomForm"
        :model="roomForm"
        :rules="roomRules"
        label-width="100px"
      >
        <el-form-item label="机房名称" prop="name">
          <el-input v-model="roomForm.name"></el-input>
        </el-form-item>
        <el-form-item label="位置" prop="location">
          <el-input v-model="roomForm.location"></el-input>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input type="textarea" v-model="roomForm.description" rows="4"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="roomDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveRoom">保存</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getRooms, createRoom, updateRoom, deleteRoom } from '../services/resourceService'

export default {
  name: 'RoomsPage',
  data() {
    return {
      rooms: [],
      filteredRooms: [],
      searchQuery: '',
      currentPage: 1,
      pageSize: 10,
      totalRooms: 0,
      
      roomDialogVisible: false,
      roomDialogTitle: '添加机房',
      currentRoomId: null,
      roomForm: {
        name: '',
        location: '',
        description: ''
      },
      roomRules: {
        name: [
          { required: true, message: '请输入机房名称', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.loadRooms()
  },
  methods: {
    loadRooms() {
      const params = {
        page: this.currentPage,
        page_size: this.pageSize
      }
      if (this.searchQuery) {
        params.search = this.searchQuery
      }
      
      getRooms(params).then(response => {
        this.rooms = response.results
        this.totalRooms = response.count
        this.filteredRooms = this.rooms
      }).catch(error => {
        const errorDetail = error.response && error.response.data && error.response.data.detail;
        this.$message.error('获取机房列表失败: ' + (errorDetail || error.message));
      });
    },
    handleSearch() {
      this.currentPage = 1
      this.loadRooms()
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.currentPage = 1
      this.loadRooms()
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.loadRooms()
    },
    showAddRoomDialog() {
      this.roomDialogTitle = '添加机房'
      this.currentRoomId = null
      this.roomForm = {
        name: '',
        location: '',
        description: ''
      }
      this.roomDialogVisible = true
    },
    showEditRoomDialog(room) {
      this.roomDialogTitle = '编辑机房'
      this.currentRoomId = room.id
      this.roomForm = {
        name: room.name,
        location: room.location,
        description: room.description
      }
      this.roomDialogVisible = true
    },
    saveRoom() {
      this.$refs.roomForm.validate(valid => {
        if (valid) {
          if (this.currentRoomId) {
            updateRoom(this.currentRoomId, this.roomForm).then(() => {
              this.$message.success('机房更新成功')
              this.roomDialogVisible = false
              this.loadRooms()
            }).catch(error => {
              const errorDetail = error.response && error.response.data && error.response.data.detail;
              this.$message.error('机房更新失败: ' + (errorDetail || error.message));
            });
          } else {
            createRoom(this.roomForm).then(() => {
              this.$message.success('机房添加成功')
              this.roomDialogVisible = false
              this.loadRooms()
            }).catch(error => {
              const errorDetail = error.response && error.response.data && error.response.data.detail;
              this.$message.error('机房添加失败: ' + (errorDetail || error.message));
            });
          }
        }
      })
    },
    handleDeleteRoom(id) {
      this.$confirm('确定要删除这个机房吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteRoom(id).then(() => {
          this.$message.success('删除成功')
          this.loadRooms()
        }).catch(error => {
          const errorDetail = error.response && error.response.data && error.response.data.detail;
          this.$message.error('删除失败: ' + (errorDetail || error.message));
        });
      }).catch(() => {
        this.$message.info('已取消删除')
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
    