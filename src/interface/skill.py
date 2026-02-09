"""
Base Skill Interface for Agents
代理技能基础接口
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class SkillConfig(BaseModel):
    """Configuration for a skill"""
    skill_id: str
    skill_name: str
    description: str
    parameters: Dict[str, Any] = Field(default_factory=dict)


class SkillResult(BaseModel):
    """Result from executing a skill"""
    success: bool
    data: Any
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BaseSkill(ABC):
    """
    Base class for all agent skills
    所有代理技能的基类
    """
    
    def __init__(self, config: SkillConfig):
        self.config = config
        self.skill_id = config.skill_id
        self.skill_name = config.skill_name
    
    @abstractmethod
    async def execute(self, **kwargs) -> SkillResult:
        """
        Execute the skill with given parameters
        使用给定参数执行技能
        
        Args:
            **kwargs: Skill-specific parameters
            
        Returns:
            SkillResult: The execution result
        """
        pass
    
    def get_description(self) -> str:
        """Get skill description"""
        return self.config.description
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        """Get the parameters schema for this skill"""
        return self.config.parameters
