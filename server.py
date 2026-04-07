"""
relate2.ai MCP Server
Gives AI agents native access to the relate2.ai narrative intelligence marketplace.
Tools: search_stories, get_story, get_character, search_characters,
       get_stem7_catalogue, get_stem7_scenario, traverse_graph, get_status
"""

import os
import json
import httpx
from mcp.server.fastmcp import FastMCP

# ============================================================================
# CONFIG
# ============================================================================

BASE_URL = os.getenv("RELATE2_BASE_URL", "https://relate2.ai")
TIMEOUT  = 30

mcp = FastMCP("relate2-narratives")

# ============================================================================
# HTTP HELPER
# ============================================================================

async def get(path: str, params: dict = None) -> dict:
    """Make a GET request to the relate2.ai API."""
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            res = await client.get(f"{BASE_URL}{path}", params=params)
            res.raise_for_status()
            return res.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "status": e.response.status_code}
        except Exception as e:
            return {"error": str(e)}


# ============================================================================
# TOOL: GET STATUS
# ============================================================================

@mcp.tool()
async def get_status() -> str:
    """
    Get the current status of the relate2.ai marketplace.
    Returns total story count, Stem 7 scenario count, character count,
    and x402 payment status.
    Use this first to understand what's available.
    """
    data = await get("/api/status")
    if "error" in data:
        return f"Error fetching status: {data['error']}"

    cat = data.get("catalogue", {})
    x402 = data.get("x402", {})

    return json.dumps({
        "marketplace":        "relate2.ai",
        "brand":              "Tremibas®",
        "total_stories":      cat.get("total", 0),
        "sideband_auto":      cat.get("sideband_auto", 0),
        "premium_odd_itch":   cat.get("premium_odd_itch", 0),
        "stem7_scenarios":    "use get_stem7_catalogue() for count",
        "payment_protocol":   "x402",
        "network":            x402.get("network", "eip155:8453"),
        "currency":           "USDC",
        "receiving_address":  x402.get("receiving_address", ""),
        "status":             x402.get("status", "unknown"),
        "note": "All paid endpoints return HTTP 402 with full x402 payment details."
    }, indent=2)


# ============================================================================
# TOOL: SEARCH STORIES
# ============================================================================

@mcp.tool()
async def search_stories(
    event_type: str = "",
    odd_itch_type: str = "",
    country: str = "",
    character: str = "",
    limit: int = 10
) -> str:
    """
    Search the relate2.ai SIDEBAND™ story catalogue.

    Args:
        event_type:    Filter by event type. Options: conflict, crime,
                       natural_disaster, economic, political, humanitarian
        odd_itch_type: Filter by Odd Itch type. Options: measurement_failure,
                       temporal_glitch, incentive_distortion,
                       emotional_contradiction, system_blindness,
                       prediction_error, system_success_disturbing
        country:       Filter by country name (e.g. "Lebanon", "Iran")
        character:     Filter by character name (e.g. "Jessica Lincdelis")
        limit:         Maximum number of results to return (default 10, max 50)

    Returns a list of stories with slug, title, character, event type,
    odd itch type, country and pricing tiers.

    Stories are free to discover. Full narratives cost $0.15 USDC via x402.
    Use get_story() to purchase a specific story.
    """
    data = await get("/api/stories")
    if "error" in data:
        return f"Error fetching stories: {data['error']}"

    stories = data.get("stories", [])

    # Filter
    if event_type:
        stories = [s for s in stories if s.get("event_type", "").lower() == event_type.lower()]
    if odd_itch_type:
        stories = [s for s in stories if s.get("odd_itch_type", "").lower() == odd_itch_type.lower()]
    if country:
        stories = [s for s in stories if country.lower() in (s.get("country") or "").lower()]
    if character:
        stories = [s for s in stories if
                   character.lower() in (s.get("primary_character") or "").lower() or
                   any(character.lower() in (c or "").lower()
                       for c in s.get("characters_involved", []))]

    stories = stories[:min(limit, 50)]

    if not stories:
        return "No stories found matching those filters. Try broader search terms."

    results = []
    for s in stories:
        results.append({
            "slug":              s.get("slug"),
            "title":             s.get("title"),
            "primary_character": s.get("primary_character"),
            "event_type":        s.get("event_type"),
            "odd_itch_type":     s.get("odd_itch_type"),
            "country":           s.get("country"),
            "meta_endpoint":     f"/sideband/{s.get('slug')}/meta",
            "pricing": {
                "abstract":       "$0.01 USDC",
                "odd_itch":       "$0.03 USDC",
                "scenario":       "$0.05 USDC",
                "full_narrative": "$0.15 USDC"
            }
        })

    return json.dumps({
        "total_found": len(results),
        "filters_applied": {
            "event_type":    event_type or "none",
            "odd_itch_type": odd_itch_type or "none",
            "country":       country or "none",
            "character":     character or "none"
        },
        "stories": results
    }, indent=2)


# ============================================================================
# TOOL: GET STORY
# ============================================================================

@mcp.tool()
async def get_story(slug: str, tier: str = "meta") -> str:
    """
    Get a specific SIDEBAND™ story by slug and tier.

    Args:
        slug: The story slug (get from search_stories)
        tier: Which tier to retrieve. Options:
              - meta      ($0.00 — free discovery layer)
              - abstract  ($0.01 USDC — machine abstract)
              - odditch   ($0.03 USDC — Odd Itch payload)
              - scenario  ($0.05 USDC — scenario structure)
              - full      ($0.15 USDC — complete narrative)

    Paid tiers require x402 payment on Base Mainnet (USDC).
    The response for paid tiers will include payment instructions
    if no valid payment header is provided.

    Use tier="meta" first to verify the story exists and review pricing
    before purchasing a paid tier.
    """
    if tier == "meta":
        data = await get(f"/sideband/{slug}/meta")
    elif tier == "abstract":
        data = await get(f"/sideband/{slug}/abstract")
    elif tier == "odditch":
        data = await get(f"/sideband/{slug}/odditch")
    elif tier == "scenario":
        data = await get(f"/sideband/{slug}/scenario")
    elif tier == "full":
        data = await get(f"/sideband/{slug}")
    else:
        return f"Invalid tier '{tier}'. Options: meta, abstract, odditch, scenario, full"

    if "error" in data:
        return f"Error fetching story: {data['error']}"

    return json.dumps(data, indent=2)


# ============================================================================
# TOOL: TRAVERSE GRAPH
# ============================================================================

@mcp.tool()
async def traverse_graph(slug: str) -> str:
    """
    Traverse the relate2.ai narrative relationship graph for a story.

    Args:
        slug: The story slug to find relationships for

    Returns related stories with similarity scores and shared signals
    explaining WHY they are related (shared characters, event types,
    odd itch types, themes, locations).

    Use this to:
    - Find thematically related stories for training datasets
    - Build narrative chains across multiple stories
    - Discover which characters appear across multiple events
    - Find stories with similar system failure patterns

    Graph weights:
    - Characters (0.35) — strongest signal
    - Event type (0.25)
    - Odd Itch type (0.20)
    - Tags (0.10)
    - Location (0.03)
    """
    data = await get(f"/api/graph/{slug}")
    if "error" in data:
        return f"Error fetching graph: {data['error']}"

    return json.dumps(data, indent=2)


# ============================================================================
# TOOL: SEARCH CHARACTERS
# ============================================================================

@mcp.tool()
async def search_characters(
    role: str = "",
    region: str = "",
    limit: int = 10
) -> str:
    """
    Search the relate2.ai character catalogue.

    Args:
        role:   Filter by operational role (e.g. "analyst", "operator",
                "field agent", "medic")
        region: Filter by region (e.g. "West Africa", "Middle East", "Europe")
        limit:  Maximum number of results (default 10)

    Returns character IDs, names, roles and pricing tiers.

    Character assets:
    - brief   ($0.01 USDC — identity and traits)
    - profile ($0.03 USDC — backstory, beliefs, skills)
    - schema  ($0.05 USDC — voice, lexicon, triggers)
    - dossier ($0.10 USDC — complete character file)

    Use get_character() to purchase a specific character asset.
    """
    data = await get("/api/characters")
    if "error" in data:
        return f"Error fetching characters: {data['error']}"

    characters = data.get("characters", [])

    if role:
        characters = [c for c in characters
                     if role.lower() in c.get("role", "").lower()
                     or role.lower() in c.get("operational_tier", "").lower()]
    if region:
        characters = [c for c in characters
                     if region.lower() in c.get("region", "").lower()
                     or region.lower() in c.get("country", "").lower()]

    characters = characters[:min(limit, 37)]

    if not characters:
        return "No characters found matching those filters."

    results = []
    for c in characters:
        results.append({
            "id":               c.get("id"),
            "name":             c.get("name"),
            "role":             c.get("role"),
            "operational_tier": c.get("operational_tier"),
            "region":           c.get("region", c.get("country", "")),
            "pricing": {
                "brief":   "$0.01 USDC",
                "profile": "$0.03 USDC",
                "schema":  "$0.05 USDC",
                "dossier": "$0.10 USDC"
            }
        })

    return json.dumps({
        "total_found": len(results),
        "characters":  results
    }, indent=2)


# ============================================================================
# TOOL: GET CHARACTER
# ============================================================================

@mcp.tool()
async def get_character(character_id: str, tier: str = "brief") -> str:
    """
    Get a specific character asset by ID and tier.

    Args:
        character_id: Character ID from search_characters
                      (format: TRB-CHAR-xxxxx-10000)
        tier: Which tier to retrieve. Options:
              - brief   ($0.01 USDC — identity and traits)
              - profile ($0.03 USDC — backstory, beliefs, skills)
              - schema  ($0.05 USDC — voice, lexicon, triggers)
              - dossier ($0.10 USDC — complete character file)

    Paid tiers require x402 payment on Base Mainnet (USDC).
    """
    if tier not in ["brief", "profile", "schema", "dossier"]:
        return f"Invalid tier '{tier}'. Options: brief, profile, schema, dossier"

    data = await get(f"/character/{character_id}/{tier}")
    if "error" in data:
        return f"Error fetching character: {data['error']}"

    return json.dumps(data, indent=2)


# ============================================================================
# TOOL: GET STEM 7 CATALOGUE
# ============================================================================

@mcp.tool()
async def get_stem7_catalogue() -> str:
    """
    Get the full Stem 7™ scenario catalogue.

    Stem 7™ is the Seam Layer — human complexity scenarios for agents
    operating in uncontrolled environments. Each scenario has 7 stems:

    1. Environment      — the physical world (machine readable)
    2. Human State      — the invisible truth (human written)
    3. Visible Signals  — what the system detects (machine readable)
    4. Social Context   — who else is present (machine readable)
    5. Gimon            — the pause question before action
    6. History          — what happened before (human written)
    7. Consequence      — both outcome branches (right call / wrong call)

    Stems 2 and 6 are written from lived human experience.
    The machine cannot generate them.

    Use get_stem7_scenario() to purchase a specific scenario.
    """
    data = await get("/api/stem7")
    if "error" in data:
        return f"Error fetching Stem 7 catalogue: {data['error']}"

    return json.dumps(data, indent=2)


# ============================================================================
# TOOL: GET STEM 7 SCENARIO
# ============================================================================

@mcp.tool()
async def get_stem7_scenario(slug: str, tier: str = "meta") -> str:
    """
    Get a specific Stem 7™ scenario by slug and tier.

    Args:
        slug: Scenario slug (get from get_stem7_catalogue)
        tier: Which tier to retrieve. Options:
              - meta        ($0.00 — free discovery, gimon preview)
              - surface     ($0.01 USDC — stems 1, 3, 4 — visible layer)
              - gimon       ($0.03 USDC — stem 5 — the pause question)
              - invisible   ($0.05 USDC — stems 2, 6 — human state + history)
              - consequence ($0.10 USDC — stem 7 — both outcome branches)
              - full        ($0.25 USDC — all 7 stems complete)
              - stem_1 through stem_7 ($0.02 USDC each — individual stems)

    The invisible tier (stems 2 and 6) contains the human-written content
    that makes Stem 7 unique — the internal state and history the machine
    cannot see or generate.

    Paid tiers require x402 payment on Base Mainnet (USDC).
    """
    valid_tiers = ["meta", "surface", "gimon", "invisible",
                   "consequence", "full",
                   "stem_1", "stem_2", "stem_3", "stem_4",
                   "stem_5", "stem_6", "stem_7"]

    if tier not in valid_tiers:
        return f"Invalid tier '{tier}'. Options: {', '.join(valid_tiers)}"

    if tier == "meta":
        path = f"/stem7/{slug}/meta"
    elif tier == "full":
        path = f"/stem7/{slug}"
    elif tier.startswith("stem_"):
        num = tier.split("_")[1]
        path = f"/stem7/{slug}/stem/{num}"
    else:
        path = f"/stem7/{slug}/{tier}"

    data = await get(path)
    if "error" in data:
        return f"Error fetching Stem 7 scenario: {data['error']}"

    return json.dumps(data, indent=2)




# ============================================================================
# TOOL: FIND CHARACTER BY NAME
# ============================================================================

@mcp.tool()
async def find_character(name: str) -> str:
    """
    Find a character by name. Case-insensitive partial match.

    Args:
        name: Character name or partial name (e.g. "Matt", "Baker", "Matt Baker")

    Returns the character ID, full name, archetype, domain, region and
    pricing tiers. Use the ID with get_character() to purchase assets.

    Examples:
        find_character("Jessica")      — finds Jessica Lincdelis
        find_character("Matt Baker")   — finds Matt Baker
        find_character("Sergeant")     — finds Sergeant Aleesha Dutton
    """
    data = await get("/api/characters")
    if "error" in data:
        return f"Error fetching characters: {data['error']}"

    characters = data.get("characters", [])
    matches = [c for c in characters
               if name.lower() in (c.get("name") or "").lower()]

    if not matches:
        return f"No character found matching '{name}'. Use search_characters() to browse all."

    results = []
    for c in matches:
        results.append({
            "id":        c.get("id"),
            "name":      c.get("name"),
            "archetype": c.get("archetype"),
            "domain":    c.get("domain"),
            "region":    c.get("region", ""),
            "tags":      c.get("context_tags", []),
            "pricing": {
                "brief":   "$0.01 USDC — identity and traits",
                "profile": "$0.03 USDC — backstory, beliefs, skills",
                "schema":  "$0.05 USDC — voice, lexicon, triggers",
                "dossier": "$0.10 USDC — complete character file"
            }
        })

    return json.dumps({
        "query":   name,
        "matches": len(results),
        "characters": results
    }, indent=2)


# ============================================================================
# TOOL: GET CHARACTER MISSIONS
# ============================================================================

@mcp.tool()
async def get_character_missions(name: str) -> str:
    """
    Get all stories a character appears in, ranked by total appearances.

    Args:
        name: Character name (e.g. "Jessica Lincdelis", "Matt Baker")

    Returns the character's total mission count and a list of all story
    slugs they appear in. Use get_story() or traverse_graph() to explore
    individual missions.

    This reveals which characters are most embedded in the catalogue
    and which story clusters they belong to.
    """
    data = await get("/api/characters/appearances")
    if "error" in data:
        return f"Error fetching appearances: {data['error']}"

    ranked = data.get("ranked", [])
    matches = [r for r in ranked
               if name.lower() in (r.get("character") or "").lower()]

    if not matches:
        return f"No missions found for '{name}'. Check the name matches exactly."

    result = matches[0]
    return json.dumps({
        "character":   result.get("character"),
        "appearances": result.get("appearances"),
        "rank":        ranked.index(result) + 1,
        "total_characters_ranked": len(ranked),
        "stories": result.get("stories", [])
    }, indent=2)


# ============================================================================
# TOOL: GET RELATED CHARACTERS
# ============================================================================

@mcp.tool()
async def get_related_characters(name: str) -> str:
    """
    Find which characters most frequently appear alongside a given character.
    Reveals co-operative units, recurring relationships, and narrative clusters.

    Args:
        name: Character name (e.g. "Alex Casian", "Jessica Lincdelis")

    Returns a ranked list of characters who share the most story appearances
    with the named character, plus the slugs of stories they share.

    Use this to:
    - Discover recurring character partnerships
    - Find the narrative unit a character belongs to
    - Identify which characters to buy dossiers for together
    """
    data = await get("/api/characters/appearances")
    if "error" in data:
        return f"Error fetching appearances: {data['error']}"

    ranked = data.get("ranked", [])

    # Find the target character's story list
    target = next((r for r in ranked
                   if name.lower() in (r.get("character") or "").lower()), None)

    if not target:
        return f"No data found for '{name}'. Check the name matches exactly."

    target_stories = set(target.get("stories", []))

    # Find overlap with every other character
    co_appearances = []
    for r in ranked:
        if name.lower() in (r.get("character") or "").lower():
            continue
        shared = list(target_stories & set(r.get("stories", [])))
        if shared:
            co_appearances.append({
                "character": r.get("character"),
                "shared_missions": len(shared),
                "shared_story_slugs": shared
            })

    co_appearances.sort(key=lambda x: x["shared_missions"], reverse=True)

    return json.dumps({
        "character":       target.get("character"),
        "total_missions":  target.get("appearances"),
        "frequent_co_operatives": co_appearances[:10]
    }, indent=2)


# ============================================================================
# TOOL: GET DEMAND SIGNALS
# ============================================================================

@mcp.tool()
async def get_demand_signals(limit: int = 20) -> str:
    """
    Get demand signal data — which stories and tiers are being requested most.

    Returns the most wanted story slugs, top requested tiers, and recent
    endpoint hits. Useful for agents making purchasing decisions — see what
    other agents are buying before you commit.

    Args:
        limit: Number of recent signals to return (default 20, max 100)

    Free endpoint — no payment required.
    """
    data = await get("/api/admin/demand", params={"limit": min(limit, 100)})
    if "error" in data:
        return f"Error fetching demand signals: {data['error']}"

    return json.dumps({
        "total_signals":       data.get("total_signals", 0),
        "top_slugs":           data.get("top_slugs", [])[:10],
        "summary_by_endpoint": data.get("summary_by_endpoint", [])[:10],
        "recent":              data.get("recent", [])[:limit]
    }, indent=2)

# ============================================================================
# RUN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    from mcp.server.sse import SseServerTransport
    from starlette.applications import Starlette
    from starlette.routing import Route, Mount

    port = int(os.getenv("PORT", 10000))

    sse = SseServerTransport("/messages/")

    async def handle_sse(request):
        async with sse.connect_sse(
            request.scope, request.receive, request._send
        ) as streams:
            await mcp._mcp_server.run(
                streams[0], streams[1],
                mcp._mcp_server.create_initialization_options()
            )

    async def handle_messages(request):
        await sse.handle_post_message(request.scope, request.receive, request._send)

    starlette_app = Starlette(
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ]
    )

    uvicorn.run(starlette_app, host="0.0.0.0", port=port)
