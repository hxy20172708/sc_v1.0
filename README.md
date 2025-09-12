# 服务器管理系统

一个基于Django和Vue的服务器管理系统，支持机房、服务器、环境管理和任务执行。

## 功能特点

- 机房管理：管理物理机房信息
- 服务器管理：记录服务器基本信息和状态
- 环境管理：将服务器分组为不同环境（开发、测试、生产等）
- 任务管理：在服务器或环境上执行命令并查看结果

## 技术栈

- 后端：Django, Django REST Framework
- 前端：Vue 3, Element Plus
- 数据库：MySQL 8.0

## 部署指南

### 开发环境

1. 克隆代码仓库
2. 配置环境变量：复制.env.example为.env并修改
3. 启动服务：`docker-compose up -d`
4. 初始化数据库：
   ```bash
   docker-compose exec backend python manage.py migrate
   docker-compose exec backend python manage.py createsuperuser
   ```
5. 访问前端：http://localhost:5173
6. 访问后端API：http://localhost:8000/api
7. 访问管理后台：http://localhost:8000/admin

### 生产环境

参考部署文档进行生产环境配置，主要包括：
- 配置域名和HTTPS
- 调整安全相关设置
- 设置定期备份
# sc_v1
# sc_v1.0
