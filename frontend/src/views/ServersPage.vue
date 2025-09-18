<template>
  <div class="servers-page">
    <div class="page-header">
      <h1>服务器管理</h1>
      <button
        class="btn-add"
        @click="handleAddServer"
      >
        <i class="fa fa-plus"></i> 添加服务器
      </button>
    </div>

    <div class="filters">
      <el-input
        v-model="searchQuery"
        placeholder="搜索服务器名称或IP"
        clearable
        @clear="handleSearch"
        @keyup.enter.native="handleSearch"
        class="search-input"
      ></el-input>

      <el-select
        v-model="selectedRoom"
        placeholder="选择机房"
        clearable
        @change="handleRoomChange"
        class="room-select"
      >
        <el-option
          v-for="room in rooms"
          :key="room.id"
          :label="room.name"
          :value="room.id"
        ></el-option>
      </el-select>
    </div>

    <el-table
      v-loading="isLoading"
      :data="filteredServers"
      border
      stripe
      class="servers-table"
    >
      <el-table-column
        prop="name"
        label="服务器名称"
        width="180"
      ></el-table-column>
      <el-table-column
        prop="ip_address"
        label="IP地址"
        width="150"
      ></el-table-column>
      <el-table-column
        prop="room_name"
        label="所属机房"
        width="180"
      ></el-table-column>
      <el-table-column
        prop="status"
        label="状态"
        width="120"
      >
        <template slot-scope="scope">
          <el-tag
            :type="scope.row.status === 'running' ? 'success' : 'warning'"
          >
            {{ scope.row.status === 'running' ? '运行中' : '已停止' }}
          </el-tag>
        </template>
      </el-table-column>
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
            size="mini"
            @click="handleEditServer(scope.row)"
          >编辑</el-button>
          <el-button
            size="mini"
            type="danger"
            @click="handleDeleteServer(scope.row)"
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination">
      <el-pagination
        @current-change="handlePageChange"
        :current-page="currentPage"
        :page-size="pageSize"
        :total="totalServers"
        layout="total, prev, pager, next"
      ></el-pagination>
    </div>

    <!-- 服务器表单对话框 -->
    <server-form
      :visible="isDialogVisible"
      :type="dialogType"
      :server="currentServer"
      :rooms="rooms"
      @close="handleDialogClose"
      @submit="handleFormSubmit"
    ></server-form>

    <!-- 删除确认对话框 -->
    <confirm-dialog
      :visible="isDeleteDialogVisible"
      title="确认删除"
      content="确定要删除这台服务器吗？此操作不可撤销。"
      @confirm="confirmDelete"
      @cancel="() => { isDeleteDialogVisible = false; serverToDelete = null; }"
    ></confirm-dialog>
  </div>
</template>

<script>
import { getServers, deleteServer, getRooms } from '@/services/api';
import ServerForm from '@/views/ServerForm';
import ConfirmDialog from '@/views/ConfirmDialog';

export default {
  components: {
    ServerForm,
    ConfirmDialog
  },
  data() {
    return {
      servers: [],
      filteredServers: [],
      rooms: [],
      totalServers: 0,
      currentPage: 1,
      pageSize: 10,
      searchQuery: '',
      selectedRoom: '',
      isLoading: false,
      isDialogVisible: false,
      dialogType: 'add', // 'add' 或 'edit'
      currentServer: null,
      isDeleteDialogVisible: false,
      serverToDelete: null
    };
  },
  created() {
    this.loadRooms();
    this.loadServers();
  },
  methods: {
    loadRooms() {
      getRooms().then(response => {
        this.rooms = response.results;
      }).catch(error => {
        console.error('获取机房列表失败:', error);
        this.$message.error('获取机房列表失败，请重试');
      });
    },

    // 修复后的服务器列表加载方法
    loadServers() {
      this.isLoading = true;
      const params = {
        page: this.currentPage,
        page_size: this.pageSize
      };

      if (this.selectedRoom) {
        params.room = this.selectedRoom;
      }

      if (this.searchQuery) {
        params.search = this.searchQuery;
      }

      getServers(params)
        .then(response => {
          // 修正：直接使用response.results和response.count
          this.servers = response.results;
          this.totalServers = response.count;
          this.filteredServers = this.servers;
        })
        .catch(error => {
          console.error('获取服务器列表失败:', error);
          this.$message.error('获取服务器列表失败，请重试');
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    handleSearch() {
      this.currentPage = 1;
      this.loadServers();
    },

    handleRoomChange(roomId) {
      this.selectedRoom = roomId;
      this.currentPage = 1;
      this.loadServers();
    },

    handlePageChange(page) {
      this.currentPage = page;
      this.loadServers();
    },

    handleAddServer() {
      this.dialogType = 'add';
      this.currentServer = null;
      this.isDialogVisible = true;
    },

    handleEditServer(server) {
      this.dialogType = 'edit';
      this.currentServer = { ...server };
      this.isDialogVisible = true;
    },

    handleDeleteServer(server) {
      this.serverToDelete = server;
      this.isDeleteDialogVisible = true;
    },

    confirmDelete() {
      if (this.serverToDelete) {
        deleteServer(this.serverToDelete.id)
          .then(() => {
            this.$message.success('服务器删除成功');
            this.loadServers();
          })
          .catch(error => {
            console.error('删除服务器失败:', error);
            this.$message.error('删除服务器失败，请重试');
          })
          .finally(() => {
            this.isDeleteDialogVisible = false;
            this.serverToDelete = null;
          });
      }
    },

    handleDialogClose() {
      this.isDialogVisible = false;
      this.currentServer = null;
    },

    handleFormSubmit() {
      this.isDialogVisible = false;
      this.loadServers(); // 提交后重新加载列表
    }
  },
  watch: {
    searchQuery(val) {
      if (val === '') {
        this.filteredServers = this.servers;
      } else {
        this.filteredServers = this.servers.filter(server =>
          server.name.toLowerCase().includes(val.toLowerCase()) ||
          server.ip_address.includes(val)
        );
      }
    }
  }
};
</script>

<style scoped>
.servers-page {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.btn-add {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.btn-add i {
  margin-right: 5px;
}

.filters {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.search-input {
  width: 300px;
}

.room-select {
  width: 200px;
}

.servers-table {
  background-color: white;
  margin-bottom: 20px;
}

.pagination {
  text-align: right;
}
</style>
