<template>
  <el-dialog
    :visible.sync="visible"
    :title="dialogTitle"
    width="500px"
    :close-on-click-modal="false"
  >
    <el-form
      ref="serverForm"
      :model="server"
      :rules="rules"
      label-width="100px"
    >
      <el-form-item label="服务器名称" prop="name">
        <el-input v-model="server.name"></el-input>
      </el-form-item>

      <el-form-item label="IP地址" prop="ip_address">
        <el-input v-model="server.ip_address"></el-input>
      </el-form-item>

      <el-form-item label="所属机房" prop="room">
        <el-select v-model="server.room" placeholder="请选择机房">
          <el-option
            v-for="room in rooms"
            :key="room.id"
            :label="room.name"
            :value="room.id"
          ></el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="状态" prop="status">
        <el-select v-model="server.status">
          <el-option label="运行中" value="running"></el-option>
          <el-option label="已停止" value="stopped"></el-option>
        </el-select>
      </el-form-item>
    </el-form>

    <span slot="footer" class="dialog-footer">
      <el-button @click="handleCancel">取消</el-button>
      <el-button type="primary" @click="handleSubmit">提交</el-button>
    </span>
  </el-dialog>
</template>

<script>
import { createServer, updateServer } from '@/services/api';

export default {
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    type: {
      type: String,
      default: 'add', // 'add' 或 'edit'
      validator: value => ['add', 'edit'].includes(value)
    },
    server: {
      type: Object,
      default: () => ({})
    },
    rooms: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      formServer: { ...this.server },
      rules: {
        name: [
          { required: true, message: '请输入服务器名称', trigger: 'blur' }
        ],
        ip_address: [
          { required: true, message: '请输入IP地址', trigger: 'blur' },
          { type: 'ip', message: '请输入有效的IP地址', trigger: 'blur' }
        ],
        room: [
          { required: true, message: '请选择所属机房', trigger: 'change' }
        ]
      }
    };
  },
  computed: {
    dialogTitle() {
      return this.type === 'add' ? '添加服务器' : '编辑服务器';
    }
  },
  watch: {
    server(newVal) {
      this.formServer = { ...newVal };
    }
  },
  methods: {
    handleSubmit() {
      this.$refs.serverForm.validate(valid => {
        if (valid) {
          if (this.type === 'add') {
            createServer(this.formServer)
              .then(() => {
                this.$message.success('服务器添加成功');
                this.$emit('submit');
              })
              .catch(error => {
                console.error('添加服务器失败:', error);
                this.$message.error('添加服务器失败，请重试');
              });
          } else {
            updateServer(this.formServer.id, this.formServer)
              .then(() => {
                this.$message.success('服务器更新成功');
                this.$emit('submit');
              })
              .catch(error => {
                console.error('更新服务器失败:', error);
                this.$message.error('更新服务器失败，请重试');
              });
          }
        }
      });
    },
    handleCancel() {
      this.$emit('close');
    }
  }
};
</script>

<style scoped>
.dialog-footer {
  text-align: right;
}
</style>
