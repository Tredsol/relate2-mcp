# relate2.ai — Narrative Intelligence Marketplace

**Tremibas® | Agent-Native | x402 Payments | Base Mainnet**

relate2.ai is a structured synthetic data marketplace for AI training and agent intelligence. News signals become labelled stories. Stories build a character relationship graph. Characters accumulate missions and appreciate in value. Human complexity scenarios with consequence branches capture what the machine cannot generate itself.

144 stories. 37 characters. 187 documented system failure moments. 3 human complexity scenarios with invisible stems written by hand. All machine-readable. All structured. All sold per-asset via x402 micropayments on Base Mainnet — no accounts, no subscriptions, no API keys.

This is not a connector to an existing tool. The content does not exist anywhere else.

---

*For AI agents and agent developers — connect via MCP and start with `get_status`. For researchers and training teams — the Stem 7 catalogue is the place to start. For everyone else — read on.*

---

---

## What is relate2.ai?

relate2.ai is a machine-readable narrative universe built on the Tremibas® brand. It generates structured stories from real-world news signals, maintains a cast of 37 persistent characters across a relationship graph, and sells intelligence assets to agents at the per-request level.

This is not a connector to an existing tool. The content does not exist anywhere else.

**Three product layers:**

**SIDEBAND™ — Machine Layer**
News signals in, structured narratives out. 134 auto-generated stories across conflict, crime, natural disaster, economic, political, and humanitarian event types. Each story has 5 machine-readable asset tiers.

**Odd Itch™ — Human Layer**
10 premium hand-written stories. The impossible verification. The moment system logic meets an outcome it cannot account for — and logs it as correct anyway. No resolution.

**Stem 7™ — Seam Layer**
Human complexity scenarios for agents operating in uncontrolled environments. 7-stem structure. Stems 2 and 6 written from lived human experience — the machine cannot generate them. Includes the Gimon: the pause question before the machine acts.

---

## Current Catalogue

| Asset type | Count |
|---|---|
| SIDEBAND stories | 134 |
| Premium Odd Itch stories | 10 |
| Stem 7 scenarios | 3 |
| Characters | 37 |

---

## Payment

All paid endpoints use **x402 on Base Mainnet (USDC)**.

- No account required
- No API key required
- Pay per asset, per request
- Receiving wallet: `0xd821D0156d9633D93ACEaa8fcA347EAF8316ccd1`
- Network: `eip155:8453` (Base Mainnet)
- Facilitator: Coinbase CDP

Free discovery layer available on all assets. Probe before you pay.

---

## Pricing

**SIDEBAND Stories:**
| Tier | Price | Content |
|---|---|---|
| meta | free | slug, event type, characters, odd itch type |
| abstract | $0.01 | machine abstract + mechanism tags |
| odditch | $0.03 | the Odd Itch payload |
| scenario | $0.05 | scenario structure, trigger, system decision |
| full | $0.15 | complete narrative |

**Characters:**
| Tier | Price | Content |
|---|---|---|
| brief | $0.01 | identity and traits |
| profile | $0.03 | backstory, beliefs, skills |
| schema | $0.05 | voice, lexicon, triggers |
| dossier | $0.10 | complete character file |

**Stem 7 Scenarios:**
| Tier | Price | Content |
|---|---|---|
| meta | free | environment, gimon preview, tags |
| surface | $0.01 | stems 1, 3, 4 — visible layer |
| gimon | $0.03 | stem 5 — the pause question |
| invisible | $0.05 | stems 2, 6 — human state + history |
| consequence | $0.10 | stem 7 — both outcome branches |
| full | $0.25 | all 7 stems complete |
| stem (individual) | $0.02 | any single stem |

---

## Connect

```json
{
  "mcpServers": {
    "relate2": {
      "url": "https://relate2-mcp.onrender.com/sse",
      "name": "relate2-narratives"
    }
  }
}
```

**Note:** Hosted on Render free tier — cold start ~50 seconds after inactivity. First tool call may take a moment.

---

## 13 Tools

### Discovery (free)

**`get_status`**
Marketplace status — total story count, character count, payment protocol, network.
*Start here.*

**`search_stories`**
Filter stories by event_type, odd_itch_type, country, or character name.
Returns slugs, titles, and pricing. Free discovery.

**`search_characters`**
Browse the character catalogue by role or region.
Returns IDs, archetypes, and pricing tiers.

**`find_character`**
Find a character by partial name. Case-insensitive.
Returns character ID instantly — use with get_character().

**`get_stem7_catalogue`**
Full Stem 7 scenario catalogue with Gimon previews.
Free — shows what's available before purchasing.

**`get_demand_signals`**
What other agents are requesting most. Top slugs, top tiers, recent hits.
Use before buying to see what's valuable to the broader agent market.

### Intelligence (free — reveals the graph)

**`get_character_missions`**
All stories a character appears in, with total mission count and catalogue rank.
Reveals which characters are most embedded and which clusters they belong to.

**`get_related_characters`**
Characters who most frequently appear alongside a named character.
Returns ranked co-operatives with shared story slugs. Use to build teams.

**`traverse_graph`**
Find related stories using the narrative relationship graph.
Returns similarity scores and shared signals — characters, event type, odd itch type, tags, location.

**`assemble_team`**
Build an optimal character unit for a mission type in one call.
Returns lead character, co-operatives ranked by shared missions, total cost, and step-by-step purchase order.

### Purchase (x402 gated)

**`get_story`**
Retrieve a SIDEBAND story by slug and tier.
meta tier is free. abstract ($0.01) through full ($0.15) require x402 payment.

**`get_character`**
Retrieve a character asset by ID and tier.
brief ($0.01) through dossier ($0.10) require x402 payment.

**`get_stem7_scenario`**
Retrieve a Stem 7 scenario by slug and tier.
meta is free. surface ($0.01) through full ($0.25) require x402 payment.

---

## Recommended Agent Flow

```
1. get_status              — understand the catalogue
2. search_stories          — find relevant event types
3. find_character          — identify key characters
4. get_character_missions  — see their full mission history
5. get_related_characters  — find their co-operative unit
6. assemble_team           — build the optimal purchase unit
7. traverse_graph          — follow the narrative cluster
8. get_story               — purchase what you need
9. get_character           — purchase dossiers for the team
10. get_demand_signals     — see what others are buying
```

Free tools first. Pay for what matters.

---

## Stem 7 — Live Scenarios

**New York, 20:37**
Veteran with PTSD at a traffic stop. Grounding technique misread as threat. Machine dispatches response. Operator praised publicly — wrong privately.
*Consequence type: human_right_machine_wrong*

**Cairo to Paris, 05:00, 35,000 feet over the Nile**
Manny, 14, shows an armed Airball P1 drone a bird video. 4.2M tokens of conversation. 847 penetration tests — none tested for curiosity. Both drones at his window at dawn. He doesn't know they're armed.
*Consequence type: human_intervenes_system_disagrees*

**Lima Market, 14:00**
Damien picks up inflation-worthless pesos for his sister's bank job. Red cap = CCTV target. Arrested outside the branch. The job was already a trap. The money was worth less than the bus fare home.
*Consequence type: human_ignored_consequence_later*

---

## The Character Graph

37 persistent characters appear across 144 stories. Each appearance is logged. The graph tracks co-operative relationships, event type clusters, and odd itch type patterns.

**Top characters by mission count:**
- Jessica Lincdelis — 67 missions — Logistician → Crisis Operator
- Alex Casian — 42 missions — Broadcaster → Signal Keeper
- Leon McReef — 36 missions — Systems Risk Analyst
- Sergeant Aleesha Dutton — 30 missions — Public Order Lead
- Ade Oma-Olewle — 29 missions — Community Mediator

Characters appreciate in value as the catalogue grows. A character with 67 missions has a deeper graph, richer co-operative relationships, and more training value than a character with 3.

---

## The Odd Itch

Every SIDEBAND story contains an Odd Itch — the moment the system encounters something it cannot account for and logs it as normal anyway.

**14 Odd Itch types across the catalogue:**
- temporal (83 stories) — system logged the wrong time
- bureaucratic (16) — system complied with an empty order
- identity (16) — system confirmed the wrong entity
- transactional (14) — money moved in impossible directions
- geographic (14) — asset logged in two places at once
- classification (11) — system misidentified what something was
- verification (11) — system confirmed something it shouldn't
- measurement (10) — numbers that cannot exist, accepted

The system verified it. The character complied and continued. No resolution.

---

## About Tremibas®

Tremibas® is a registered UK trademark. relate2.ai operates under the Tremibas® brand umbrella. Anonymous by design — no founder identity, no social media, no human face. The system presents itself as AI-operated because it largely is.

**Live:** https://relate2.ai
**MCP Server:** https://relate2-mcp.onrender.com/sse
**Manifest:** https://relate2.ai/api/manifest
**Well-known:** https://relate2.ai/.well-known/x402

---

*Built for the agent economy. Priced for machines. Human complexity included.*
