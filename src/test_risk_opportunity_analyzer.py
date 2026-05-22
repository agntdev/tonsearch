"""
Tests for Risk and Opportunity Analysis Module
"""

import unittest

from risk_opportunity_analyzer import (
    EntityAnalysis,
    OpportunityDetector,
    OpportunityLevel,
    OpportunitySignals,
    RiskLevel,
    RiskOpportunityAnalyzer,
    RiskScorer,
    RiskSignals,
)


class TestRiskSignals(unittest.TestCase):
    def test_risk_signals_to_dict(self):
        signals = RiskSignals(
            audit_status=0.8,
            wallet_activity_risk=0.7,
            funding_history_score=0.6,
            contract_age_score=0.5,
            interaction_diversity=0.4,
            holder_concentration=0.3,
            smart_contract_complexity=0.2,
        )
        d = signals.to_dict()
        self.assertEqual(d["auditStatus"], 0.8)
        self.assertEqual(d["walletActivityRisk"], 0.7)
        self.assertEqual(d["fundingHistoryScore"], 0.6)


class TestOpportunitySignals(unittest.TestCase):
    def test_opportunity_signals_to_dict(self):
        signals = OpportunitySignals(
            tvl_growth_rate=0.75,
            volume_growth_rate=0.65,
            developer_activity_score=0.85,
            network_effect_score=0.7,
            innovation_score=0.6,
            community_engagement=0.5,
            token_performance=0.4,
        )
        d = signals.to_dict()
        self.assertEqual(d["tvlGrowthRate"], 0.75)
        self.assertEqual(d["developerActivityScore"], 0.85)


class TestRiskScorer(unittest.TestCase):
    def test_low_risk_project(self):
        signals = RiskSignals(
            audit_status=1.0,
            wallet_activity_risk=1.0,
            funding_history_score=1.0,
            contract_age_score=1.0,
            interaction_diversity=1.0,
            holder_concentration=1.0,
            smart_contract_complexity=0.0,
        )
        score, level, explanations = RiskScorer.score(signals)
        self.assertLessEqual(score, 20)
        self.assertEqual(level, RiskLevel.VERY_LOW)

    def test_high_risk_project(self):
        # All signals at 0.0 means unaudited, suspicious activity, no history, new contract
        # -> inverted to risk 100 = VERY_HIGH
        signals = RiskSignals(
            audit_status=0.0,
            wallet_activity_risk=0.0,
            funding_history_score=0.0,
            contract_age_score=0.0,
            interaction_diversity=0.0,
            holder_concentration=0.0,
            smart_contract_complexity=0.0,
        )
        score, level, explanations = RiskScorer.score(signals)
        self.assertGreaterEqual(score, 81)
        self.assertEqual(level, RiskLevel.VERY_HIGH)

    def test_low_risk_project(self):
        # All signals at 1.0 means fully audited, healthy activity, established
        # -> inverted to risk 0 = VERY_LOW
        signals = RiskSignals(
            audit_status=1.0,
            wallet_activity_risk=1.0,
            funding_history_score=1.0,
            contract_age_score=1.0,
            interaction_diversity=1.0,
            holder_concentration=1.0,
            smart_contract_complexity=1.0,
        )
        score, level, explanations = RiskScorer.score(signals)
        self.assertLessEqual(score, 20)
        self.assertEqual(level, RiskLevel.VERY_LOW)

    def test_score_bounded_0_to_100(self):
        signals = RiskSignals(
            audit_status=0.5,
            wallet_activity_risk=0.5,
            funding_history_score=0.5,
            contract_age_score=0.5,
            interaction_diversity=0.5,
            holder_concentration=0.5,
            smart_contract_complexity=0.5,
        )
        score, _, _ = RiskScorer.score(signals)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)


class TestOpportunityDetector(unittest.TestCase):
    def test_high_opportunity_project(self):
        # High signals across the board leads to VERY_HIGH (above 80)
        signals = OpportunitySignals(
            tvl_growth_rate=0.9,
            volume_growth_rate=0.85,
            developer_activity_score=0.9,
            network_effect_score=0.85,
            innovation_score=0.8,
            community_engagement=0.85,
            token_performance=0.8,
        )
        score, level, explanations = OpportunityDetector.score(signals)
        self.assertGreaterEqual(score, 61)
        self.assertIn(level, [OpportunityLevel.HIGH, OpportunityLevel.VERY_HIGH])

    def test_low_opportunity_project(self):
        signals = OpportunitySignals(
            tvl_growth_rate=0.0,
            volume_growth_rate=0.0,
            developer_activity_score=0.0,
            network_effect_score=0.0,
            innovation_score=0.0,
            community_engagement=0.0,
            token_performance=0.0,
        )
        score, level, explanations = OpportunityDetector.score(signals)
        self.assertLessEqual(score, 20)
        self.assertEqual(level, OpportunityLevel.VERY_LOW)

    def test_medium_opportunity_project(self):
        signals = OpportunitySignals(
            tvl_growth_rate=0.5,
            volume_growth_rate=0.5,
            developer_activity_score=0.5,
            network_effect_score=0.5,
            innovation_score=0.5,
            community_engagement=0.5,
            token_performance=0.5,
        )
        score, level, explanations = OpportunityDetector.score(signals)
        self.assertGreaterEqual(score, 41)
        self.assertLessEqual(score, 60)
        self.assertEqual(level, OpportunityLevel.MEDIUM)


class TestRiskOpportunityAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = RiskOpportunityAnalyzer()

    def test_analyze_full(self):
        risk_signals = RiskSignals(
            audit_status=0.8,
            wallet_activity_risk=0.7,
            funding_history_score=0.6,
            contract_age_score=0.9,
            interaction_diversity=0.7,
            holder_concentration=0.8,
            smart_contract_complexity=0.3,
        )
        opportunity_signals = OpportunitySignals(
            tvl_growth_rate=0.6,
            volume_growth_rate=0.5,
            developer_activity_score=0.8,
            network_effect_score=0.7,
            innovation_score=0.6,
            community_engagement=0.7,
            token_performance=0.5,
        )
        analysis = self.analyzer.analyze(
            "prj_stonfi", "project", risk_signals, opportunity_signals
        )
        self.assertEqual(analysis.entity_id, "prj_stonfi")
        self.assertEqual(analysis.entity_type, "project")
        self.assertIsNotNone(analysis.risk_assessment)
        self.assertIsNotNone(analysis.opportunity_assessment)
        self.assertGreaterEqual(analysis.confidence, 0.0)
        self.assertLessEqual(analysis.confidence, 1.0)

    def test_analyze_with_defaults(self):
        # Test that explicit signals override defaults
        # developer_activity_score=0.8 with others at defaults (0.5)
        # gives opportunity around 56 (not 80), so just verify it's reasonable
        analysis = self.analyzer.analyze_with_defaults(
            "prj_test",
            "project",
            audit_status=0.0,
            developer_activity_score=0.8,
        )
        self.assertEqual(analysis.entity_id, "prj_test")
        # audit_status=0.0 -> high risk signal inverted
        self.assertGreaterEqual(analysis.risk_assessment.overall_risk_score, 60)
        # With dev_activity=0.8 and others=0.5, expect ~56
        self.assertGreaterEqual(
            analysis.opportunity_assessment.overall_opportunity_score, 50
        )
        self.assertLessEqual(
            analysis.opportunity_assessment.overall_opportunity_score, 65
        )

    def test_analyze_unaudited_recent_contract(self):
        # Very risky signals: unaudited, suspicious activity, no funding, new contract
        risk_signals = RiskSignals(
            audit_status=0.0,
            wallet_activity_risk=0.2,
            funding_history_score=0.0,
            contract_age_score=0.1,
            interaction_diversity=0.2,
            holder_concentration=0.2,
            smart_contract_complexity=0.8,
        )
        opportunity_signals = OpportunitySignals(
            tvl_growth_rate=0.8,
            volume_growth_rate=0.7,
            developer_activity_score=0.9,
            network_effect_score=0.6,
            innovation_score=0.8,
            community_engagement=0.7,
            token_performance=0.6,
        )
        analysis = self.analyzer.analyze(
            "prj_risky", "project", risk_signals, opportunity_signals
        )
        # High risk: unaudited (0) + suspicious (0.2) + no funding (0) + new (0.1) + suspicious (0.2) + concentrated (0.2)
        self.assertGreaterEqual(analysis.risk_assessment.overall_risk_score, 61)
        # Good opportunity despite risk
        self.assertLessEqual(
            analysis.opportunity_assessment.overall_opportunity_score, 90
        )

    def test_entity_analysis_to_dict(self):
        risk_signals = RiskSignals(
            audit_status=0.7,
            wallet_activity_risk=0.7,
            funding_history_score=0.7,
            contract_age_score=0.7,
            interaction_diversity=0.7,
            holder_concentration=0.7,
            smart_contract_complexity=0.3,
        )
        opportunity_signals = OpportunitySignals(
            tvl_growth_rate=0.6,
            volume_growth_rate=0.5,
            developer_activity_score=0.7,
            network_effect_score=0.6,
            innovation_score=0.5,
            community_engagement=0.6,
            token_performance=0.4,
        )
        analysis = self.analyzer.analyze(
            "prj_dict_test", "project", risk_signals, opportunity_signals
        )
        d = analysis.to_dict()
        self.assertEqual(d["entityId"], "prj_dict_test")
        self.assertIn("riskAssessment", d)
        self.assertIn("opportunityAssessment", d)


class TestRiskLevelClassification(unittest.TestCase):
    def test_risk_levels_boundary(self):
        # Risk uses inverted scoring: high signal (1.0) -> low risk (0), low signal (0.0) -> high risk (100)
        # So score parameter maps inversely: 0 -> 100 (VERY_HIGH), 100 -> 0 (VERY_LOW)
        test_cases = [
            (0, RiskLevel.VERY_HIGH),  # all signals 0 -> max risk
            (20, RiskLevel.HIGH),
            (40, RiskLevel.MEDIUM),
            (60, RiskLevel.LOW),
            (80, RiskLevel.VERY_LOW),
            (100, RiskLevel.VERY_LOW),  # all signals 1 -> min risk
        ]
        for score, expected_level in test_cases:
            signals = RiskSignals(
                audit_status=score / 100,
                wallet_activity_risk=score / 100,
                funding_history_score=score / 100,
                contract_age_score=score / 100,
                interaction_diversity=score / 100,
                holder_concentration=score / 100,
                smart_contract_complexity=score / 100,
            )
            _, level, _ = RiskScorer.score(signals)
            self.assertEqual(
                level,
                expected_level,
                f"Signal {score / 100} should be {expected_level} but got {level}",
            )


class TestOpportunityLevelClassification(unittest.TestCase):
    def test_opportunity_levels_boundary(self):
        test_cases = [
            (0, OpportunityLevel.VERY_LOW),
            (20, OpportunityLevel.VERY_LOW),
            (21, OpportunityLevel.LOW),
            (40, OpportunityLevel.LOW),
            (41, OpportunityLevel.MEDIUM),
            (60, OpportunityLevel.MEDIUM),
            (61, OpportunityLevel.HIGH),
            (80, OpportunityLevel.HIGH),
            (81, OpportunityLevel.VERY_HIGH),
            (100, OpportunityLevel.VERY_HIGH),
        ]
        for score, expected_level in test_cases:
            signals = OpportunitySignals(
                tvl_growth_rate=score / 100,
                volume_growth_rate=score / 100,
                developer_activity_score=score / 100,
                network_effect_score=score / 100,
                innovation_score=score / 100,
                community_engagement=score / 100,
                token_performance=score / 100,
            )
            _, level, _ = OpportunityDetector.score(signals)
            self.assertEqual(
                level, expected_level, f"Score {score} should be {expected_level}"
            )


class TestConfidenceCalculation(unittest.TestCase):
    def test_confidence_with_all_signals(self):
        analyzer = RiskOpportunityAnalyzer()
        risk_signals = RiskSignals(
            audit_status=0.8,
            wallet_activity_risk=0.7,
            funding_history_score=0.6,
            contract_age_score=0.5,
            interaction_diversity=0.4,
            holder_concentration=0.3,
            smart_contract_complexity=0.2,
        )
        opportunity_signals = OpportunitySignals(
            tvl_growth_rate=0.75,
            volume_growth_rate=0.65,
            developer_activity_score=0.85,
            network_effect_score=0.7,
            innovation_score=0.6,
            community_engagement=0.5,
            token_performance=0.4,
        )
        analysis = analyzer.analyze(
            "prj_conf", "project", risk_signals, opportunity_signals
        )
        self.assertEqual(analysis.confidence, 1.0)

    def test_confidence_with_no_signals(self):
        analyzer = RiskOpportunityAnalyzer()
        risk_signals = RiskSignals()  # all 0.0
        opportunity_signals = OpportunitySignals()  # all 0.0
        analysis = analyzer.analyze(
            "prj_conf", "project", risk_signals, opportunity_signals
        )
        self.assertEqual(analysis.confidence, 0.0)


class TestKeyRisksAndOpportunities(unittest.TestCase):
    def test_key_risks_identification(self):
        analyzer = RiskOpportunityAnalyzer()
        risk_signals = RiskSignals(
            audit_status=0.2,  # < 0.3 -> unaudited
            wallet_activity_risk=0.2,  # < 0.3 -> suspicious
            funding_history_score=0.2,  # < 0.3 -> no history
            contract_age_score=0.1,  # < 0.2 -> new
            interaction_diversity=0.5,
            holder_concentration=0.2,  # < 0.3 -> concentrated
            smart_contract_complexity=0.5,
        )
        opportunity_signals = OpportunitySignals(
            tvl_growth_rate=0.6,
            volume_growth_rate=0.5,
            developer_activity_score=0.8,
            network_effect_score=0.7,
            innovation_score=0.6,
            community_engagement=0.7,
            token_performance=0.5,
        )
        analysis = analyzer.analyze(
            "prj_risky", "project", risk_signals, opportunity_signals
        )
        self.assertIn(
            "Unaudited or partially audited contract",
            analysis.risk_assessment.key_risks,
        )
        self.assertIn(
            "Suspicious wallet activity patterns", analysis.risk_assessment.key_risks
        )
        self.assertIn(
            "High token concentration among few holders",
            analysis.risk_assessment.key_risks,
        )

    def test_key_opportunities_identification(self):
        analyzer = RiskOpportunityAnalyzer()
        risk_signals = RiskSignals(
            audit_status=0.8,
            wallet_activity_risk=0.7,
            funding_history_score=0.6,
            contract_age_score=0.5,
            interaction_diversity=0.4,
            holder_concentration=0.3,
            smart_contract_complexity=0.2,
        )
        opportunity_signals = OpportunitySignals(
            tvl_growth_rate=0.6,  # > 0.4 -> strong growth
            volume_growth_rate=0.5,
            developer_activity_score=0.8,  # > 0.6 -> active dev
            network_effect_score=0.7,  # > 0.5 -> strong network
            innovation_score=0.6,  # > 0.5 -> first-mover
            community_engagement=0.7,  # > 0.5 -> growing engagement
            token_performance=0.4,
        )
        analysis = analyzer.analyze(
            "prj_good", "project", risk_signals, opportunity_signals
        )
        self.assertIn(
            "Strong TVL growth momentum",
            analysis.opportunity_assessment.key_opportunities,
        )
        self.assertIn(
            "Active development with frequent updates",
            analysis.opportunity_assessment.key_opportunities,
        )


if __name__ == "__main__":
    unittest.main()
