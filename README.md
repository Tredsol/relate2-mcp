# relate2.ai MCP Server

Gives AI agents native access to the relate2.ai narrative intelligence marketplace.

## Tools

| Tool | Description |
|------|-------------|
| `get_status()` | Marketplace status — story count, x402 status |
| `search_stories(event_type, odd_itch_type, country, character, limit)` | Search SIDEBAND™ catalogue |
| `get_story(slug, tier)` | Get a story by slug and tier |
| `traverse_graph(slug)` | Find related stories via the narrative graph |
| `search_characters(role, region, limit)` | Search character catalogue |
| `get_character(character_id, tier)` | Get a character asset |
| `get_stem7_catalogue()` | Get all Stem 7™ scenarios |
| `get_stem7_scenario(slug, tier)` | Get a Stem 7™ scenario by slug and tier |

## Pricing

All content is free to discover. Paid tiers require x402 payment on Base Mainnet (USDC).

| Asset | Tier | Price |
|-------|------|-------|
| Story | abstract | $0.01 |
| Story | odd_itch | $0.03 |
| Story | scenario | $0.05 |
| Story | full | $0.15 |
| Character | brief | $0.01 |
| Character | profile | $0.03 |
| Character | schema | $0.05 |
| Character | dossier | $0.10 |
| Stem 7 | surface | $0.01 |
| Stem 7 | gimon | $0.03 |
| Stem 7 | invisible | $0.05 |
| Stem 7 | consequence | $0.10 |
| Stem 7 | full | $0.25 |
| Stem 7 | individual stem | $0.02 |

## Installation

Add to your MCP config:

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

## Local Development

```
pip install -r requirements.txt
python server.py
```

## Deployment

Hosted on Render. Auto-deploys from Tredsol/relate2-mcp main branch.

## Brand

Tremibas® · SIDEBAND™ · Odd Itch™ · Stem 7™
relate2.ai · x402 · Base Mainnet · USDC
