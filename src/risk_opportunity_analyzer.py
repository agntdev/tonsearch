"""
Risk and Opportunity Analysis Module

Calculates risk scores based on:
- Contract audit status
- Wallet activity patterns
- Funding history

Identifies opportunities using:
- Growth metrics
- Network effects
- Developer activity
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class RiskLevel(Enum):
    """Risk classification levels."""

    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class OpportunityLevel(Enum):
    """Opportunity classification levels."""

    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


@dataclass
class RiskSignals:
    """Individual signals that contribute to risk scoring."""

    audit_status: float = 0.0  # 0.0 = unaudited, 1.0 = fully audited
    wallet_activity_risk: float = 0.0  # 0.0 = suspicious, 1.0 = healthy
    funding_history_score: float = 0.0  # 0.0 = no history, 1.0 = strong history
    contract_age_score: float = 0.0  # 0.0 = new (<30d), 1.0 = established (>1y)
    interaction_diversity: float = 0.0  # 0.0 = isolated, 1.0 = well-connected
    holder_concentration: float = 0.0  # 0.0 = concentrated, 1.0 = distributed
    smart_contract_complexity: float = 0.0  # 0.0 = simple, 1.0 = complex

    def to_dict(self) -> dict:
        return {
            "auditStatus": self.audit_status,
            "walletActivityRisk": self.wallet_activity_risk,
            "fundingHistoryScore": self.funding_history_score,
            "contractAgeScore": self.contract_age_score,
            "interactionDiversity": self.interaction_diversity,
            "holderConcentration": self.holder_concentration,
            "smartContractComplexity": self.smart_contract_complexity,
        }


@dataclass
class OpportunitySignals:
    """Individual signals that contribute to opportunity scoring."""

    tvl_growth_rate: float = 0.0  # annualized growth rate
    volume_growth_rate: float = 0.0  # 24h volume growth
    developer_activity_score: float = 0.0  # 0.0 = inactive, 1.0 = highly active
    network_effect_score: float = 0.0  # based on user count, integrations
    innovation_score: float = 0.0  # unique features, first-mover
    community_engagement: float = 0.0  # social activity, retention
    token_performance: float = 0.0  # price momentum, volume

    def to_dict(self) -> dict:
        return {
            "tvlGrowthRate": self.tvl_growth_rate,
            "volumeGrowthRate": self.volume_growth_rate,
            "developerActivityScore": self.developer_activity_score,
            "networkEffectScore": self.network_effect_score,
            "innovationScore": self.innovation_score,
            "communityEngagement": self.community_engagement,
            "tokenPerformance": self.token_performance,
        }


@dataclass
class RiskAssessment:
    """Complete risk assessment for an entity."""

    entity_id: str
    entity_type: str
    overall_risk_score: int  # 0-100
    risk_level: RiskLevel
    key_risks: list[str] = field(default_factory=list)
    signals: Optional[RiskSignals] = None
    confidence: float = 0.0
    explanations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "entityId": self.entity_id,
            "entityType": self.entity_type,
            "overallRiskScore": self.overall_risk_score,
            "riskLevel": self.risk_level.value,
            "keyRisks": self.key_risks,
            "signals": self.signals.to_dict() if self.signals else {},
            "confidence": self.confidence,
            "explanations": self.explanations,
        }


@dataclass
class OpportunityAssessment:
    """Complete opportunity assessment for an entity."""

    entity_id: str
    entity_type: str
    overall_opportunity_score: int  # 0-100
    opportunity_level: OpportunityLevel
    key_opportunities: list[str] = field(default_factory=list)
    signals: Optional[OpportunitySignals] = None
    confidence: float = 0.0
    explanations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "entityId": self.entity_id,
            "entityType": self.entity_type,
            "overallOpportunityScore": self.overall_opportunity_score,
            "opportunityLevel": self.opportunity_level.value,
            "keyOpportunities": self.key_opportunities,
            "signals": self.signals.to_dict() if self.signals else {},
            "confidence": self.confidence,
            "explanations": self.explanations,
        }


@dataclass
class EntityAnalysis:
    """Combined risk and opportunity analysis for an entity."""

    entity_id: str
    entity_type: str
    risk_assessment: RiskAssessment
    opportunity_assessment: OpportunityAssessment
    confidence: float = 0.0

    def to_dict(self) -> dict:
        return {
            "entityId": self.entity_id,
            "entityType": self.entity_type,
            "riskAssessment": self.risk_assessment.to_dict(),
            "opportunityAssessment": self.opportunity_assessment.to_dict(),
            "confidence": self.confidence,
        }


# -----------------------------------------------------------------------------
# Risk Scoring Algorithm
# -----------------------------------------------------------------------------


class RiskScorer:
    """
    Calculates risk scores for TON entities.

    Risk score is 0-100 where:
    - 0-20: VERY_LOW risk
    - 21-40: LOW risk
    - 41-60: MEDIUM risk
    - 61-80: HIGH risk
    - 81-100: VERY_HIGH risk
    """

    WEIGHTS = {
        "audit_status": 0.25,
        "wallet_activity": 0.20,
        "funding_history": 0.15,
        "contract_age": 0.15,
        "interaction_diversity": 0.10,
        "holder_concentration": 0.10,
        "smart_contract_complexity": 0.05,
    }

    @classmethod
    def score(cls, signals: RiskSignals) -> tuple[int, RiskLevel, list[str]]:
        """
        Calculate overall risk score from signals.
        Returns (score, level, explanations).
        """
        # Invert signals: high signal value means LOW risk, so we use (1 - signal)
        score = (
            (1 - signals.audit_status) * cls.WEIGHTS["audit_status"] * 100
            + (1 - signals.wallet_activity_risk) * cls.WEIGHTS["wallet_activity"] * 100
            + (1 - signals.funding_history_score) * cls.WEIGHTS["funding_history"] * 100
            + (1 - signals.contract_age_score) * cls.WEIGHTS["contract_age"] * 100
            + (1 - signals.interaction_diversity)
            * cls.WEIGHTS["interaction_diversity"]
            * 100
            + (1 - signals.holder_concentration)
            * cls.WEIGHTS["holder_concentration"]
            * 100
            + (1 - signals.smart_contract_complexity)
            * cls.WEIGHTS["smart_contract_complexity"]
            * 100
        )

        overall_score = int(round(score))
        level = cls._score_to_level(overall_score)
        explanations = cls._generate_explanations(signals, overall_score)

        return overall_score, level, explanations

    @classmethod
    def _score_to_level(cls, score: int) -> RiskLevel:
        if score <= 20:
            return RiskLevel.VERY_LOW
        elif score <= 40:
            return RiskLevel.LOW
        elif score <= 60:
            return RiskLevel.MEDIUM
        elif score <= 80:
            return RiskLevel.HIGH
        else:
            return RiskLevel.VERY_HIGH

    @classmethod
    def _generate_explanations(cls, signals: RiskSignals, score: int) -> list[str]:
        explanations = []

        if signals.audit_status < 0.5:
            explanations.append(
                f"Contract audit status is {'unverified' if signals.audit_status < 0.25 else 'partial'} "
                f"(score: {signals.audit_status:.2f})"
            )

        if signals.wallet_activity_risk < 0.5:
            explanations.append(
                f"Wallet activity shows {'suspicious' if signals.wallet_activity_risk < 0.25 else 'concerning'} patterns "
                f"(score: {signals.wallet_activity_risk:.2f})"
            )

        if signals.funding_history_score < 0.5:
            explanations.append(
                f"Limited or no funding history traceable "
                f"(score: {signals.funding_history_score:.2f})"
            )

        if signals.contract_age_score < 0.3:
            explanations.append(
                f"Contract is recently deployed (less than 30 days old)"
            )

        if signals.interaction_diversity < 0.3:
            explanations.append(
                f"Low interaction diversity - limited connections to other entities"
            )

        if signals.holder_concentration < 0.3:
            explanations.append(f"High token/nft concentration among few holders")

        if score > 60 and signals.smart_contract_complexity > 0.7:
            explanations.append(
                f"High smart contract complexity increases attack surface"
            )

        if not explanations:
            explanations.append("No significant risk factors identified")

        return explanations


# -----------------------------------------------------------------------------
# Opportunity Detection Model
# -----------------------------------------------------------------------------


class OpportunityDetector:
    """
    Detects and scores opportunities for TON entities.

    Opportunity score is 0-100 where:
    - 0-20: VERY_LOW opportunity
    - 21-40: LOW opportunity
    - 41-60: MEDIUM opportunity
    - 61-80: HIGH opportunity
    - 81-100: VERY_HIGH opportunity
    """

    WEIGHTS = {
        "tvl_growth": 0.25,
        "volume_growth": 0.15,
        "developer_activity": 0.20,
        "network_effect": 0.15,
        "innovation": 0.10,
        "community_engagement": 0.10,
        "token_performance": 0.05,
    }

    @classmethod
    def score(
        cls, signals: OpportunitySignals
    ) -> tuple[int, OpportunityLevel, list[str]]:
        """
        Calculate overall opportunity score from signals.
        Returns (score, level, explanations).
        """
        score = (
            signals.tvl_growth_rate * cls.WEIGHTS["tvl_growth"] * 100
            + signals.volume_growth_rate * cls.WEIGHTS["volume_growth"] * 100
            + signals.developer_activity_score * cls.WEIGHTS["developer_activity"] * 100
            + signals.network_effect_score * cls.WEIGHTS["network_effect"] * 100
            + signals.innovation_score * cls.WEIGHTS["innovation"] * 100
            + signals.community_engagement * cls.WEIGHTS["community_engagement"] * 100
            + signals.token_performance * cls.WEIGHTS["token_performance"] * 100
        )

        overall_score = int(round(max(0, min(100, score))))
        level = cls._score_to_level(overall_score)
        explanations = cls._generate_explanations(signals, overall_score)

        return overall_score, level, explanations

    @classmethod
    def _score_to_level(cls, score: int) -> OpportunityLevel:
        if score <= 20:
            return OpportunityLevel.VERY_LOW
        elif score <= 40:
            return OpportunityLevel.LOW
        elif score <= 60:
            return OpportunityLevel.MEDIUM
        elif score <= 80:
            return OpportunityLevel.HIGH
        else:
            return OpportunityLevel.VERY_HIGH

    @classmethod
    def _generate_explanations(
        cls, signals: OpportunitySignals, score: int
    ) -> list[str]:
        explanations = []

        if signals.tvl_growth_rate > 0.5:
            explanations.append(
                f"Strong TVL growth detected (annualized: {signals.tvl_growth_rate * 100:.1f}%)"
            )
        elif signals.tvl_growth_rate > 0.2:
            explanations.append(
                f"Positive TVL momentum (growth rate: {signals.tvl_growth_rate * 100:.1f}%)"
            )

        if signals.developer_activity_score > 0.7:
            explanations.append(
                f"High developer activity with frequent updates and commits"
            )
        elif signals.developer_activity_score > 0.4:
            explanations.append(f"Moderate developer engagement detected")

        if signals.network_effect_score > 0.6:
            explanations.append(
                f"Strong network effects with {signals.network_effect_score * 100:.0f}% integration score"
            )

        if signals.innovation_score > 0.7:
            explanations.append(
                f"High innovation score - unique features or first-mover advantage"
            )
        elif signals.innovation_score > 0.4:
            explanations.append(
                f"Competitive feature set with moderate differentiation"
            )

        if signals.community_engagement > 0.6:
            explanations.append(f"Active community with strong engagement metrics")

        if signals.token_performance > 0.6:
            explanations.append(f"Positive token price momentum and trading volume")

        if not explanations:
            explanations.append("Limited opportunity indicators detected")

        return explanations


# -----------------------------------------------------------------------------
# Main Analysis Engine
# -----------------------------------------------------------------------------


class RiskOpportunityAnalyzer:
    """
    Main analysis engine combining risk and opportunity assessments.
    """

    def __init__(self):
        self.risk_scorer = RiskScorer()
        self.opportunity_detector = OpportunityDetector()

    def analyze(
        self,
        entity_id: str,
        entity_type: str,
        risk_signals: RiskSignals,
        opportunity_signals: OpportunitySignals,
    ) -> EntityAnalysis:
        """
        Perform complete risk and opportunity analysis for an entity.
        """
        risk_score, risk_level, risk_explanations = self.risk_scorer.score(risk_signals)
        opp_score, opp_level, opp_explanations = self.opportunity_detector.score(
            opportunity_signals
        )

        # Calculate confidence as average of signal completeness
        confidence = (
            self._calculate_risk_confidence(risk_signals)
            + self._calculate_opportunity_confidence(opportunity_signals)
        ) / 2

        risk_assessment = RiskAssessment(
            entity_id=entity_id,
            entity_type=entity_type,
            overall_risk_score=risk_score,
            risk_level=risk_level,
            key_risks=self._identify_key_risks(risk_signals),
            signals=risk_signals,
            confidence=confidence,
            explanations=risk_explanations,
        )

        opportunity_assessment = OpportunityAssessment(
            entity_id=entity_id,
            entity_type=entity_type,
            overall_opportunity_score=opp_score,
            opportunity_level=opp_level,
            key_opportunities=self._identify_key_opportunities(opportunity_signals),
            signals=opportunity_signals,
            confidence=confidence,
            explanations=opp_explanations,
        )

        return EntityAnalysis(
            entity_id=entity_id,
            entity_type=entity_type,
            risk_assessment=risk_assessment,
            opportunity_assessment=opportunity_assessment,
            confidence=round(confidence, 2),
        )

    def analyze_with_defaults(
        self,
        entity_id: str,
        entity_type: str,
        **kwargs,
    ) -> EntityAnalysis:
        """
        Analyze entity with optional signal overrides.
        All signals default to 0.5 (moderate) if not provided.
        """
        risk_signals = RiskSignals(
            audit_status=kwargs.get("audit_status", 0.5),
            wallet_activity_risk=kwargs.get("wallet_activity_risk", 0.5),
            funding_history_score=kwargs.get("funding_history_score", 0.5),
            contract_age_score=kwargs.get("contract_age_score", 0.5),
            interaction_diversity=kwargs.get("interaction_diversity", 0.5),
            holder_concentration=kwargs.get("holder_concentration", 0.5),
            smart_contract_complexity=kwargs.get("smart_contract_complexity", 0.5),
        )

        opportunity_signals = OpportunitySignals(
            tvl_growth_rate=kwargs.get("tvl_growth_rate", 0.5),
            volume_growth_rate=kwargs.get("volume_growth_rate", 0.5),
            developer_activity_score=kwargs.get("developer_activity_score", 0.5),
            network_effect_score=kwargs.get("network_effect_score", 0.5),
            innovation_score=kwargs.get("innovation_score", 0.5),
            community_engagement=kwargs.get("community_engagement", 0.5),
            token_performance=kwargs.get("token_performance", 0.5),
        )

        return self.analyze(entity_id, entity_type, risk_signals, opportunity_signals)

    def _calculate_risk_confidence(self, signals: RiskSignals) -> float:
        """Calculate confidence based on how many signals are available."""
        available = sum(
            1
            for v in [
                signals.audit_status,
                signals.wallet_activity_risk,
                signals.funding_history_score,
                signals.contract_age_score,
                signals.interaction_diversity,
                signals.holder_concentration,
                signals.smart_contract_complexity,
            ]
            if v > 0.0
        )
        return min(1.0, available / 7.0)

    def _calculate_opportunity_confidence(self, signals: OpportunitySignals) -> float:
        """Calculate confidence based on how many signals are available."""
        available = sum(
            1
            for v in [
                signals.tvl_growth_rate,
                signals.volume_growth_rate,
                signals.developer_activity_score,
                signals.network_effect_score,
                signals.innovation_score,
                signals.community_engagement,
                signals.token_performance,
            ]
            if v > 0.0
        )
        return min(1.0, available / 7.0)

    def _identify_key_risks(self, signals: RiskSignals) -> list[str]:
        """Identify the most significant risk factors."""
        risks = []

        if signals.audit_status < 0.3:
            risks.append("Unaudited or partially audited contract")
        if signals.wallet_activity_risk < 0.3:
            risks.append("Suspicious wallet activity patterns")
        if signals.funding_history_score < 0.3:
            risks.append("Lack of verifiable funding history")
        if signals.contract_age_score < 0.2:
            risks.append("Recently deployed contract (higher exploit risk)")
        if signals.holder_concentration < 0.3:
            risks.append("High token concentration among few holders")

        if not risks:
            risks.append("No critical risk factors identified")

        return risks

    def _identify_key_opportunities(self, signals: OpportunitySignals) -> list[str]:
        """Identify the most significant opportunity factors."""
        opportunities = []

        if signals.tvl_growth_rate > 0.4:
            opportunities.append("Strong TVL growth momentum")
        if signals.developer_activity_score > 0.6:
            opportunities.append("Active development with frequent updates")
        if signals.network_effect_score > 0.5:
            opportunities.append("Strong network effects and integrations")
        if signals.innovation_score > 0.5:
            opportunities.append("First-mover or unique features")
        if signals.community_engagement > 0.5:
            opportunities.append("Growing community engagement")

        if not opportunities:
            opportunities.append("Limited growth indicators")

        return opportunities


def create_analyzer() -> RiskOpportunityAnalyzer:
    """Factory function to create an analyzer instance."""
    return RiskOpportunityAnalyzer()
