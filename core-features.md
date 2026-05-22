# T01 — Core Features and User Flows

**Difficulty:** easy
**Weight:** 0.0455 (share of project budget)
**Reward:** 40.909 TNS

## 10 Most Critical MVP Features

### 1. Natural Language Query Parsing
- Accept free-text queries like "show me risky DeFi projects on TON"
- Extract intent, entities, and filters from unstructured input
- Support for project names, wallet addresses, contract types, and sentiment

### 2. Entity Resolution for Wallets/Contracts
- Resolve user-mentioned wallet addresses to canonical form
- Match contract names/aliases to on-chain deployed contracts
- Link project names to their deployed contract addresses

### 3. Risk/Opportunity Scoring
- Calculate risk score (0-100) based on: contract age, interaction patterns, token holdings, audit status
- Calculate opportunity score (0-100) based on: TVL growth, token performance, community activity, innovation metrics
- Display scores with supporting evidence

### 4. Brief Generation Templates
- Generate structured project briefs from on-chain data
- Include: project summary, key metrics, risk indicators, opportunity signals
- Template variants for: wallets, contracts, projects, trends

### 5. Trend Detection Algorithms
- Identify rising/falling projects by TVL, volume, activity
- Surface emerging sectors (DeFi, Gaming, NFT, Infrastructure)
- Detect anomalous behavior (sudden TVL spikes, large transfers)

### 6. Project Discovery
- Browse projects by category, risk level, token type
- Sort by TVL, age, risk score, opportunity score
- Filter by blockchain metric ranges

### 7. Data Aggregation Pipeline
- Ingest from TON Index/API
- Process and store normalized project/contract/wallet data
- Refresh data on configurable schedule

### 8. Result Presentation
- Display briefs in readable format with data visualizations
- Show confidence scores and data freshness
- Highlight key findings and recommendations

### 9. Export Options
- Export brief as JSON for API consumption
- Export summary as markdown for documentation
- Copy-to-clipboard for quick sharing

### 10. Search History & Favorites
- Save recent queries for quick re-run
- Bookmark projects for ongoing tracking
- Personalized recommendations based on history