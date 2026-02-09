#!/usr/bin/env python3
"""
Gradio Frontend for Competitive Analysis
竞品分析Gradio前端
"""
import asyncio
import gradio as gr
from typing import Dict, Any, Optional
from src.workflow import CompetitiveAnalysisWorkflow


def create_user_messages(
    industry: str,
    product_name: str,
    product_purpose: str,
    target_audience: str,
    price_range: str,
    company_culture: str,
    user_needs: str
) -> list:
    """Create user messages list from form inputs"""
    messages = []
    
    if industry:
        messages.append(f"我们的行业是{industry}" if is_chinese(industry) else f"Our industry is {industry}")
    if product_name:
        messages.append(f"产品名称是{product_name}" if is_chinese(product_name) else f"Product name is {product_name}")
    if product_purpose:
        messages.append(f"产品用途：{product_purpose}" if is_chinese(product_purpose) else f"Product purpose: {product_purpose}")
    if target_audience:
        messages.append(f"目标受众：{target_audience}" if is_chinese(target_audience) else f"Target audience: {target_audience}")
    if price_range:
        messages.append(f"价格范围：{price_range}" if is_chinese(price_range) else f"Price range: {price_range}")
    if company_culture:
        messages.append(f"企业文化：{company_culture}" if is_chinese(company_culture) else f"Company culture: {company_culture}")
    if user_needs:
        messages.append(f"用户需求：{user_needs}" if is_chinese(user_needs) else f"User needs: {user_needs}")
    
    return messages


def is_chinese(text: str) -> bool:
    """Check if text contains Chinese characters"""
    for char in text:
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False


async def run_analysis_async(
    industry: str,
    product_name: str,
    product_purpose: str,
    target_audience: str,
    price_range: str,
    company_culture: str,
    user_needs: str,
    progress=gr.Progress()
) -> tuple:
    """
    Run competitive analysis workflow
    运行竞品分析工作流
    """
    try:
        # Validate inputs
        if not industry or not product_name:
            return (
                "错误：行业和产品名称是必填项 / Error: Industry and Product Name are required",
                "",
                0.0,
                ""
            )
        
        # Create user messages
        user_messages = create_user_messages(
            industry, product_name, product_purpose,
            target_audience, price_range, company_culture, user_needs
        )
        
        progress(0.1, desc="初始化工作流 / Initializing workflow...")
        
        # Create and run workflow
        workflow = CompetitiveAnalysisWorkflow()
        
        progress(0.2, desc="Step 1: 收集信息 / Collecting information...")
        
        # Execute workflow
        result = await workflow.execute({
            "user_messages": user_messages
        })
        
        progress(1.0, desc="完成 / Complete!")
        
        # Process results
        if result.status.value == "completed":
            final_report = result.results.get("final_report", {})
            report_content = final_report.get("report", "No report generated")
            
            evaluation = result.results.get("evaluation", {})
            overall_score = evaluation.get("overall_score", 0.0)
            
            # Get collected info for summary
            user_info = result.results.get("user_info", {})
            summary = f"""
### 分析摘要 / Analysis Summary

**状态 / Status:** {result.status.value}
**完成步骤 / Steps Completed:** {result.steps_completed}/{result.total_steps}
**报告质量分数 / Report Quality Score:** {overall_score:.2f}

**收集的信息 / Collected Information:**
- 行业 / Industry: {user_info.get('industry', 'N/A')}
- 产品名称 / Product Name: {user_info.get('product_name', 'N/A')}
- 产品用途 / Product Purpose: {user_info.get('product_purpose', 'N/A')}
- 目标受众 / Target Audience: {user_info.get('target_audience', 'N/A')}
- 价格范围 / Price Range: {user_info.get('price_range', 'N/A')}
"""
            
            return (
                "✅ 分析成功完成 / Analysis completed successfully!",
                summary,
                overall_score,
                report_content
            )
        else:
            return (
                f"❌ 分析失败 / Analysis failed: {result.error}",
                "",
                0.0,
                ""
            )
            
    except Exception as e:
        return (
            f"❌ 错误 / Error: {str(e)}",
            "",
            0.0,
            ""
        )


def run_analysis(
    industry: str,
    product_name: str,
    product_purpose: str,
    target_audience: str,
    price_range: str,
    company_culture: str,
    user_needs: str
) -> tuple:
    """Synchronous wrapper for async analysis"""
    return asyncio.run(
        run_analysis_async(
            industry, product_name, product_purpose,
            target_audience, price_range, company_culture, user_needs
        )
    )


def create_gradio_interface():
    """
    Create Gradio interface for competitive analysis
    创建竞品分析的Gradio界面
    """
    
    with gr.Blocks(
        title="竞品分析工具 / Competitive Analysis Tool"
    ) as demo:
        
        gr.Markdown("""
        # 🔍 竞品分析工具 / Competitive Analysis Tool
        
        使用多智能体系统进行全面的竞品分析 / Comprehensive competitive analysis using multi-agent system
        
        ---
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("""
                ### 📝 输入信息 / Input Information
                请填写以下信息开始分析 / Please fill in the information below to start analysis
                """)
                
                industry = gr.Textbox(
                    label="🏢 行业 / Industry *",
                    placeholder="例如：电子商务、医疗科技、教育 / e.g., E-commerce, Healthcare, Education",
                    info="必填 / Required"
                )
                
                product_name = gr.Textbox(
                    label="📦 产品名称 / Product Name *",
                    placeholder="例如：ShopEasy / e.g., ShopEasy",
                    info="必填 / Required"
                )
                
                product_purpose = gr.Textbox(
                    label="🎯 产品用途 / Product Purpose",
                    placeholder="例如：为中小企业提供在线商店解决方案 / e.g., Online store solution for SMEs",
                    lines=3
                )
                
                target_audience = gr.Textbox(
                    label="👥 目标受众 / Target Audience",
                    placeholder="例如：中小型企业主和创业者 / e.g., SME owners and entrepreneurs"
                )
                
                price_range = gr.Textbox(
                    label="💰 价格范围 / Price Range",
                    placeholder="例如：每月99-499元 / e.g., $99-$499 per month"
                )
                
                company_culture = gr.Textbox(
                    label="🌟 企业文化 / Company Culture",
                    placeholder="例如：注重客户成功和创新 / e.g., Focus on customer success and innovation",
                    lines=2
                )
                
                user_needs = gr.Textbox(
                    label="📋 用户需求 / User Needs",
                    placeholder="例如：了解市场竞争情况并找到差异化定位 / e.g., Understand competition and find differentiation",
                    lines=2
                )
                
                with gr.Row():
                    submit_btn = gr.Button(
                        "🚀 开始分析 / Start Analysis",
                        variant="primary",
                        size="lg"
                    )
                    clear_btn = gr.Button(
                        "🔄 清除 / Clear",
                        variant="secondary"
                    )
            
            with gr.Column(scale=1):
                gr.Markdown("""
                ### 📊 分析结果 / Analysis Results
                """)
                
                status_output = gr.Textbox(
                    label="状态 / Status",
                    interactive=False
                )
                
                summary_output = gr.Markdown(
                    label="摘要 / Summary"
                )
                
                score_output = gr.Number(
                    label="📈 报告质量分数 / Report Quality Score",
                    interactive=False
                )
        
        with gr.Row():
            gr.Markdown("""
            ### 📄 最终报告 / Final Report
            """)
        
        with gr.Row():
            report_output = gr.Markdown(
                label="完整报告 / Full Report"
            )
        
        gr.Markdown("""
        ---
        
        ### 💡 使用提示 / Usage Tips
        
        1. **必填字段 / Required Fields**: 行业和产品名称是必填的 / Industry and Product Name are required
        2. **详细信息 / Detailed Info**: 提供越详细的信息，分析结果越准确 / More detailed information leads to better analysis
        3. **处理时间 / Processing Time**: 完整分析可能需要几分钟时间 / Full analysis may take a few minutes
        4. **报告内容 / Report Contents**: 
           - 行业分析 / Industry Analysis
           - 竞品对比 / Competitor Comparison
           - 价格分析 / Price Analysis
           - 战略建议 / Strategic Recommendations
        
        ### 🏗️ 系统架构 / System Architecture
        
        本系统使用8个专业AI代理协同工作：
        - **AgentA**: 信息收集 / Information Collection
        - **AgentB**: 行业分析 / Industry Analysis
        - **AgentC**: 产品名称搜索 / Product Name Search
        - **AgentD**: 产品用途搜索 / Product Purpose Search
        - **AgentE**: 价格分析 / Price Analysis
        - **AgentF**: 整合分析 / Integration Analysis
        - **AgentG**: 报告生成 / Report Generation
        - **AgentH**: 报告评估 / Report Evaluation
        """)
        
        # Button actions
        submit_btn.click(
            fn=run_analysis,
            inputs=[
                industry, product_name, product_purpose,
                target_audience, price_range, company_culture, user_needs
            ],
            outputs=[status_output, summary_output, score_output, report_output]
        )
        
        clear_btn.click(
            fn=lambda: ("", "", "", "", "", "", "", "", "", 0.0, ""),
            inputs=[],
            outputs=[
                industry, product_name, product_purpose,
                target_audience, price_range, company_culture, user_needs,
                status_output, summary_output, score_output, report_output
            ]
        )
        
        # Examples
        gr.Examples(
            examples=[
                [
                    "电子商务平台",  # E-commerce Platform
                    "ShopEasy",
                    "为中小企业提供在线商店解决方案的SaaS平台",
                    "中小型企业主和创业者",
                    "每月99-499元",
                    "注重客户成功和创新",
                    "了解市场竞争情况并找到差异化定位"
                ],
                [
                    "Healthcare Technology",
                    "HealthTrack Pro",
                    "Patient health monitoring system for hospitals",
                    "Healthcare providers and hospital administrators",
                    "$199-$999 per month",
                    "Innovation in healthcare delivery",
                    "Understand competitive landscape in health tech"
                ]
            ],
            inputs=[
                industry, product_name, product_purpose,
                target_audience, price_range, company_culture, user_needs
            ]
        )
    
    return demo


def main():
    """Main entry point for Gradio app"""
    demo = create_gradio_interface()
    
    print("\n" + "="*60)
    print("🚀 Starting Gradio Competitive Analysis Tool")
    print("正在启动Gradio竞品分析工具")
    print("="*60 + "\n")
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        theme=gr.themes.Soft()
    )


if __name__ == "__main__":
    main()
