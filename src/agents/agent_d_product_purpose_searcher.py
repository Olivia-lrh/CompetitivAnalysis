"""
Agent D: Product Purpose Searcher
代理D: 产品用途搜索代理 - 收集产品用途相近的产品
"""
from typing import Dict, Any, List
from ..interface.agent import BaseAgent, AgentConfig, AgentRole, AgentResponse
from ..skills import InternetSearchSkill, DataAnalysisSkill


class ProductPurposeSearcherAgent(BaseAgent):
    """
    AgentD: Searches for products with similar purposes/use cases
    代理D: 搜索产品用途相近的产品
    """
    
    def __init__(self, agent_id: str = "agent_d"):
        config = AgentConfig(
            agent_id=agent_id,
            agent_name="Product Purpose Searcher",
            agent_role=AgentRole.PRODUCT_PURPOSE_SEARCHER,
            description="Finds products with similar purposes or use cases",
            system_prompt="""You are an expert at identifying products with similar purposes.
Your role is to find products that serve similar use cases or solve similar problems.

For each similar product:
1. Product name and company
2. Primary use case/purpose
3. Target users
4. Key features
5. Unique value proposition
6. How it compares to target product

Focus on functional similarity rather than just category matching.""",
            skills=["internet_search", "data_analysis"],
            max_iterations=5,
            temperature=0.6
        )
        super().__init__(config)
        
        self.add_skill(InternetSearchSkill())
        self.add_skill(DataAnalysisSkill())
    
    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        Process product purpose search request
        处理产品用途搜索请求
        """
        try:
            product_purpose = input_data.get("product_purpose", "")
            product_name = input_data.get("product_name", "")
            
            if not product_purpose:
                return AgentResponse(
                    agent_id=self.agent_id,
                    success=False,
                    data={},
                    error="Product purpose information is required"
                )
            
            # Search for similar purpose products
            similar_products = await self._find_purpose_similar_products(product_purpose)
            
            # Analyze similarity
            analysis = await self._analyze_purpose_similarity(similar_products, product_purpose)
            
            return AgentResponse(
                agent_id=self.agent_id,
                success=True,
                data={
                    "target_product": product_name,
                    "target_purpose": product_purpose,
                    "similar_purpose_products": similar_products,
                    "similarity_analysis": analysis,
                },
                metadata={"products_found": len(similar_products)}
            )
            
        except Exception as e:
            return AgentResponse(
                agent_id=self.agent_id,
                success=False,
                data={},
                error=f"Product purpose search failed: {str(e)}"
            )
    
    async def _find_purpose_similar_products(self, purpose: str) -> List[Dict[str, Any]]:
        """Find products with similar purposes"""
        search_skill = self.skills[0]  # InternetSearchSkill
        
        # Create search queries based on purpose
        queries = [
            f"products for {purpose}",
            f"solutions for {purpose}",
            f"tools for {purpose}",
        ]
        
        all_products = []
        for query in queries[:2]:
            search_result = await search_skill.execute(query=query, max_results=5)
            
            if search_result.success:
                for result in search_result.data:
                    all_products.append({
                        "name": result.get("title", ""),
                        "description": result.get("snippet", ""),
                        "purpose_match": "high",  # Simplified matching
                        "source": result.get("url", ""),
                    })
        
        return all_products[:10]
    
    async def _analyze_purpose_similarity(self, products: List[Dict[str, Any]], 
                                         target_purpose: str) -> Dict[str, Any]:
        """Analyze how similar the purposes are"""
        analysis_skill = self.skills[1]  # DataAnalysisSkill
        
        analysis_result = await analysis_skill.execute(
            data=products,
            analysis_type="purpose_similarity"
        )
        
        return {
            "total_products": len(products),
            "high_similarity": len([p for p in products if p.get("purpose_match") == "high"]),
            "medium_similarity": len([p for p in products if p.get("purpose_match") == "medium"]),
            "key_insights": [
                f"Multiple products serve the purpose of: {target_purpose}",
                "Market has various solutions with different approaches",
                "Opportunity for differentiation based on unique features"
            ]
        }
    
    def get_capabilities(self) -> List[str]:
        """Get agent capabilities"""
        return [
            "Use case analysis",
            "Functional similarity assessment",
            "Problem-solution matching",
            "Alternative solution discovery",
        ]
