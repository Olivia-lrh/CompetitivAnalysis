"""Competitive Analysis Interface Package"""

from .agent import (
    BaseAgent,
    AgentRole,
    AgentConfig,
    AgentMessage,
    AgentResponse,
)
from .skill import (
    BaseSkill,
    SkillConfig,
    SkillResult,
)
from .workflow import (
    BaseWorkflow,
    WorkflowConfig,
    WorkflowStep,
    WorkflowStatus,
    WorkflowResult,
)

__all__ = [
    "BaseAgent",
    "AgentRole",
    "AgentConfig",
    "AgentMessage",
    "AgentResponse",
    "BaseSkill",
    "SkillConfig",
    "SkillResult",
    "BaseWorkflow",
    "WorkflowConfig",
    "WorkflowStep",
    "WorkflowStatus",
    "WorkflowResult",
]
