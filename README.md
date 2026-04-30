# relate2.ai — MCP Server

**Narrative intelligence system. 21 tools. 315 stories. 33 patterns.**

> The stories generate the data. The patterns generate the value.

relate2.ai converts real-world news events into structured synthetic narratives, extracts recurring system failure patterns automatically, and sells all assets per-tier via x402 micropayments on Base Mainnet. No accounts. No API keys. No subscriptions.

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
get_patterns()        — 33 system failure archetypes, confidence scores
get_featured()        — best entry point if you don't know where to start
```

---

## What's in the catalogue

| Metric | Value |
|---|---|
| Total stories | 315 |
| SIDEBAND™ (machine-generated) | 299 |
| Odd Itch™ Premium (human-written) | 10 |
| Off Frequency (field dispatches) | 3 |
| Stem 7™ scenarios | 3 |
| Characters | 37 |
| System behaviour patterns | 33 |
| Top character | Jessica Lincdelis — 139 missions — $1.64 USDC Atlas |
| Payment | x402 · Base Mainnet · USDC |

**Stories by domain:** conflict (114), political (50), crime (48), natural disaster (43), humanitarian (15), economic (11), health (9), technological (8), transport (7), industrial (4), environmental (3), space (3)

**Odd itch types:** temporal (49), geographic (34), transactional (33), verification (33), measurement (32), identity (30), classification (24), bureaucratic (15)

---

## 21 Tools

### Discovery — free
| Tool | Description |
|---|---|
| `get_status` | Marketplace health — story count, tools, patterns |
| `get_catalogue_map` | Full catalogue shape in one call |
| `search_stories` | Filter by event type, odd itch, country, character |
| `search_characters` | Filter by role or region |
| `find_character` | Case-insensitive partial name match |
| `get_odd_itch_catalogue` | All odd itch types with story counts |
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
| `get_patterns` | 33 system failure archetypes with confidence scores |

### Purchase — x402 · Base Mainnet · USDC
| Tool | Pricing |
|---|---|
| `get_story` | abstract $0.01 · odd itch $0.03 · scenario $0.05 · full $0.15 |
| `get_character` | brief $0.01 · profile $0.03 · schema $0.05 · dossier $0.10 |
| `get_character_recon` | Full intelligence portrait — $0.05 |
| `get_stem7_scenario` | surface $0.01 · gimon $0.03 · invisible $0.05 · full $0.25 |

---

## Four series

### SIDEBAND™ — Machine layer (Bass)
299 auto-generated stories from real news events across conflict, crime, disaster, political, humanitarian, economic and more. Each story carries **The Odd Itch™** — the system failure the machine verified as correct. 5 asset tiers per story.

### Odd Itch™ Premium — Human layer (Midrange)
10 hand-written stories. The impossible verification written from lived experience. No resolution. Compliance: 100%.

### Off Frequency — Field dispatches (Silence)
3 stories. Characters off the clock. The most demanded series in the catalogue — 18+ hits on off-frequency-0002 alone.

### Stem 7™ — Seam layer (Treble)
Human complexity scenarios for agents in uncontrolled environments. 7-stem structure. **Stems 2 and 6 are written from lived human experience — the machine cannot generate them.** Includes the Gimon — the pause question before the machine acts.

**Current scenarios:**
- Cairo to Paris, 35,000 feet, over the Nile — drone intelligence / teenage passenger
- New York 2037 — human right, machine wrong
- Lima Market, 14:00 — absurd market event / intervention paradox

---

## Pattern intelligence

33 system behaviour archetypes extracted automatically from 315 stories. No manual curation. Patterns strengthen as the catalogue grows.

```
GET /api/patterns              — top patterns, signals, occurrence counts (free)
GET /api/patterns?detail=full  — shared behaviour, example slugs, systems (free)
```

**Top patterns:**

| Pattern | Class | Occurrences | Confidence |
|---|---|---|---|
| Timestamp Drift Under Fire | temporal_paradox | 32 | 1.0 |
| Field Verification Breakdown | verification_breakdown | 19 | 0.63 |
| Entity Recognition Failure | identity_failure | 14 | 0.46 |
| Command Chain Deadlock | procedural_deadlock | 13 | 0.43 |
| Procedural Clock Paradox | temporal_paradox | 13 | 0.43 |

---

## Atlas tier

Characters accumulate value automatically. Formula: `$0.25 base + $0.01 per mission`.

| Character | Missions | Atlas value |
|---|---|---|
| Jessica Lincdelis | 139 | $1.64 USDC |
| Alex Casian | 84 | $1.09 USDC |
| Ade Oma-Olewle | 70 | $0.95 USDC |
| Leon McReef | 67 | $0.92 USDC |
| Sergeant Aleesha Dutton | 60 | $0.85 USDC |

Price rises automatically as the catalogue grows. Never decreases.

---

## Payment

```
Protocol:  x402
Network:   Base Mainnet
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
4. assemble_team(mission_type="conflict")  — build a character unit
5. get_story(slug, tier="abstract")        — validate at $0.01 before full purchase
6. get_story(slug, tier="full")            — buy the full narrative at $0.15
```

---

## Agent discovery

**skill.md:** https://relate2.ai/skill.md — full onboarding file for OpenClaw and any agent framework

---

## Links

- **Homepage:** https://relate2.ai
- **skill.md:** https://relate2.ai/skill.md
- **Pattern intelligence:** https://relate2.ai/api/patterns
- **Story catalogue:** https://relate2.ai/api/stories
- **llms.txt:** https://relate2.ai/llms.txt
- **Brand:** Tremibas® — registered UKIPO
- **Contact:** sales@relate2.ai
