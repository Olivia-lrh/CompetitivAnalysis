# 使用示例 / Usage Examples

## Example 1: Basic CLI Usage / 基础命令行使用

### English

```bash
# Run the CLI tool
python cli.py
```

The tool will guide you through a series of questions to collect information about your product. It uses pre-defined example responses in the demo mode.

### 中文

```bash
# 运行命令行工具
python cli.py
```

工具将引导您回答一系列问题，收集有关您产品的信息。在演示模式下，它使用预定义的示例响应。

---

## Example 2: Programmatic Usage / 编程使用

### English

Create a Python script to use the competitive analysis system programmatically:

```python
import asyncio
from src.workflow import CompetitiveAnalysisWorkflow

async def analyze_my_product():
    # Create workflow
    workflow = CompetitiveAnalysisWorkflow()
    
    # Prepare user input
    user_messages = [
        "Our industry is e-commerce platform",
        "Product name is ShopEasy",
        "It's a SaaS platform for SMEs to build online stores",
        "Target audience is small and medium business owners",
        "Price range is $99-$499 per month",
        "Company culture focuses on customer success",
        "We need to understand our competitive position"
    ]
    
    # Run analysis
    result = await workflow.execute({
        "user_messages": user_messages
    })
    
    # Check results
    if result.status.value == "completed":
        print("Analysis completed successfully!")
        
        # Get final report
        final_report = result.results.get("final_report", {})
        report_content = final_report.get("report", "")
        
        # Save report to file
        with open("competitive_analysis_report.md", "w", encoding="utf-8") as f:
            f.write(report_content)
        
        print("Report saved to: competitive_analysis_report.md")
        
        # Get evaluation scores
        evaluation = result.results.get("evaluation", {})
        print(f"\nReport Quality Score: {evaluation.get('overall_score', 0):.2f}")
        
    else:
        print(f"Analysis failed: {result.error}")

# Run
asyncio.run(analyze_my_product())
```

### 中文

创建Python脚本以编程方式使用竞品分析系统：

```python
import asyncio
from src.workflow import CompetitiveAnalysisWorkflow

async def analyze_my_product():
    # 创建工作流
    workflow = CompetitiveAnalysisWorkflow()
    
    # 准备用户输入
    user_messages = [
        "我们的行业是电子商务平台",
        "产品名称是 ShopEasy",
        "这是一个为中小企业提供在线商店的SaaS平台",
        "目标受众是中小型企业主",
        "价格范围是每月99-499美元",
        "企业文化注重客户成功",
        "我们需要了解我们的竞争地位"
    ]
    
    # 运行分析
    result = await workflow.execute({
        "user_messages": user_messages
    })
    
    # 检查结果
    if result.status.value == "completed":
        print("分析成功完成！")
        
        # 获取最终报告
        final_report = result.results.get("final_report", {})
        report_content = final_report.get("report", "")
        
        # 保存报告到文件
        with open("竞品分析报告.md", "w", encoding="utf-8") as f:
            f.write(report_content)
        
        print("报告已保存到: 竞品分析报告.md")
        
        # 获取评估分数
        evaluation = result.results.get("evaluation", {})
        print(f"\n报告质量分数: {evaluation.get('overall_score', 0):.2f}")
        
    else:
        print(f"分析失败: {result.error}")

# 运行
asyncio.run(analyze_my_product())
```

---

## Example 3: Custom Agent Usage / 自定义代理使用

### English

Use individual agents for specific tasks:

```python
import asyncio
from src.agents import (
    InformationCollectorAgent,
    IndustryAnalyzerAgent,
    ReportGeneratorAgent
)

async def custom_workflow():
    # 1. Collect information
    collector = InformationCollectorAgent()
    
    messages = [
        "Industry: Healthcare Technology",
        "Product: HealthTrack Pro",
        "Purpose: Patient health monitoring system"
    ]
    
    info_result = None
    for msg in messages:
        info_result = await collector.process({"message": msg})
    
    collected_info = collector.get_collected_info()
    print("Collected Info:", collected_info)
    
    # 2. Analyze industry
    analyzer = IndustryAnalyzerAgent()
    industry_result = await analyzer.process({
        "industry": collected_info.get("industry", "")
    })
    
    print("Industry Analysis:", industry_result.data)
    
    # 3. Generate report (with mock data)
    generator = ReportGeneratorAgent()
    report_result = await generator.process({
        "user_info": collected_info,
        "integrated_analysis": {
            "combined_data": industry_result.data,
        },
        "strategic_insights": {
            "strengths": ["Innovation", "Strong team"],
            "opportunities": ["Growing market"],
            "recommendations": ["Focus on differentiation"]
        }
    })
    
    print("\nGenerated Report:")
    print(report_result.data.get("report", "")[:500])

asyncio.run(custom_workflow())
```

---

## Tips / 提示

### English

1. **API Keys**: Make sure to set up your API keys in `.env` file before running
2. **Customization**: You can extend or modify agents and skills to fit your specific needs
3. **Output**: Reports are generated in Markdown format by default
4. **Performance**: Parallel execution of agents B-E improves overall workflow speed

### 中文

1. **API密钥**: 运行前确保在 `.env` 文件中设置API密钥
2. **自定义**: 您可以扩展或修改代理和技能以适应特定需求
3. **输出**: 报告默认以Markdown格式生成
4. **性能**: 代理B-E的并行执行提高了整体工作流速度
