"""
Base Agent Interface for Competitive Analysis
竞品分析基础代理接口
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum


class AgentRole(str, Enum):
    """Agent roles in the competitive analysis system"""
    INFO_COLLECTOR = "info_collector"  # AgentA: 信息收集
    INDUSTRY_ANALYZER = "industry_analyzer"  # AgentB: 行业分析
    PRODUCT_NAME_SEARCHER = "product_name_searcher"  # AgentC: 产品名称搜索
    PRODUCT_PURPOSE_SEARCHER = "product_purpose_searcher"  # AgentD: 产品用途搜索
    PRICE_ANALYZER = "price_analyzer"  # AgentE: 价格分析
    INTEGRATION_ANALYZER = "integration_analyzer"  # AgentF: 整合分析
    REPORT_GENERATOR = "report_generator"  # AgentG: 报告生成
    REPORT_EVALUATOR = "report_evaluator"  # AgentH: 报告评估


class AgentConfig(BaseModel):
    """Configuration for an agent"""
    agent_id: str
    agent_name: str
    agent_role: AgentRole
    description: str
    system_prompt: str
    skills: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    max_iterations: int = 10
    temperature: float = 0.7


class AgentMessage(BaseModel):
    """Message structure for agent communication"""
    sender: str
    receiver: str
    content: Dict[str, Any]
    message_type: str
    timestamp: Optional[str] = None


class AgentResponse(BaseModel):
    """Response from an agent"""
    agent_id: str
    success: bool
    data: Dict[str, Any]
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BaseAgent(ABC):
    """
    Base class for all competitive analysis agents
    所有竞品分析代理的基类
    """
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.agent_id = config.agent_id
        self.agent_name = config.agent_name
        self.agent_role = config.agent_role
        self.skills = []
        self.tools = []
        self.conversation_history = []
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        Process the input data and return a response
        处理输入数据并返回响应
        
        Args:
            input_data: Input data for processing
            
        Returns:
            AgentResponse: The agent's response
        """
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """
        Get the list of capabilities this agent provides
        获取此代理提供的能力列表
        
        Returns:
            List of capability descriptions
        """
        pass
    
    def add_skill(self, skill):
        """Add a skill to the agent"""
        self.skills.append(skill)
    
    def add_tool(self, tool):
        """Add a tool to the agent"""
        self.tools.append(tool)
    
    def get_info(self) -> Dict[str, Any]:
        """Get agent information"""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "agent_role": self.agent_role.value,
            "description": self.config.description,
            "capabilities": self.get_capabilities(),
            "skills": [skill.__class__.__name__ for skill in self.skills],
            "tools": [tool.__class__.__name__ for tool in self.tools],
        }
