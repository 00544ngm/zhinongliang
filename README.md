# 智农粮（ZhiNongLiang）

家庭粮食收购站工业级数字化管理系统

## 技术栈

- **前端**: Vue3 + TypeScript + Vite + Pinia + Element Plus
- **后端**: Python FastAPI + SQLAlchemy + Pydantic
- **数据库**: PostgreSQL 16
- **部署**: Docker Compose + Nginx

## 快速启动

### 开发环境

**后端：**

```bash
cd backend
pip install -r requirements.txt
# 确保 PostgreSQL 运行中
python -m app.seed    # 创建默认管理员
uvicorn app.main:app --reload --port 8000
```

**前端：**

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:3000

### Docker 部署

```bash
docker compose up -d --build
```

访问 http://localhost

## 默认账号

- 用户名: `admin`
- 密码: `admin123`

## 核心功能

- 收购管理（完整状态机：毛重→报价→卸粮→空车→完成）
- 库存管理（实时更新，行级锁，事务保证）
- 农户管理（自动累计统计）
- 数据看板
- JWT 认证

## 项目结构

```
backend/
├── app/
│   ├── api/          # RESTful 路由层
│   ├── core/         # 配置、数据库、安全
│   ├── models/       # SQLAlchemy ORM 模型
│   ├── schemas/      # Pydantic 数据校验
│   ├── services/     # 核心业务逻辑层
│   ├── repositories/ # 数据访问层
│   ├── plugins/      # 插件化架构
│   └── main.py
├── alembic/          # 数据库迁移
└── Dockerfile

frontend/
├── src/
│   ├── api/          # API 客户端
│   ├── views/        # 页面组件
│   ├── layouts/      # 布局
│   ├── stores/       # Pinia 状态管理
│   └── router/       # 路由
└── Dockerfile
```

## 数据安全

- 金额/重量全程 Decimal 类型（禁止 float）
- 所有业务操作事务化（全部成功或全部回滚）
- PostgreSQL WAL 保障断电恢复
- 软删除（禁止物理删除）
- 每日自动备份（pg_dump + 异地备份）

## 许可证

内部使用 - 马西军收购站
