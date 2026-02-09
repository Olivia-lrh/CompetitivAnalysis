"""
Agent A: Information Collector
代理A: 信息收集代理 - 通过多轮对话收集用户信息
"""
from typing import Dict, Any, List
from ..interface.agent import BaseAgent, AgentConfig, AgentRole, AgentResponse
from ..skills import InternetSearchSkill, InformationExtractionSkill


class InformationCollectorAgent(BaseAgent):
    """
    AgentA: Collects user information through multi-round conversations
    代理A: 通过多轮对话收集用户信息
    
    Collects:
    - Industry (行业)
    - Product name (产品名称)
    - Product purpose/usage (产品用途)
    - Target audience (产品受众)
    - Product price (产品价格)
    - Company culture (企业文化)
    - Actual user needs (用户实际需求)
    """
    
    def __init__(self, agent_id: str = "agent_a"):
        config = AgentConfig(
            agent_id=agent_id,
            agent_name="Information Collector",
            agent_role=AgentRole.INFO_COLLECTOR,
            description="Collects comprehensive information from users through interactive dialogue",
            system_prompt="""You are an expert information collector for competitive analysis.
Your role is to gather comprehensive information about the user's product and market through natural conversation.

Information to collect:
1. Industry/Market (行业)
2. Product name (产品名称)
3. Product purpose and features (产品用途和特点)
4. Target audience/customers (产品受众)
5. Product pricing (产品价格)
6. Company culture and values (企业文化)
7. Actual needs and goals (实际需求)

Be conversational, ask follow-up questions, and ensure you understand the context fully before moving to the next topic.""",
            skills=["internet_search", "information_extraction"],
            max_iterations=10,
            temperature=0.7
        )
        super().__init__(config)
        
        # Add skills
        self.add_skill(InternetSearchSkill())
        self.add_skill(InformationExtractionSkill())
        
        # Information tracking
        self.collected_info = {
            "industry": None,
            "product_name": None,
            "product_purpose": None,
            "target_audience": None,
            "price_range": None,
            "company_culture": None,
            "user_needs": None,
        }
        self.conversation_rounds = 0
        self.max_rounds = 10
    
    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        Process user input and collect information
        处理用户输入并收集信息
        """
        try:
            user_message = input_data.get("message", "")
            self.conversation_rounds += 1
            
            # Extract information from user message
            await self._extract_and_store_info(user_message)
            
            # Determine next question or completion
            if self._is_collection_complete():
                return AgentResponse(
                    agent_id=self.agent_id,
                    success=True,
                    data={
                        "status": "complete",
                        "collected_info": self.collected_info,
                        "conversation_rounds": self.conversation_rounds,
                        "response": "Thank you! I have collected all the necessary information. Here's a summary:\n" + 
                                  self._format_collected_info()
                    },
                    metadata={"stage": "complete"}
                )
            else:
                next_question = self._generate_next_question()
                return AgentResponse(
                    agent_id=self.agent_id,
                    success=True,
                    data={
                        "status": "in_progress",
                        "collected_info": self.collected_info,
                        "conversation_rounds": self.conversation_rounds,
                        "response": next_question
                    },
                    metadata={"stage": "collecting"}
                )
                
        except Exception as e:
            return AgentResponse(
                agent_id=self.agent_id,
                success=False,
                data={},
                error=f"Error in information collection: {str(e)}"
            )
    
    async def _extract_and_store_info(self, message: str):
        """Extract and store information from user message"""
        # Simple keyword-based extraction
        # In production, use LLM for better extraction
        
        message_lower = message.lower()
        
        # Check for industry
        if not self.collected_info["industry"] and any(word in message_lower for word in ["行业", "industry", "市场", "market"]):
            self.collected_info["industry"] = message
        
        # Check for product name
        if not self.collected_info["product_name"] and any(word in message_lower for word in ["产品", "product", "名称", "name", "叫"]):
            self.collected_info["product_name"] = message
        
        # Check for product purpose
        if not self.collected_info["product_purpose"] and any(word in message_lower for word in ["用途", "purpose", "功能", "features", "用于"]):
            self.collected_info["product_purpose"] = message
        
        # Check for target audience
        if not self.collected_info["target_audience"] and any(word in message_lower for word in ["受众", "audience", "用户", "users", "客户", "customers"]):
            self.collected_info["target_audience"] = message
        
        # Check for price
        if not self.collected_info["price_range"] and any(word in message_lower for word in ["价格", "price", "定价", "pricing", "元", "$", "¥"]):
            self.collected_info["price_range"] = message
        
        # Check for company culture
        if not self.collected_info["company_culture"] and any(word in message_lower for word in ["文化", "culture", "价值观", "values", "理念"]):
            self.collected_info["company_culture"] = message
        
        # Check for user needs
        if not self.collected_info["user_needs"] and any(word in message_lower for word in ["需求", "needs", "目标", "goals", "希望", "want"]):
            self.collected_info["user_needs"] = message
    
    def _is_collection_complete(self) -> bool:
        """Check if all required information has been collected"""
        required_fields = ["industry", "product_name", "product_purpose"]
        return all(self.collected_info[field] is not None for field in required_fields)
    
    def _generate_next_question(self) -> str:
        """Generate the next question based on missing information"""
        questions = {
            "industry": "Could you tell me about your industry or market? (请告诉我您所在的行业或市场?)",
            "product_name": "What is the name of your product? (您的产品名称是什么?)",
            "product_purpose": "What is the main purpose or use case of your product? (您的产品主要用途是什么?)",
            "target_audience": "Who is your target audience or customer base? (您的目标受众或客户群体是谁?)",
            "price_range": "What is your product's price range? (您的产品价格范围是多少?)",
            "company_culture": "Could you describe your company culture or values? (能描述一下您的企业文化或价值观吗?)",
            "user_needs": "What are your specific needs or goals for this analysis? (您对这次分析的具体需求或目标是什么?)",
        }
        
        for field, question in questions.items():
            if self.collected_info[field] is None:
                return question
        
        return "Is there anything else you'd like to add? (还有其他要补充的吗?)"
    
    def _format_collected_info(self) -> str:
        """Format collected information for display"""
        lines = []
        field_names = {
            "industry": "Industry/行业",
            "product_name": "Product Name/产品名称",
            "product_purpose": "Product Purpose/产品用途",
            "target_audience": "Target Audience/目标受众",
            "price_range": "Price Range/价格范围",
            "company_culture": "Company Culture/企业文化",
            "user_needs": "User Needs/用户需求",
        }
        
        for field, name in field_names.items():
            value = self.collected_info[field]
            if value:
                lines.append(f"- {name}: {value}")
        
        return "\n".join(lines)
    
    def get_capabilities(self) -> List[str]:
        """Get agent capabilities"""
        return [
            "Multi-round conversation management",
            "Information extraction from natural language",
            "Context-aware question generation",
            "Comprehensive user profiling",
        ]
    
    def get_collected_info(self) -> Dict[str, Any]:
        """Get all collected information"""
        return self.collected_info.copy()
