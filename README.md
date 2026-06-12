# CFA Stock Ontology - CFA 选股分析平台

## 项目概述

基于 **本体论驱动（Ontology-Driven）** 的 CFA 六步选股分析平台，核心特色：

- **A+D 四维行业分析框架**：波特五力 → 行业生命周期 → Bain 进入壁垒 → Porter 竞争战略
- **可解释推理链**：每个评分都有原始数据、评分规则、计算过程的完整追溯
- **机会驱动 UI**：Bloomberg/TradingView 风格，先发现机会再看个股

## 技术架构

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND                                   │
│  Next.js 15 + React 19 + TypeScript + TailwindCSS                      │
│  ├─ Recharts (数据可视化)                                                │
│  ├─ Framer Motion (动画)                                                 │
│  ├─ Zustand (状态管理)                                                   │
│  └─ React Flow (本体推理图谱)                                             │
├─────────────────────────────────────────────────────────────────────────┤
│                              BACKEND                                    │
│  FastAPI + Python 3.12 + SQLAlchemy + PostgreSQL + Redis + Celery      │
│  ├─ Domain Layer (DDD)                                                   │
│  ├─ Application Layer (AI Agent + Workflow)                              │
│  ├─ Infrastructure Layer (ETL + Cache + DB)                              │
│  └─ API Layer (REST)                                                     │
└─────────────────────────────────────────────────────────────────────────┘
```

## 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd cfa-stock-ontology
```

### 2. 环境配置

```bash
# 复制环境变量模板
cp backend/.env.example backend/.env

# 编辑 .env 文件，配置数据库和 API 密钥
```

### 3. Docker 启动

```bash
cd docker
docker-compose up -d
```

服务将启动在：
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### 4. 本地开发

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn api.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 核心功能

### 1. 市场机会总览
- 综合机会评分 (Opportunity Score)
- 高价值投资机会数量
- 热门主题标签

### 2. 行业机会地图
- 气泡图：X=市场规模, Y=机会评分, Bubble=增速, Color=风险
- 支持悬停查看详情

### 3. 候选股票池
- 综合评分排序
- 五维评分条 (行业/财务/估值/成长/风险)
- BUY/HOLD/SELL 评级标签

### 4. 股票详情分析
- **综合看板**：五维雷达图 + 综合评分
- **行业分析**：A+D 四维框架展开
  - ① 波特五力 (Porter's Five Forces)
  - ② 行业生命周期 (Industry Lifecycle) + S曲线
  - ③ Bain 进入壁垒 (Entry Barriers)
  - ④ Porter 竞争战略 (Competitive Strategy)
- **财务质量**：DuPont 分解
- **估值分析**：PE/PB/PEG + DCF 区间
- **成长性**：CAGR + 分析师预期
- **风险分析**：Beta/负债/政策风险

### 5. 本体推理图谱 (React Flow)
- 可视化推理链路
- 支持展开/悬停/高亮

## 数据模型

### 7 大核心实体

| 实体 | 说明 |
|---|---|
| Stock | 股票基础信息 |
| Sector | 行业分析 (A+D 四维) |
| FinancialQuality | 财务质量 (DuPont) |
| Valuation | 估值 (绝对+相对) |
| Growth | 成长性 |
| Risk | 风险画像 |
| Conclusion | 投资结论 |

### 13 条推理边 (Edge)

| 边 | 说明 |
|---|---|
| E1a-E1e | Stock → Sector 子维度 |
| E2-E5 | Stock → 财务/估值/成长/风险 |
| E6-E8 | 实体间修饰边 |
| E9-E13 | 所有实体 → Conclusion |

## API 接口

### Stocks
- `GET /api/stocks/search?q={query}` - 搜索股票
- `GET /api/stocks/{ticker}` - 获取股票详情
- `GET /api/stocks/` - 股票列表

### Analysis
- `GET /api/analysis/{ticker}/full` - 完整分析
- `POST /api/analysis/{ticker}/trigger` - 触发分析

### Opportunities
- `GET /api/opportunities/` - 机会列表
- `GET /api/opportunities/top` - Top 机会

## 评分规则

### Sector 四维加权
```
Sector.score = round(
    ff_score × 0.25 +
    lc_score × 0.25 +
    eb_score × 0.25 +
    cp_score × 0.25
), capped [1, 10]
```

### 投资结论加权
```
composite_score = 
    sector × 0.20 +
    financial × 0.25 +
    valuation × 0.25 +
    growth × 0.15 +
    risk × 0.15

Rating: ≥8.0 BUY, ≥6.0 HOLD, <6.0 SELL
```

## 开发阶段

| 阶段 | 内容 | 状态 |
|---|---|---|
| Phase 0 | 项目初始化、Docker 环境 | ✅ |
| Phase 1 | 核心领域模型 (7实体) | ✅ |
| Phase 2 | 本体引擎 + 评分规则 | ✅ |
| Phase 3 | AI Agent + 数据库 + API | ✅ |
| Phase 4 | ETL 数据管道 | ✅ |
| Phase 5 | FastAPI + 工作流 | ✅ |
| Phase 6 | 前端 Dashboard | ✅ |
| Phase 7 | React Flow 推理图谱 | 🔄 |
| Phase 8 | Mock 数据 + 测试 | 🔄 |

## 技术栈

**Frontend:**
- Next.js 15
- React 19
- TypeScript
- TailwindCSS
- Framer Motion
- Recharts
- React Flow
- Zustand

**Backend:**
- FastAPI
- Python 3.12
- SQLAlchemy
- PostgreSQL
- Redis
- Celery
- OpenAI

## License

MIT
