"""
Visualization Templates for Risk/Opportunity Analysis

Provides chart rendering helpers and template data structures
for displaying risk and opportunity scores visually.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ChartData:
    """Data structure for chart rendering."""

    label: str
    value: float
    color: Optional[str] = None


@dataclass
class RiskRadarData:
    """Data for radar/spider chart displaying multiple risk signals."""

    entity_id: str
    audit_status: float
    wallet_activity: float
    funding_history: float
    contract_age: float
    interaction_diversity: float
    holder_concentration: float
    smart_contract_complexity: float

    def to_chart_data(self) -> list[ChartData]:
        return [
            ChartData(label="Audit Status", value=self.audit_status),
            ChartData(label="Wallet Activity", value=self.wallet_activity),
            ChartData(label="Funding History", value=self.funding_history),
            ChartData(label="Contract Age", value=self.contract_age),
            ChartData(label="Interaction Diversity", value=self.interaction_diversity),
            ChartData(label="Holder Concentration", value=self.holder_concentration),
            ChartData(
                label="Contract Complexity", value=self.smart_contract_complexity
            ),
        ]


@dataclass
class OpportunityRadarData:
    """Data for radar/spider chart displaying multiple opportunity signals."""

    entity_id: str
    tvl_growth: float
    volume_growth: float
    developer_activity: float
    network_effect: float
    innovation: float
    community_engagement: float
    token_performance: float

    def to_chart_data(self) -> list[ChartData]:
        return [
            ChartData(label="TVL Growth", value=self.tvl_growth),
            ChartData(label="Volume Growth", value=self.volume_growth),
            ChartData(label="Developer Activity", value=self.developer_activity),
            ChartData(label="Network Effect", value=self.network_effect),
            ChartData(label="Innovation", value=self.innovation),
            ChartData(label="Community Engagement", value=self.community_engagement),
            ChartData(label="Token Performance", value=self.token_performance),
        ]


@dataclass
class ScoreGaugeData:
    """Data for gauge/meter display of overall scores."""

    entity_id: str
    score: int
    level: str
    label: str
    color: str

    @classmethod
    def from_risk(cls, entity_id: str, score: int, level: str) -> "ScoreGaugeData":
        color_map = {
            "very_low": "#22c55e",  # green
            "low": "#84cc16",  # lime
            "medium": "#eab308",  # yellow
            "high": "#f97316",  # orange
            "very_high": "#ef4444",  # red
        }
        return cls(
            entity_id=entity_id,
            score=score,
            level=level,
            label="Risk Score",
            color=color_map.get(level, "#6b7280"),
        )

    @classmethod
    def from_opportunity(
        cls, entity_id: str, score: int, level: str
    ) -> "ScoreGaugeData":
        color_map = {
            "very_low": "#ef4444",  # red
            "low": "#f97316",  # orange
            "medium": "#eab308",  # yellow
            "high": "#84cc16",  # lime
            "very_high": "#22c55e",  # green
        }
        return cls(
            entity_id=entity_id,
            score=score,
            level=level,
            label="Opportunity Score",
            color=color_map.get(level, "#6b7280"),
        )


@dataclass
class TrendBarData:
    """Data for bar chart showing trend comparisons."""

    entity_id: str
    metric_name: str
    current: float
    previous: float
    change_percent: float

    def to_chart_data(self) -> list[ChartData]:
        return [
            ChartData(label=f"{self.metric_name} (current)", value=self.current),
            ChartData(label=f"{self.metric_name} (previous)", value=self.previous),
        ]


def generate_risk_html(gauge_data: ScoreGaugeData, radar_data: RiskRadarData) -> str:
    """
    Generate HTML for risk score visualization.
    Includes a gauge meter and radar chart data for embedding.
    """
    return f"""
<div class="risk-visualization" data-entity="{gauge_data.entity_id}">
  <div class="gauge-container">
    <div class="gauge-label">{gauge_data.label}</div>
    <div class="gauge-score" style="color: {gauge_data.color}">{gauge_data.score}</div>
    <div class="gauge-level" style="background: {gauge_data.color}">{gauge_data.level.upper()}</div>
  </div>
  <div class="radar-container">
    <div class="radar-title">Risk Signal Breakdown</div>
    <div class="radar-chart">
      {"".join(f'<div class="radar-bar"><span class="bar-label">{d.label}</span><div class="bar-fill" style="width:{d.value * 100}%"></div><span class="bar-value">{d.value:.2f}</span></div>' for d in radar_data.to_chart_data())}
    </div>
  </div>
</div>
"""


def generate_opportunity_html(
    gauge_data: ScoreGaugeData, radar_data: OpportunityRadarData
) -> str:
    """
    Generate HTML for opportunity score visualization.
    Includes a gauge meter and radar chart data for embedding.
    """
    return f"""
<div class="opportunity-visualization" data-entity="{gauge_data.entity_id}">
  <div class="gauge-container">
    <div class="gauge-label">{gauge_data.label}</div>
    <div class="gauge-score" style="color: {gauge_data.color}">{gauge_data.score}</div>
    <div class="gauge-level" style="background: {gauge_data.color}">{gauge_data.level.upper()}</div>
  </div>
  <div class="radar-container">
    <div class="radar-title">Opportunity Signal Breakdown</div>
    <div class="radar-chart">
      {"".join(f'<div class="radar-bar"><span class="bar-label">{d.label}</span><div class="bar-fill" style="width:{d.value * 100}%"></div><span class="bar-value">{d.value:.2f}</span></div>' for d in radar_data.to_chart_data())}
    </div>
  </div>
</div>
"""


def generate_comparison_bars(
    entity_id: str, risk_score: int, opportunity_score: int
) -> str:
    """Generate side-by-side comparison bars for risk vs opportunity."""
    return f"""
<div class="score-comparison" data-entity="{entity_id}">
  <div class="comparison-item">
    <span class="comparison-label">Risk</span>
    <div class="comparison-bar">
      <div class="comparison-fill" style="width:{risk_score}%; background: {"#ef4444" if risk_score > 60 else "#eab308" if risk_score > 40 else "#22c55e"}"></div>
    </div>
    <span class="comparison-value">{risk_score}</span>
  </div>
  <div class="comparison-item">
    <span class="comparison-label">Opportunity</span>
    <div class="comparison-bar">
      <div class="comparison-fill" style="width:{opportunity_score}%; background: {"#22c55e" if opportunity_score > 60 else "#eab308" if opportunity_score > 40 else "#ef4444"}"></div>
    </div>
    <span class="comparison-value">{opportunity_score}</span>
  </div>
</div>
"""


# -----------------------------------------------------------------------------
# SVG Templates
# -----------------------------------------------------------------------------

RISK_GAUGE_SVG = """
<svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="gaugeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#22c55e"/>
      <stop offset="40%" stop-color="#eab308"/>
      <stop offset="70%" stop-color="#f97316"/>
      <stop offset="100%" stop-color="#ef4444"/>
    </linearGradient>
  </defs>
  <!-- Gauge background arc -->
  <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="#e5e7eb" stroke-width="12" stroke-linecap="round"/>
  <!-- Colored arc would go here - rendered dynamically -->
  <!-- Gauge needle -->
  <line x1="100" y1="100" x2="100" y2="30" stroke="#374151" stroke-width="3" stroke-linecap="round"/>
  <circle cx="100" cy="100" r="8" fill="#374151"/>
  <!-- Score text -->
  <text x="100" y="95" text-anchor="middle" font-family="sans-serif" font-size="24" font-weight="bold" fill="#1f2937">{score}</text>
</svg>
"""

OPPORTUNITY_GAUGE_SVG = """
<svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="oppGaugeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ef4444"/>
      <stop offset="40%" stop-color="#eab308"/>
      <stop offset="70%" stop-color="#84cc16"/>
      <stop offset="100%" stop-color="#22c55e"/>
    </linearGradient>
  </defs>
  <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="#e5e7eb" stroke-width="12" stroke-linecap="round"/>
  <line x1="100" y1="100" x2="100" y2="30" stroke="#374151" stroke-width="3" stroke-linecap="round"/>
  <circle cx="100" cy="100" r="8" fill="#374151"/>
  <text x="100" y="95" text-anchor="middle" font-family="sans-serif" font-size="24" font-weight="bold" fill="#1f2937">{score}</text>
</svg>
"""


def render_gauge_svg(score: int, is_risk: bool = True) -> str:
    """Render a gauge SVG with the given score."""
    template = RISK_GAUGE_SVG if is_risk else OPPORTUNITY_GAUGE_SVG
    return template.format(score=score)


# -----------------------------------------------------------------------------
# Visualization Renderer
# -----------------------------------------------------------------------------


class VisualizationRenderer:
    """
    Renders visualizations for entity analysis results.
    """

    @staticmethod
    def render_risk_dashboard(
        entity_id: str, score: int, level: str, radar: RiskRadarData
    ) -> str:
        """Render complete risk dashboard HTML."""
        gauge = ScoreGaugeData.from_risk(entity_id, score, level)
        return generate_risk_html(gauge, radar)

    @staticmethod
    def render_opportunity_dashboard(
        entity_id: str, score: int, level: str, radar: OpportunityRadarData
    ) -> str:
        """Render complete opportunity dashboard HTML."""
        gauge = ScoreGaugeData.from_opportunity(entity_id, score, level)
        return generate_opportunity_html(gauge, radar)

    @staticmethod
    def render_comparison(
        entity_id: str, risk_score: int, opportunity_score: int
    ) -> str:
        """Render risk vs opportunity comparison bars."""
        return generate_comparison_bars(entity_id, risk_score, opportunity_score)

    @staticmethod
    def render_gauge(score: int, is_risk: bool = True) -> str:
        """Render a standalone gauge SVG."""
        return render_gauge_svg(score, is_risk)


def create_renderer() -> VisualizationRenderer:
    """Factory function to create a renderer instance."""
    return VisualizationRenderer()
