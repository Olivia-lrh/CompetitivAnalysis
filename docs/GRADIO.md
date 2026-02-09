# Gradio Web Interface Guide / Gradio Web界面指南

## 🌐 Overview / 概述

This document provides a comprehensive guide to using the Gradio web interface for the Competitive Analysis tool.

本文档提供了使用竞品分析工具Gradio Web界面的全面指南。

---

## 🚀 Quick Start / 快速开始

### 1. Installation / 安装

```bash
# Install the project with dependencies
pip install -e .

# Gradio is automatically installed as a dependency
```

### 2. Start the Server / 启动服务器

```bash
# Start the Gradio web interface
python gradio_app.py

# You should see output like:
# ============================================================
# 🚀 Starting Gradio Competitive Analysis Tool
# 正在启动Gradio竞品分析工具
# ============================================================
#
# Running on local URL:  http://127.0.0.1:7860
```

### 3. Open in Browser / 在浏览器中打开

```
http://localhost:7860
```

---

## 📋 Interface Layout / 界面布局

### Left Panel: Input Form / 左侧面板：输入表单

**Required Fields / 必填字段:**
- 🏢 **Industry / 行业**: Your business industry
  - Example: 电子商务、医疗科技、教育
  - Example: E-commerce, Healthcare, Education

- 📦 **Product Name / 产品名称**: Your product's name
  - Example: ShopEasy, HealthTrack Pro

**Optional Fields / 可选字段:**
- 🎯 **Product Purpose / 产品用途**: What your product does
- 👥 **Target Audience / 目标受众**: Who uses your product
- 💰 **Price Range / 价格范围**: Product pricing
- 🌟 **Company Culture / 企业文化**: Your company values
- 📋 **User Needs / 用户需求**: What you want to learn

### Right Panel: Results / 右侧面板：结果

- **Status / 状态**: Current analysis status
- **Summary / 摘要**: Quick overview of results
- **Quality Score / 质量分数**: Report quality rating (0-1)
- **Full Report / 完整报告**: Detailed analysis (Markdown)

---

## 🎯 How to Use / 使用方法

### Step 1: Fill in the Form / 第1步：填写表单

1. Enter your **Industry** (required)
   - 输入您的**行业**（必填）

2. Enter your **Product Name** (required)
   - 输入您的**产品名称**（必填）

3. Fill in other fields (optional but recommended)
   - 填写其他字段（可选但推荐）

### Step 2: Start Analysis / 第2步：开始分析

Click the **"🚀 开始分析 / Start Analysis"** button

点击 **"🚀 开始分析 / Start Analysis"** 按钮

### Step 3: Wait for Results / 第3步：等待结果

- The system will process through 8 AI agents
- 系统将通过8个AI代理进行处理
- This may take several minutes
- 这可能需要几分钟时间

### Step 4: Review Report / 第4步：查看报告

- Check the status message
- 查看状态消息
- Review the summary
- 查看摘要
- Read the full report
- 阅读完整报告

---

## 💡 Tips & Tricks / 技巧与窍门

### For Best Results / 获得最佳结果

1. **Be Specific / 具体说明**
   - Provide detailed information in all fields
   - 在所有字段中提供详细信息
   - More details = better analysis
   - 更多细节 = 更好的分析

2. **Use Examples / 使用示例**
   - Click on the example inputs at the bottom
   - 点击底部的示例输入
   - See how to format your inputs
   - 查看如何格式化输入

3. **Clear and Retry / 清除并重试**
   - Use the "🔄 清除 / Clear" button to reset
   - 使用"🔄 清除 / Clear"按钮重置
   - Try different inputs to compare results
   - 尝试不同的输入以比较结果

### Language Support / 语言支持

You can input in **Chinese** or **English**:
- 中文输入：系统会自动识别
- English input: System auto-detects
- Mixed input: Also works!
- 混合输入：也可以！

---

## 🏗️ Technical Architecture / 技术架构

### Workflow / 工作流程

```
User Input (Gradio Forms)
         ↓
  Validation & Formatting
         ↓
CompetitiveAnalysisWorkflow
         ↓
┌────────────────────────────┐
│ Step 1: AgentA             │ Information Collection
│ Step 2: AgentB-E (Parallel)│ Data Collection
│ Step 3: AgentF             │ Integration
│ Step 4: AgentG             │ Report Generation
│ Step 5: AgentH             │ Evaluation
│ Step 6: AgentG (if needed) │ Revision
└────────────────────────────┘
         ↓
  Results Display (Gradio)
```

### Technology Stack / 技术栈

- **Frontend**: Gradio 6.x (Python-based)
- **Backend**: Python 3.12+
- **AI Agents**: 8 specialized agents
- **Async**: asyncio for workflow execution

---

## 🎨 Customization / 自定义

### Modify Port / 修改端口

Edit `gradio_app.py`:

```python
demo.launch(
    server_name="0.0.0.0",
    server_port=7860,  # Change this
    share=False,
    show_error=True,
    theme=gr.themes.Soft()
)
```

### Enable Sharing / 启用分享

Set `share=True` to get a public URL:

```python
demo.launch(
    share=True,  # Enable public sharing
    ...
)
```

### Change Theme / 更改主题

```python
demo.launch(
    theme=gr.themes.Glass(),  # or Base(), Monochrome(), etc.
    ...
)
```

---

## 🔧 Troubleshooting / 故障排除

### Port Already in Use / 端口已被占用

**Error:** `Address already in use`

**Solution:**
```bash
# Find process using port 7860
lsof -i :7860

# Kill the process
kill <PID>

# Or use a different port in gradio_app.py
```

### Import Errors / 导入错误

**Error:** `ModuleNotFoundError: No module named 'gradio'`

**Solution:**
```bash
pip install gradio>=4.0.0
```

### Workflow Errors / 工作流错误

**Error:** Analysis fails or times out

**Solutions:**
1. Check your `.env` file has API keys
2. Ensure all required fields are filled
3. Check network connection
4. Review error messages in terminal

---

## 📊 Example Usage / 使用示例

### Example 1: E-commerce Platform / 电子商务平台

**Inputs:**
- Industry: 电子商务平台
- Product Name: ShopEasy
- Product Purpose: 为中小企业提供在线商店解决方案的SaaS平台
- Target Audience: 中小型企业主和创业者
- Price Range: 每月99-499元
- Company Culture: 注重客户成功和创新
- User Needs: 了解市场竞争情况并找到差异化定位

**Expected Output:**
- Report on e-commerce competitors
- Industry analysis
- Price positioning
- Strategic recommendations

### Example 2: Healthcare Technology

**Inputs:**
- Industry: Healthcare Technology
- Product Name: HealthTrack Pro
- Product Purpose: Patient health monitoring system for hospitals
- Target Audience: Healthcare providers and hospital administrators
- Price Range: $199-$999 per month
- Company Culture: Innovation in healthcare delivery
- User Needs: Understand competitive landscape in health tech

**Expected Output:**
- Healthcare industry analysis
- Competitor comparison
- Technology trends
- Market positioning advice

---

## 🚀 Advanced Features / 高级功能

### Programmatic Access / 编程访问

You can also use the functions programmatically:

```python
from gradio_app import run_analysis

result = run_analysis(
    industry="Healthcare",
    product_name="MyProduct",
    product_purpose="Patient monitoring",
    target_audience="Hospitals",
    price_range="$500/month",
    company_culture="Innovation",
    user_needs="Market analysis"
)

status, summary, score, report = result
print(report)
```

### Integration with Other Tools / 与其他工具集成

The Gradio interface can be embedded in:
- Jupyter notebooks
- Other web applications
- Custom dashboards

Example:
```python
from gradio_app import create_gradio_interface

demo = create_gradio_interface()
demo.launch(share=True)  # Get shareable link
```

---

## 📝 Best Practices / 最佳实践

### For Users / 对于用户

1. ✅ Fill all optional fields for better results
2. ✅ Use specific, detailed descriptions
3. ✅ Review the summary before reading full report
4. ✅ Save important reports for future reference

### For Developers / 对于开发者

1. ✅ Keep Gradio updated: `pip install --upgrade gradio`
2. ✅ Monitor server logs for errors
3. ✅ Test with various input combinations
4. ✅ Consider adding authentication for production use

---

## 🔗 Related Documentation / 相关文档

- [README.md](../README.md) - Project overview
- [FRONTEND.md](FRONTEND.md) - Other frontend options
- [EXAMPLES.md](EXAMPLES.md) - More usage examples
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture

---

## 🤝 Support / 支持

### Getting Help / 获取帮助

- 📖 Check documentation first
- 🐛 Open GitHub issue for bugs
- 💬 Discussion for questions
- 📧 Email for private inquiries

### Feedback / 反馈

We welcome feedback on the Gradio interface!

欢迎对Gradio界面提供反馈！

- Suggest improvements
- Report bugs
- Request features
- Share your experience

---

**Last Updated:** 2024-02-09  
**Gradio Version:** 6.5.1  
**Status:** ✅ Production Ready
