"""
Test suite for NLP Query Parser with 500+ sample queries.
Covers all query types, intent extraction, entity extraction,
filter extraction, and fuzzy matching.
"""

import pytest

from .nlp_query_parser import (
    EntityExtractor,
    FilterExtractor,
    FuzzyMatcher,
    Intent,
    NLPQueryParser,
    QueryClassifier,
    QueryFilters,
    QueryType,
    create_parser,
)

# =============================================================================
# Sample Query Bank - 500+ queries covering various patterns
# =============================================================================

SAMPLE_QUERIES = {
    QueryType.PROJECT_DISCOVERY: [
        "show me DeFi projects",
        "find NFT projects on TON",
        "list all gaming projects",
        "discover infrastructure projects",
        "what are the best yield projects",
        "show me projects on TON",
        "find projects like Uniswap",
        "list projects with high TVL",
        "what projects are trending",
        "show me projects from last week",
        "find social projects",
        "list all verified projects",
        "show me projects with audits",
        "find new projects launched recently",
        "what are the top DeFi projects by TVL",
        "show me projects with low risk",
        "find projects in the gaming sector",
        "list projects that are audited",
        "show me all NFT marketplace projects",
        "find projects with good token performance",
        "what projects have the highest growth",
        "show me projects with high activity",
        "find projects similar to StonFi",
        "list projects by category",
        "show me projects with risk assessment",
        "find projects in the DeFi category",
        "list all projects sorted by TVL",
        "show me projects with opportunity signals",
        "find projects that are secure",
        "what are the most popular projects",
        # Additional queries to reach 500+
        "show me high TVL DeFi projects",
        "find low risk NFT projects",
        "list audited gaming projects",
        "show me trending infrastructure",
        "find rising yield projects",
        "show me social projects with high activity",
        "find new DeFi projects launched this month",
        "list projects by TVL descending",
        "show me verified NFT collections",
        "find governance projects with high TVL",
        "show me storage projects sorted by activity",
        "list all social projects on TON",
        "find high growth gaming projects",
        "show me audited DeFi protocols",
        "find projects with low risk score",
        "list trending NFT projects by volume",
        "show me infrastructure projects with good security",
        "find yield farms with high APY",
        "show me projects with certik audit",
        "find wallet analyzer tools",
        "show me cross-chain bridge projects",
        "list DeFi aggregators on TON",
        "find liquid staking projects",
        "show me royalty-free NFT marketplace",
        "find DAO governance tools",
        "show me decentralized exchange projects",
        "list prediction market platforms",
        "find oracle services on TON",
        "show me gambling DApps on TON",
        "find music NFT platforms",
        "show me art NFT marketplaces",
        "list play-to-earn gaming projects",
        "find metaverse projects on TON",
        "show me DeFi lending platforms",
        "find insurance protocols",
        "show me synthetic asset platforms",
        "list yield optimizers",
        "find vault strategies",
        "show me liquidity pool projects",
        "find token launchpad platforms",
        "show me airdrop farming projects",
        "list NFT staking protocols",
        "find governance token projects",
        "show me revenue sharing DApps",
        "find staking pool projects",
        "show me trading bot platforms",
        "list copy trading projects",
        "find portfolio management tools",
        "show me institutional grade projects",
        "find retail friendly platforms",
        "show me community driven projects",
        "list developer focused tools",
        "find user friendly interfaces",
        "show me privacy focused projects",
        "find transparent protocols",
        "show me audited smart contracts",
        "list bug bounty programs",
        "find security audit firms",
        "show me penetration testing results",
        "find code review reports",
        "show me open source projects",
        "list on-chain analytics tools",
        "find wallet tracking services",
        "show me whale alert systems",
        "find trend detection algorithms",
        "show me market sentiment tools",
        "list risk assessment frameworks",
        "find opportunity scoring models",
        "show me TVL analysis tools",
        "find trading volume analyzers",
        "show me user activity metrics",
    ],
    QueryType.WALLET_ANALYSIS: [
        "analyze wallet 0:6cf686df95e060375a92184754b364f16b5b3b175c331b339ba6a27bd639adf2",
        "show wallet activity for EQB9TriH0AKlUaUBtio0QbSnjM66nxKm0tCukadidwCVCYr-",
        "wallet of Vitalik",
        "show me wallets with high balance",
        "find wallets belonging to insiders",
        "analyze this wallet: 0:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        "what does this wallet hold",
        "show wallet portfolio",
        "find wallets with suspicious activity",
        "who owns this contract",
        "analyze wallet for risky behavior",
        "show me wallets with large transactions",
        "find wallets that interact with DeFi",
        "what is the activity of this wallet",
        "show me wallets with recent activity",
        "analyze wallet transaction history",
        "find wallets with high frequency trading",
        "show me wallets with governance participation",
        "what wallets are holding this token",
        "find wallets with yield positions",
        # Additional queries
        "check wallet balance for 0:abcdef1234567890abcdef1234567890abcdef1234567890abcdef12345678",
        "show all transactions for wallet EQB9TriH0AKlUaUBtio0QbSnjM66nxKm0tCukadidwCVCYr-",
        "find whale wallets on TON",
        "show me top 10 wallets by balance",
        "analyze smart money wallets",
        "track whale movements",
        "find institutional wallets",
        "show me team wallets",
        "find insider wallets",
        "track governance voter wallets",
        "show me staking reward recipients",
        "find airdrop claim wallets",
        "track NFT trader wallets",
        "show me DeFi depositor wallets",
        "find liquidity provider wallets",
        "show me yield farmer wallets",
        "find leverage trader wallets",
        "show me margin position wallets",
        "find oracle watcher wallets",
        "show me validator wallets",
        "find nominator wallets",
        "show me dApp developer wallets",
        "find contract deployer wallets",
        "show me multisig owner wallets",
        "find treasury wallets",
        "show me ecosystem fund wallets",
        "find marketing fund wallets",
        "show me community reward wallets",
        "find vesting schedule wallets",
        "show me token sale participant wallets",
        "find early adopter wallets",
        "show me beta tester wallets",
        "find testnet user wallets",
        "show me mainnet user wallets",
        "find new wallet addresses",
        "show me active trader wallets",
        "find dormant wallet detection",
        "show me reactivated wallets",
        "find wallet clustering analysis",
        "show me ownership graph for wallet",
        "find related contracts for wallet",
        "show me token flow from wallet",
        "find arbitrageur wallets",
        "show me MEV bot wallets",
        "find sandwich attack wallets",
        "show me liquidator wallets",
        "find treasury management wallets",
    ],
    QueryType.CONTRACT_LOOKUP: [
        "find contract address for StonFi",
        "show me the contract for USDT",
        "lookup contract 0:abcdef1234567890abcdef1234567890abcdef1234567890abcdef12345678",
        "what is the master contract address",
        "show contract for staking",
        "find the liquidity contract",
        "lookup this contract: EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        "show me the router contract",
        "find contract for token swaps",
        "what is the vault contract address",
        "show me the governance contract",
        "find the pool contract",
        "lookup masterchef contract",
        "show me the contract ABI",
        "find contract deployment date",
        "what contracts are related to this project",
        "show me the proxy contract",
        "find the implementation contract",
        "lookup multisig contract",
        "show me all contracts for this project",
        # Additional queries
        "find DEX router contract",
        "show me farming contract address",
        "lookup vault contract for yield",
        "find bridge contract address",
        "show me NFT marketplace contract",
        "lookup staking reward contract",
        "find governance vote contract",
        "show me token mint contract",
        "lookup burn contract address",
        "find fee collector contract",
        "show me treasury contract address",
        "lookup airdrop contract",
        "find Vesting contract address",
        "show me emission contract",
        "lookup gauge contract for farming",
        "find collector contract address",
        "show me strategist contract",
        "lookup risk manager contract",
        "find price oracle contract",
        "show me liquidity gauge contract",
        "lookupveToken contract address",
        "find reward distributor contract",
        "show me fee recipient contract",
        "lookup proxy admin contract",
        "find timelock contract address",
        "show me multisig wallet contract",
        "lookup canonical hub contract",
        "find spend limit contract",
        "show me transfer validator contract",
    ],
    QueryType.RISK_ASSESSMENT: [
        "show me risky DeFi projects",
        "is this project safe",
        "check if this contract is a scam",
        "show risk level for this project",
        "find risky wallets",
        "is this rug pull",
        "show me projects with low risk",
        "check audit status",
        "find unverified contracts",
        "what is the risk score",
        "show projects with high risk",
        "find projects that are safe",
        "is this project audited",
        "check if this is a scam",
        "show me risky investments",
        "find projects with danger signs",
        "what is the trust score",
        "show me secure projects",
        "find projects with audit reports",
        "is this wallet safe to interact with",
        "check risk of this investment",
        "show me low risk opportunities",
        "find projects without audits",
        "what is the danger level",
        "show me projects with audit warnings",
        # Additional queries
        "find high risk DeFi protocols",
        "show me rug pull detection results",
        "find suspicious contract behavior",
        "show me code exploit risk",
        "find reentrancy attack risk",
        "show me front running vulnerability",
        "find flash loan vulnerability",
        "show me impermanent loss risk",
        "find admin key risk",
        "show me upgrade key risk",
        "find pause function risk",
        "show me blacklist function risk",
        "find whitelist function risk",
        "show me transfer fee risk",
        "find mint function risk",
        "show me burn function risk",
        "find proxy implementation risk",
        "show me governance attack risk",
        "find economic exploit risk",
        "show me model risk in protocols",
    ],
    QueryType.OPPORTUNITY_FINDING: [
        "show me opportunities with high TVL growth",
        "find hidden gems",
        "what are the best opportunities",
        "show me projects with high returns",
        "find undervalued projects",
        "show me opportunities in DeFi",
        "what projects have high growth potential",
        "find trending projects",
        "show me opportunities with low risk",
        "find projects with good tokenomics",
        "what are the best investments",
        "show me projects with high APY",
        "find opportunities in gaming",
        "show me projects with momentum",
        "find the next big thing",
        "show me opportunities with high activity",
        "find projects with good fundamentals",
        "what are the best opportunities right now",
        "show me projects with increasing TVL",
        "find opportunities in NFT",
        "show me projects with high trading volume",
        "find undervalued tokens",
        "show me opportunities in infrastructure",
        "what projects are about to pump",
        # Additional queries
        "find undervalued DeFi tokens",
        "show me early stage gaming projects",
        "find emerging NFT collections",
        "show me undercapitalized protocols",
        "find low market cap gems",
        "show me protocols with high revenue",
        "find tokens with low FDV",
        "show me projects with strong tokenomics",
        "find protocols with token buybacks",
        "show me yield farming opportunities",
        "find staking as a service projects",
        "show me liquid staking derivatives",
        "find protocols with good incentives",
        "show me governance token value plays",
        "find ecosystems with growth potential",
        "show me cross-chain opportunity",
        "find multi-chain DeFi projects",
        "show me layer 2 opportunities",
        "find optimistic rollup projects",
        "show me zk rollup ecosystems",
        "find modular blockchain projects",
        "show me data availability projects",
        "find shared sequencing projects",
        "show me intent centric protocols",
        "find intent-based流动性 solutions",
        "show me专业化 Rollup projects",
        "find gamefi projects with token",
        "show me socialfi token opportunities",
        "find memecoin ecosystems",
        "show me NFT-Fi projects",
        "find real world asset protocols",
        "show me RWAs tokenization",
    ],
    QueryType.TREND_QUERY: [
        "what trends are hot",
        "show me trending projects",
        "find rising DeFi projects",
        "what is popular in TON",
        "show me trending NFTs",
        "find growing sectors",
        "what is trending right now",
        "show me projects on the rise",
        "find emerging trends",
        "what is hot in gaming",
        "show me popular projects",
        "find trending wallets",
        "what sectors are growing",
        "show me rising stars",
        "find emerging projects",
        "what is trending in DeFi",
        "show me projects gaining momentum",
        "find the latest trends",
        "what is popular in TON ecosystem",
        "show me trending tokens",
        "find growing categories",
        "what is hot right now",
        "show me rising projects in yield",
        "find trending categories",
        "what projects are getting attention",
        # Additional queries
        "show me trending DeFi protocols",
        "find trending NFT collections",
        "show me rising gaming projects",
        "find trending infrastructure projects",
        "show me popular social DApps",
        "find hot yield strategies",
        "show me trending mining projects",
        "find trending oracle services",
        "show me popular DAO tools",
        "find trending analytics platforms",
        "show me rising DEX protocols",
        "find trending lending platforms",
        "show me hot NFT marketplaces",
        "find trending gaming guilds",
        "show me rising DeFi aggregators",
        "find trending cross-chain bridges",
        "show me hot liquid staking",
        "find trending vault strategies",
        "show me popular prediction markets",
        "find trending governance tools",
        "show me emerging Layer2 projects",
        "find trending zk rollup ecosystems",
        "show me hot modular chains",
        "find trending data availability projects",
        "show me popular intent markets",
        "find trending restaking protocols",
        "show me hot eigenlayer ecosystem",
        "find trending liquid restaking",
        "show me popular restaking operators",
        "find trending AVS projects",
        "show me hot crypto twitter trends",
        "find trending on-chain metrics",
        "show me rising TVL chains",
        "find trending developer activity",
        "show me hot ecosystem funds",
        "find trending community growth",
    ],
    QueryType.COMPARISON: [
        "compare StonFi vs Dedprotocol",
        "which is better: Ethereum vs TON",
        "compare these two projects",
        "what is the difference between these wallets",
        "compare TVL of projects",
        "which project has better security",
        "compare audit status",
        "what is better: staking vs lending",
        "compare the risk of these projects",
        "which has higher TVL",
        "compare project performance",
        "what differs between these contracts",
        "compare activity levels",
        "which project is safer",
        "compare token prices",
        "what is the difference in fees",
        "compare liquidity",
        "which has better returns",
        "compare the teams behind projects",
        "what is better: CEX vs DEX",
        # Additional queries
        "compare Ethereum vs Solana vs TON",
        "which blockchain has better TVL",
        "compare DeFi vs CeFi yields",
        "show me Bitcoin vs Ethereum returns",
        "compare staking vs farming returns",
        "which is safer: staking or lending",
        "compare liquidity pools vs bond markets",
        "show me CEX vs DEX trading fees",
        "compare layer 1 vs layer 2 costs",
        "which has better privacy: Monero vs Zcash",
        "compare optimistic vs zk rollups",
        "show me EVM vs non-EVM chains",
        "compare wallet vs exchange security",
        "which is faster: Solana vs TON",
        "compare NFT marketplaces by volume",
        "show me centralized vs decentralized exchanges",
        "compare governance models: token vs NFT",
        "which yield strategy is safer",
        "compare audit firms by reputation",
        "show me TVL vs market cap rankings",
    ],
    QueryType.AUDIT_CHECK: [
        "is this project audited",
        "show me audited projects",
        "check audit status of this contract",
        "find verified contracts",
        "what audits does this project have",
        "is the contract verified",
        "show me projects with audit reports",
        "find audited DeFi projects",
        "check if this is a trusted project",
        "is this contract safe",
        "show me verified projects only",
        "find projects with certik audit",
        "what is the audit result",
        "is this project verified by trail of bits",
        "show me audit certificates",
        "find projects with multiple audits",
        "is this wallet trusted",
        "show me audited contracts",
        "find projects with good audit scores",
        "what audit firms reviewed this",
        # Additional queries
        "find projects audited by trail of bits",
        "show me certik audited projects",
        "find hacken audited protocols",
        "show me openzeppelin audited contracts",
        "find quantstamp audited projects",
        "show me sigma prime audited protocols",
        "find least authority audited projects",
        "show me consensus audited contracts",
        "find security audit by sherlock",
        "show me audits by saltermeta",
        "find decompyler audited projects",
        "show me statemind audited protocols",
        "find audit by zellic",
        "show me hexens audited projects",
        "find on finding audited protocols",
        "show me trust audits by triad",
        "find validify audited projects",
        "show me obelisk audited contracts",
        "find audit by tokenshield",
        "show me quillhash audited projects",
    ],
    QueryType.TVL_QUERY: [
        "show projects with TVL greater than 1M",
        "what is the TVL of StonFi",
        "find projects with tvl > 100k",
        "show me TVL over 10 million",
        "what projects have high TVL",
        "show TVL for this project",
        "find projects with tvl less than 100k",
        "what is the total value locked",
        "show me TVL rankings",
        "find projects with TVL between 1M and 10M",
        "what projects have low TVL",
        "show me TVL trends",
        "find projects with increasing TVL",
        "what is the TVL ranking",
        "show projects with TVL above 1B",
        "find DeFi projects by TVL",
        "what is the TVL of this protocol",
        "show me top TVL projects",
        "find projects with highest TVL",
        "what is the TVL of the ecosystem",
        # Additional queries
        "find projects with tvl over 10M",
        "show me projects with tvl between 1M and 100M",
        "find low tvl gems",
        "show me tvl rankings for defi",
        "find nft projects by tvl",
        "show me gaming projects tvl",
        "find infrastructure tvl leaders",
        "show me tvl for each chain",
        "find tvl concentration by category",
        "show me tvl trend over 30 days",
        "find projects with growing tvl",
        "show me tvl decline in bear market",
        "find tvl stablecoins",
        "show me tvl for bridges",
        "find tvl for oracles",
        "show me tvl for lending",
        "find tvl for dexes",
        "show me tvl for derivatives",
        "find tvl for options",
        "show me tvl for perpetuals",
        "find tvl for liquid staking",
        "show me tvl for restaking",
        "find tvl for yieldfarms",
        "show me tvl for vaults",
    ],
    QueryType.ACTIVITY_QUERY: [
        "show projects with high activity",
        "what is the transaction volume",
        "find active wallets",
        "show me daily transactions",
        "what projects have high volume",
        "show activity for this wallet",
        "find projects by trading volume",
        "what is the activity level",
        "show me most active projects",
        "find wallets with many transactions",
        "what is the daily tx count",
        "show projects with low activity",
        "find dormant wallets",
        "what is the transaction frequency",
        "show me activity trends",
        "find projects by daily volume",
        "what is the trading activity",
        "show me active contracts",
        "find wallets with high frequency",
        "what is the activity score",
        # Additional queries
        "find projects with daily tx > 10000",
        "show me active defi protocols",
        "find nft projects by trading volume",
        "show me gaming projects activity",
        "find social dapps user activity",
        "show me wallets with high tx count",
        "find contracts by call frequency",
        "show me dapps by unique users",
        "find protocols by gas consumption",
        "show me chains by daily txs",
        "find l2s by activity",
        "show me defi by trading volume",
        "find nft by sales volume",
        "show me gaming by active players",
        "find social by message count",
        "show me dao by vote participation",
        "find protocols by contract calls",
        "show me projects by interaction count",
        "find wallets by tx frequency",
        "show me contracts by invocation count",
    ],
    QueryType.HOLDINGS_QUERY: [
        "what does this wallet hold",
        "show me token balances",
        "find what this address holds",
        "what is the portfolio of this wallet",
        "show me holdings of this project",
        "what tokens are held here",
        "find the token balance",
        "what is the wallet balance",
        "show me all holdings",
        "find what tokens are in this wallet",
        "what is the portfolio value",
        "show me the token distribution",
        "find large holders",
        "what percentage does this wallet hold",
        "show me the top holders",
        "find whale wallets",
        "what is the total holdings",
        "show me wallet composition",
        "find governance token holders",
        "what tokens are accumulated here",
        # Additional queries
        "find large ton holders",
        "show me top eth holders",
        "find whale btc wallets",
        "show me wallets holding稳定币",
        "find wallets with defi tokens",
        "show me nft collector wallets",
        "find wallets with gaming tokens",
        "show me governance token holders",
        "find wallets with yield tokens",
        "show me wallets with lp tokens",
        "find rebalancing wallets",
        "show me multi-chain holders",
        "find cross-chain portfolios",
        "show me wallets by asset diversity",
        "find single asset holders",
        "show me diversified portfolios",
        "find concentrated positions",
        "show me whale concentration metrics",
        "find retail vs institutional holders",
        "show me holder distribution",
        "find tokens by holder count",
        "show me projects by investor holdings",
        "find team token allocations",
        "show me advisor token shares",
        "find vesting schedule analysis",
        "show me unlock schedule",
        "find token distribution by category",
        "show me supply concentration",
        "find wallets with unlocked tokens",
    ],
}

# Additional edge case queries
EDGE_CASE_QUERIES = [
    "show",  # Minimal
    "find",  # Minimal
    "12345",  # Numbers
    "!!!",  # Punctuation
    "show me projects with very long text that goes on and on and on and should still be handled properly",
    "0:0000000000000000000000000000000000000000000000000000000000000000",  # Valid address
    "EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",  # Valid address
    "",  # Empty
    "   ",  # Whitespace
    "show me 👀 projects",  # Emoji
    "what is the best???",  # Trailing punctuation
    "compare A vs B vs C",  # Multiple comparisons
    "show me projects / with / slashes",  # Special characters
    "TVL > $1,000,000",  # Currency format
    "1000000000000",  # Large number
]


class TestQueryClassification:
    """Test query classification into query types."""

    @pytest.mark.parametrize("query_type,queries", SAMPLE_QUERIES.items())
    def test_classify_query_types(self, query_type, queries):
        classifier = QueryClassifier()
        for query in queries[:10]:  # Test subset for speed
            qtype, confidence = classifier.classify(query)
            assert qtype == query_type, (
                f"Expected {query_type}, got {qtype} for query: {query}"
            )
            assert 0.0 <= confidence <= 1.0

    def test_classify_all_queries_coverage(self):
        """Test that all sample queries are classified."""
        classifier = QueryClassifier()
        total_queries = sum(len(queries) for queries in SAMPLE_QUERIES.values())
        classified_count = 0

        for query_type, queries in SAMPLE_QUERIES.items():
            for query in queries:
                qtype, _ = classifier.classify(query)
                if qtype != QueryType.UNKNOWN:
                    classified_count += 1

        coverage = classified_count / total_queries if total_queries > 0 else 0
        assert coverage >= 0.7, (
            f"Only {coverage:.0%} of queries classified, expected >= 70%"
        )

    def test_classify_edge_cases(self):
        classifier = QueryClassifier()
        for query in EDGE_CASE_QUERIES:
            qtype, confidence = classifier.classify(query)
            assert isinstance(qtype, QueryType)
            assert 0.0 <= confidence <= 1.0


class TestIntentExtraction:
    """Test intent extraction from queries."""

    @pytest.mark.parametrize(
        "query",
        [
            "find DeFi projects",
            "analyze this wallet",
            "compare these two",
            "show me the risk",
            "find opportunities",
            "check the audit",
            "show trends",
            "list all projects",
            "compare TVL",
            "compare activity",
        ],
    )
    def test_extract_intent(self, query):
        classifier = QueryClassifier()
        intent, confidence = classifier.extract_intent(query)
        assert isinstance(intent, Intent)
        assert 0.0 <= confidence <= 1.0

    def test_intent_confidence_scores(self):
        classifier = QueryClassifier()
        queries = [
            ("find DeFi projects", Intent.FIND),
            ("analyze wallet activity", Intent.ANALYZE),
            ("compare TVL of projects", Intent.COMPARE_TVL),
        ]
        for query, expected_intent in queries:
            intent, confidence = classifier.extract_intent(query)
            assert intent == expected_intent


class TestEntityExtraction:
    """Test entity extraction from queries."""

    def test_extract_raw_addresses(self):
        extractor = EntityExtractor()
        query = "show wallet 0:6cf686df95e060375a92184754b364f16b5b3b175c331b339ba6a27bd639adf2"
        entities = extractor.extract_entities(query)

        raw_addrs = [e for e in entities if e.entity_type == "raw_address"]
        assert len(raw_addrs) == 1
        assert (
            raw_addrs[0].value
            == "0:6cf686df95e060375a92184754b364f16b5b3b175c331b339ba6a27bd639adf2"
        )

    def test_extract_hex_addresses(self):
        extractor = EntityExtractor()
        query = "check contract EQB9TriH0AKlUaUBtio0QbSnjM66nxKm0tCukadidwCVCYr-"
        entities = extractor.extract_entities(query)

        hex_addrs = [e for e in entities if e.entity_type == "hex_address"]
        assert len(hex_addrs) == 1

    def test_extract_multiple_addresses(self):
        extractor = EntityExtractor()
        query = "compare wallets 0:aaaa000000000000000000000000000000000000000000000000000000000000 and 0:bbbb111111111111111111111111111111111111111111111111111111111111"
        entities = extractor.extract_entities(query)

        raw_addrs = [e for e in entities if e.entity_type == "raw_address"]
        assert len(raw_addrs) == 2

    def test_extract_quoted_names(self):
        extractor = EntityExtractor()
        query = 'find project "StonFi"'
        entities = extractor.extract_entities(query)

        quoted = [e for e in entities if e.entity_type == "quoted_name"]
        assert len(quoted) == 1
        assert quoted[0].value == "StonFi"

    def test_extract_no_addresses(self):
        extractor = EntityExtractor()
        query = "show me DeFi projects"
        entities = extractor.extract_entities(query)
        assert len(entities) == 0


class TestFuzzyMatching:
    """Test fuzzy matching for misspelled terms."""

    def test_correct_common_typos(self):
        matcher = FuzzyMatcher()
        test_cases = [
            ("projct", "project", 1.0),
            ("wallett", "wallet", 1.0),
            ("contarct", "contract", 1.0),
            ("opurtunity", "opportunity", 1.0),
        ]
        for misspelled, expected, conf in test_cases:
            corrected, confidence = matcher.correct(misspelled)
            assert corrected == expected
            assert confidence == conf

    def test_correct_tvl_variant(self):
        matcher = FuzzyMatcher()
        corrected, confidence = matcher.correct("tv1")
        assert corrected == "tvl"
        assert confidence == 1.0

    def test_no_change_for_correct_words(self):
        matcher = FuzzyMatcher()
        corrected, confidence = matcher.correct("project")
        assert corrected == "project"
        assert confidence == 0.0

    def test_correct_query_with_suggestions(self):
        matcher = FuzzyMatcher()
        query = "show me projcts with high tv1"
        corrected, suggestions = matcher.correct_query(query)

        assert "projcts" not in corrected
        assert "tv1" not in corrected
        assert len(suggestions) > 0

    def test_levenshtein_distance(self):
        matcher = FuzzyMatcher()
        dist = matcher._levenshtein_distance("kitten", "sitting")
        assert dist == 3

    def test_max_edit_distance_threshold(self):
        matcher = FuzzyMatcher(max_edit_distance=1)
        corrected, confidence = matcher.correct("xyz")
        assert confidence <= 0.5


class TestFilterExtraction:
    """Test filter extraction from queries."""

    def test_extract_risk_high(self):
        extractor = FilterExtractor()
        filters = extractor.extract_filters("show me high risk projects")
        assert filters.risk_level == "high"

    def test_extract_risk_low(self):
        extractor = FilterExtractor()
        filters = extractor.extract_filters("show me audited safe projects")
        assert filters.risk_level == "low"

    def test_extract_category_defi(self):
        extractor = FilterExtractor()
        filters = extractor.extract_filters("show DeFi projects")
        assert filters.project_category == "defi"

    def test_extract_category_nft(self):
        extractor = FilterExtractor()
        filters = extractor.extract_filters("find NFT collection projects")
        assert filters.project_category == "nft"

    def test_extract_tvl_greater(self):
        extractor = FilterExtractor()
        filters = extractor.extract_filters("show projects with tvl > 100k")
        assert filters.tvl_min is not None
        assert filters.tvl_min == 100000

    def test_extract_tvl_range(self):
        extractor = FilterExtractor()
        filters = extractor.extract_filters("show projects with tvl between 1M and 10M")
        assert filters.tvl_min is not None
        assert filters.tvl_max is not None

    def test_extract_activity(self):
        extractor = FilterExtractor()
        filters = extractor.extract_filters("show me active projects")
        assert filters.activity_level == "high"

    def test_extract_sort(self):
        extractor = FilterExtractor()
        filters = extractor.extract_filters("show me projects sorted by TVL")
        assert filters.sort_by == "tvl"
        assert filters.sort_order == "desc"

    def test_extract_time_range(self):
        extractor = FilterExtractor()
        filters = extractor.extract_filters("show me projects from last 7 days")
        assert filters.time_range == "7d"

    def test_extract_no_filters(self):
        extractor = FilterExtractor()
        filters = extractor.extract_filters("show me projects")
        assert filters.risk_level is None
        assert filters.project_category is None
        assert filters.tvl_min is None


class TestQueryNormalization:
    """Test query normalization."""

    def test_normalize_whitespace(self):
        classifier = QueryClassifier()
        normalized = classifier.normalize_query("  show   me   projects  ")
        assert normalized == "show me projects"

    def test_normalize_punctuation(self):
        classifier = QueryClassifier()
        normalized = classifier.normalize_query("show me projects!!!")
        assert "!" not in normalized


class TestParsedQueryStructure:
    """Test parsed query structure."""

    def test_parse_basic_query(self):
        parser = create_parser()
        result = parser.parse("show me DeFi projects with high TVL")

        assert result.original_query == "show me DeFi projects with high TVL"
        assert result.query_type == QueryType.PROJECT_DISCOVERY
        assert result.intent == Intent.FIND
        assert result.filters.project_category == "defi"
        assert result.filters.tvl_min is not None
        assert 0.0 <= result.confidence <= 1.0

    def test_parse_with_address(self):
        parser = create_parser()
        query = "analyze wallet 0:6cf686df95e060375a92184754b364f16b5b3b175c331b339ba6a27bd639adf2"
        result = parser.parse(query)

        assert result.query_type == QueryType.WALLET_ANALYSIS
        assert len(result.entities) == 1

    def test_parse_batch(self):
        parser = create_parser()
        queries = [
            "show me DeFi projects",
            "find NFT projects",
            "analyze wallet",
        ]
        results = parser.parse_batch(queries)

        assert len(results) == 3
        assert all(hasattr(r, "query_type") for r in results)

    def test_parse_empty_query(self):
        parser = create_parser()
        result = parser.parse("")
        assert result.query_type == QueryType.UNKNOWN


class TestNLPQueryParserIntegration:
    """Integration tests for the full NLP parser."""

    def test_full_pipeline_project_discovery(self):
        parser = create_parser()
        query = "show me DeFi projects with TVL > 1M and high activity"
        result = parser.parse(query)

        assert result.query_type == QueryType.PROJECT_DISCOVERY
        assert result.filters.project_category == "defi"
        assert result.filters.tvl_min >= 1000000
        assert result.filters.activity_level == "high"

    def test_full_pipeline_wallet_analysis(self):
        parser = create_parser()
        query = "analyze wallet 0:6cf686df95e060375a92184754b364f16b5b3b175c331b339ba6a27bd639adf2"
        result = parser.parse(query)

        assert result.query_type == QueryType.WALLET_ANALYSIS
        assert len(result.entities) == 1

    def test_full_pipeline_risk_assessment(self):
        parser = create_parser()
        query = "is this project safe and audited"
        result = parser.parse(query)

        assert result.filters.risk_level == "low"
        assert result.intent in [Intent.GET_RISK, Intent.CHECK_AUDIT]

    def test_full_pipeline_with_fuzzy_correction(self):
        parser = create_parser()
        query = "show me defi projcts with high tv1"
        result = parser.parse(query)

        assert result.filters.project_category == "defi"
        assert len(result.suggestions) > 0


# =============================================================================
# Large Scale Tests - 500+ queries
# =============================================================================


class TestLargeScaleClassification:
    """Test classification with 500+ queries."""

    def test_classify_500_queries(self):
        """Test that we can classify 500+ queries."""
        classifier = QueryClassifier()
        all_queries = []

        for queries in SAMPLE_QUERIES.values():
            all_queries.extend(queries)

        results = []
        for query in all_queries:
            qtype, confidence = classifier.classify(query)
            results.append((query, qtype, confidence))

        assert len(results) >= 500, f"Expected at least 500 queries, got {len(results)}"
        classified = sum(1 for _, qtype, _ in results if qtype != QueryType.UNKNOWN)
        assert classified >= 400, f"Only {classified} queries classified"

    def test_classify_500_unique_queries(self):
        """Test classification of 500 unique queries with various patterns."""
        classifier = QueryClassifier()

        queries = []
        for qtype, qlist in SAMPLE_QUERIES.items():
            queries.extend([(q, qtype) for q in qlist])

        queries.extend([(q, QueryType.UNKNOWN) for q in EDGE_CASE_QUERIES])

        unique_queries = []
        seen = set()
        for query, expected in queries:
            if query not in seen:
                unique_queries.append((query, expected))
                seen.add(query)

        assert len(unique_queries) >= 500

        correct = 0
        for query, expected in unique_queries:
            qtype, _ = classifier.classify(query)
            if qtype == expected:
                correct += 1

        accuracy = correct / len(unique_queries) if unique_queries else 0
        assert accuracy >= 0.6


class TestLargeScaleParsing:
    """Test parsing with 500+ queries."""

    def test_parse_500_queries(self):
        """Test that we can parse 500+ queries."""
        parser = create_parser()
        all_queries = []

        for queries in SAMPLE_QUERIES.values():
            all_queries.extend(queries)

        all_queries.extend(EDGE_CASE_QUERIES)

        results = []
        for query in all_queries:
            result = parser.parse(query)
            results.append(result)

        assert len(results) >= 500

        valid_results = sum(1 for r in results if r.query_type != QueryType.UNKNOWN)
        assert valid_results >= 450

    def test_parse_batch_500(self):
        """Test batch parsing of 500 queries."""
        parser = create_parser()
        all_queries = []

        for queries in SAMPLE_QUERIES.values():
            all_queries.extend(queries)

        all_queries.extend(EDGE_CASE_QUERIES)

        results = parser.parse_batch(all_queries[:500])

        assert len(results) == 500
        assert all(isinstance(r.confidence, float) for r in results)


class TestQueryTypeCoverage:
    """Test coverage of all query types."""

    def test_all_query_types_represented(self):
        """Verify all query types have sample queries."""
        for qtype in QueryType:
            if qtype != QueryType.UNKNOWN:
                assert qtype in SAMPLE_QUERIES, f"Missing samples for {qtype}"
                assert len(SAMPLE_QUERIES[qtype]) >= 10, f"Too few samples for {qtype}"

    def test_intent_coverage(self):
        """Verify all intents can be extracted."""
        classifier = QueryClassifier()
        test_intents = {
            Intent.FIND: "find DeFi projects",
            Intent.ANALYZE: "analyze wallet",
            Intent.COMPARE: "compare these projects",
            Intent.GET_RISK: "show risk",
            Intent.GET_OPPORTUNITY: "find opportunities",
            Intent.CHECK_AUDIT: "check audit",
            Intent.SHOW_TRENDS: "show trends",
            Intent.LIST: "list all",
            Intent.COMPARE_TVL: "compare TVL",
            Intent.COMPARE_ACTIVITY: "compare activity",
        }

        for intent, query in test_intents.items():
            extracted, _ = classifier.extract_intent(query)
            assert extracted != Intent.UNKNOWN or intent == Intent.UNKNOWN


class TestPerformance:
    """Test performance characteristics."""

    def test_parse_performance(self):
        """Test that parsing is reasonably fast."""
        import time

        parser = create_parser()
        all_queries = []
        for queries in SAMPLE_QUERIES.values():
            all_queries.extend(queries)

        start = time.time()
        for _ in range(100):
            for query in all_queries[:50]:
                parser.parse(query)
        elapsed = time.time() - start

        assert elapsed < 5.0, f"Parsing took too long: {elapsed:.2f}s"

    def test_batch_parse_performance(self):
        """Test that batch parsing is fast."""
        import time

        parser = create_parser()
        all_queries = []
        for queries in SAMPLE_QUERIES.values():
            all_queries.extend(queries)

        start = time.time()
        for _ in range(10):
            parser.parse_batch(all_queries[:100])
        elapsed = time.time() - start

        assert elapsed < 2.0, f"Batch parsing took too long: {elapsed:.2f}s"


class TestFuzzyMatcherLargeScale:
    """Large scale fuzzy matching tests."""

    def test_correct_many_typos(self):
        """Test correction of many typo variations."""
        matcher = FuzzyMatcher()
        typos = [
            "projct",
            "projcts",
            "projctss",
            "wallett",
            "walletss",
            "contarct",
            "contrat",
            "auditt",
            "auditted",
            "trned",
            "trendss",
            "risj",
            "risck",
            "defi",
            "deffi",
        ]

        corrections = [matcher.correct(t)[0] for t in typos]
        assert all(c != t for t, c in zip(typos, corrections) if t not in ["defi"])

    def test_levenshtein_performance(self):
        """Test Levenshtein distance performance."""
        import time

        matcher = FuzzyMatcher()

        words1 = ["project", "wallet", "contract", "audit", "risk"]
        words2 = ["projct", "wallett", "contarct", "auditt", "risj"]

        start = time.time()
        for w1, w2 in zip(words1, words2):
            matcher._levenshtein_distance(w1, w2)
        elapsed = time.time() - start

        assert elapsed < 0.1


class TestFilterExtractionEdgeCases:
    """Test filter extraction edge cases."""

    def test_multiple_filters(self):
        extractor = FilterExtractor()
        filters = extractor.extract_filters(
            "show me DeFi projects with TVL > 1M and high activity, sorted by TVL"
        )

        assert filters.project_category == "defi"
        assert filters.tvl_min is not None
        assert filters.activity_level == "high"
        assert filters.sort_by == "tvl"

    def test_tvl_with_suffix(self):
        extractor = FilterExtractor()
        filters = extractor.extract_filters("show projects with tvl > 100k")
        assert filters.tvl_min == 100000

        filters = extractor.extract_filters("show projects with tvl > 10m")
        assert filters.tvl_min == 10000000

        filters = extractor.extract_filters("show projects with tvl > 1b")
        assert filters.tvl_min == 1000000000

    def test_risk_medium(self):
        extractor = FilterExtractor()
        filters = extractor.extract_filters("show me new projects")
        assert filters.risk_level == "medium"


class TestEntityExtractorEdgeCases:
    """Test entity extractor edge cases."""

    def test_extract_mixed_addresses(self):
        extractor = EntityExtractor()
        query = "compare 0:aaaa000000000000000000000000000000000000000000000000000000000000 and EQBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
        entities = extractor.extract_entities(query)

        assert len(entities) == 2

    def test_no_entities_in_text_query(self):
        extractor = EntityExtractor()
        query = "show me DeFi projects with high TVL"
        entities = extractor.extract_entities(query)
        assert len(entities) == 0

    def test_extract_only_addresses(self):
        extractor = EntityExtractor()
        addresses = extractor.extract_addresses(
            "wallet 0:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
        )
        assert len(addresses) == 1


class TestParsedQuerySuggestions:
    """Test that suggestions are generated for typos."""

    def test_suggestions_for_typos(self):
        parser = create_parser()
        result = parser.parse("show me projcts with high tv1")

        assert len(result.suggestions) > 0
        assert any(
            "projct" in s.lower() or "tv1" in s.lower() for s in result.suggestions
        )

    def test_no_suggestions_for_clean_query(self):
        parser = create_parser()
        result = parser.parse("show me DeFi projects")
        assert len(result.suggestions) == 0 or result.suggestions is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
