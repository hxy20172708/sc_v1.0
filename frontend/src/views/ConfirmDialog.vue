<template>
  <el-dialog
    :visible.sync="visible"
    :title="title"
    :close-on-click-modal="false"
  >
    <div class="dialog-content">{{ content }}</div>
    <span slot="footer" class="dialog-footer">
      <el-button @click="handleCancel">取消</el-button>
      <el-button type="danger" @click="handleConfirm">确定</el-button>
    </span>
  </el-dialog>
</template>

<script>
export default {
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: '确认操作'
    },
    content: {
      type: String,
      default: '确定要执行此操作吗？'
    }
  },
  methods: {
    handleConfirm() {
      this.$emit('confirm');
    },
    handleCancel() {
      this.$emit('cancel');
    }
  }
};
</script>

<style scoped>
.dialog-content {
  font-size: 14px;
  color: #333;
}

.dialog-footer {
  text-align: right;
}
</style>
