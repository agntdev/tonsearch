"""
Test suite for Brief Generation Engine.

Tests template engine, brief generation, format output,
and integration with risk/opportunity analysis.
"""

from datetime import datetime

import pytest
from brief_generation.brief_generator import (
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


class TestRiskAssessment:
    """Tests for RiskAssessment dataclass."""

    def test_to_dict(self):
        risk = RiskAssessment(
            overall_risk_score=0.35,
            risk_level="medium",
            confidence=0.82,
            key_risks=["Unaudited contract", "High holder concentration"],
            explanations=["Contract lacks external audit"],
        )
        d = risk.to_dict()
        assert d["overall_risk_score"] == 0.35
        assert d["risk_level"] == "medium"
        assert d["confidence"] == 0.82
        assert len(d["key_risks"]) == 2

    def test_low_risk_score(self):
        risk = RiskAssessment(
            overall_risk_score=0.15,
            risk_level="low",
            confidence=0.9,
            key_risks=[],
        )
        assert risk.overall_risk_score < 0.3
        assert risk.risk_level == "low"

    def test_high_risk_score(self):
        risk = RiskAssessment(
            overall_risk_score=0.85,
            risk_level="high",
            confidence=0.75,
            key_risks=["No audit", "Rug risk"],
        )
        assert risk.overall_risk_score > 0.7
        assert risk.risk_level == "high"


class TestOpportunityAnalysis:
    """Tests for OpportunityAnalysis dataclass."""

    def test_to_dict(self):
        opp = OpportunityAnalysis(
            overall_opportunity_score=0.72,
            opportunity_level="high",
            confidence=0.88,
            key_opportunities=["Strong TVL growth", "Active dev team"],
            explanations=["TVL grew 150% in 30 days"],
        )
        d = opp.to_dict()
        assert d["overall_opportunity_score"] == 0.72
        assert d["opportunity_level"] == "high"
        assert len(d["key_opportunities"]) == 2

    def test_medium_opportunity(self):
        opp = OpportunityAnalysis(
            overall_opportunity_score=0.5,
            opportunity_level="medium",
            confidence=0.7,
        )
        assert 0.4 <= opp.overall_opportunity_score <= 0.6


class TestEntityMetrics:
    """Tests for EntityMetrics dataclass."""

    def test_to_dict_full(self):
        metrics = EntityMetrics(
            tvl=10_500_000,
            tvl_change_24h=0.052,
            volume_24h=2_300_000,
            volume_change_24h=-0.015,
            transactions_24h=15420,
            active_addresses_24h=892,
            contract_age_days=245,
            holder_count=4521,
            token_price=0.00001234,
            token_price_change_24h=0.082,
        )
        d = metrics.to_dict()
        assert d["tvl"] == 10_500_000
        assert d["tvl_change_24h"] == 0.052
        assert d["transactions_24h"] == 15420
        assert d["token_price"] == 0.00001234

    def test_default_metrics(self):
        metrics = EntityMetrics()
        assert metrics.tvl == 0.0
        assert metrics.transactions_24h == 0
        assert metrics.holder_count == 0


class TestBriefSection:
    """Tests for BriefSection dataclass."""

    def test_to_dict(self):
        section = BriefSection(
            title="Test Section",
            content="Test content with details",
            key_findings=["Finding 1", "Finding 2"],
            data_points={"tvl": 1000000, "category": "DeFi"},
        )
        d = section.to_dict()
        assert d["title"] == "Test Section"
        assert len(d["key_findings"]) == 2
        assert d["data_points"]["tvl"] == 1000000


class TestGeneratedBrief:
    """Tests for GeneratedBrief class."""

    def test_to_dict(self):
        metadata = BriefMetadata(
            brief_id="abc123",
            generated_at=datetime(2026, 5, 26, 10, 30, 0),
            query="DeFi projects on TON",
            entity_count=1,
            format=BriefFormat.STANDARD,
            confidence=0.85,
        )
        brief = GeneratedBrief(
            brief_id="abc123",
            query="DeFi projects on TON",
            metadata=metadata,
            sections=[],
        )
        d = brief.to_dict()
        assert d["brief_id"] == "abc123"
        assert d["query"] == "DeFi projects on TON"
        assert d["metadata"]["confidence"] == 0.85

    def test_to_text(self):
        metadata = BriefMetadata(
            brief_id="xyz789",
            generated_at=datetime(2026, 5, 26, 12, 0, 0),
            query="Show me NFT projects",
            entity_count=2,
            format=BriefFormat.STANDARD,
            confidence=0.90,
        )
        section = BriefSection(
            title="Test",
            content="Content here",
            key_findings=["Important finding"],
        )
        brief = GeneratedBrief(
            brief_id="xyz789",
            query="Show me NFT projects",
            metadata=metadata,
            sections=[section],
        )
        text = brief.to_text()
        assert "PROJECT BRIEF" in text
        assert "xyz789" in text
        assert "Test" in text
        assert "Important finding" in text

    def test_to_json(self):
        metadata = BriefMetadata(
            brief_id="json1",
            generated_at=datetime(2026, 5, 26, 14, 0, 0),
            query="test query",
            entity_count=1,
            format=BriefFormat.STANDARD,
            confidence=0.8,
        )
        brief = GeneratedBrief(
            brief_id="json1",
            query="test query",
            metadata=metadata,
            sections=[],
        )
        json_str = brief.to_json()
        import json

        d = json.loads(json_str)
        assert d["brief_id"] == "json1"
        assert d["metadata"]["query"] == "test query"


class TestBriefTemplate:
    """Tests for BriefTemplate class."""

    def test_format_executive_summary(self):
        result = BriefTemplate.format_executive_summary(
            entity_name="StonFi",
            category="DeFi",
            risk_level="low",
            opportunity_level="high",
            main_finding="Strong TVL growth momentum",
        )
        assert "StonFi" in result
        assert "DeFi" in result
        assert "low risk" in result
        assert "high opportunity" in result

    def test_format_metrics_summary(self):
        metrics = EntityMetrics(
            tvl=5_000_000,
            tvl_change_24h=0.035,
            volume_24h=1_200_000,
            contract_age_days=180,
            holder_count=2500,
        )
        text = BriefTemplate.format_metrics_summary(metrics, "StonFi")
        assert "StonFi" in text
        assert "5,000,000" in text
        assert "180" in text
        assert "2,500" in text

    def test_format_metrics_with_token_price(self):
        metrics = EntityMetrics(
            tvl=1000000,
            token_price=0.5,
            token_price_change_24h=0.1,
        )
        text = BriefTemplate.format_metrics_summary(metrics)
        assert "0.500000" in text or "$0.5" in text

    def test_format_risk_summary(self):
        risk = RiskAssessment(
            overall_risk_score=0.3,
            risk_level="medium",
            confidence=0.8,
            key_risks=["Unaudited contract"],
            explanations=["No external audit completed"],
        )
        text = BriefTemplate.format_risk_summary(risk)
        assert "MEDIUM" in text
        assert "30%" in text
        assert "Unaudited" in text

    def test_format_opportunity_summary(self):
        opp = OpportunityAnalysis(
            overall_opportunity_score=0.75,
            opportunity_level="high",
            confidence=0.85,
            key_opportunities=["Strong growth"],
        )
        text = BriefTemplate.format_opportunity_summary(opp)
        assert "HIGH" in text
        assert "75%" in text
        assert "Strong growth" in text


class TestBriefGenerator:
    """Tests for BriefGenerator class."""

    def test_create_generator(self):
        gen = create_brief_generator()
        assert isinstance(gen, BriefGenerator)
        assert isinstance(gen.template, BriefTemplate)

    def test_generate_minimal(self):
        gen = create_brief_generator()
        sections = [
            BriefSection(title="Test", content="Test content"),
        ]
        brief = gen.generate(
            query="test query",
            sections=sections,
            entity_count=1,
        )
        assert brief.query == "test query"
        assert len(brief.sections) == 1
        assert brief.metadata.entity_count == 1

    def test_generate_with_all_data(self):
        gen = create_brief_generator()
        sections = [
            BriefSection(title="Summary", content="Overview"),
            BriefSection(title="Details", content="More info"),
        ]
        risk = RiskAssessment(
            overall_risk_score=0.4,
            risk_level="medium",
            confidence=0.85,
        )
        opp = OpportunityAnalysis(
            overall_opportunity_score=0.65,
            opportunity_level="high",
            confidence=0.8,
        )
        metrics = EntityMetrics(tvl=5_000_000)

        brief = gen.generate(
            query="Full test",
            sections=sections,
            risk_assessment=risk,
            opportunity_analysis=opp,
            metrics=metrics,
            entity_count=1,
            confidence=0.82,
        )
        assert brief.risk_assessment is not None
        assert brief.opportunity_analysis is not None
        assert brief.metrics is not None
        assert brief.metadata.confidence == 0.82

    def test_generate_with_search_results(self):
        gen = create_brief_generator()
        search_results = [
            {"name": "StonFi", "category": "DeFi", "description": "DEX on TON"},
            {"name": "Dedust", "category": "DeFi", "description": "AMM"},
        ]
        text = gen.generate_with_search_results(
            query="DeFi projects",
            search_results=search_results,
        )
        assert "DeFi projects" in text or "2" in text
        assert "StonFi" in text
        assert "Dedust" in text

    def test_generate_with_search_results_json(self):
        gen = create_brief_generator()
        search_results = [{"name": "Test", "category": "NFT"}]
        json_out = gen.generate_with_search_results(
            query="NFT query",
            search_results=search_results,
            output_format=OutputFormat.JSON,
        )
        import json

        d = json.loads(json_out)
        assert "brief_id" in d

    def test_validation_empty_query(self):
        gen = create_brief_generator()
        with pytest.raises(ValueError, match="Query cannot be empty"):
            gen.generate(query="", sections=[], entity_count=1)

    def test_validation_zero_entity_count(self):
        gen = create_brief_generator()
        with pytest.raises(ValueError, match="Entity count must be at least 1"):
            gen.generate(query="test", sections=[], entity_count=0)

    def test_validation_invalid_confidence(self):
        gen = create_brief_generator()
        with pytest.raises(ValueError, match="Confidence must be between"):
            gen.generate(query="test", sections=[], entity_count=1, confidence=1.5)

    def test_validation_invalid_risk_score(self):
        gen = create_brief_generator()
        risk = RiskAssessment(
            overall_risk_score=1.5,
            risk_level="high",
            confidence=0.8,
        )
        with pytest.raises(ValueError, match="Risk score must be"):
            gen.generate(query="test", sections=[], risk_assessment=risk)

    def test_validation_invalid_risk_level(self):
        gen = create_brief_generator()
        risk = RiskAssessment(
            overall_risk_score=0.5,
            risk_level="veryhigh",
            confidence=0.8,
        )
        with pytest.raises(ValueError, match="Invalid risk level"):
            gen.generate(query="test", sections=[], risk_assessment=risk)

    def test_validation_negative_tvl(self):
        gen = create_brief_generator()
        metrics = EntityMetrics(tvl=-100)
        with pytest.raises(ValueError, match="TVL cannot be negative"):
            gen.generate(query="test", sections=[], metrics=metrics)

    def test_text_output_format(self):
        gen = create_brief_generator()
        sections = [BriefSection(title="T", content="C")]
        brief = gen.generate(query="format test", sections=sections)
        text = brief.to_text()
        assert isinstance(text, str)
        lines = text.split("\n")
        assert len(lines) > 0
        assert "PROJECT BRIEF" in text


class TestOutputFormat:
    """Tests for OutputFormat enum."""

    def test_format_values(self):
        assert OutputFormat.TEXT.value == "text"
        assert OutputFormat.JSON.value == "json"
        assert OutputFormat.PDF.value == "pdf"

    def test_is_string_enum(self):
        assert isinstance(OutputFormat.TEXT, str)


class TestBriefFormat:
    """Tests for BriefFormat enum."""

    def test_format_values(self):
        assert BriefFormat.STANDARD.value == "standard"
        assert BriefFormat.DETAILED.value == "detailed"
        assert BriefFormat.EXECUTIVE.value == "executive"


class TestIntegration:
    """Integration tests with risk_opportunity_analyzer."""

    def test_brief_integration_with_risk_analyzer(self):
        from risk_opportunity_analyzer import (
            OpportunitySignals,
            RiskOpportunityAnalyzer,
            RiskSignals,
            create_analyzer,
        )

        # Create analyzer and get analysis
        analyzer = create_analyzer()
        risk_signals = RiskSignals(
            audit_status=0.8,
            wallet_activity_risk=0.7,
            funding_history_score=0.6,
            contract_age_score=0.5,
            interaction_diversity=0.4,
            holder_concentration=0.3,
            smart_contract_complexity=0.5,
        )
        opp_signals = OpportunitySignals(
            tvl_growth_rate=0.7,
            volume_growth_rate=0.6,
            developer_activity_score=0.8,
            network_effect_score=0.5,
            innovation_score=0.6,
            community_engagement=0.7,
            token_performance=0.5,
        )

        analysis = analyzer.analyze(
            entity_id="stake.dart",
            entity_type="project",
            risk_signals=risk_signals,
            opportunity_signals=opp_signals,
        )

        # Create brief generator
        gen = create_brief_generator()
        # Normalize scores from 0-100 to 0-1
        risk_assessment = RiskAssessment(
            overall_risk_score=analysis.risk_assessment.overall_risk_score / 100.0,
            risk_level=analysis.risk_assessment.risk_level.value,
            confidence=analysis.risk_assessment.confidence,
            key_risks=analysis.risk_assessment.key_risks,
            explanations=analysis.risk_assessment.explanations,
        )
        opp_analysis = OpportunityAnalysis(
            overall_opportunity_score=analysis.opportunity_assessment.overall_opportunity_score
            / 100.0,
            opportunity_level=analysis.opportunity_assessment.opportunity_level.value,
            confidence=analysis.opportunity_assessment.confidence,
            key_opportunities=analysis.opportunity_assessment.key_opportunities,
            explanations=analysis.opportunity_assessment.explanations,
        )

        sections = [
            BriefSection(
                title="Executive Summary",
                content=f"Analysis of {analysis.entity_id}",
                key_findings=analysis.risk_assessment.key_risks[:2],
            ),
        ]

        brief = gen.generate(
            query="stake.dart analysis",
            sections=sections,
            risk_assessment=risk_assessment,
            opportunity_analysis=opp_analysis,
            entity_count=1,
            confidence=analysis.confidence,
        )

        assert brief.query == "stake.dart analysis"
        assert brief.risk_assessment is not None
        assert brief.opportunity_analysis is not None
        assert brief.metadata.confidence > 0

    def test_brief_with_metrics_from_analysis(self):
        from risk_opportunity_analyzer import create_analyzer

        analyzer = create_analyzer()
        # Use default analysis
        analysis = analyzer.analyze_with_defaults(
            entity_id="test.project",
            entity_type="project",
        )

        metrics = EntityMetrics(
            tvl=5_000_000,
            tvl_change_24h=0.03,
            volume_24h=1_500_000,
            volume_change_24h=-0.02,
            transactions_24h=5000,
            active_addresses_24h=450,
            contract_age_days=180,
            holder_count=3200,
        )

        gen = create_brief_generator()
        brief = gen.generate(
            query="test metrics",
            sections=[BriefSection(title="Test", content="Content")],
            metrics=metrics,
            entity_count=1,
        )

        assert brief.metrics is not None
        assert brief.metrics.tvl == 5_000_000


class TestPerformanceAndEdgeCases:
    """Tests for performance and edge cases."""

    def test_multiple_entities(self):
        gen = create_brief_generator()
        sections = [
            BriefSection(title=f"Entity {i}", content=f"Content {i}") for i in range(10)
        ]
        brief = gen.generate(
            query="batch test",
            sections=sections,
            entity_count=10,
        )
        assert brief.metadata.entity_count == 10
        assert len(brief.sections) == 10

    def test_empty_sections(self):
        gen = create_brief_generator()
        brief = gen.generate(
            query="empty sections",
            sections=[],
            entity_count=1,
        )
        assert len(brief.sections) == 0

    def test_special_characters_in_query(self):
        gen = create_brief_generator()
        sections = [BriefSection(title="T", content="C")]
        special_query = "DeFi project with $100M TVL & 50%+ APY"
        brief = gen.generate(query=special_query, sections=sections)
        assert brief.query == special_query

    def test_unicode_content(self):
        gen = create_brief_generator()
        sections = [
            BriefSection(
                title="日本語セクション",
                content="テストコンテンツ 🎉",
                key_findings=["発見1", "発見2"],
            )
        ]
        brief = gen.generate(
            query="unicode test",
            sections=sections,
        )
        assert "日本語セクション" in brief.sections[0].title

    def test_large_metrics_values(self):
        gen = create_brief_generator()
        metrics = EntityMetrics(
            tvl=1_000_000_000_000,  # 1 trillion
            volume_24h=500_000_000_000,
            transactions_24h=10_000_000,
            holder_count=1_000_000_000,
        )
        brief = gen.generate(
            query="large values",
            sections=[],
            metrics=metrics,
            entity_count=1,
        )
        text = brief.to_text()
        assert "1,000,000,000,000" in text
        assert "10,000,000" in text
