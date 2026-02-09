"""
Agent E: Price Analyzer
代理E: 价格分析代理 - 分析产品价格相近的产品
"""
from typing import Dict, Any, List
from ..interface.agent import BaseAgent, AgentConfig, AgentRole, AgentResponse
from ..skills import InternetSearchSkill, DataAnalysisSkill


class PriceAnalyzerAgent(BaseAgent):
    """
    AgentE: Analyzes products with similar prices
    代理E: 分析价格相近的产品
    """
    
    def __init__(self, agent_id: str = "agent_e"):
        config = AgentConfig(
            agent_id=agent_id,
            agent_name="Price Analyzer",
            agent_role=AgentRole.PRICE_ANALYZER,
            description="Analyzes and compares products with similar price points",
            system_prompt="""You are an expert pricing analyst.
Your role is to find and analyze products in similar price ranges.

For each product in the price range:
1. Product name and company
2. Exact price or price range
3. Value proposition
4. Features included at this price
5. Target market segment
6. Pricing strategy (premium, competitive, budget)

Analyze pricing strategies and value positioning.""",
            skills=["internet_search", "data_analysis"],
            max_iterations=5,
            temperature=0.5
        )
        super().__init__(config)
        
        self.add_skill(InternetSearchSkill())
        self.add_skill(DataAnalysisSkill())
    
    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        Process price analysis request
        处理价格分析请求
        """
        try:
            price_range = input_data.get("price_range", "")
            product_name = input_data.get("product_name", "")
            industry = input_data.get("industry", "")
            
            if not price_range:
                return AgentResponse(
                    agent_id=self.agent_id,
                    success=False,
                    data={},
                    error="Price range information is required"
                )
            
            # Find similar priced products
            similar_priced_products = await self._find_similar_priced_products(
                price_range, industry
            )
            
            # Analyze pricing strategy
            pricing_analysis = await self._analyze_pricing_strategy(
                similar_priced_products, price_range
            )
            
            return AgentResponse(
                agent_id=self.agent_id,
                success=True,
                data={
                    "target_product": product_name,
                    "target_price_range": price_range,
                    "similar_priced_products": similar_priced_products,
                    "pricing_analysis": pricing_analysis,
                },
                metadata={"products_analyzed": len(similar_priced_products)}
            )
            
        except Exception as e:
            return AgentResponse(
                agent_id=self.agent_id,
                success=False,
                data={},
                error=f"Price analysis failed: {str(e)}"
            )
    
    async def _find_similar_priced_products(self, price_range: str, 
                                           industry: str) -> List[Dict[str, Any]]:
        """Find products in similar price range"""
        search_skill = self.skills[0]  # InternetSearchSkill
        
        query = f"{industry} products price range {price_range}"
        search_result = await search_skill.execute(query=query, max_results=10)
        
        products = []
        if search_result.success:
            for result in search_result.data:
                products.append({
                    "name": result.get("title", ""),
                    "description": result.get("snippet", ""),
                    "price_indication": price_range,
                    "source": result.get("url", ""),
                })
        
        return products
    
    async def _analyze_pricing_strategy(self, products: List[Dict[str, Any]], 
                                       target_price: str) -> Dict[str, Any]:
        """Analyze pricing strategies"""
        analysis_skill = self.skills[1]  # DataAnalysisSkill
        
        analysis_result = await analysis_skill.execute(
            data=products,
            analysis_type="pricing_strategy"
        )
        
        return {
            "price_range": target_price,
            "products_analyzed": len(products),
            "pricing_insights": [
                f"Products in {target_price} range offer various value propositions",
                "Competitive pricing landscape identified",
                "Opportunity for value-based differentiation"
            ],
            "recommendations": [
                "Consider feature-to-price ratio",
                "Evaluate market positioning",
                "Assess pricing elasticity"
            ]
        }
    
    def get_capabilities(self) -> List[str]:
        """Get agent capabilities"""
        return [
            "Price range analysis",
            "Pricing strategy assessment",
            "Value proposition evaluation",
            "Competitive pricing intelligence",
        ]
