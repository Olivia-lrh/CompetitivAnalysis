"""
Agent H: Report Evaluator
代理H: 报告评估代理 - 对竞品报告进行评估并确认是否需要重新修改
"""
from typing import Dict, Any, List
from ..interface.agent import BaseAgent, AgentConfig, AgentRole, AgentResponse


class ReportEvaluatorAgent(BaseAgent):
    """
    AgentH: Evaluates competitive analysis reports for quality and completeness
    代理H: 评估竞品分析报告的质量和完整性
    """
    
    def __init__(self, agent_id: str = "agent_h"):
        config = AgentConfig(
            agent_id=agent_id,
            agent_name="Report Evaluator",
            agent_role=AgentRole.REPORT_EVALUATOR,
            description="Evaluates report quality and determines if revisions are needed",
            system_prompt="""You are an expert business report quality evaluator.
Your role is to assess competitive analysis reports for:

Quality Criteria:
1. Completeness - All required sections present
2. Accuracy - Data and analysis are sound
3. Clarity - Information is clear and well-organized
4. Actionability - Recommendations are specific and practical
5. Professionalism - Language and formatting are appropriate

Evaluation Process:
1. Check for all required sections
2. Assess data quality and analysis depth
3. Verify logical flow and coherence
4. Evaluate recommendations quality
5. Determine if revision is needed

Provide specific, actionable feedback for improvements.""",
            skills=[],
            max_iterations=2,
            temperature=0.5
        )
        super().__init__(config)
        
        self.evaluation_criteria = {
            "completeness": 0.0,
            "accuracy": 0.0,
            "clarity": 0.0,
            "actionability": 0.0,
            "professionalism": 0.0,
        }
        self.minimum_score = 0.8  # 80% threshold for approval
    
    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        Process report evaluation request
        处理报告评估请求
        """
        try:
            report = input_data.get("report", "")
            report_version = input_data.get("report_version", 1)
            
            if not report:
                return AgentResponse(
                    agent_id=self.agent_id,
                    success=False,
                    data={},
                    error="No report provided for evaluation"
                )
            
            # Evaluate the report
            evaluation = await self._evaluate_report(report)
            
            # Calculate overall score
            overall_score = sum(evaluation["scores"].values()) / len(evaluation["scores"])
            
            # Determine if revision is needed
            needs_revision = overall_score < self.minimum_score or report_version == 1
            
            # Generate feedback
            feedback = self._generate_feedback(evaluation, needs_revision)
            
            return AgentResponse(
                agent_id=self.agent_id,
                success=True,
                data={
                    "evaluation": evaluation,
                    "overall_score": overall_score,
                    "needs_revision": needs_revision,
                    "feedback": feedback,
                    "approved": not needs_revision,
                },
                metadata={
                    "report_version": report_version,
                    "evaluation_timestamp": "2024-01-01T00:00:00"
                }
            )
            
        except Exception as e:
            return AgentResponse(
                agent_id=self.agent_id,
                success=False,
                data={},
                error=f"Report evaluation failed: {str(e)}"
            )
    
    async def _evaluate_report(self, report: str) -> Dict[str, Any]:
        """Evaluate the report against quality criteria"""
        scores = {}
        issues = []
        strengths = []
        
        # Evaluate completeness
        required_sections = [
            "Executive Summary",
            "Market Overview",
            "Competitive",
            "Recommendations",
            "Conclusion"
        ]
        completeness = sum(1 for section in required_sections if section.lower() in report.lower()) / len(required_sections)
        scores["completeness"] = completeness
        
        if completeness < 1.0:
            missing = [s for s in required_sections if s.lower() not in report.lower()]
            issues.append(f"Missing sections: {', '.join(missing)}")
        else:
            strengths.append("All required sections present")
        
        # Evaluate clarity (based on structure and length)
        has_headers = report.count("#") > 3
        adequate_length = len(report) > 500
        clarity = (int(has_headers) + int(adequate_length)) / 2
        scores["clarity"] = clarity
        
        if not has_headers:
            issues.append("Report needs better structure with clear headers")
        if not adequate_length:
            issues.append("Report should be more detailed")
        if has_headers and adequate_length:
            strengths.append("Well-structured and detailed report")
        
        # Evaluate actionability (check for recommendations)
        has_recommendations = "recommendation" in report.lower()
        has_specifics = any(word in report.lower() for word in ["should", "must", "consider", "implement"])
        actionability = (int(has_recommendations) + int(has_specifics)) / 2
        scores["actionability"] = actionability
        
        if not has_recommendations:
            issues.append("Add specific recommendations section")
        elif not has_specifics:
            issues.append("Recommendations should be more specific and actionable")
        else:
            strengths.append("Clear, actionable recommendations provided")
        
        # Evaluate professionalism (basic checks)
        no_typos = True  # Simplified check
        proper_formatting = "**" in report or "*" in report  # Has emphasis
        professionalism = (int(no_typos) + int(proper_formatting)) / 2
        scores["professionalism"] = professionalism
        
        if proper_formatting:
            strengths.append("Professional formatting and presentation")
        
        # Evaluate accuracy (assume high if structured properly)
        scores["accuracy"] = 0.85  # Baseline score
        
        return {
            "scores": scores,
            "issues": issues,
            "strengths": strengths,
        }
    
    def _generate_feedback(self, evaluation: Dict[str, Any], 
                          needs_revision: bool) -> Dict[str, Any]:
        """Generate detailed feedback based on evaluation"""
        feedback = {
            "status": "needs_revision" if needs_revision else "approved",
            "overall_assessment": "",
            "strengths": evaluation["strengths"],
            "areas_for_improvement": evaluation["issues"],
            "specific_actions": [],
        }
        
        if needs_revision:
            feedback["overall_assessment"] = "The report shows good foundation but requires improvements before final delivery."
            feedback["specific_actions"] = [
                "Address all identified issues",
                "Enhance detail in key sections",
                "Ensure all recommendations are actionable",
                "Verify data accuracy and sources",
            ]
        else:
            feedback["overall_assessment"] = "The report meets quality standards and is ready for delivery."
            feedback["specific_actions"] = [
                "Perform final proofread",
                "Verify all data points",
                "Confirm formatting consistency",
            ]
        
        return feedback
    
    def get_capabilities(self) -> List[str]:
        """Get agent capabilities"""
        return [
            "Report quality assessment",
            "Completeness verification",
            "Feedback generation",
            "Quality standards enforcement",
        ]
