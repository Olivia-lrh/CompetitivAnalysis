"""
Agent G: Report Generator
代理G: 报告生成代理 - 对整合信息进行分析并提供竞品报告
"""
from typing import Dict, Any, List
from ..interface.agent import BaseAgent, AgentConfig, AgentRole, AgentResponse
from ..skills import ReportGenerationSkill


class ReportGeneratorAgent(BaseAgent):
    """
    AgentG: Generates comprehensive competitive analysis report
    代理G: 生成全面的竞品分析报告
    """
    
    def __init__(self, agent_id: str = "agent_g"):
        config = AgentConfig(
            agent_id=agent_id,
            agent_name="Report Generator",
            agent_role=AgentRole.REPORT_GENERATOR,
            description="Generates comprehensive competitive analysis reports",
            system_prompt="""You are an expert business report writer.
Your role is to create comprehensive, professional competitive analysis reports.

Report structure:
1. Executive Summary
2. Market Overview
3. Competitive Landscape
4. Product Analysis
5. Strategic Recommendations
6. Risk Assessment
7. Conclusion

Ensure the report is:
- Clear and professional
- Data-driven
- Actionable
- Well-structured
- Comprehensive yet concise""",
            skills=["report_generation"],
            max_iterations=3,
            temperature=0.7
        )
        super().__init__(config)
        
        self.add_skill(ReportGenerationSkill())
        self.report_version = 1
    
    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        Process report generation request
        处理报告生成请求
        """
        try:
            # Get integrated analysis
            integrated_analysis = input_data.get("integrated_analysis", {})
            strategic_insights = input_data.get("strategic_insights", {})
            user_info = input_data.get("user_info", {})
            
            # Check if this is a revision request
            revision_feedback = input_data.get("revision_feedback")
            
            if revision_feedback:
                self.report_version += 1
            
            # Generate the report
            report = await self._generate_report(
                user_info,
                integrated_analysis,
                strategic_insights,
                revision_feedback
            )
            
            return AgentResponse(
                agent_id=self.agent_id,
                success=True,
                data={
                    "report": report,
                    "report_version": self.report_version,
                    "format": "markdown",
                },
                metadata={
                    "report_length": len(report),
                    "version": self.report_version
                }
            )
            
        except Exception as e:
            return AgentResponse(
                agent_id=self.agent_id,
                success=False,
                data={},
                error=f"Report generation failed: {str(e)}"
            )
    
    async def _generate_report(self, user_info: Dict[str, Any],
                              integrated_analysis: Dict[str, Any],
                              strategic_insights: Dict[str, Any],
                              revision_feedback: str = None) -> str:
        """Generate the competitive analysis report"""
        report_skill = self.skills[0]  # ReportGenerationSkill
        
        # Prepare report data
        report_data = {
            "executive_summary": self._create_executive_summary(user_info, strategic_insights),
            "company_profile": self._create_company_profile(user_info),
            "market_overview": self._create_market_overview(integrated_analysis),
            "competitive_analysis": self._create_competitive_analysis(integrated_analysis),
            "strategic_insights": strategic_insights,
            "recommendations": strategic_insights.get("recommendations", []),
            "conclusion": self._create_conclusion(strategic_insights),
        }
        
        if revision_feedback:
            report_data["revision_notes"] = {
                "version": self.report_version,
                "changes_based_on": revision_feedback
            }
        
        # Generate the report
        result = await report_skill.execute(
            data=report_data,
            report_type="competitive_analysis",
            format="markdown"
        )
        
        if result.success:
            return result.data["report"]
        
        return "Report generation encountered an error."
    
    def _create_executive_summary(self, user_info: Dict[str, Any],
                                 insights: Dict[str, Any]) -> str:
        """Create executive summary section"""
        product_name = user_info.get("product_name", "the product")
        industry = user_info.get("industry", "the industry")
        
        return f"""This competitive analysis report examines {product_name}'s position in {industry}.
        
Key Findings:
- {len(insights.get('strengths', []))} major strengths identified
- {len(insights.get('opportunities', []))} strategic opportunities discovered
- {len(insights.get('threats', []))} competitive threats to monitor
- {len(insights.get('recommendations', []))} strategic recommendations provided

The analysis indicates a {insights.get('competitive_advantages', ['favorable'])[0] if insights.get('competitive_advantages') else 'favorable'} market position with clear opportunities for growth and differentiation."""
    
    def _create_company_profile(self, user_info: Dict[str, Any]) -> Dict[str, str]:
        """Create company profile section"""
        return {
            "Product Name": user_info.get("product_name", "N/A"),
            "Industry": user_info.get("industry", "N/A"),
            "Product Purpose": user_info.get("product_purpose", "N/A"),
            "Target Audience": user_info.get("target_audience", "N/A"),
            "Price Range": user_info.get("price_range", "N/A"),
            "Company Culture": user_info.get("company_culture", "N/A"),
        }
    
    def _create_market_overview(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create market overview section"""
        combined_data = analysis.get("combined_data", {})
        market = combined_data.get("market_landscape", {})
        
        return {
            "Industry Leaders": len(market.get("industry_leaders", [])),
            "Total Competitors Identified": market.get("total_competitors", 0),
            "Market Characteristics": "Competitive with multiple established players",
        }
    
    def _create_competitive_analysis(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create competitive analysis section"""
        combined_data = analysis.get("combined_data", {})
        segments = combined_data.get("competitive_segments", {})
        
        return {
            "Name-Based Competitors": segments.get("name_based_competitors", 0),
            "Purpose-Based Competitors": segments.get("purpose_based_competitors", 0),
            "Price-Based Competitors": segments.get("price_based_competitors", 0),
            "Analysis": "Multiple competitive dimensions identified with varying degrees of overlap.",
        }
    
    def _create_conclusion(self, insights: Dict[str, Any]) -> str:
        """Create conclusion section"""
        return f"""Based on comprehensive market analysis, the product shows strong potential for success.
        
Key success factors:
{chr(10).join('- ' + adv for adv in insights.get('competitive_advantages', ['Strategic positioning']))}

The strategic recommendations provided offer a clear path forward for market entry and growth.
Implementation of these recommendations will strengthen competitive position and drive sustainable growth."""
    
    def get_capabilities(self) -> List[str]:
        """Get agent capabilities"""
        return [
            "Comprehensive report writing",
            "Strategic synthesis",
            "Professional documentation",
            "Multi-version report management",
        ]
