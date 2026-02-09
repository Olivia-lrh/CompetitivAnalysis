# Architecture Documentation / 架构文档

## System Overview / 系统概述

The Competitive Analysis system is built on a multi-agent architecture where specialized agents collaborate to complete a comprehensive market analysis workflow.

竞品分析系统建立在多智能体架构上，专业代理协作完成全面的市场分析工作流。

## Architecture Diagram / 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Competitive Analysis System                   │
│                         竞品分析系统                              │
└─────────────────────────────────────────────────────────────────┘

                              ┌──────────┐
                              │   User   │
                              │  用户     │
                              └────┬─────┘
                                   │
                                   ▼
                    ┌──────────────────────────┐
                    │   CLI / API Interface    │
                    │   命令行/API接口          │
                    └──────────┬───────────────┘
                               │
                               ▼
              ┌────────────────────────────────────┐
              │   Workflow Orchestrator             │
              │   工作流编排器                       │
              │   - Task coordination               │
              │   - Data flow management            │
              │   - Error handling                  │
              └────────────────┬───────────────────┘
                               │
          ┌────────────────────┴────────────────────┐
          │                                          │
          ▼                                          ▼
┌─────────────────┐                      ┌─────────────────┐
│   Agent Layer   │                      │   Skills Layer  │
│   代理层         │◄────────────────────►│   技能层        │
└─────────────────┘                      └─────────────────┘
```

## Component Layers / 组件层次

### 1. Interface Layer / 接口层

```
┌─────────────────────────────────────────────┐
│          Interface Definitions              │
│          接口定义                            │
├─────────────────────────────────────────────┤
│  • BaseAgent         (agent.py)             │
│  • BaseSkill         (skill.py)             │
│  • BaseWorkflow      (workflow.py)          │
│                                             │
│  Defines contracts for all components      │
│  定义所有组件的契约                         │
└─────────────────────────────────────────────┘
```

### 2. Agent Layer / 代理层

```
┌────────────────────────────────────────────────────────────┐
│                       8 Specialized Agents                  │
│                       8个专业代理                           │
└────────────────────────────────────────────────────────────┘

    ┌──────────────┐
    │   AgentA     │  Information Collector (信息收集)
    │   多轮对话    │  • Dialogue management
    └──────┬───────┘  • Context tracking
           │
           ▼
    ┌──────────────────────────────────────────┐
    │     Parallel Data Collection             │
    │     并行数据收集                          │
    └──────────────────────────────────────────┘
           │
    ┌──────┴─────────────────────────────┐
    │      │            │          │      │
    ▼      ▼            ▼          ▼      ▼
┌──────┐ ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐
│AgentB│ │Agent│  │Agent│  │Agent│  │Agent│
│行业   │ │  C  │  │  D  │  │  E  │  │  F  │
│分析   │ │产品 │  │用途 │  │价格 │  │整合 │
│      │ │名称 │  │搜索 │  │分析 │  │分析 │
└──┬───┘ └──┬──┘  └──┬──┘  └──┬──┘  └──┬──┘
   │        │         │         │        │
   └────────┴─────────┴─────────┴────────┘
                      │
                      ▼
              ┌──────────────┐
              │   AgentG     │  Report Generator (报告生成)
              │   报告生成    │  • Synthesis
              └──────┬───────┘  • Formatting
                     │
                     ▼
              ┌──────────────┐
              │   AgentH     │  Report Evaluator (报告评估)
              │   报告评估    │  • Quality check
              └──────┬───────┘  • Feedback
                     │
                     ▼
          ┌──────────────────────┐
          │  Revision Loop        │
          │  (if needed)          │
          │  修订循环（如需要）   │
          └───────────────────────┘
```

### 3. Skills Layer / 技能层

```
┌─────────────────────────────────────────────────────┐
│                    Core Skills                       │
│                    核心技能                          │
└─────────────────────────────────────────────────────┘

┌──────────────────┐  ┌──────────────────┐
│ Internet Search  │  │  Data Analysis   │
│ 互联网搜索        │  │  数据分析         │
│                  │  │                  │
│ • Multi-engine   │  │ • Pattern detect │
│ • Query optimize │  │ • Insight extract│
└──────────────────┘  └──────────────────┘

┌──────────────────┐  ┌──────────────────┐
│ Info Extraction  │  │ Report Generate  │
│ 信息提取          │  │ 报告生成          │
│                  │  │                  │
│ • Structured data│  │ • Markdown       │
│ • Entity extract │  │ • Professional   │
└──────────────────┘  └──────────────────┘
```

## Data Flow / 数据流

```
User Input (用户输入)
    │
    ▼
Information Collection (信息收集)
    │
    ├──→ user_info {
    │      industry: string
    │      product_name: string
    │      product_purpose: string
    │      target_audience: string
    │      price_range: string
    │      company_culture: string
    │      user_needs: string
    │    }
    │
    ▼
Parallel Collection (并行收集)
    │
    ├──→ industry_data
    ├──→ name_similar_products
    ├──→ purpose_similar_products
    └──→ price_similar_products
    │
    ▼
Integration (整合)
    │
    ├──→ integrated_analysis
    └──→ strategic_insights
    │
    ▼
Report Generation (报告生成)
    │
    └──→ preliminary_report
    │
    ▼
Evaluation (评估)
    │
    ├──→ evaluation_scores
    └──→ feedback
    │
    ▼
Revision (if needed) (修订)
    │
    └──→ final_report
    │
    ▼
Output to User (输出给用户)
```

## Agent Communication / 代理通信

### Message Structure / 消息结构

```python
AgentMessage {
    sender: str           # Agent ID
    receiver: str         # Target agent ID
    content: dict        # Message payload
    message_type: str    # Type of message
    timestamp: str       # ISO timestamp
}
```

### Response Structure / 响应结构

```python
AgentResponse {
    agent_id: str        # Responding agent
    success: bool        # Operation status
    data: dict          # Response data
    error: str | None   # Error message if failed
    metadata: dict      # Additional information
}
```

## Workflow States / 工作流状态

```
PENDING → RUNNING → COMPLETED
            ↓
          FAILED
            ↓
          PAUSED (可选)
```

## Extensibility / 可扩展性

### Adding New Agents / 添加新代理

```python
from src.interface.agent import BaseAgent, AgentConfig

class CustomAgent(BaseAgent):
    def __init__(self):
        config = AgentConfig(
            agent_id="custom_agent",
            agent_name="Custom Agent",
            agent_role=AgentRole.CUSTOM,
            description="Custom functionality",
            system_prompt="...",
            skills=["skill1", "skill2"]
        )
        super().__init__(config)
    
    async def process(self, input_data):
        # Implementation
        pass
    
    def get_capabilities(self):
        return ["capability1", "capability2"]
```

### Adding New Skills / 添加新技能

```python
from src.interface.skill import BaseSkill, SkillConfig

class CustomSkill(BaseSkill):
    def __init__(self):
        config = SkillConfig(
            skill_id="custom_skill",
            skill_name="Custom Skill",
            description="Custom functionality",
            parameters={...}
        )
        super().__init__(config)
    
    async def execute(self, **kwargs):
        # Implementation
        return SkillResult(...)
```

## Performance Considerations / 性能考虑

### Parallel Execution / 并行执行

- Agents B, C, D, E execute in parallel
- 代理B、C、D、E并行执行
- Reduces total workflow time by ~4x
- 总工作流时间减少约4倍

### Caching Strategy / 缓存策略

- Search results can be cached
- 搜索结果可以缓存
- Reduces redundant API calls
- 减少冗余API调用

### Error Handling / 错误处理

- Graceful degradation
- 优雅降级
- Retry mechanisms for network failures
- 网络故障重试机制
- Partial results still useful
- 部分结果仍然有用

## Security / 安全性

- API keys stored in environment variables
- API密钥存储在环境变量中
- No sensitive data in logs
- 日志中无敏感数据
- Input validation at all entry points
- 所有入口点的输入验证

## Monitoring / 监控

- Progress tracking through workflow steps
- 通过工作流步骤跟踪进度
- Agent execution metrics
- 代理执行指标
- Report quality scores
- 报告质量分数
