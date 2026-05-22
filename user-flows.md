# T01 — User Flow Diagrams

## Flow 1: Query Input → Entity Resolution

```
┌──────────────┐
│  User Input  │
│  Query Text  │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│  NLP Parser      │
│  - Intent        │
│  - Entities      │
│  - Filters       │
└──────┬──────────┘
       │
       ▼
┌──────────────────┐
│ Entity Resolution│
│ - Wallets        │◄── TON Index
│ - Contracts      │◄── DNS Resolver
│ - Projects       │◄── Project Registry
└──────┬──────────┘
       │
       ▼
┌──────────────────┐
│ Canonical Form   │
│ - Resolved Addr  │
│ - Matched Entity │
│ - Confidence %   │
└──────────────────┘
```

## Flow 2: Data Aggregation → Brief Generation

```
┌──────────────────┐
│ Resolved Entity  │
└──────┬──────────┘
       │
       ▼
┌──────────────────┐
│ Data Aggregation │
│ - On-chain data  │◄── TON Index API
│ - Token metrics  │◄── Token APIs
│ - Social signals  │◄── External APIs
└──────┬──────────┘
       │
       ▼
┌──────────────────┐
│ Analysis Engine  │
│ - Risk Scorer    │
│ - Opp Scorer     │
│ - Trend Detector │
└──────┬──────────┘
       │
       ▼
┌──────────────────┐
│ Template Engine  │
│ - Select template│
│ - Fill data      │
│ - Format output  │
└──────┬──────────┘
       │
       ▼
┌──────────────────┐
│ Brief Generated  │
└──────────────────┘
```

## Flow 3: Result Presentation → Export Options

```
┌──────────────────┐
│ Brief Rendered   │
│ - Summary        │
│ - Metrics        │
│ - Scores         │
│ - Evidence       │
└──────┬──────────┘
       │
       ▼
┌──────────────────┐
│ User Views Result│
└──────┬──────────┘
       │
  ┌────┴────┬───────────┬────────────┐
  ▼         ▼           ▼            ▼
┌──────┐ ┌──────┐  ┌─────────┐  ┌──────────┐
│JSON  │ │Markdown│ │Copy     │  │Bookmark  │
│Export│ │Export │  │to Clip  │  │Project   │
└──────┘ └──────┘  └─────────┘  └──────────┘
```

---

## Implementation Notes

- Keep query parser modular for future NLP model upgrades
- Entity resolution should cache results to reduce API calls
- Brief templates should be versioned for backwards compatibility
- Risk/opportunity scoring should be documented with formula transparency