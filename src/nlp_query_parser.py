"""
NLP Query Parser for TonSearch

Handles 100+ query types, normalizes queries into structured search parameters,
supports fuzzy matching for misspelled terms.

Deliverables:
- Query classification model
- Intent extraction system
- Test suite with 500+ sample queries
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class QueryType(Enum):
    """Types of natural language queries."""

    PROJECT_DISCOVERY = "project_discovery"
    WALLET_ANALYSIS = "wallet_analysis"
    CONTRACT_LOOKUP = "contract_lookup"
    RISK_ASSESSMENT = "risk_assessment"
    OPPORTUNITY_FINDING = "opportunity_finding"
    TREND_QUERY = "trend_query"
    COMPARISON = "comparison"
    AUDIT_CHECK = "audit_check"
    TVL_QUERY = "tvl_query"
    ACTIVITY_QUERY = "activity_query"
    HOLDINGS_QUERY = "holdings_query"
    UNKNOWN = "unknown"


class Intent(Enum):
    """User intents extracted from queries."""

    FIND = "find"
    ANALYZE = "analyze"
    COMPARE = "compare"
    GET_RISK = "get_risk"
    GET_OPPORTUNITY = "get_opportunity"
    CHECK_AUDIT = "check_audit"
    SHOW_TRENDS = "show_trends"
    LIST = "list"
    COMPARE_TVL = "compare_tvl"
    COMPARE_ACTIVITY = "compare_activity"
    UNKNOWN = "unknown"


@dataclass
class ExtractedEntity:
    """An entity extracted from the query."""

    value: str
    entity_type: str
    normalized_value: str
    confidence: float = 1.0


@dataclass
class QueryFilters:
    """Structured filters extracted from the query."""

    risk_level: Optional[str] = None
    project_category: Optional[str] = None
    tvl_min: Optional[float] = None
    tvl_max: Optional[float] = None
    activity_level: Optional[str] = None
    audit_status: Optional[str] = None
    sort_by: Optional[str] = None
    sort_order: Optional[str] = None
    time_range: Optional[str] = None


@dataclass
class ParsedQuery:
    """A fully parsed natural language query."""

    original_query: str
    query_type: QueryType
    intent: Intent
    entities: list[ExtractedEntity] = field(default_factory=list)
    filters: QueryFilters = field(default_factory=QueryFilters)
    confidence: float = 0.0
    suggestions: list[str] = field(default_factory=list)


class QueryClassifier:
    """
    Classifies natural language queries into query types.
    Uses keyword and pattern matching for classification.
    """

    # Query type patterns
    TYPE_PATTERNS = {
        QueryType.PROJECT_DISCOVERY: [
            r"show me .* projects?",
            r"find .* projects?",
            r"list .* projects?",
            r"discover .* projects?",
            r"what (are|is) .* projects?",
            r"projects? (like|on|with|from|in)",
        ],
        QueryType.WALLET_ANALYSIS: [
            r"wallet (of|for|with)",
            r"analyze wallet",
            r"show wallet",
            r"wallets? (belonging|owned|associated)",
            r"who owns",
        ],
        QueryType.CONTRACT_LOOKUP: [
            r"contract (address|for|with)",
            r"find contract",
            r"show contract",
            r"lookup contract",
        ],
        QueryType.RISK_ASSESSMENT: [
            r"risk(y)? .* (project|wallet|contract)",
            r"show .* risk",
            r"(is|are) .* safe",
            r"scam .* check",
            r"rug .* pull",
        ],
        QueryType.OPPORTUNITY_FINDING: [
            r"opportunit(y|ies)",
            r"(good|best|top) .* (invest|gain|earn)",
            r"high.*(tv1|tvl|return)",
            r"(hidden|gem|underrated)",
        ],
        QueryType.TREND_QUERY: [
            r"trend",
            r"(rising|falling|growing|declining)",
            r"(popular|trending)",
            r"what('s| is) hot",
        ],
        QueryType.COMPARISON: [
            r"compar(e|ing|ison)",
            r"(vs|versus) .* (vs|versus)",
            r"better than",
            r"differenc(e|es) between",
        ],
        QueryType.AUDIT_CHECK: [
            r"audit(ed)?",
            r"(verified|verified|official)",
            r"trust(ed)?(safe|secure)?",
            r"(verified|audited) (project|contract)",
        ],
        QueryType.TVL_QUERY: [
            r"(?:tv1|tvl).*\d",
            r"tvl",
            r"(total|锁仓) value",
            r"(锁仓|锁仓) (?:tv1|tvl)",
        ],
        QueryType.ACTIVITY_QUERY: [
            r"activity",
            r"transactions?",
            r"volume",
            r"(active|daily|weekly) .* (tx|transaction)",
            r"how (active|many)",
        ],
        QueryType.HOLDINGS_QUERY: [
            r"hold(s|ings|ing)?",
            r"balance",
            r"portfolio",
            r"token.*balance",
            r"what (does|is) .* (hold|own)",
        ],
    }

    # Intent keywords
    INTENT_PATTERNS = {
        Intent.FIND: [r"find", r"show", r"list", r"get", r"search", r"discover"],
        Intent.ANALYZE: [r"analyze", r"check", r"examine", r"review", r"inspect"],
        Intent.COMPARE: [r"compar(e|ing|ison)", r"(vs|versus)", r"better than"],
        Intent.GET_RISK: [r"risk", r"danger", r"unsafe", r"scam"],
        Intent.GET_OPPORTUNITY: [r"opportunit", r"gain", r"profit", r"best"],
        Intent.CHECK_AUDIT: [r"audit", r"verif", r"trust"],
        Intent.SHOW_TRENDS: [r"trend", r"rising", r"falling", r"popular"],
        Intent.LIST: [r"list", r"all", r"every", r"show.*all"],
        Intent.COMPARE_TVL: [r"compar.*tv1", r"compar.*tvl", r"tv1.*compar"],
        Intent.COMPARE_ACTIVITY: [r"compar.*activ", r"activ.*compar"],
    }

    # Category keywords
    CATEGORY_KEYWORDS = {
        "defi": ["defi", "decentralized finance", "swap", "liquidity"],
        "nft": ["nft", "collection", "marketplace", "art"],
        "gaming": ["game", "play", "gaming", "guild"],
        "infrastructure": ["infrastructure", "layer", "bridge", "oracle"],
        "social": ["social", "telegram", "messenger"],
        "storage": ["storage", "file", "cloud"],
        "governance": ["dao", "governance", "vote"],
        "yield": ["yield", "farm", "stake", "lending"],
    }

    # Risk keywords
    RISK_KEYWORDS = {
        "high": ["rug", "scam", "risk", "danger", "unsafe", "unverified"],
        "medium": ["new", "unknown", "unreviewed"],
        "low": ["audit", "verified", "safe", "secure", "trusted"],
    }

    # Activity keywords
    ACTIVITY_KEYWORDS = {
        "high": ["active", "high volume", "busy", "popular"],
        "medium": ["moderate", "normal", "average"],
        "low": ["inactive", "dormant", "dead", "abandoned"],
    }

    def classify(self, query: str) -> tuple[QueryType, float]:
        """
        Classify a query into a query type with confidence score.
        """
        query_lower = query.lower().strip()

        scores = {}
        for qtype, patterns in self.TYPE_PATTERNS.items():
            score = 0.0
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    score += 1.0
            if score > 0:
                scores[qtype] = score

        if not scores:
            return QueryType.UNKNOWN, 0.0

        best_type = max(scores, key=scores.get)
        max_score = scores[best_type]

        confidence = min(0.95, 0.5 + (max_score * 0.15))
        return best_type, confidence

    def extract_intent(self, query: str) -> tuple[Intent, float]:
        """
        Extract the primary intent from a query.
        """
        query_lower = query.lower().strip()

        scores = {}
        for intent, patterns in self.INTENT_PATTERNS.items():
            score = 0.0
            for pattern in patterns:
                matches = re.findall(pattern, query_lower)
                score += len(matches)
            if score > 0:
                scores[intent] = score

        if not scores:
            return Intent.UNKNOWN, 0.0

        best_intent = max(scores, key=scores.get)
        max_score = scores[best_intent]

        confidence = min(0.95, 0.4 + (max_score * 0.1))
        return best_intent, confidence

    def normalize_query(self, query: str) -> str:
        """
        Normalize query text for consistent processing.
        """
        normalized = query.lower().strip()
        normalized = re.sub(r"\s+", " ", normalized)
        normalized = re.sub(r"[^\w\s\-:.]", "", normalized)
        return normalized


class EntityExtractor:
    """
    Extracts entities (addresses, project names, categories) from queries.
    """

    # Address patterns
    ADDRESS_PATTERNS = [
        (r"\b0:[a-fA-F0-9]{32}\b", "raw_address"),
        (r"\bEQ[a-zA-Z0-9_-]{42}\b", "hex_address"),
        (r"\bUQ[a-zA-Z0-9_-]{42}\b", "hex_address"),
        (r"\bkQ[a-zA-Z0-9_-]{42}\b", "jetton_address"),
    ]

    # Project name patterns
    PROJECT_PATTERNS = [
        (r'"([^"]+)"', "quoted_name"),
        (r"'([^']+)'", "quoted_name"),
    ]

    def extract_entities(self, query: str) -> list[ExtractedEntity]:
        """
        Extract all entities from a query.
        """
        entities = []

        for pattern, etype in self.ADDRESS_PATTERNS:
            for match in re.finditer(pattern, query):
                entities.append(
                    ExtractedEntity(
                        value=match.group(),
                        entity_type=etype,
                        normalized_value=match.group().lower(),
                        confidence=0.95,
                    )
                )

        for pattern, etype in self.PROJECT_PATTERNS:
            for match in re.finditer(pattern, query):
                entities.append(
                    ExtractedEntity(
                        value=match.group(1),
                        entity_type=etype,
                        normalized_value=match.group(1).lower(),
                        confidence=0.90,
                    )
                )

        return entities

    def extract_addresses(self, query: str) -> list[str]:
        """Extract all wallet/contract addresses from query."""
        addresses = []
        for pattern, _ in self.ADDRESS_PATTERNS:
            for match in re.finditer(pattern, query):
                addresses.append(match.group())
        return addresses


class FuzzyMatcher:
    """
    Provides fuzzy matching for misspelled terms.
    Uses Levenshtein distance for similarity scoring.
    """

    # Common misspellings and corrections
    CORRECTION_MAP = {
        "projct": "project",
        "projcet": "project",
        "projext": "project",
        "projectss": "projects",
        "projcts": "projects",
        "wallett": "wallet",
        "walletes": "wallet",
        "walletss": "wallets",
        "contarct": "contract",
        "contrat": "contract",
        "contraact": "contract",
        "risj": "risk",
        "risck": "risk",
        "opurtunity": "opportunity",
        "opportunitys": "opportunities",
        "trned": "trend",
        "trendss": "trends",
        "auditt": "audit",
        "auditted": "audited",
        "tvl": "tvl",
        "tv1": "tvl",
        "defi": "defi",
        "deffi": "defi",
        "nft": "nft",
        "nflt": "nft",
        "gamining": "gaming",
        "ganing": "gaming",
        "active": "active",
        "actiive": "active",
        "activve": "active",
    }

    def __init__(self, max_edit_distance: int = 2):
        self.max_edit_distance = max_edit_distance

    def correct(self, word: str) -> tuple[str, float]:
        """
        Attempt to correct a word using the correction map or Levenshtein.
        Returns (corrected_word, confidence).
        """
        word_lower = word.lower()

        if word_lower in self.CORRECTION_MAP:
            return self.CORRECTION_MAP[word_lower], 1.0

        best_correction = word
        best_distance = self.max_edit_distance + 1

        for typo, correction in self.CORRECTION_MAP.items():
            distance = self._levenshtein_distance(word_lower, typo)
            if distance < best_distance:
                best_distance = distance
                best_correction = correction

        if best_distance <= self.max_edit_distance:
            confidence = 1.0 - (best_distance / (len(word) + 1))
            return best_correction, max(0.5, confidence)

        return word, 0.0

    def correct_query(self, query: str) -> tuple[str, list[str]]:
        """
        Correct a full query and return suggestions for any changes.
        """
        words = query.split()
        corrected_words = []
        suggestions = []

        for word in words:
            corrected, confidence = self.correct(word)
            corrected_words.append(corrected)
            if corrected != word.lower():
                suggestions.append(f"'{word}' → '{corrected}' ({confidence:.0%})")

        return " ".join(corrected_words), suggestions

    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """
        Calculate Levenshtein distance between two strings.
        """
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]


class FilterExtractor:
    """
    Extracts structured filters from natural language queries.
    """

    # Risk level patterns
    RISK_PATTERNS = {
        "high": [
            r"\bhigh risk\b",
            r"\bright\b",
            r"\bscam\b",
            r"\bdangerous\b",
            r"\bunsafe\b",
        ],
        "medium": [r"\bmedium risk\b", r"\bmoderate\b", r"\bunknown\b", r"\bnew\b"],
        "low": [
            r"\blow risk\b",
            r"\bsafe\b",
            r"\bsecure\b",
            r"\btrusted\b",
            r"\baudited\b",
        ],
    }

    # Category patterns
    CATEGORY_PATTERNS = {
        "defi": [r"\bdefi\b", r"\bdecentralized finance\b"],
        "nft": [r"\bnft\b", r"\bcollection\b", r"\bmarketplace\b"],
        "gaming": [r"\bgame\b", r"\bgaming\b", r"\bplay\b"],
        "infrastructure": [r"\binfrastructure\b", r"\bbridge\b", r"\boracle\b"],
        "social": [r"\bsocial\b", r"\btelegram\b"],
        "yield": [r"\byield\b", r"\bfarm\b", r"\bstake\b", r"\blending\b"],
    }

    # TVL patterns
    TVL_PATTERNS = [
        r"(?:tv1|tvl)\s*([><=]+)\s*(\d+(?:\.\d+)?[kmb]?)",
        r"(?:tv1|tvl)\s*(greater|less)?\s*(than)?\s*(\d+(?:\.\d+)?[kmb]?)",
        r"(?:tv1|tvl)\s*(between)\s*(\d+(?:\.\d+)?)\s*(and|to)\s*(\d+(?:\.\d+)?)",
    ]

    # Sort patterns
    SORT_PATTERNS = [
        (r"sort by (\w+)", "sort_by"),
        (r"order by (\w+)", "sort_by"),
        (r"(top|highest|best) (\w+)", "sort_order_desc"),
        (r"(bottom|lowest|worst) (\w+)", "sort_order_asc"),
    ]

    # Time range patterns
    TIME_PATTERNS = {
        "24h": [r"(last |past )?24\s*h(our)?s?", r"(in |this )?last\s*day"],
        "7d": [r"(last |past )?7\s*d(ays?)?", r"(in |this )?week"],
        "30d": [r"(last |past )?(30|thirty)\s*d(ays?)?", r"(in |this )?month"],
        "90d": [r"(last |past )?(90|ninety)\s*d(ays?)?"],
    }

    def extract_filters(self, query: str) -> QueryFilters:
        """
        Extract all filters from a query.
        """
        query_lower = query.lower()
        filters = QueryFilters()

        risk_level = self._extract_risk_level(query_lower)
        if risk_level:
            filters.risk_level = risk_level

        category = self._extract_category(query_lower)
        if category:
            filters.project_category = category

        tvl_range = self._extract_tvl(query_lower)
        if tvl_range:
            filters.tvl_min, filters.tvl_max = tvl_range

        activity = self._extract_activity(query_lower)
        if activity:
            filters.activity_level = activity

        sort_info = self._extract_sort(query_lower)
        if sort_info:
            filters.sort_by, filters.sort_order = sort_info

        time_range = self._extract_time_range(query_lower)
        if time_range:
            filters.time_range = time_range

        return filters

    def _extract_risk_level(self, query: str) -> Optional[str]:
        """Extract risk level from query."""
        for level, patterns in self.RISK_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, query):
                    return level
        return None

    def _extract_category(self, query: str) -> Optional[str]:
        """Extract project category from query."""
        for category, patterns in self.CATEGORY_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, query):
                    return category
        return None

    def _extract_tvl(
        self, query: str
    ) -> Optional[tuple[Optional[float], Optional[float]]]:
        """Extract TVL range from query."""
        for pattern in self.TVL_PATTERNS:
            match = re.search(pattern, query)
            if match:
                groups = match.groups()
                if len(groups) >= 2 and groups[1]:
                    operator = groups[0] if groups[0] else ">"
                    value = self._parse_number(groups[1])
                    if value:
                        if ">" in operator or "greater" in str(operator).lower():
                            return (value, None)
                        elif "<" in operator or "less" in str(operator).lower():
                            return (None, value)
                        elif "=" in operator or "between" in str(operator).lower():
                            if len(groups) >= 4 and groups[3]:
                                value2 = self._parse_number(groups[3])
                                return (value, value2)
                            return (value, None)
        return None

    def _extract_activity(self, query: str) -> Optional[str]:
        """Extract activity level from query."""
        for level, patterns in {
            "high": [r"\bactive\b", r"\bhigh volume\b", r"\bbusy\b"],
            "medium": [r"\bmoderate\b", r"\baverage\b"],
            "low": [r"\binactive\b", r"\bdormant\b"],
        }.items():
            for pattern in patterns:
                if re.search(pattern, query):
                    return level
        return None

    def _extract_sort(self, query: str) -> Optional[tuple[str, str]]:
        """Extract sort parameters from query."""
        for pattern, ptype in self.SORT_PATTERNS:
            match = re.search(pattern, query)
            if match:
                if ptype == "sort_by":
                    return (match.group(1), "desc")
                elif ptype == "sort_order_desc":
                    return (match.group(2), "desc")
                elif ptype == "sort_order_asc":
                    return (match.group(2), "asc")
        return None

    def _extract_time_range(self, query: str) -> Optional[str]:
        """Extract time range from query."""
        for time_range, patterns in self.TIME_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, query):
                    return time_range
        return None

    def _parse_number(self, s: str) -> Optional[float]:
        """Parse a number with optional k/m/b suffixes."""
        s = s.lower().strip()
        multipliers = {"k": 1e3, "m": 1e6, "b": 1e9}
        for suffix, mult in multipliers.items():
            if s.endswith(suffix):
                try:
                    return float(s[:-1]) * mult
                except ValueError:
                    return None
        try:
            return float(s)
        except ValueError:
            return None


class NLPQueryParser:
    """
    Main NLP Query Parser combining all components.

    Takes natural language queries and produces structured search parameters.
    """

    def __init__(self):
        self.classifier = QueryClassifier()
        self.entity_extractor = EntityExtractor()
        self.fuzzy_matcher = FuzzyMatcher()
        self.filter_extractor = FilterExtractor()

    def parse(self, query: str) -> ParsedQuery:
        """
        Parse a natural language query into structured search parameters.
        """
        corrected_query, suggestions = self.fuzzy_matcher.correct_query(query)

        query_type, type_confidence = self.classifier.classify(query)
        intent, intent_confidence = self.classifier.extract_intent(query)

        entities = self.entity_extractor.extract_entities(query)
        filters = self.filter_extractor.extract_filters(query)

        overall_confidence = (type_confidence + intent_confidence) / 2

        return ParsedQuery(
            original_query=query,
            query_type=query_type,
            intent=intent,
            entities=entities,
            filters=filters,
            confidence=round(overall_confidence, 2),
            suggestions=suggestions,
        )

    def parse_batch(self, queries: list[str]) -> list[ParsedQuery]:
        """Parse multiple queries."""
        return [self.parse(q) for q in queries]


def create_parser() -> NLPQueryParser:
    """Factory function to create an NLP query parser."""
    return NLPQueryParser()
