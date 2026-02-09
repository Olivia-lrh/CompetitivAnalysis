"""
Competitive Analysis Workflow
竞品分析工作流
"""
import asyncio
from typing import Dict, Any, Optional
from ..interface.workflow import BaseWorkflow, WorkflowConfig, WorkflowStep, WorkflowStatus, WorkflowResult
from ..agents import (
    InformationCollectorAgent,
    IndustryAnalyzerAgent,
    ProductNameSearcherAgent,
    ProductPurposeSearcherAgent,
    PriceAnalyzerAgent,
    IntegrationAnalyzerAgent,
    ReportGeneratorAgent,
    ReportEvaluatorAgent,
)


class CompetitiveAnalysisWorkflow(BaseWorkflow):
    """
    Main workflow for competitive analysis
    竞品分析主工作流
    
    Workflow Steps:
    1. AgentA: Collect user information (信息收集)
    2. AgentB-E: Parallel data collection (并行数据收集)
        - AgentB: Industry analysis
        - AgentC: Similar name products
        - AgentD: Similar purpose products
        - AgentE: Similar price products
    3. AgentF: Integration analysis (整合分析)
    4. AgentG: Report generation (报告生成)
    5. AgentH: Report evaluation (报告评估)
    6. AgentG: Report revision (if needed) (报告修改)
    """
    
    def __init__(self, workflow_id: str = "competitive_analysis_v1"):
        steps = [
            WorkflowStep(
                step_id="step_1",
                agent_role="info_collector",
                description="Collect user information through dialogue",
                depends_on=[]
            ),
            WorkflowStep(
                step_id="step_2a",
                agent_role="industry_analyzer",
                description="Analyze industry and top companies",
                depends_on=["step_1"]
            ),
            WorkflowStep(
                step_id="step_2b",
                agent_role="product_name_searcher",
                description="Search for similar name products",
                depends_on=["step_1"]
            ),
            WorkflowStep(
                step_id="step_2c",
                agent_role="product_purpose_searcher",
                description="Search for similar purpose products",
                depends_on=["step_1"]
            ),
            WorkflowStep(
                step_id="step_2d",
                agent_role="price_analyzer",
                description="Analyze similar price products",
                depends_on=["step_1"]
            ),
            WorkflowStep(
                step_id="step_3",
                agent_role="integration_analyzer",
                description="Integrate and analyze all collected data",
                depends_on=["step_2a", "step_2b", "step_2c", "step_2d"]
            ),
            WorkflowStep(
                step_id="step_4",
                agent_role="report_generator",
                description="Generate competitive analysis report",
                depends_on=["step_3"]
            ),
            WorkflowStep(
                step_id="step_5",
                agent_role="report_evaluator",
                description="Evaluate report quality",
                depends_on=["step_4"]
            ),
        ]
        
        config = WorkflowConfig(
            workflow_id=workflow_id,
            workflow_name="Competitive Analysis Workflow",
            description="End-to-end competitive analysis workflow with multi-agent collaboration",
            steps=steps,
            max_iterations=2
        )
        
        super().__init__(config)
        
        # Initialize agents
        self.agents = {
            "info_collector": InformationCollectorAgent(),
            "industry_analyzer": IndustryAnalyzerAgent(),
            "product_name_searcher": ProductNameSearcherAgent(),
            "product_purpose_searcher": ProductPurposeSearcherAgent(),
            "price_analyzer": PriceAnalyzerAgent(),
            "integration_analyzer": IntegrationAnalyzerAgent(),
            "report_generator": ReportGeneratorAgent(),
            "report_evaluator": ReportEvaluatorAgent(),
        }
        
        self.collected_data = {}
    
    async def execute(self, initial_data: Dict[str, Any]) -> WorkflowResult:
        """
        Execute the complete workflow
        执行完整工作流
        """
        try:
            self.status = WorkflowStatus.RUNNING
            
            # Step 1: Information Collection (AgentA)
            print("\n=== Step 1: Information Collection ===")
            user_info = await self._step_information_collection(initial_data)
            if not user_info:
                return self._create_failed_result("Information collection failed")
            
            self.collected_data["user_info"] = user_info
            self.current_step = 1
            
            # Step 2: Parallel Data Collection (AgentB-E)
            print("\n=== Step 2: Parallel Data Collection ===")
            parallel_results = await self._step_parallel_collection(user_info)
            self.collected_data.update(parallel_results)
            self.current_step = 5
            
            # Step 3: Integration Analysis (AgentF)
            print("\n=== Step 3: Integration Analysis ===")
            integration_result = await self._step_integration_analysis()
            self.collected_data["integration"] = integration_result
            self.current_step = 6
            
            # Step 4: Report Generation (AgentG)
            print("\n=== Step 4: Report Generation ===")
            report = await self._step_report_generation()
            self.collected_data["report"] = report
            self.current_step = 7
            
            # Step 5: Report Evaluation (AgentH)
            print("\n=== Step 5: Report Evaluation ===")
            evaluation = await self._step_report_evaluation(report)
            self.collected_data["evaluation"] = evaluation
            self.current_step = 8
            
            # Step 6: Report Revision if needed (AgentG again)
            if evaluation.get("needs_revision", False):
                print("\n=== Step 6: Report Revision ===")
                revised_report = await self._step_report_revision(
                    evaluation.get("feedback", {})
                )
                self.collected_data["final_report"] = revised_report
            else:
                self.collected_data["final_report"] = report
            
            # Mark as completed
            self.status = WorkflowStatus.COMPLETED
            
            return WorkflowResult(
                workflow_id=self.workflow_id,
                status=WorkflowStatus.COMPLETED,
                steps_completed=len(self.config.steps),
                total_steps=len(self.config.steps),
                results=self.collected_data,
                error=None
            )
            
        except Exception as e:
            self.status = WorkflowStatus.FAILED
            return self._create_failed_result(str(e))
    
    async def _step_information_collection(self, initial_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Step 1: Collect user information"""
        agent = self.agents["info_collector"]
        
        # Simulate multi-round conversation
        # In production, this would be an interactive process
        conversations = initial_data.get("user_messages", [])
        
        for message in conversations:
            response = await agent.process({"message": message})
            if not response.success:
                return None
            
            if response.data.get("status") == "complete":
                return response.data.get("collected_info", {})
        
        # Return collected info
        return agent.get_collected_info()
    
    async def _step_parallel_collection(self, user_info: Dict[str, Any]) -> Dict[str, Any]:
        """Step 2: Parallel data collection from AgentB-E"""
        # Run all data collection agents in parallel
        tasks = {
            "industry_data": self.agents["industry_analyzer"].process({
                "industry": user_info.get("industry", "")
            }),
            "name_similar_products": self.agents["product_name_searcher"].process({
                "product_name": user_info.get("product_name", "")
            }),
            "purpose_similar_products": self.agents["product_purpose_searcher"].process({
                "product_name": user_info.get("product_name", ""),
                "product_purpose": user_info.get("product_purpose", "")
            }),
            "price_similar_products": self.agents["price_analyzer"].process({
                "product_name": user_info.get("product_name", ""),
                "price_range": user_info.get("price_range", ""),
                "industry": user_info.get("industry", "")
            }),
        }
        
        # Wait for all to complete
        results = {}
        for key, task in tasks.items():
            response = await task
            if response.success:
                results[key] = response.data
            else:
                results[key] = {}
        
        return results
    
    async def _step_integration_analysis(self) -> Dict[str, Any]:
        """Step 3: Integration analysis"""
        agent = self.agents["integration_analyzer"]
        
        response = await agent.process({
            "user_info": self.collected_data.get("user_info", {}),
            "industry_data": self.collected_data.get("industry_data", {}),
            "name_similar_products": self.collected_data.get("name_similar_products", {}),
            "purpose_similar_products": self.collected_data.get("purpose_similar_products", {}),
            "price_similar_products": self.collected_data.get("price_similar_products", {}),
        })
        
        if response.success:
            return response.data
        
        return {}
    
    async def _step_report_generation(self, revision_feedback: Optional[str] = None) -> Dict[str, Any]:
        """Step 4: Generate report"""
        agent = self.agents["report_generator"]
        
        integration_data = self.collected_data.get("integration", {})
        
        response = await agent.process({
            "user_info": self.collected_data.get("user_info", {}),
            "integrated_analysis": integration_data.get("integrated_analysis", {}),
            "strategic_insights": integration_data.get("strategic_insights", {}),
            "revision_feedback": revision_feedback,
        })
        
        if response.success:
            return response.data
        
        return {}
    
    async def _step_report_evaluation(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Step 5: Evaluate report"""
        agent = self.agents["report_evaluator"]
        
        response = await agent.process({
            "report": report_data.get("report", ""),
            "report_version": report_data.get("report_version", 1),
        })
        
        if response.success:
            return response.data
        
        return {"needs_revision": False}
    
    async def _step_report_revision(self, feedback: Dict[str, Any]) -> Dict[str, Any]:
        """Step 6: Revise report based on feedback"""
        feedback_text = "\n".join([
            "Feedback:",
            f"Status: {feedback.get('status', '')}",
            f"Assessment: {feedback.get('overall_assessment', '')}",
            "Areas for improvement:",
            *[f"- {issue}" for issue in feedback.get('areas_for_improvement', [])],
        ])
        
        revised_report = await self._step_report_generation(feedback_text)
        return revised_report
    
    async def resume(self, from_step: int) -> WorkflowResult:
        """Resume workflow from a specific step"""
        # Implementation for resuming workflow
        self.current_step = from_step
        # Continue execution from the specified step
        return await self.execute({})
    
    def _create_failed_result(self, error: str) -> WorkflowResult:
        """Create a failed workflow result"""
        return WorkflowResult(
            workflow_id=self.workflow_id,
            status=WorkflowStatus.FAILED,
            steps_completed=self.current_step,
            total_steps=len(self.config.steps),
            results=self.collected_data,
            error=error
        )
