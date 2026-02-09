# Competitive Analysis / 竞品分析

An AI-powered competitive analysis tool using multi-agent collaboration, skills, and MCP tools.

一个基于多智能体协作、技能和MCP工具的AI竞品分析工具。

## 项目概述 / Project Overview

This project implements a comprehensive competitive analysis system based on the [cooragent](https://github.com/LeapLabTHU/cooragent) architecture. It uses multiple specialized AI agents working together to collect, analyze, and generate detailed competitive analysis reports.

本项目基于 [cooragent](https://github.com/LeapLabTHU/cooragent) 架构实现了一个全面的竞品分析系统。它使用多个专业AI代理协同工作，收集、分析并生成详细的竞品分析报告。

### 💻 Interface / 界面

**Current Version:** Command Line Interface (CLI) only

**当前版本：** 仅命令行界面（CLI）

- **Language:** Python 3.12+
- **Type:** CLI application (`cli.py`)
- **No Web Frontend:** This is currently a backend-only project
- **无Web前端：** 这是一个纯后端项目

> 📝 **Note:** For information about potential frontend implementation, see [docs/FRONTEND.md](docs/FRONTEND.md)
> 
> 📝 **注意：** 有关潜在前端实现的信息，请参阅 [docs/FRONTEND.md](docs/FRONTEND.md)

## 架构设计 / Architecture Design

### Multi-Agent System / 多智能体系统

The system consists of 8 specialized agents working in a coordinated workflow:

系统由8个专业代理在协调工作流中协作：

1. **AgentA - Information Collector / 信息收集代理**
   - Role: Collects user information through multi-round conversations
   - 角色：通过多轮对话收集用户信息
   - Collects: Industry, product name, purpose, audience, price, culture, needs
   - 收集：行业、产品名称、用途、受众、价格、企业文化、需求

2. **AgentB - Industry Analyzer / 行业分析代理**
   - Role: Identifies and analyzes top 10 companies in the industry
   - 角色：识别并分析行业排名前十的企业
   - Skills: Internet search, data analysis
   - 技能：互联网搜索、数据分析

3. **AgentC - Product Name Searcher / 产品名称搜索代理**
   - Role: Finds products with similar names
   - 角色：查找产品名称相近的产品
   - Skills: Internet search, information extraction
   - 技能：互联网搜索、信息提取

4. **AgentD - Product Purpose Searcher / 产品用途搜索代理**
   - Role: Finds products with similar purposes/use cases
   - 角色：查找产品用途相近的产品
   - Skills: Internet search, data analysis
   - 技能：互联网搜索、数据分析

5. **AgentE - Price Analyzer / 价格分析代理**
   - Role: Analyzes products with similar price points
   - 角色：分析产品价格相近的产品
   - Skills: Internet search, data analysis
   - 技能：互联网搜索、数据分析

6. **AgentF - Integration Analyzer / 整合分析代理**
   - Role: Integrates all collected data with company culture and audience analysis
   - 角色：结合企业文化和产品受众对收集到的信息进行分析整合
   - Skills: Data analysis
   - 技能：数据分析

7. **AgentG - Report Generator / 报告生成代理**
   - Role: Generates comprehensive competitive analysis reports
   - 角色：生成全面的竞品分析报告
   - Skills: Report generation
   - 技能：报告生成
   - Note: Can perform revisions based on feedback
   - 说明：可根据反馈进行二次修改

8. **AgentH - Report Evaluator / 报告评估代理**
   - Role: Evaluates report quality and determines if revision is needed
   - 角色：评估报告质量并确定是否需要修改
   - Skills: Quality assessment
   - 技能：质量评估

### Workflow / 工作流

```
┌─────────────────────────────────────────────────────────────┐
│                     Workflow Execution                        │
└─────────────────────────────────────────────────────────────┘

Step 1: Information Collection (AgentA)
        ↓
        User dialogue → Collect comprehensive product info
        用户对话 → 收集全面的产品信息

Step 2: Parallel Data Collection (AgentB-E)
        ↓
        ├─→ AgentB: Industry analysis (行业分析)
        ├─→ AgentC: Similar name products (相似名称产品)
        ├─→ AgentD: Similar purpose products (相似用途产品)
        └─→ AgentE: Similar price products (相似价格产品)

Step 3: Integration Analysis (AgentF)
        ↓
        Synthesize data with culture & audience context
        结合企业文化和受众背景综合分析数据

Step 4: Report Generation (AgentG)
        ↓
        Generate comprehensive analysis report
        生成全面的分析报告

Step 5: Report Evaluation (AgentH)
        ↓
        Quality check and feedback generation
        质量检查和反馈生成

Step 6: Report Revision (AgentG - if needed)
        ↓
        Revise based on evaluator feedback
        根据评估反馈进行修改
        ↓
Final Report Delivery to User
最终报告交付给用户
```

## 项目结构 / Project Structure

```
CompetitivAnalysis/
├── src/
│   ├── interface/          # Base interfaces / 基础接口
│   │   ├── agent.py       # Agent interface / 代理接口
│   │   ├── skill.py       # Skill interface / 技能接口
│   │   └── workflow.py    # Workflow interface / 工作流接口
│   ├── agents/            # Agent implementations / 代理实现
│   │   ├── agent_a_info_collector.py
│   │   ├── agent_b_industry_analyzer.py
│   │   ├── agent_c_product_name_searcher.py
│   │   ├── agent_d_product_purpose_searcher.py
│   │   ├── agent_e_price_analyzer.py
│   │   ├── agent_f_integration_analyzer.py
│   │   ├── agent_g_report_generator.py
│   │   └── agent_h_report_evaluator.py
│   ├── skills/            # Skill implementations / 技能实现
│   │   ├── internet_search.py
│   │   ├── data_analysis.py
│   │   ├── information_extraction.py
│   │   └── report_generation.py
│   └── workflow/          # Workflow orchestration / 工作流编排
│       └── competitive_analysis_workflow.py
├── docs/                  # Documentation / 文档
│   ├── EXAMPLES.md        # Usage examples / 使用示例
│   ├── ARCHITECTURE.md    # Architecture docs / 架构文档
│   ├── DEVELOPMENT.md     # Development guide / 开发指南
│   ├── SECURITY.md        # Security advisories / 安全公告
│   ├── SUMMARY.md         # Project summary / 项目总结
│   └── FRONTEND.md        # Frontend options / 前端选项 ⭐ NEW
├── cli.py                 # CLI entry point / 命令行入口
├── pyproject.toml         # Project configuration / 项目配置
├── .env.example           # Environment variables template / 环境变量模板
└── README.md             # This file / 本文件
```

> ⚠️ **Important:** There is no `frontend/` directory because this project currently has no frontend.
> 
> ⚠️ **重要提示：** 没有 `frontend/` 目录，因为该项目目前没有前端。

## 安装 / Installation

### Prerequisites / 前置要求

- Python 3.12 or higher / Python 3.12 或更高版本
- pip or uv package manager / pip 或 uv 包管理器

### Install Dependencies / 安装依赖

```bash
# Clone the repository / 克隆仓库
git clone https://github.com/Olivia-lrh/CompetitivAnalysis.git
cd CompetitivAnalysis

# Create virtual environment / 创建虚拟环境
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies / 安装依赖
pip install -e .
```

### Configuration / 配置

```bash
# Copy environment template / 复制环境变量模板
cp .env.example .env

# Edit .env and add your API keys / 编辑 .env 并添加API密钥
# Required:
# - OPENAI_API_KEY or alternative LLM provider
# - TAVILY_API_KEY or SERPER_API_KEY for search
```

## 使用方法 / Usage

### Command Line Interface / 命令行界面

```bash
# Run the CLI tool / 运行命令行工具
python cli.py
```

### Programmatic Usage / 编程使用

```python
import asyncio
from src.workflow import CompetitiveAnalysisWorkflow

async def main():
    # Create workflow / 创建工作流
    workflow = CompetitiveAnalysisWorkflow()
    
    # Define user inputs / 定义用户输入
    user_messages = [
        "我们的行业是电子商务",
        "产品名称是 MyProduct",
        "这是一个SaaS平台",
        # ... more messages
    ]
    
    # Execute workflow / 执行工作流
    result = await workflow.execute({
        "user_messages": user_messages
    })
    
    # Get final report / 获取最终报告
    if result.status.value == "completed":
        final_report = result.results.get("final_report", {})
        print(final_report.get("report", ""))

asyncio.run(main())
```

## 核心功能 / Core Features

### 1. Multi-Round Dialogue / 多轮对话
- Natural conversation flow for information collection
- 自然的对话流程收集信息
- Context-aware question generation
- 上下文感知的问题生成

### 2. Parallel Processing / 并行处理
- Concurrent execution of data collection agents
- 数据收集代理的并发执行
- Efficient resource utilization
- 高效的资源利用

### 3. Comprehensive Analysis / 全面分析
- Industry landscape analysis / 行业格局分析
- Product comparison across multiple dimensions / 多维度产品对比
- Cultural and audience alignment / 文化和受众匹配

### 4. Quality Assurance / 质量保证
- Automated report evaluation / 自动报告评估
- Iterative improvement based on feedback / 基于反馈的迭代改进
- Professional report formatting / 专业报告格式

### 5. Extensible Architecture / 可扩展架构
- Modular agent design / 模块化代理设计
- Pluggable skill system / 可插拔技能系统
- Easy to add new agents or skills / 易于添加新代理或技能

## 技能系统 / Skills System

Each agent is equipped with relevant skills:

每个代理都配备了相关技能：

- **Internet Search Skill / 互联网搜索技能**: All agents have access to search capabilities
- **Data Analysis Skill / 数据分析技能**: For analyzing collected data
- **Information Extraction Skill / 信息提取技能**: For extracting structured data
- **Report Generation Skill / 报告生成技能**: For creating formatted reports

## 输出示例 / Output Example

The final report includes:

最终报告包括：

1. **Executive Summary / 执行摘要**
   - Key findings and recommendations
   - 关键发现和建议

2. **Company Profile / 公司概况**
   - Product information and positioning
   - 产品信息和定位

3. **Market Overview / 市场概览**
   - Industry landscape and trends
   - 行业格局和趋势

4. **Competitive Analysis / 竞品分析**
   - Detailed competitor comparison
   - 详细的竞争对手对比

5. **Strategic Insights / 战略洞察**
   - SWOT analysis
   - SWOT分析
   - Recommendations
   - 建议

6. **Conclusion / 结论**
   - Summary and next steps
   - 总结和下一步行动

## 开发 / Development

### Running Tests / 运行测试

```bash
pytest tests/
```

### Code Formatting / 代码格式化

```bash
black src/
ruff check src/
```

## 常见问题 / FAQ

### Q1: 这个项目的前端是使用什么语言和架构写的？
### Q1: What language and architecture is this project's frontend written in?

**A:** This project **currently has NO frontend**. It is a CLI (Command Line Interface) application written entirely in Python 3.12+.

**答：** 本项目**目前没有前端**。它是一个完全用 Python 3.12+ 编写的命令行界面（CLI）应用程序。

- **Current Interface / 当前界面:** Command Line (CLI) only
- **Language / 语言:** Python
- **Entry Point / 入口点:** `cli.py`
- **Output / 输出:** Text-based reports (Markdown)

**If you want to add a frontend**, please see the detailed guide in [docs/FRONTEND.md](docs/FRONTEND.md) which includes:
- Recommended tech stacks (React, Vue, Next.js)
- Implementation plans
- Code examples
- Architecture diagrams

**如果您想添加前端**，请参阅 [docs/FRONTEND.md](docs/FRONTEND.md) 中的详细指南，其中包括：
- 推荐的技术栈（React、Vue、Next.js）
- 实施计划
- 代码示例
- 架构图

---

### Q2: Can I use this project without programming knowledge?
### Q2: 我可以在不懂编程的情况下使用这个项目吗？

**A:** Currently, **no**. The project requires:
- Basic Python knowledge to run the CLI
- Ability to configure `.env` files
- Terminal/command line usage

**答：** 目前**不行**。该项目需要：
- 基本的Python知识来运行CLI
- 配置 `.env` 文件的能力
- 终端/命令行使用

**Future:** A web frontend would make it accessible to non-technical users.

**未来：** Web前端将使非技术用户也能使用。

---

### Q3: How do I get a graphical interface?
### Q3: 如何获得图形界面？

**A:** You have three options:

**答：** 您有三个选择：

1. **Wait for future development** - A web frontend may be added later
   **等待未来开发** - 可能稍后添加Web前端

2. **Build your own frontend** - Follow the guide in [docs/FRONTEND.md](docs/FRONTEND.md)
   **构建自己的前端** - 遵循 [docs/FRONTEND.md](docs/FRONTEND.md) 中的指南

3. **Use programmatically** - Integrate the Python API into your own application
   **以编程方式使用** - 将Python API集成到您自己的应用程序中

---

### Q4: What interface types are supported?
### Q4: 支持哪些接口类型？

**A:** Currently supported / 当前支持：
- ✅ **CLI (Command Line Interface)** - `python cli.py`
- ✅ **Python API** - Import and use programmatically

Not yet available / 尚不可用：
- ❌ Web UI (Browser-based interface)
- ❌ Desktop App (Electron/Tauri)
- ❌ Mobile App (iOS/Android)
- ❌ REST API (FastAPI server)

See [docs/FRONTEND.md](docs/FRONTEND.md) for implementation guides.

---

### Q5: Is this project only for developers?
### Q5: 这个项目仅适用于开发人员吗？

**A:** Currently, **yes**. The CLI interface requires:
- Python installation and environment setup
- Command line proficiency
- API key configuration

**答：** 目前**是的**。CLI界面需要：
- Python安装和环境设置
- 命令行熟练度
- API密钥配置

However, the architecture is designed to be easily extended with a user-friendly frontend in the future.

然而，该架构设计为在未来可以轻松扩展为用户友好的前端。

---

## 贡献 / Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

欢迎贡献！请随时提交Pull Request。

## 许可证 / License

This project is licensed under the MIT License.

本项目采用MIT许可证。

## 致谢 / Acknowledgments

This project is inspired by and based on the architecture of [cooragent](https://github.com/LeapLabTHU/cooragent).

本项目受 [cooragent](https://github.com/LeapLabTHU/cooragent) 架构启发并基于其开发。

## 联系方式 / Contact

For questions or support, please open an issue on GitHub.

如有问题或需要支持，请在GitHub上开issue。
