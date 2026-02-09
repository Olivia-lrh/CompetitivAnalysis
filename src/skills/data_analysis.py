"""
Data Analysis Skill
数据分析技能
"""
from typing import Dict, Any, List
from ..interface.skill import BaseSkill, SkillConfig, SkillResult


class DataAnalysisSkill(BaseSkill):
    """
    Skill for analyzing data and extracting insights
    数据分析和提取洞察的技能
    """
    
    def __init__(self):
        config = SkillConfig(
            skill_id="data_analysis",
            skill_name="Data Analysis",
            description="Analyze data and extract meaningful insights",
            parameters={
                "data": {"type": "object", "required": True, "description": "Data to analyze"},
                "analysis_type": {"type": "string", "required": False, "default": "general"},
            }
        )
        super().__init__(config)
    
    async def execute(self, data: Any, analysis_type: str = "general", **kwargs) -> SkillResult:
        """
        Execute data analysis
        执行数据分析
        
        Args:
            data: Data to analyze
            analysis_type: Type of analysis to perform
            
        Returns:
            SkillResult with analysis results
        """
        try:
            insights = await self._analyze_data(data, analysis_type)
            
            return SkillResult(
                success=True,
                data=insights,
                metadata={
                    "analysis_type": analysis_type,
                    "data_size": len(data) if isinstance(data, (list, dict)) else 1
                }
            )
        except Exception as e:
            return SkillResult(
                success=False,
                data={},
                error=f"Analysis failed: {str(e)}"
            )
    
    async def _analyze_data(self, data: Any, analysis_type: str) -> Dict[str, Any]:
        """
        Perform data analysis
        执行数据分析
        """
        insights = {
            "summary": "Data analysis completed",
            "analysis_type": analysis_type,
            "key_findings": []
        }
        
        if isinstance(data, list):
            insights["item_count"] = len(data)
            if data and isinstance(data[0], dict):
                insights["fields"] = list(data[0].keys())
        elif isinstance(data, dict):
            insights["fields"] = list(data.keys())
        
        return insights
