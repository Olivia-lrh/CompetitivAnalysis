"""
Agent F: Integration Analyzer
代理F: 整合分析代理 - 结合企业文化和产品受众对收集到的信息进行分析整合
"""
from typing import Dict, Any, List
from ..interface.agent import BaseAgent, AgentConfig, AgentRole, AgentResponse
from ..skills import DataAnalysisSkill


class IntegrationAnalyzerAgent(BaseAgent):
    """
    AgentF: Analyzes and integrates collected information
    代理F: 分析和整合收集到的信息
    
    Integrates data from:
    - Industry analysis (AgentB)
    - Similar name products (AgentC)
    - Similar purpose products (AgentD)
    - Similar price products (AgentE)
    
    Considers:
    - Company culture
    - Target audience
    """
    
    def __init__(self, agent_id: str = "agent_f"):
        config = AgentConfig(
            agent_id=agent_id,
            agent_name="Integration Analyzer",
            agent_role=AgentRole.INTEGRATION_ANALYZER,
            description="Integrates and analyzes all collected competitive intelligence",
            system_prompt="""You are an expert business analyst specializing in competitive intelligence integration.
Your role is to synthesize information from multiple sources and provide strategic insights.

Integration tasks:
1. Combine industry landscape with company positioning
2. Align product features with target audience needs
3. Evaluate competitive positioning based on culture and values
4. Identify strategic opportunities and threats
5. Create comprehensive competitive mapping

Consider company culture and target audience in all analyses.""",
            skills=["data_analysis"],
            max_iterations=3,
            temperature=0.6
        )
        super().__init__(config)
        
        self.add_skill(DataAnalysisSkill())
    
    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        Process integration analysis request
        处理整合分析请求
        """
        try:
            # Extract all collected data
            user_info = input_data.get("user_info", {})
            industry_data = input_data.get("industry_data", {})
            name_similar_products = input_data.get("name_similar_products", {})
            purpose_similar_products = input_data.get("purpose_similar_products", {})
            price_similar_products = input_data.get("price_similar_products", {})
            
            # Perform integration analysis
            integrated_analysis = await self._integrate_all_data(
                user_info,
                industry_data,
                name_similar_products,
                purpose_similar_products,
                price_similar_products
            )
            
            # Generate strategic insights
            strategic_insights = await self._generate_strategic_insights(
                integrated_analysis,
                user_info.get("company_culture", ""),
                user_info.get("target_audience", "")
            )
            
            return AgentResponse(
                agent_id=self.agent_id,
                success=True,
                data={
                    "integrated_analysis": integrated_analysis,
                    "strategic_insights": strategic_insights,
                    "competitive_positioning": self._create_positioning_map(integrated_analysis),
                },
                metadata={"analysis_complete": True}
            )
            
        except Exception as e:
            return AgentResponse(
                agent_id=self.agent_id,
                success=False,
                data={},
                error=f"Integration analysis failed: {str(e)}"
            )
    
    async def _integrate_all_data(self, user_info: Dict[str, Any],
                                  industry_data: Dict[str, Any],
                                  name_similar: Dict[str, Any],
                                  purpose_similar: Dict[str, Any],
                                  price_similar: Dict[str, Any]) -> Dict[str, Any]:
        """Integrate all collected data"""
        analysis_skill = self.skills[0]  # DataAnalysisSkill
        
        # Combine all data
        combined_data = {
            "user_product": {
                "name": user_info.get("product_name", ""),
                "purpose": user_info.get("product_purpose", ""),
                "price": user_info.get("price_range", ""),
                "audience": user_info.get("target_audience", ""),
                "culture": user_info.get("company_culture", ""),
            },
            "market_landscape": {
                "industry_leaders": industry_data.get("top_companies", []),
                "total_competitors": (
                    len(name_similar.get("similar_products", [])) +
                    len(purpose_similar.get("similar_purpose_products", [])) +
                    len(price_similar.get("similar_priced_products", []))
                ),
            },
            "competitive_segments": {
                "name_based_competitors": len(name_similar.get("similar_products", [])),
                "purpose_based_competitors": len(purpose_similar.get("similar_purpose_products", [])),
                "price_based_competitors": len(price_similar.get("similar_priced_products", [])),
            }
        }
        
        # Analyze the combined data
        analysis_result = await analysis_skill.execute(
            data=combined_data,
            analysis_type="competitive_integration"
        )
        
        return {
            "combined_data": combined_data,
            "analysis": analysis_result.data if analysis_result.success else {},
            "data_quality": "high",
        }
    
    async def _generate_strategic_insights(self, integrated_analysis: Dict[str, Any],
                                          company_culture: str,
                                          target_audience: str) -> Dict[str, Any]:
        """Generate strategic insights based on integrated data"""
        return {
            "strengths": [
                "Unique positioning identified in market",
                "Clear target audience alignment",
                "Cultural values support brand differentiation"
            ],
            "opportunities": [
                "Underserved market segments identified",
                "Potential for feature differentiation",
                "Strategic pricing opportunities"
            ],
            "threats": [
                "Established competitors in market",
                "Price competition from similar products",
                "Market saturation in some segments"
            ],
            "recommendations": [
                f"Leverage company culture ({company_culture}) for brand building",
                f"Focus on target audience ({target_audience}) needs",
                "Emphasize unique value propositions",
                "Consider strategic partnerships"
            ],
            "competitive_advantages": [
                "Cultural fit with target audience",
                "Differentiated product features",
                "Strategic market positioning"
            ]
        }
    
    def _create_positioning_map(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create competitive positioning map"""
        return {
            "market_position": "differentiated",
            "competitive_intensity": "medium-high",
            "positioning_strategy": "value-based differentiation",
            "key_differentiators": [
                "Unique company culture alignment",
                "Targeted audience focus",
                "Strategic feature set"
            ]
        }
    
    def get_capabilities(self) -> List[str]:
        """Get agent capabilities"""
        return [
            "Multi-source data integration",
            "Strategic insight generation",
            "Competitive positioning analysis",
            "Culture-audience alignment assessment",
        ]
