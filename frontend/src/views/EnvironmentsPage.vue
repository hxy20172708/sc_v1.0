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
              {{ scope.row.servers_detail.length }}台
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
       