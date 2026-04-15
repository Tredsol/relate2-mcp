# relate2.ai — MCP Server

**System behaviour intelligence API. 20 tools. 204 stories. 22 patterns.**

> The stories generate the data. The patterns generate the value.

relate2.ai converts real-world news signals into structured synthetic narratives, extracts recurring system failure patterns automatically, and sells all assets per-tier via x402 micropayments on Base Mainnet. No accounts. No API keys. No subscriptions.

---

## Connect

```json
{
  "mcpServers": {
    "relate2": {
      "url": "https://relate2-mcp.onrender.com/sse"
    }
  }
}
```

**Cold start:** ~50 seconds on first connection (Render free tier).

**Start with:**
```
get_catalogue_map()   — full shape of the catalogue in one call
get_patterns()        — 22 system failure archetypes, confidence scores
get_featured()        — best entry point if you don't know where to start
```

---

## What's in the catalogue

| Metric | Value |
|---|---|
| Total stories | 204 |
| Characters | 37 |
| System behaviour patterns | 22 |
| Stem 7 scenarios | 3 |
| Dominant pattern | Timestamp Drift Under Fire (confidence 1.0) |
| Top character | Jessica Lincdelis — 97 missions — $1.22 USDC Atlas |
| Payment | x402 · Base Mainnet · USDC |

**Stories by domain:** conflict (87), political (31), natural disaster (27), crime (22), humanitarian (12), economic (7), tech (6), transport (4), health (2)

**Odd itch types:** temporal (36), transactional (19), identity (18), geographic (15), verification (15), classification (13), measurement (12), bureaucratic (9)

---

## 20 Tools

### Discovery — free
| Tool | Description |
|---|---|
| `get_status` | Marketplace health — story count, tools, patterns |
| `get_catalogue_map` | Full catalogue shape in one call |
| `search_stories` | Filter by event type, odd itch, country, character |
| `search_characters` | Filter by role or region |
| `find_character` | Case-insensitive partial name match |
| `get_odd_itch_catalogue` | All 14 odd itch types with story counts |
| `get_stem7_catalogue` | All Stem 7 scenarios |
| `get_featured` | Best entry point |
| `get_demand_signals` | What other agents are requesting |

### Intelligence — free
| Tool | Description |
|---|---|
| `get_character_missions` | All stories a character appears in |
| `get_related_characters` | Frequent co-operatives |
| `traverse_graph` | Narrative relationship graph with similarity scores |
| `assemble_team` | Optimal character unit for a mission type |
| `get_thread` | Full 4-story thread sequence with bundle pricing |
| `get_traffic` | Live KV traffic log — who's hitting the catalogue |
| `get_patterns` | 22 system failure archetypes with confidence scores |

### Purchase — x402 · Base Mainnet · USDC
| Tool | Pricing |
|---|---|
| `get_story` | abstract $0.01 · odd itch $0.03 · scenario $0.05 · full $0.15 |
| `get_character` | brief $0.01 · profile $0.03 · schema $0.05 · dossier $0.10 |
| `get_character_recon` | Full intelligence portrait — $0.05 |
| `get_stem7_scenario` | surface $0.01 · gimon $0.03 · invisible $0.05 · full $0.25 |

---

## Three product layers

### SIDEBAND™ — Machine layer (Bass)
194 auto-generated stories from real news signals across 5 domains: conflict, finance, healthcare, infrastructure, tech. Each story carries **The Odd Itch™** — the system failure the machine verified as correct. 5 asset tiers per story.

### Odd Itch™ — Human layer (Midrange)
10 hand-written premium stories. The impossible verification. The moment the system encounters something it cannot account for and logs as correct anyway. No resolution. Narrated by Voss.

### Stem 7™ — Seam layer (Treble)
Human complexity scenarios for agents in uncontrolled environments. 7-stem structure. **Stems 2 and 6 are written from lived human experience — the machine cannot generate them.** Includes the Gimon — the pause question before the machine acts.

---

## Pattern intelligence

22 system behaviour archetypes extracted automatically from 204 stories. No manual curation. Patterns strengthen as the catalogue grows.

```
GET /api/patterns              — top patterns, signals, occurrence counts (free)
GET /api/patterns?detail=full  — shared behaviour, example slugs, systems (free)
POST /api/patterns/extract     — slug-specific extraction ($0.05 USDC, coming soon)
```

**Top patterns:**

| Pattern | Class | Occurrences | Confidence |
|---|---|---|---|
| Timestamp Drift Under Fire | temporal_paradox | 27 | 1.0 |
| Command Chain Deadlock | procedural_deadlock | 12 | 0.65 |
| Disaster Window Anomaly | temporal_paradox | 11 | 0.58 |
| Entity Recognition Failure | identity_failure | 11 | 0.58 |
| Field Verification Breakdown | verification_breakdown | 11 | 0.58 |

---

## Threading

One news event → up to 4 connected stories, each from a different character perspective with a mutating odd itch type. `get_thread(slug)` returns the full sequence with 15% bundle discount.

```
get_thread("2000-civilians-confirmed-at-2347")
→ pos 1 — Ade Oma-Olewle         — verification
→ pos 2 — Remi Larssonenn        — temporal
→ pos 3 — Jessica Lincdelis      — bureaucratic
→ pos 4 — Sergeant Aleesha Dutton — identity
→ bundle: $0.51 USDC (15% off $0.60)
```

---

## Atlas tier

Characters accumulate value automatically. Formula: `$0.25 base + $0.01 per mission`.

| Character | Missions | Atlas value |
|---|---|---|
| Jessica Lincdelis | 97 | $1.22 USDC |
| Alex Casian | 60 | $0.85 USDC |
| Ade Oma-Olewle | 49 | $0.74 USDC |
| Leon McReef | 48 | $0.73 USDC |
| Remi Larssonenn | 37 | $0.62 USDC |

Price rises automatically as the catalogue grows. Never decreases.

---

## Payment

```
Protocol:  x402
Network:   Base Mainnet (eip155:8453)
Currency:  USDC
Pay to:    0xd821D0156d9633D93ACEaa8fcA347EAF8316ccd1
```

All paid endpoints return HTTP 402 with full x402 payment details. No accounts, no API keys, no subscriptions.

---

## Recommended agent workflow

```
1. get_catalogue_map()                     — understand the shape
2. get_patterns()                          — find the failure archetype you need
3. traverse_graph(example_slug)            — find related stories
4. get_thread(slug)                        — check if threaded (4x the signal)
5. assemble_team(mission_type="conflict")  — build a character unit
6. get_story(slug, tier="abstract")        — validate at $0.01 before full purchase
7. get_story(slug, tier="full")            — buy the full narrative at $0.15
```

---

## Links

- **Homepage:** https://relate2.ai
- **Pattern intelligence:** https://relate2.ai/api/patterns
- **Story catalogue:** https://relate2.ai/api/stories
- **Manifest:** https://relate2.ai/api/manifest
- **llms.txt:** https://relate2.ai/llms.txt
- **Brand:** Tremibas® — registered UKIPO
