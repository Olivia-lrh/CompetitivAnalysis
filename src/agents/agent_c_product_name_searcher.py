"""
Agent C: Product Name Searcher
代理C: 产品名称搜索代理 - 收集产品名称相近的产品信息
"""
from typing import Dict, Any, List
from ..interface.agent import BaseAgent, AgentConfig, AgentRole, AgentResponse
from ..skills import InternetSearchSkill, InformationExtractionSkill


class ProductNameSearcherAgent(BaseAgent):
    """
    AgentC: Searches for products with similar names
    代理C: 搜索产品名称相近的产品
    """
    
    def __init__(self, agent_id: str = "agent_c"):
        config = AgentConfig(
            agent_id=agent_id,
            agent_name="Product Name Searcher",
            agent_role=AgentRole.PRODUCT_NAME_SEARCHER,
            description="Finds products with similar names to identify potential competitors",
            system_prompt="""You are an expert at finding products with similar names.
Your role is to search for products that have similar or related names to the target product.

For each similar product found:
1. Product name
2. Company/Brand
3. Product category
4. Key features
5. Market presence
6. How it differs from the target product

Use various search strategies to find naming variations and similar products.""",
            skills=["internet_search", "information_extraction"],
            max_iterations=5,
            temperature=0.6
        )
        super().__init__(config)
        
        self.add_skill(InternetSearchSkill())
        self.add_skill(InformationExtractionSkill())
    
    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        Process product name search request
        处理产品名称搜索请求
        """
        try:
            product_name = input_data.get("product_name", "")
            
            if not product_name:
                return AgentResponse(
                    agent_id=self.agent_id,
                    success=False,
                    data={},
                    error="Product name is required"
                )
            
            # Search for similar products
            similar_products = await self._find_similar_products(product_name)
            
            # Extract detailed information
            detailed_info = await self._extract_product_details(similar_products)
            
            return AgentResponse(
                agent_id=self.agent_id,
                success=True,
                data={
                    "target_product": product_name,
                    "similar_products": similar_products,
                    "detailed_analysis": detailed_info,
                },
                metadata={"products_found": len(similar_products)}
            )
            
        except Exception as e:
            return AgentResponse(
                agent_id=self.agent_id,
                success=False,
                data={},
                error=f"Product name search failed: {str(e)}"
            )
    
    async def _find_similar_products(self, product_name: str) -> List[Dict[str, Any]]:
        """Find products with similar names"""
        search_skill = self.skills[0]  # InternetSearchSkill
        
        # Search with variations
        queries = [
            f"{product_name} alternatives",
            f"products similar to {product_name}",
            f"{product_name} competitors",
        ]
        
        all_products = []
        for query in queries[:2]:  # Limit searches
            search_result = await search_skill.execute(query=query, max_results=5)
            
            if search_result.success:
                for result in search_result.data:
                    all_products.append({
                        "name": result.get("title", ""),
                        "description": result.get("snippet", ""),
                        "source": result.get("url", ""),
                    })
        
        return all_products[:10]  # Return top 10
    
    async def _extract_product_details(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract detailed information from products"""
        extraction_skill = self.skills[1]  # InformationExtractionSkill
        
        fields = ["name", "company", "features", "price"]
        
        detailed_products = []
        for product in products:
            text = f"{product.get('name', '')} {product.get('description', '')}"
            extraction_result = await extraction_skill.execute(text=text, fields=fields)
            
            if extraction_result.success:
                detailed_products.append(extraction_result.data)
        
        return {
            "products_analyzed": len(detailed_products),
            "detailed_products": detailed_products,
            "summary": f"Found {len(products)} products with similar names"
        }
    
    def get_capabilities(self) -> List[str]:
        """Get agent capabilities"""
        return [
            "Product name similarity matching",
            "Alternative product discovery",
            "Brand name analysis",
            "Product differentiation assessment",
        ]
