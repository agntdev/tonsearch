"""
Brief Generation Engine.

Combines search results with analysis data to generate structured briefs
with executive summaries, key metrics, risk assessments, and opportunity analyses.
"""

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class OutputFormat(str, Enum):
    """Supported output format types."""

    TEXT = "text"
    JSON = "json"
    PDF = "pdf"


class BriefFormat(str, Enum):
    """Brief formatting styles."""

    STANDARD = "standard"
    DETAILED = "detailed"
    EXECUTIVE = "executive"


@dataclass
class RiskAssessment:
    """Risk assessment data for brief generation."""

    overall_risk_score: float  # 0.0 - 1.0
    risk_level: str  # "low", "medium", "high", "critical"
    confidence: float  # 0.0 - 1.0
    key_risks: list[str] = field(default_factory=list)
    explanations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "overall_risk_score": self.overall_risk_score,
            "risk_level": self.risk_level,
            "confidence": self.confidence,
            "key_risks": self.key_risks,
            "explanations": self.explanations,
        }


@dataclass
class OpportunityAnalysis:
    """Opportunity analysis data for brief generation."""

    overall_opportunity_score: float  # 0.0 - 1.0
    opportunity_level: str  # "low", "medium", "high"
    confidence: float  # 0.0 - 1.0
    key_opportunities: list[str] = field(default_factory=list)
    explanations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "overall_opportunity_score": self.overall_opportunity_score,
            "opportunity_level": self.opportunity_level,
            "confidence": self.confidence,
            "key_opportunities": self.key_opportunities,
            "explanations": self.explanations,
        }


@dataclass
class EntityMetrics:
    """Key metrics for an entity."""

    tvl: float = 0.0
    tvl_change_24h: float = 0.0
    volume_24h: float = 0.0
    volume_change_24h: float = 0.0
    transactions_24h: int = 0
    active_addresses_24h: int = 0
    contract_age_days: int = 0
    holder_count: int = 0
    token_price: float = 0.0
    token_price_change_24h: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "tvl": self.tvl,
            "tvl_change_24h": self.tvl_change_24h,
            "volume_24h": self.volume_24h,
            "volume_change_24h": self.volume_change_24h,
            "transactions_24h": self.transactions_24h,
            "active_addresses_24h": self.active_addresses_24h,
            "contract_age_days": self.contract_age_days,
            "holder_count": self.holder_count,
            "token_price": self.token_price,
            "token_price_change_24h": self.token_price_change_24h,
        }


@dataclass
class BriefMetadata:
    """Metadata for a generated brief."""

    brief_id: str
    generated_at: datetime
    query: str
    entity_count: int
    format: BriefFormat
    confidence: float


@dataclass
class BriefSection:
    """Individual section of a brief."""

    title: str
    content: str
    key_findings: list[str] = field(default_factory=list)
    data_points: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "content": self.content,
            "key_findings": self.key_findings,
            "data_points": self.data_points,
        }


@dataclass
class GeneratedBrief:
    """
    Complete generated brief with all sections.

    Attributes:
        brief_id: Unique identifier for the brief
        query: Original search query
        metadata: Brief metadata
        sections: List of brief sections
        risk_assessment: Risk assessment data
        opportunity_analysis: Opportunity analysis data
        metrics: Key metrics for primary entity
    """

    brief_id: str
    query: str
    metadata: BriefMetadata
    sections: list[BriefSection] = field(default_factory=list)
    risk_assessment: RiskAssessment | None = None
    opportunity_analysis: OpportunityAnalysis | None = None
    metrics: EntityMetrics | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert brief to dictionary."""
        return {
            "brief_id": self.brief_id,
            "query": self.query,
            "metadata": {
                "brief_id": self.metadata.brief_id,
                "generated_at": self.metadata.generated_at.isoformat(),
                "query": self.metadata.query,
                "entity_count": self.metadata.entity_count,
                "format": self.metadata.format.value,
                "confidence": self.metadata.confidence,
            },
            "sections": [s.to_dict() for s in self.sections],
            "risk_assessment": self.risk_assessment.to_dict()
            if self.risk_assessment
            else None,
            "opportunity_analysis": (
                self.opportunity_analysis.to_dict()
                if self.opportunity_analysis
                else None
            ),
            "metrics": self.metrics.to_dict() if self.metrics else None,
        }

    def to_text(self) -> str:
        """Format brief as human-readable text."""
        lines = [
            "=" * 60,
            "PROJECT BRIEF",
            "=" * 60,
            f"Brief ID: {self.brief_id}",
            f"Generated: {self.metadata.generated_at.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Query: {self.query}",
            f"Entities Analyzed: {self.metadata.entity_count}",
            f"Confidence: {self.metadata.confidence:.0%}",
            "=" * 60,
            "",
        ]

        for section in self.sections:
            lines.append("-" * 40)
            lines.append(f"## {section.title}")
            lines.append("")
            lines.append(section.content)
            if section.key_findings:
                lines.append("")
                lines.append("Key Findings:")
                for finding in section.key_findings:
                    lines.append(f"  • {finding}")
            if section.data_points:
                lines.append("")
                lines.append("Data Points:")
                for key, value in section.data_points.items():
                    lines.append(f"  • {key}: {value}")
            lines.append("")

        if self.risk_assessment:
            lines.append("-" * 40)
            lines.append("## Risk Assessment")
            lines.append("")
            lines.append(
                f"Overall Risk Score: {self.risk_assessment.overall_risk_score:.0%} "
                f"({self.risk_assessment.risk_level.upper()})"
            )
            lines.append(f"Confidence: {self.risk_assessment.confidence:.0%}")
            if self.risk_assessment.key_risks:
                lines.append("")
                lines.append("Key Risks:")
                for risk in self.risk_assessment.key_risks:
                    lines.append(f"  ⚠ {risk}")

        if self.opportunity_analysis:
            lines.append("-" * 40)
            lines.append("## Opportunity Analysis")
            lines.append("")
            lines.append(
                f"Overall Opportunity Score: {self.opportunity_analysis.overall_opportunity_score:.0%} "
                f"({self.opportunity_analysis.opportunity_level.upper()})"
            )
            lines.append(f"Confidence: {self.opportunity_analysis.confidence:.0%}")
            if self.opportunity_analysis.key_opportunities:
                lines.append("")
                lines.append("Key Opportunities:")
                for opp in self.opportunity_analysis.key_opportunities:
                    lines.append(f"  ★ {opp}")

        if self.metrics:
            lines.append("-" * 40)
            lines.append("## Key Metrics")
            lines.append("")
            m = self.metrics
            lines.append(f"  TVL: ${m.tvl:,.2f}")
            if m.tvl_change_24h != 0:
                sign = "+" if m.tvl_change_24h > 0 else ""
                lines.append(f"  TVL 24h Change: {sign}{m.tvl_change_24h:.2%}")
            lines.append(f"  24h Volume: ${m.volume_24h:,.2f}")
            if m.volume_change_24h != 0:
                sign = "+" if m.volume_change_24h > 0 else ""
                lines.append(f"  Volume 24h Change: {sign}{m.volume_change_24h:.2%}")
            lines.append(f"  24h Transactions: {m.transactions_24h:,}")
            lines.append(f"  Active Addresses: {m.active_addresses_24h:,}")
            lines.append(f"  Contract Age: {m.contract_age_days} days")
            lines.append(f"  Holders: {m.holder_count:,}")

        lines.append("=" * 60)
        return "\n".join(lines)

    def to_json(self) -> str:
        """Format brief as JSON."""
        return json.dumps(self.to_dict(), indent=2)


class BriefTemplate:
    """Template engine for brief formatting."""

    @staticmethod
    def format_executive_summary(
        entity_name: str,
        category: str,
        risk_level: str,
        opportunity_level: str,
        main_finding: str,
    ) -> str:
        """Format executive summary."""
        return (
            f"{entity_name} is a {category} project with {risk_level} risk "
            f"and {opportunity_level} opportunity. {main_finding}"
        )

    @staticmethod
    def format_metrics_summary(
        metrics: EntityMetrics, entity_name: str = "Project"
    ) -> str:
        """Format metrics summary text."""
        lines = [f"{entity_name} Metrics Overview", ""]

        lines.append(f"Total Value Locked (TVL): ${metrics.tvl:,.2f}")
        if metrics.tvl_change_24h != 0:
            sign = "+" if metrics.tvl_change_24h > 0 else ""
            lines.append(f"TVL 24h Change: {sign}{metrics.tvl_change_24h:.2%}")

        lines.append(f"24h Volume: ${metrics.volume_24h:,.2f}")
        if metrics.volume_change_24h != 0:
            sign = "+" if metrics.volume_change_24h > 0 else ""
            lines.append(f"Volume 24h Change: {sign}{metrics.volume_change_24h:.2%}")

        lines.append(f"24h Transactions: {metrics.transactions_24h:,}")
        lines.append(f"Active Addresses (24h): {metrics.active_addresses_24h:,}")
        lines.append(f"Contract Age: {metrics.contract_age_days} days")
        lines.append(f"Holder Count: {metrics.holder_count:,}")

        if metrics.token_price > 0:
            lines.append(f"Token Price: ${metrics.token_price:,.6f}")
            if metrics.token_price_change_24h != 0:
                sign = "+" if metrics.token_price_change_24h > 0 else ""
                lines.append(
                    f"Token Price 24h: {sign}{metrics.token_price_change_24h:.2%}"
                )

        return "\n".join(lines)

    @staticmethod
    def format_risk_summary(risk: RiskAssessment) -> str:
        """Format risk assessment summary."""
        lines = [
            f"Risk Level: {risk.risk_level.upper()}",
            f"Risk Score: {risk.overall_risk_score:.0%}",
            f"Assessment Confidence: {risk.confidence:.0%}",
        ]

        if risk.key_risks:
            lines.append("")
            lines.append("Key Risk Factors:")
            for i, r in enumerate(risk.key_risks, 1):
                lines.append(f"  {i}. {r}")

        if risk.explanations:
            lines.append("")
            lines.append("Risk Explanations:")
            for exp in risk.explanations:
                lines.append(f"  • {exp}")

        return "\n".join(lines)

    @staticmethod
    def format_opportunity_summary(opp: OpportunityAnalysis) -> str:
        """Format opportunity assessment summary."""
        lines = [
            f"Opportunity Level: {opp.opportunity_level.upper()}",
            f"Opportunity Score: {opp.overall_opportunity_score:.0%}",
            f"Assessment Confidence: {opp.confidence:.0%}",
        ]

        if opp.key_opportunities:
            lines.append("")
            lines.append("Key Opportunity Factors:")
            for i, o in enumerate(opp.key_opportunities, 1):
                lines.append(f"  {i}. {o}")

        if opp.explanations:
            lines.append("")
            lines.append("Opportunity Explanations:")
            for exp in opp.explanations:
                lines.append(f"  • {exp}")

        return "\n".join(lines)


class BriefGenerator:
    """
    Generators for structured project briefs.

    Supports multiple output formats (text, JSON, PDF placeholder)
    and data validation.
    """

    def __init__(self):
        self.template = BriefTemplate()
        self._supported_formats = {
            OutputFormat.TEXT,
            OutputFormat.JSON,
            OutputFormat.PDF,
        }

    def generate(
        self,
        query: str,
        sections: list[BriefSection],
        risk_assessment: RiskAssessment | None = None,
        opportunity_analysis: OpportunityAnalysis | None = None,
        metrics: EntityMetrics | None = None,
        format: BriefFormat = BriefFormat.STANDARD,
        entity_count: int = 1,
        confidence: float = 0.85,
    ) -> GeneratedBrief:
        """
        Generate a complete brief.

        Args:
            query: Original search query
            sections: List of content sections
            risk_assessment: Optional risk assessment data
            opportunity_analysis: Optional opportunity analysis data
            metrics: Optional key metrics
            format: Brief formatting style
            entity_count: Number of entities analyzed
            confidence: Overall confidence score (0.0 - 1.0)

        Returns:
            GeneratedBrief with all components
        """
        # Validate inputs
        if not query:
            raise ValueError("Query cannot be empty")
        if entity_count < 1:
            raise ValueError("Entity count must be at least 1")
        if not (0.0 <= confidence <= 1.0):
            raise ValueError("Confidence must be between 0.0 and 1.0")

        # Validate risk assessment
        if risk_assessment:
            self._validate_risk_assessment(risk_assessment)

        # Validate opportunity analysis
        if opportunity_analysis:
            self._validate_opportunity_analysis(opportunity_analysis)

        # Validate metrics
        if metrics:
            self._validate_metrics(metrics)

        brief_id = str(uuid.uuid4())[:8]
        metadata = BriefMetadata(
            brief_id=brief_id,
            generated_at=datetime.utcnow(),
            query=query,
            entity_count=entity_count,
            format=format,
            confidence=confidence,
        )

        return GeneratedBrief(
            brief_id=brief_id,
            query=query,
            metadata=metadata,
            sections=sections,
            risk_assessment=risk_assessment,
            opportunity_analysis=opportunity_analysis,
            metrics=metrics,
        )

    def generate_with_search_results(
        self,
        query: str,
        search_results: list[dict[str, Any]],
        risk_assessments: list[RiskAssessment] | None = None,
        opportunity_analyses: list[OpportunityAnalysis] | None = None,
        metrics: list[EntityMetrics] | None = None,
        output_format: OutputFormat = OutputFormat.TEXT,
    ) -> str:
        """
        Generate a brief from search results and analysis data.

        Args:
            query: Original search query
            search_results: List of entity search results
            risk_assessments: Optional list of risk assessments
            opportunity_analyses: Optional list of opportunity analyses
            metrics: Optional list of entity metrics
            output_format: Output format (text, json, pdf)

        Returns:
            Formatted brief string
        """
        if not search_results:
            raise ValueError("Search results cannot be empty")

        # Build sections from search results
        sections = []
        entity_count = len(search_results)

        # Create summary section
        entity_names = [r.get("name", "Unknown") for r in search_results]
        main_entity = entity_names[0] if entity_names else "Unknown"

        summary_section = BriefSection(
            title="Executive Summary",
            content=f"Analysis of {entity_count} project(s) based on query: '{query}'",
            key_findings=[f"Found {entity_count} relevant project(s)"],
            data_points={"entities": entity_names},
        )
        sections.append(summary_section)

        # Add detailed sections for each result
        for i, result in enumerate(search_results):
            entity_name = result.get("name", f"Entity {i + 1}")
            category = result.get("category", "General")

            content_lines = [f"## {entity_name}", ""]
            content_lines.append(f"Category: {category}")

            if description := result.get("description"):
                content_lines.append(f"Description: {description}")

            section = BriefSection(
                title=entity_name,
                content="\n".join(content_lines),
                key_findings=result.get("highlights", []),
                data_points=result,
            )
            sections.append(section)

        # Add metrics sections
        if metrics:
            primary_metrics = metrics[0] if metrics else None
            if primary_metrics:
                metrics_text = self.template.format_metrics_summary(
                    primary_metrics, main_entity
                )
                sections.append(
                    BriefSection(
                        title="Key Metrics",
                        content=metrics_text,
                        key_findings=[f"TVL: ${primary_metrics.tvl:,.2f}"]
                        if primary_metrics.tvl > 0
                        else [],
                    )
                )

        # Add risk assessments
        risk_assessments_list: list[RiskAssessment] = []
        if risk_assessments:
            risk_assessments_list = risk_assessments

        if risk_assessments_list:
            # Use the first entity's risk assessment
            risk = risk_assessments_list[0]
            risk_text = self.template.format_risk_summary(risk)
            sections.append(
                BriefSection(
                    title="Risk Assessment",
                    content=risk_text,
                    key_findings=risk.key_risks
                    if len(risk.key_risks) <= 3
                    else risk.key_risks[:3],
                )
            )

        # Add opportunity analyses
        opportunity_analyses_list: list[OpportunityAnalysis] = []
        if opportunity_analyses:
            opportunity_analyses_list = opportunity_analyses

        if opportunity_analyses_list:
            opp = opportunity_analyses_list[0]
            opp_text = self.template.format_opportunity_summary(opp)
            sections.append(
                BriefSection(
                    title="Opportunity Analysis",
                    content=opp_text,
                    key_findings=opp.key_opportunities
                    if len(opp.key_opportunities) <= 3
                    else ["Strong momentum indicators"],
                )
            )

        # Calculate average confidence
        confidence = 0.85
        if risk_assessments_list:
            confidence = (confidence + risk_assessments_list[0].confidence) / 2
        if opportunity_analyses_list:
            confidence = (confidence + opportunity_analyses_list[0].confidence) / 2

        # Generate brief
        brief = self.generate(
            query=query,
            sections=sections,
            risk_assessment=risk_assessments_list[0] if risk_assessments_list else None,
            opportunity_analysis=opportunity_analyses_list[0]
            if opportunity_analyses_list
            else None,
            metrics=metrics[0] if metrics else None,
            entity_count=entity_count,
            confidence=round(confidence, 2),
        )

        # Format output
        if output_format == OutputFormat.JSON:
            return brief.to_json()
        elif output_format == OutputFormat.TEXT:
            return brief.to_text()
        else:
            # PDF format - return JSON as placeholder
            # In production, this would convert to PDF
            return brief.to_json()

    def _validate_risk_assessment(self, risk: RiskAssessment) -> None:
        """Validate risk assessment data."""
        if not (0.0 <= risk.overall_risk_score <= 1.0):
            raise ValueError("Risk score must be between 0.0 and 1.0")
        if not (0.0 <= self._clamp_confidence(risk.confidence) <= 1.0):
            raise ValueError("Risk confidence must be between 0.0 and 1.0")
        if risk.risk_level not in ("low", "medium", "high", "critical"):
            raise ValueError(f"Invalid risk level: {risk.risk_level}")

    def _validate_opportunity_analysis(self, opp: OpportunityAnalysis) -> None:
        """Validate opportunity analysis data."""
        if not (0.0 <= opp.overall_opportunity_score <= 1.0):
            raise ValueError("Opportunity score must be between 0.0 and 1.0")
        if not (0.0 <= self._clamp_confidence(opp.confidence) <= 1.0):
            raise ValueError("Opportunity confidence must be between 0.0 and 1.0")
        if opp.opportunity_level not in ("low", "medium", "high"):
            raise ValueError(f"Invalid opportunity level: {opp.opportunity_level}")

    def _validate_metrics(self, metrics: EntityMetrics) -> None:
        """Validate metrics data."""
        if metrics.tvl < 0:
            raise ValueError("TVL cannot be negative")
        if metrics.volume_24h < 0:
            raise ValueError("24h volume cannot be negative")
        if metrics.transactions_24h < 0:
            raise ValueError("Transaction count cannot be negative")
        if metrics.contract_age_days < 0:
            raise ValueError("Contract age cannot be negative")
        if metrics.holder_count < 0:
            raise ValueError("Holder count cannot be negative")

    @staticmethod
    def _clamp_confidence(value: float) -> float:
        """Clamp confidence to valid range."""
        return max(0.0, min(1.0, value))


def create_brief_generator() -> BriefGenerator:
    """Factory function to create a brief generator."""
    return BriefGenerator()
