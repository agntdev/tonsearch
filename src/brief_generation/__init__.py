"""
Brief Generation Engine for TonSearch.

Combines search results with analysis data to generate structured project briefs.
"""

from .brief_generator import (
    BriefFormat,
    BriefGenerator,
    BriefMetadata,
    BriefSection,
    BriefTemplate,
    EntityMetrics,
    GeneratedBrief,
    OpportunityAnalysis,
    OutputFormat,
    RiskAssessment,
    create_brief_generator,
)

__all__ = [
    "BriefFormat",
    "BriefGenerator",
    "BriefMetadata",
    "BriefSection",
    "BriefTemplate",
    "EntityMetrics",
    "GeneratedBrief",
    "OpportunityAnalysis",
    "OutputFormat",
    "RiskAssessment",
    "create_brief_generator",
]
