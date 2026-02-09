"""
Workflow Interface for Agent Orchestration
工作流接口，用于代理编排
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum


class WorkflowStatus(str, Enum):
    """Workflow execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


class WorkflowStep(BaseModel):
    """A step in the workflow"""
    step_id: str
    agent_role: str
    description: str
    depends_on: List[str] = Field(default_factory=list)
    status: WorkflowStatus = WorkflowStatus.PENDING
    result: Optional[Dict[str, Any]] = None


class WorkflowConfig(BaseModel):
    """Configuration for a workflow"""
    workflow_id: str
    workflow_name: str
    description: str
    steps: List[WorkflowStep]
    max_iterations: int = 10


class WorkflowResult(BaseModel):
    """Result from workflow execution"""
    workflow_id: str
    status: WorkflowStatus
    steps_completed: int
    total_steps: int
    results: Dict[str, Any]
    error: Optional[str] = None


class BaseWorkflow(ABC):
    """
    Base class for workflow orchestration
    工作流编排基类
    """
    
    def __init__(self, config: WorkflowConfig):
        self.config = config
        self.workflow_id = config.workflow_id
        self.status = WorkflowStatus.PENDING
        self.current_step = 0
        self.results = {}
    
    @abstractmethod
    async def execute(self, initial_data: Dict[str, Any]) -> WorkflowResult:
        """
        Execute the workflow
        执行工作流
        
        Args:
            initial_data: Initial data for the workflow
            
        Returns:
            WorkflowResult: The workflow execution result
        """
        pass
    
    @abstractmethod
    async def resume(self, from_step: int) -> WorkflowResult:
        """
        Resume workflow from a specific step
        从特定步骤恢复工作流
        """
        pass
    
    def get_status(self) -> WorkflowStatus:
        """Get current workflow status"""
        return self.status
    
    def get_progress(self) -> Dict[str, Any]:
        """Get workflow progress"""
        return {
            "workflow_id": self.workflow_id,
            "status": self.status.value,
            "current_step": self.current_step,
            "total_steps": len(self.config.steps),
            "progress_percentage": (self.current_step / len(self.config.steps)) * 100
        }
