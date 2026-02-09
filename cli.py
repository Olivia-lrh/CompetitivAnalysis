#!/usr/bin/env python3
"""
Competitive Analysis CLI Tool
竞品分析命令行工具
"""
import asyncio
import sys
from typing import Optional
from src.workflow import CompetitiveAnalysisWorkflow


async def run_interactive_analysis():
    """
    Run interactive competitive analysis
    运行交互式竞品分析
    """
    print("=" * 60)
    print("Competitive Analysis Tool / 竞品分析工具")
    print("=" * 60)
    print()
    
    # Simulate user input collection
    # In production, this would be interactive
    print("Please provide information about your product:")
    print("请提供您的产品信息：")
    print()
    
    # Example user inputs
    user_messages = [
        "我们的行业是电子商务平台",  # Our industry is e-commerce platform
        "产品名称是 ShopEasy",  # Product name is ShopEasy
        "这是一个为中小企业提供在线商店解决方案的SaaS平台",  # SaaS platform for SME online stores
        "目标受众是中小型企业主和创业者",  # Target audience is SME owners and entrepreneurs
        "价格在每月99-499元之间",  # Price range 99-499 per month
        "企业文化注重客户成功和创新",  # Company culture focuses on customer success and innovation
        "我们需要了解市场竞争情况并找到差异化定位",  # Need to understand competition and find differentiation
    ]
    
    # Create and run workflow
    print("\nStarting competitive analysis workflow...")
    print("启动竞品分析工作流...\n")
    
    workflow = CompetitiveAnalysisWorkflow()
    
    result = await workflow.execute({
        "user_messages": user_messages
    })
    
    # Display results
    print("\n" + "=" * 60)
    print("Workflow Execution Complete / 工作流执行完成")
    print("=" * 60)
    print(f"\nStatus: {result.status.value}")
    print(f"Steps Completed: {result.steps_completed}/{result.total_steps}")
    
    if result.status.value == "completed":
        print("\n=== Final Report / 最终报告 ===\n")
        final_report = result.results.get("final_report", {})
        report_content = final_report.get("report", "No report generated")
        print(report_content[:2000])  # Print first 2000 characters
        
        if len(report_content) > 2000:
            print("\n... (report truncated for display) ...")
            print("\n[Full report would be saved to file]")
        
        # Display evaluation
        evaluation = result.results.get("evaluation", {})
        if evaluation:
            print("\n=== Report Evaluation / 报告评估 ===")
            print(f"Overall Score: {evaluation.get('overall_score', 0):.2f}")
            print(f"Approved: {evaluation.get('approved', False)}")
    else:
        print(f"\nError: {result.error}")
    
    return result


def main():
    """Main CLI entry point"""
    try:
        result = asyncio.run(run_interactive_analysis())
        sys.exit(0 if result.status.value == "completed" else 1)
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\n\nError: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
