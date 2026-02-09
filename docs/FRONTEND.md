# Frontend Architecture / 前端架构

## Current Status / 当前状态

### 🔍 User Question / 用户问题
**问题：这个项目的前端是使用什么语言和架构写的？**

**Question: What language and architecture is this project's frontend written in?**

---

## ❌ No Frontend Currently Exists / 目前没有前端

### Current Architecture / 当前架构

This project **currently does NOT have a frontend**. It is designed as a **CLI (Command Line Interface) application** written entirely in Python.

本项目**目前没有前端**。它被设计为一个完全用Python编写的**命令行界面（CLI）应用程序**。

### What Exists Now / 现有内容

✅ **Backend/CLI Architecture:**
- **Language:** Python 3.12+
- **Interface:** Command Line (CLI)
- **Entry Point:** `cli.py`
- **Architecture:** Multi-agent system with workflow orchestration
- **Output:** Text-based reports (Markdown format)

✅ **后端/CLI架构：**
- **语言：** Python 3.12+
- **接口：** 命令行（CLI）
- **入口点：** `cli.py`
- **架构：** 多智能体系统与工作流编排
- **输出：** 基于文本的报告（Markdown格式）

### How to Use Currently / 当前使用方式

```bash
# Run the CLI tool
python cli.py

# Or programmatically
python -c "from src.workflow import CompetitiveAnalysisWorkflow; ..."
```

---

## 🚀 Future Frontend Options / 未来前端选项

If you want to add a frontend to this project, here are recommended architectures:

如果您想为这个项目添加前端，以下是推荐的架构：

### Option 1: Web Frontend (Recommended) / Web前端（推荐）

#### Technology Stack / 技术栈

**Framework Options:**
1. **React + TypeScript** (Most Popular)
   - Modern component-based architecture
   - Strong typing with TypeScript
   - Large ecosystem
   
2. **Vue.js 3 + TypeScript** (Easier to Learn)
   - Progressive framework
   - Excellent documentation in Chinese
   - Good for rapid development
   
3. **Next.js** (Full-stack Solution)
   - React-based with SSR/SSG
   - Built-in API routes
   - Excellent performance

**Backend API:**
- Convert CLI logic to **FastAPI** REST/WebSocket endpoints
- Already have FastAPI in dependencies (`pyproject.toml`)
- Maintain Python backend with agents

**Architecture Diagram:**
```
┌─────────────────┐
│  Web Frontend   │  React/Vue/Next.js
│  (TypeScript)   │  + Tailwind CSS
└────────┬────────┘
         │ HTTP/WebSocket
         ▼
┌─────────────────┐
│   FastAPI       │  Python Backend
│   REST API      │  (Existing agents)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Agent System   │  Python Multi-agents
│  (Current Code) │  (No changes needed)
└─────────────────┘
```

### Option 2: Desktop Application / 桌面应用

**Technology Options:**
1. **Electron** (Cross-platform)
   - HTML/CSS/JavaScript
   - Works on Windows/Mac/Linux
   - Can embed Python backend
   
2. **Tauri** (Lightweight)
   - Rust-based, smaller than Electron
   - Modern web frontend
   - Better performance

### Option 3: Mobile Application / 移动应用

**Technology Options:**
1. **React Native** (Cross-platform)
   - JavaScript/TypeScript
   - iOS and Android
   
2. **Flutter** (Cross-platform)
   - Dart language
   - Beautiful UI
   - High performance

---

## 📋 Recommended Implementation Plan / 推荐实施计划

If you decide to add a Web Frontend:

如果您决定添加Web前端：

### Phase 1: Backend API / 后端API

1. **Create FastAPI Server**
   ```python
   # api/main.py
   from fastapi import FastAPI, WebSocket
   from src.workflow import CompetitiveAnalysisWorkflow
   
   app = FastAPI()
   
   @app.post("/api/analyze")
   async def analyze(data: dict):
       workflow = CompetitiveAnalysisWorkflow()
       result = await workflow.execute(data)
       return result
   
   @app.websocket("/ws/analyze")
   async def websocket_analyze(websocket: WebSocket):
       # Real-time progress updates
       pass
   ```

2. **Add CORS Support**
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["http://localhost:3000"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

### Phase 2: Frontend Development / 前端开发

**Recommended Stack:**
- **Framework:** React with TypeScript
- **UI Library:** Ant Design or Material-UI (Chinese localization)
- **State Management:** React Query or Redux
- **Styling:** Tailwind CSS
- **Build Tool:** Vite

**Project Structure:**
```
frontend/
├── src/
│   ├── components/
│   │   ├── InfoCollectionForm.tsx    # AgentA UI
│   │   ├── AnalysisProgress.tsx      # Progress display
│   │   ├── ReportViewer.tsx          # Report display
│   │   └── Dashboard.tsx             # Main interface
│   ├── api/
│   │   └── client.ts                 # API calls
│   ├── i18n/
│   │   ├── en.json                   # English
│   │   └── zh.json                   # Chinese
│   └── App.tsx
├── package.json
└── vite.config.ts
```

### Phase 3: Integration / 集成

**File Structure After Frontend Addition:**
```
CompetitivAnalysis/
├── backend/                 # Current Python code
│   ├── src/
│   ├── cli.py
│   └── pyproject.toml
├── api/                     # New FastAPI server
│   ├── main.py
│   ├── routes/
│   └── requirements.txt
├── frontend/                # New React app
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

---

## 🎨 Frontend Features to Implement / 要实现的前端功能

### 1. User Interface / 用户界面

- **Information Collection Form** (对应 AgentA)
  - Multi-step form wizard
  - Field validation
  - Auto-save functionality
  
- **Real-time Progress Indicator** (工作流进度)
  - Show which agent is working
  - Progress bar for each phase
  - WebSocket for live updates

- **Report Viewer** (报告查看器)
  - Markdown rendering
  - PDF export
  - Share functionality

- **Dashboard** (仪表板)
  - Analysis history
  - Saved reports
  - Quick actions

### 2. Bilingual Support / 双语支持

```typescript
// i18n/zh.json
{
  "app.title": "竞品分析工具",
  "form.industry": "行业",
  "form.productName": "产品名称",
  "button.analyze": "开始分析"
}

// i18n/en.json
{
  "app.title": "Competitive Analysis Tool",
  "form.industry": "Industry",
  "form.productName": "Product Name",
  "button.analyze": "Start Analysis"
}
```

### 3. Key Components / 关键组件

**React Example:**
```typescript
// InfoCollectionForm.tsx
import { Form, Input, Button } from 'antd';
import { useTranslation } from 'react-i18next';

export const InfoCollectionForm: React.FC = () => {
  const { t } = useTranslation();
  const [form] = Form.useForm();
  
  const onFinish = async (values: any) => {
    const response = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(values)
    });
    
    const result = await response.json();
    // Handle result
  };
  
  return (
    <Form form={form} onFinish={onFinish}>
      <Form.Item 
        label={t('form.industry')} 
        name="industry"
        rules={[{ required: true }]}
      >
        <Input placeholder={t('form.industry.placeholder')} />
      </Form.Item>
      
      <Form.Item 
        label={t('form.productName')} 
        name="product_name"
      >
        <Input />
      </Form.Item>
      
      <Button type="primary" htmlType="submit">
        {t('button.analyze')}
      </Button>
    </Form>
  );
};
```

---

## 💡 Quick Start for Frontend Development / 前端开发快速开始

### Step 1: Create React App / 创建React应用

```bash
# Using Vite (Recommended)
npm create vite@latest frontend -- --template react-ts

# Or using Create React App
npx create-react-app frontend --template typescript
```

### Step 2: Install Dependencies / 安装依赖

```bash
cd frontend
npm install antd axios react-query react-i18next
npm install -D tailwindcss @types/node
```

### Step 3: Create API Server / 创建API服务器

```bash
# In project root
mkdir api
cd api

# Create main.py
cat > main.py << 'EOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
sys.path.append('..')

from src.workflow import CompetitiveAnalysisWorkflow

app = FastAPI(title="Competitive Analysis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Competitive Analysis API"}

@app.post("/api/analyze")
async def analyze(data: dict):
    workflow = CompetitiveAnalysisWorkflow()
    result = await workflow.execute(data)
    return result.dict()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF
```

### Step 4: Run Both Services / 运行两个服务

```bash
# Terminal 1: Backend API
cd api
python main.py

# Terminal 2: Frontend Dev Server
cd frontend
npm run dev
```

---

## 📊 Comparison Table / 对比表

| Aspect | Current (CLI) | With Web Frontend |
|--------|--------------|-------------------|
| **Language** | Python | Python (Backend) + TypeScript (Frontend) |
| **Interface** | Command Line | Web Browser |
| **User Experience** | Text-based | Visual, Interactive |
| **Accessibility** | Technical users | All users |
| **Deployment** | Local execution | Web server + hosting |
| **Real-time Updates** | No | Yes (WebSocket) |
| **Multi-user** | No | Yes |
| **Visualization** | Limited | Charts, graphs, dashboards |

| 方面 | 当前（CLI） | 带Web前端 |
|------|------------|-----------|
| **语言** | Python | Python（后端）+ TypeScript（前端） |
| **界面** | 命令行 | Web浏览器 |
| **用户体验** | 基于文本 | 可视化、交互式 |
| **可访问性** | 技术用户 | 所有用户 |
| **部署** | 本地执行 | Web服务器 + 托管 |
| **实时更新** | 否 | 是（WebSocket） |
| **多用户** | 否 | 是 |
| **可视化** | 有限 | 图表、图形、仪表板 |

---

## 📝 Summary / 总结

### Current State / 当前状态
❌ **No frontend exists** - CLI only
❌ **没有前端** - 仅命令行

### If You Want a Frontend / 如果需要前端

**Recommended:** React + TypeScript + FastAPI

**推荐：** React + TypeScript + FastAPI

**Reasons:**
1. ✅ Mature ecosystem
2. ✅ Great TypeScript support
3. ✅ Easy integration with Python backend
4. ✅ Excellent Chinese documentation
5. ✅ Can reuse all existing agent code

**原因：**
1. ✅ 成熟的生态系统
2. ✅ 出色的TypeScript支持
3. ✅ 易于与Python后端集成
4. ✅ 优秀的中文文档
5. ✅ 可以重用所有现有的代理代码

---

## 🔗 Related Documentation / 相关文档

- Current CLI Usage: See `README.md`
- Backend Architecture: See `docs/ARCHITECTURE.md`
- Development Guide: See `docs/DEVELOPMENT.md`

---

**Last Updated:** 2024-02-09  
**Status:** Documentation - No Frontend Implementation Yet  
**状态:** 文档说明 - 尚未实现前端
