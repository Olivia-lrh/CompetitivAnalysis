"""
Report Generation Skill
报告生成技能
"""
from typing import Dict, Any
from datetime import datetime
from ..interface.skill import BaseSkill, SkillConfig, SkillResult


class ReportGenerationSkill(BaseSkill):
    """
    Skill for generating formatted reports
    生成格式化报告的技能
    """
    
    def __init__(self):
        config = SkillConfig(
            skill_id="report_generation",
            skill_name="Report Generation",
            description="Generate formatted reports from analysis data",
            parameters={
                "data": {"type": "object", "required": True, "description": "Report data"},
                "report_type": {"type": "string", "required": False, "default": "competitive_analysis"},
                "format": {"type": "string", "required": False, "default": "markdown"},
            }
        )
        super().__init__(config)
    
    async def execute(self, data: Dict[str, Any], report_type: str = "competitive_analysis", 
                     format: str = "markdown", **kwargs) -> SkillResult:
        """
        Execute report generation
        执行报告生成
        
        Args:
            data: Report data
            report_type: Type of report to generate
            format: Output format (markdown, html, pdf)
            
        Returns:
            SkillResult with generated report
        """
        try:
            report = await self._generate_report(data, report_type, format)
            
            return SkillResult(
                success=True,
                data={"report": report, "format": format},
                metadata={
                    "report_type": report_type,
                    "format": format,
                    "generated_at": datetime.now().isoformat()
                }
            )
        except Exception as e:
            return SkillResult(
                success=False,
                data={},
                error=f"Report generation failed: {str(e)}"
            )
    
    async def _generate_report(self, data: Dict[str, Any], report_type: str, format: str) -> str:
        """
        Generate the actual report
        生成实际报告
        """
        if format == "markdown":
            return self._generate_markdown_report(data, report_type)
        else:
            return "Report generation for this format is not yet implemented"
    
    def _generate_markdown_report(self, data: Dict[str, Any], report_type: str) -> str:
        """Generate a markdown report"""
        report_lines = [
            f"# Competitive Analysis Report",
            f"",
            f"**Report Type:** {report_type}",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"",
            f"## Executive Summary",
            f"",
        ]
        
        # Add data sections
        for section, content in data.items():
            report_lines.append(f"## {section.replace('_', ' ').title()}")
            report_lines.append("")
            if isinstance(content, dict):
                for key, value in content.items():
                    report_lines.append(f"**{key}:** {value}")
            elif isinstance(content, list):
                for item in content:
                    report_lines.append(f"- {item}")
            else:
                report_lines.append(str(content))
            report_lines.append("")
        
        return "\n".join(report_lines)
