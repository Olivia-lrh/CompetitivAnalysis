# Development Guide / 开发指南

## Setup / 设置

### 1. Install Dependencies / 安装依赖

```bash
# Using pip / 使用 pip
cd CompetitivAnalysis
pip install -e .

# Or using uv (faster) / 或使用 uv（更快）
uv pip install -e .
```

### 2. Configure Environment / 配置环境

```bash
# Copy environment template / 复制环境模板
cp .env.example .env

# Edit .env file / 编辑 .env 文件
# Add your API keys:
# - OPENAI_API_KEY
# - TAVILY_API_KEY or SERPER_API_KEY
```

### 3. Verify Installation / 验证安装

```bash
# Test import / 测试导入
python -c "from src.workflow import CompetitiveAnalysisWorkflow; print('OK')"
```

## Development Workflow / 开发工作流

### Running Tests / 运行测试

```bash
# Run all tests / 运行所有测试
pytest tests/ -v

# Run with coverage / 运行并显示覆盖率
pytest tests/ --cov=src --cov-report=html
```

### Code Quality / 代码质量

```bash
# Format code / 格式化代码
black src/ tests/

# Lint code / 检查代码
ruff check src/ tests/

# Type checking (if mypy is installed) / 类型检查
mypy src/
```

## Project Structure Details / 项目结构详情

### Interface Layer / 接口层

Located in `src/interface/`:

位于 `src/interface/`:

- **agent.py**: Defines `BaseAgent` class and agent-related types
  - 定义 `BaseAgent` 类和代理相关类型
- **skill.py**: Defines `BaseSkill` class and skill interfaces
  - 定义 `BaseSkill` 类和技能接口
- **workflow.py**: Defines `BaseWorkflow` class and workflow types
  - 定义 `BaseWorkflow` 类和工作流类型

### Agent Layer / 代理层

Located in `src/agents/`:

位于 `src/agents/`:

Each agent file follows the naming pattern `agent_X_name.py`:

每个代理文件遵循命名模式 `agent_X_name.py`:

- **agent_a_info_collector.py**: Information collection through dialogue
  - 通过对话收集信息
- **agent_b_industry_analyzer.py**: Industry and competitor analysis
  - 行业和竞争对手分析
- **agent_c_product_name_searcher.py**: Similar name product search
  - 相似名称产品搜索
- **agent_d_product_purpose_searcher.py**: Similar purpose product search
  - 相似用途产品搜索
- **agent_e_price_analyzer.py**: Price-based product analysis
  - 基于价格的产品分析
- **agent_f_integration_analyzer.py**: Data integration and synthesis
  - 数据整合和综合
- **agent_g_report_generator.py**: Report generation
  - 报告生成
- **agent_h_report_evaluator.py**: Report quality evaluation
  - 报告质量评估

### Skills Layer / 技能层

Located in `src/skills/`:

位于 `src/skills/`:

- **internet_search.py**: Web search capabilities
  - 网络搜索能力
- **data_analysis.py**: Data analysis and insights
  - 数据分析和洞察
- **information_extraction.py**: Structured data extraction
  - 结构化数据提取
- **report_generation.py**: Report formatting and generation
  - 报告格式化和生成

### Workflow Layer / 工作流层

Located in `src/workflow/`:

位于 `src/workflow/`:

- **competitive_analysis_workflow.py**: Main workflow orchestration
  - 主工作流编排

## Adding New Components / 添加新组件

### Add a New Agent / 添加新代理

1. Create a new file in `src/agents/`:
   在 `src/agents/` 中创建新文件:

```python
# src/agents/agent_i_custom.py
from typing import Dict, Any, List
from ..interface.agent import BaseAgent, AgentConfig, AgentRole, AgentResponse

class CustomAgent(BaseAgent):
    def __init__(self, agent_id: str = "agent_i"):
        config = AgentConfig(
            agent_id=agent_id,
            agent_name="Custom Agent",
            agent_role=AgentRole.CUSTOM,  # Add to AgentRole enum
            description="Custom agent description",
            system_prompt="Custom system prompt...",
            skills=["skill1", "skill2"],
        )
        super().__init__(config)
    
    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        # Implement custom logic
        return AgentResponse(
            agent_id=self.agent_id,
            success=True,
            data={"result": "processed"},
            metadata={}
        )
    
    def get_capabilities(self) -> List[str]:
        return ["capability1", "capability2"]
```

2. Add to `src/agents/__init__.py`:
   添加到 `src/agents/__init__.py`:

```python
from .agent_i_custom import CustomAgent

__all__ = [
    # ... existing agents
    "CustomAgent",
]
```

3. Integrate into workflow (if needed):
   集成到工作流（如需要）:

```python
# In src/workflow/competitive_analysis_workflow.py
self.agents["custom"] = CustomAgent()
```

### Add a New Skill / 添加新技能

1. Create a new file in `src/skills/`:
   在 `src/skills/` 中创建新文件:

```python
# src/skills/custom_skill.py
from typing import Dict, Any
from ..interface.skill import BaseSkill, SkillConfig, SkillResult

class CustomSkill(BaseSkill):
    def __init__(self):
        config = SkillConfig(
            skill_id="custom_skill",
            skill_name="Custom Skill",
            description="Custom skill description",
            parameters={
                "param1": {"type": "string", "required": True},
                "param2": {"type": "integer", "required": False},
            }
        )
        super().__init__(config)
    
    async def execute(self, param1: str, param2: int = 0, **kwargs) -> SkillResult:
        try:
            # Implement custom logic
            result = {"output": f"Processed {param1} with {param2}"}
            
            return SkillResult(
                success=True,
                data=result,
                metadata={"processed": True}
            )
        except Exception as e:
            return SkillResult(
                success=False,
                data={},
                error=str(e)
            )
```

2. Add to `src/skills/__init__.py`:
   添加到 `src/skills/__init__.py`:

```python
from .custom_skill import CustomSkill

__all__ = [
    # ... existing skills
    "CustomSkill",
]
```

3. Use in agents:
   在代理中使用:

```python
from ..skills import CustomSkill

class MyAgent(BaseAgent):
    def __init__(self):
        # ...
        self.add_skill(CustomSkill())
```

## Testing / 测试

### Unit Tests / 单元测试

Create tests in `tests/` directory:

在 `tests/` 目录创建测试:

```python
# tests/test_agent_a.py
import pytest
from src.agents import InformationCollectorAgent

@pytest.mark.asyncio
async def test_info_collector():
    agent = InformationCollectorAgent()
    
    response = await agent.process({
        "message": "Our industry is e-commerce"
    })
    
    assert response.success
    assert "industry" in agent.get_collected_info()
```

### Integration Tests / 集成测试

```python
# tests/test_workflow.py
import pytest
from src.workflow import CompetitiveAnalysisWorkflow

@pytest.mark.asyncio
async def test_workflow_execution():
    workflow = CompetitiveAnalysisWorkflow()
    
    result = await workflow.execute({
        "user_messages": ["Test industry", "Test product"]
    })
    
    assert result.status.value in ["completed", "failed"]
```

## Debugging / 调试

### Enable Debug Logging / 启用调试日志

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Inspect Agent State / 检查代理状态

```python
agent = InformationCollectorAgent()
print(agent.get_info())
print(agent.get_collected_info())
```

### Workflow Progress / 工作流进度

```python
workflow = CompetitiveAnalysisWorkflow()
print(workflow.get_progress())
```

## Best Practices / 最佳实践

### 1. Error Handling / 错误处理

Always handle exceptions in agent `process` methods:

始终在代理的 `process` 方法中处理异常:

```python
async def process(self, input_data):
    try:
        # Processing logic
        return AgentResponse(success=True, data=result)
    except Exception as e:
        return AgentResponse(success=False, data={}, error=str(e))
```

### 2. Input Validation / 输入验证

Validate input data before processing:

处理前验证输入数据:

```python
async def process(self, input_data):
    required_field = input_data.get("required_field")
    if not required_field:
        return AgentResponse(
            success=False,
            data={},
            error="required_field is missing"
        )
```

### 3. Type Hints / 类型提示

Use type hints for better code clarity:

使用类型提示提高代码清晰度:

```python
async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
    pass
```

### 4. Documentation / 文档

Document your agents and skills:

为代理和技能编写文档:

```python
class MyAgent(BaseAgent):
    """
    Brief description
    简要描述
    
    Detailed description of what this agent does.
    详细描述此代理的功能。
    
    Args:
        agent_id: Unique identifier
        
    Example:
        agent = MyAgent()
        result = await agent.process(data)
    """
```

## Performance Optimization / 性能优化

### 1. Parallel Execution / 并行执行

Use `asyncio.gather` for concurrent operations:

使用 `asyncio.gather` 进行并发操作:

```python
results = await asyncio.gather(
    agent_b.process(data),
    agent_c.process(data),
    agent_d.process(data),
    agent_e.process(data),
)
```

### 2. Caching / 缓存

Cache frequently accessed data:

缓存频繁访问的数据:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_data(key: str):
    # Expensive operation
    return data
```

### 3. Resource Management / 资源管理

Properly close resources:

正确关闭资源:

```python
async with httpx.AsyncClient() as client:
    response = await client.get(url)
```

## Troubleshooting / 故障排除

### Common Issues / 常见问题

1. **Module not found / 模块未找到**
   - Ensure you installed with `pip install -e .`
   - 确保使用 `pip install -e .` 安装

2. **API key errors / API密钥错误**
   - Check `.env` file exists and has correct keys
   - 检查 `.env` 文件存在且有正确的密钥

3. **Import errors / 导入错误**
   - Verify Python version is 3.12+
   - 验证Python版本为3.12+

4. **Async errors / 异步错误**
   - Use `asyncio.run()` for top-level async functions
   - 对顶级异步函数使用 `asyncio.run()`

## Contributing / 贡献

See `CONTRIBUTING.md` for contribution guidelines.

查看 `CONTRIBUTING.md` 了解贡献指南。
