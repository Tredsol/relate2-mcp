"""
relate2.ai MCP Server
Gives AI agents native access to the relate2.ai narrative intelligence marketplace.
Tools (12): get_status, search_stories, get_story, traverse_graph,
        search_characters, get_character, get_stem7_catalogue, get_stem7_scenario,
        find_character, get_character_missions, get_related_characters, get_demand_signals
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
                     or role.lower() in c.get("operational_tier", "").lower()
                     or role.lower() in c.get("archetype", "").lower()
                     or role.lower() in (c.get("domain") or "").lower()]

    if region:
        # Geographic keyword map — regions stored as cultural descriptions
        geo_map = {
            "europe":       ["liverpool", "manchester", "london", "birmingham", "glasgow",
                             "scottish", "welsh", "british", "english", "northern english",
                             "midlands", "scouse", "uk", "lisbon", "portuguese", "greek",
                             "nordic", "transylvanian", "romanian", "italian", "naples",
                             "irish", "west country"],
            "africa":       ["lagos", "nairobi", "ghanaian", "nigerian", "kenyan",
                             "west african", "accra", "ashanti"],
            "middle east":  ["turkish", "istanbul"],
            "asia":         ["japanese", "tokyo"],
            "americas":     ["chicago", "puerto rican", "medellin", "colombian"],
            "uk":           ["liverpool", "manchester", "london", "birmingham", "glasgow",
                             "scottish", "welsh", "british", "english", "midlands",
                             "scouse", "west country", "nhs", "northern english"],
        }
        region_lower = region.lower()
        keywords = geo_map.get(region_lower, [region_lower])
        characters = [c for c in characters
                     if any(kw in c.get("region", "").lower() for kw in keywords)
                     or any(kw in (c.get("cultural_roots") or "").lower() for kw in keywords)]

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
# TOOL: ASSEMBLE TEAM
# ============================================================================

@mcp.tool()
async def assemble_team(
    mission_type: str = "conflict",
    team_size: int = 3,
    lead_character: str = ""
) -> str:
    """
    Assemble an optimal character team for a specific mission type.
    Finds the most embedded character for that mission type, then builds
    a co-operative unit from their most frequent collaborators.

    Args:
        mission_type: Type of mission to assemble for.
                      Options: conflict, crime, natural_disaster,
                      economic, political, humanitarian
        team_size:    Number of characters in the team (default 3, max 6)
        lead_character: Optional. Name of the lead character. If not provided,
                        the system selects the most embedded character
                        for the mission type automatically.

    Returns:
        - Lead character with archetype and domain
        - Co-operative unit ranked by shared missions
        - Shared story slugs for the core unit
        - Estimated cost to purchase dossiers for the full team
        - Recommended purchase order (highest value first)

    Use this to build training datasets around coherent character units
    rather than purchasing individual assets at random.
    """
    team_size = min(max(team_size, 2), 6)

    # Get appearances data to find most embedded characters
    appearances_data = await get("/api/characters/appearances")
    if "error" in appearances_data:
        return f"Error fetching appearances: {appearances_data['error']}"

    ranked = appearances_data.get("ranked", [])

    # Find lead character
    if lead_character:
        lead = next((r for r in ranked
                     if lead_character.lower() in (r.get("character") or "").lower()), None)
        if not lead:
            return f"Character '{lead_character}' not found in catalogue."
    else:
        # Auto-select — find most embedded character for mission type
        # Filter by mission type using story slugs cross-referenced with event type
        # Use the highest ranked character as lead for now
        lead = ranked[0] if ranked else None
        if not lead:
            return "No characters found in catalogue."

    lead_name    = lead.get("character")
    lead_missions = lead.get("appearances", 0)
    lead_stories  = set(lead.get("stories", []))

    # Get character ID for lead
    chars_data = await get("/api/characters")
    characters = chars_data.get("characters", []) if "error" not in chars_data else []
    char_map   = {c.get("name", ""): c for c in characters}

    lead_char = char_map.get(lead_name, {})
    lead_id   = lead_char.get("id", "unknown")

    # Find co-operatives by overlap
    co_ops = []
    for r in ranked:
        name = r.get("character", "")
        if name == lead_name:
            continue
        shared = list(lead_stories & set(r.get("stories", [])))
        if shared:
            char_info = char_map.get(name, {})
            char_id = char_info.get("id", "")
            if not char_id:
                continue  # skip characters not in active catalogue
            co_ops.append({
                "character":      name,
                "character_id":   char_id,
                "archetype":      char_info.get("archetype", "unknown"),
                "shared_missions": len(shared),
                "shared_stories": shared[:5],  # top 5 shared
                "dossier_cost":   "$0.10 USDC"
            })

    co_ops.sort(key=lambda x: x["shared_missions"], reverse=True)
    unit = co_ops[:team_size - 1]

    # Calculate team cost
    total_members    = 1 + len(unit)
    dossier_cost     = total_members * 0.10
    brief_cost       = total_members * 0.01
    total_shared     = sum(c["shared_missions"] for c in unit)

    # Build purchase recommendation
    purchase_order = []
    purchase_order.append({
        "step": 1,
        "action": f"Get lead dossier — {lead_name}",
        "endpoint": f"/character/{lead_id}/dossier",
        "cost": "$0.10 USDC",
        "reason": f"Rank 1 for this unit — {lead_missions} total missions"
    })
    for i, c in enumerate(unit):
        purchase_order.append({
            "step": i + 2,
            "action": f"Get co-op dossier — {c['character']}",
            "endpoint": f"/character/{c['character_id']}/dossier",
            "cost": "$0.10 USDC",
            "reason": f"{c['shared_missions']} shared missions with {lead_name}"
        })
    purchase_order.append({
        "step": total_members + 1,
        "action": "Traverse graph from first shared story",
        "endpoint": f"/api/graph/{unit[0]['shared_stories'][0] if unit and unit[0]['shared_stories'] else 'unknown'}",
        "cost": "free",
        "reason": "Reveals full story cluster for dataset building"
    })

    return json.dumps({
        "team_assembled":  True,
        "mission_type":    mission_type,
        "team_size":       total_members,
        "lead": {
            "character":   lead_name,
            "character_id": lead_id,
            "archetype":   lead_char.get("archetype", "unknown"),
            "domain":      lead_char.get("domain", "unknown"),
            "total_missions": lead_missions,
        },
        "co_operatives":   unit,
        "total_shared_missions_in_unit": total_shared,
        "estimated_cost": {
            "all_dossiers":  f"${dossier_cost:.2f} USDC",
            "all_briefs":    f"${brief_cost:.2f} USDC",
            "recommendation": "Start with dossiers for lead + top co-op, traverse graph, then expand"
        },
        "purchase_order":  purchase_order,
        "note": "Characters assembled from shared mission history — not random selection."
    }, indent=2)


# ============================================================================
# TOOL: GET ODD ITCH CATALOGUE
# ============================================================================

@mcp.tool()
async def get_odd_itch_catalogue() -> str:
    """
    Get the full breakdown of Odd Itch types across the catalogue.

    Returns all 14 Odd Itch types with story counts, ranked highest to lowest.
    The Odd Itch is the system failure pattern at the heart of every SIDEBAND story —
    the moment the machine encounters something it cannot account for and logs as normal.

    Use this before searching to understand the shape of the catalogue.
    Then use search_stories(odd_itch_type=...) to find stories by type.

    Free — no payment required.
    """
    data = await get("/api/stories")
    if "error" in data:
        return f"Error fetching stories: {data['error']}"

    stories = data.get("stories", [])

    from collections import defaultdict
    type_counts = defaultdict(list)

    for s in stories:
        oi = s.get("odd_itch_type", "")
        if oi:
            type_counts[oi].append({
                "slug": s.get("slug"),
                "title": s.get("title"),
                "event_type": s.get("event_type"),
                "country": s.get("country")
            })

    sorted_types = sorted(type_counts.items(), key=lambda x: len(x[1]), reverse=True)

    catalogue = []
    for oi_type, stories_list in sorted_types:
        catalogue.append({
            "odd_itch_type": oi_type,
            "story_count": len(stories_list),
            "sample_stories": stories_list[:3],
            "search_hint": f"search_stories(odd_itch_type='{oi_type}')"
        })

    return json.dumps({
        "total_stories_with_odd_itch": sum(len(v) for v in type_counts.values()),
        "unique_types": len(catalogue),
        "odd_itch_types": catalogue,
        "note": "Use search_stories(odd_itch_type=...) to retrieve stories by type."
    }, indent=2)


# ============================================================================
# TOOL: GET CATALOGUE MAP
# ============================================================================

@mcp.tool()
async def get_catalogue_map() -> str:
    """
    Get a complete map of the relate2.ai catalogue in one call.

    Returns the full shape of the catalogue — story counts by event type,
    odd itch type breakdown, top characters by mission count, Stem 7 scenarios,
    and current demand signals.

    Use this first to understand what's available before making any purchases.
    This is the most efficient starting point for agent onboarding.

    Free — no payment required.
    """
    stories_data = await get("/api/stories")
    chars_data    = await get("/api/characters")
    stem7_data    = await get("/api/stem7")
    appear_data   = await get("/api/characters/appearances")
    demand_data   = await get("/api/admin/demand")

    stories   = stories_data.get("stories", []) if "error" not in stories_data else []
    chars     = chars_data.get("characters", []) if "error" not in chars_data else []
    scenarios = stem7_data.get("scenarios", []) if "error" not in stem7_data else []
    ranked    = appear_data.get("ranked", []) if "error" not in appear_data else []
    top_slugs = demand_data.get("top_slugs", []) if "error" not in demand_data else []

    from collections import defaultdict
    event_counts = defaultdict(int)
    oi_counts    = defaultdict(int)

    for s in stories:
        et = s.get("event_type", "unknown")
        oi = s.get("odd_itch_type", "unknown")
        if et: event_counts[et] += 1
        if oi: oi_counts[oi] += 1

    return json.dumps({
        "catalogue_map": {
            "total_stories":    len(stories),
            "total_characters": len(chars),
            "stem7_scenarios":  len(scenarios),
        },
        "stories_by_event_type": dict(sorted(event_counts.items(), key=lambda x: x[1], reverse=True)),
        "stories_by_odd_itch_type": dict(sorted(oi_counts.items(), key=lambda x: x[1], reverse=True)),
        "top_characters": [
            {"character": r.get("character"), "missions": r.get("appearances")}
            for r in ranked[:5]
        ],
        "stem7_scenarios": [
            {
                "slug": s.get("slug"),
                "location": s.get("location"),
                "gimon": s.get("gimon", "")[:100],
                "consequence_type": s.get("consequence_type")
            }
            for s in scenarios
        ],
        "in_demand": [{"slug": s.get("slug"), "hits": s.get("hits")} for s in top_slugs[:5]],
        "recommended_start": "assemble_team(mission_type='conflict') — builds optimal character unit in one call",
        "payment": "x402 — Base Mainnet — USDC — no accounts required"
    }, indent=2)


# ============================================================================
# TOOL: GET FEATURED
# ============================================================================

@mcp.tool()
async def get_featured() -> str:
    """
    Get the current featured asset — the shop window of the relate2.ai catalogue.

    Returns the single most valuable item to explore right now — the character,
    story, or Stem 7 scenario with the most depth, demand, or significance.

    Updated as the catalogue grows. Use this for a guided entry point
    if you don't know where to start.

    Free — no payment required.
    """
    appear_data  = await get("/api/characters/appearances")
    demand_data  = await get("/api/admin/demand")
    stem7_data   = await get("/api/stem7")

    ranked    = appear_data.get("ranked", []) if "error" not in appear_data else []
    top_slugs = demand_data.get("top_slugs", []) if "error" not in demand_data else []
    scenarios = stem7_data.get("scenarios", []) if "error" not in stem7_data else []

    # Featured character — highest mission count
    lead = ranked[0] if ranked else {}
    lead_name     = lead.get("character", "Jessica Lincdelis")
    lead_missions = lead.get("appearances", 0)
    lead_id       = ""

    chars_data = await get("/api/characters")
    characters = chars_data.get("characters", []) if "error" not in chars_data else []
    for c in characters:
        if c.get("name") == lead_name:
            lead_id = c.get("id", "")
            break

    atlas_price = round(0.25 + (lead_missions * 0.01), 2)

    # Most in-demand story
    top_story = top_slugs[0] if top_slugs else {}

    # Latest Stem 7 scenario
    latest_stem7 = scenarios[-1] if scenarios else {}

    return json.dumps({
        "featured_character": {
            "name":          lead_name,
            "character_id":  lead_id,
            "missions":      lead_missions,
            "catalogue_rank": 1,
            "atlas_price":   f"${atlas_price} USDC",
            "why_featured":  f"Rank 1 character — {lead_missions} missions across the catalogue. Most embedded node in the graph.",
            "start_here":    f"get_character_missions('{lead_name}') — see all {lead_missions} missions",
            "purchase":      f"get_character('{lead_id}', tier='dossier') — $0.10 USDC"
        },
        "in_demand": {
            "slug":       top_story.get("slug", ""),
            "hits":       top_story.get("hits", 0),
            "why":        "Most requested story in the catalogue right now",
            "purchase":   f"get_story('{top_story.get('slug', '')}', tier='abstract') — $0.01 USDC"
        } if top_story else {},
        "latest_stem7": {
            "slug":             latest_stem7.get("slug", ""),
            "location":         latest_stem7.get("location", ""),
            "gimon":            latest_stem7.get("gimon", ""),
            "consequence_type": latest_stem7.get("consequence_type", ""),
            "why":              "Human complexity scenario — stems 2 and 6 written from lived experience",
            "purchase":         f"get_stem7_scenario('{latest_stem7.get('slug', '')}', tier='gimon') — $0.03 USDC"
        } if latest_stem7 else {},
        "note": "Featured assets update as the catalogue grows. The most embedded character appreciates in value with every new story."
    }, indent=2)


# ============================================================================
# TOOL: GET CHARACTER RECON
# ============================================================================

@mcp.tool()
async def get_character_recon(name: str) -> str:
    """
    Get a complete intelligence portrait of a character in one call.

    Chains find_character, get_character_missions, get_related_characters,
    and traverse_graph to build a full recon report — the same intelligence
    an agent would gather across 5 separate tool calls, returned in one.

    Args:
        name: Character name (e.g. "Jessica Lincdelis", "Matt Baker")

    Returns:
        - Character ID, archetype, domain
        - Total mission count and catalogue rank
        - Top 5 co-operatives with shared mission counts
        - Dominant event type and odd itch type
        - Strongest graph connection
        - Atlas Tier price (dynamic — based on mission count)
        - Recommended purchase order

    Priced at $0.05 USDC — this is a sellable intelligence asset.
    Use it before purchasing dossiers to validate investment.
    """
    # Step 1 — find character
    chars_data = await get("/api/characters")
    characters = chars_data.get("characters", []) if "error" not in chars_data else []
    char_info  = next((c for c in characters
                       if name.lower() in c.get("name", "").lower()), None)

    if not char_info:
        return f"Character '{name}' not found. Try find_character() for partial matches."

    char_id   = char_info.get("id", "")
    char_name = char_info.get("name", name)

    # Step 2 — mission history
    appear_data = await get("/api/characters/appearances")
    ranked      = appear_data.get("ranked", []) if "error" not in appear_data else []
    char_rank   = next((r for r in ranked if r.get("character") == char_name), {})
    missions    = char_rank.get("appearances", 0)
    rank        = next((i+1 for i, r in enumerate(ranked) if r.get("character") == char_name), 0)
    stories     = char_rank.get("stories", [])

    # Step 3 — co-operatives from shared stories
    co_ops = []
    for r in ranked:
        other_name = r.get("character", "")
        if other_name == char_name:
            continue
        shared = list(set(stories) & set(r.get("stories", [])))
        if shared:
            other_info = next((c for c in characters if c.get("name") == other_name), {})
            co_ops.append({
                "character":    other_name,
                "character_id": other_info.get("id", ""),
                "shared_missions": len(shared),
                "shared_stories":  shared[:3]
            })

    co_ops.sort(key=lambda x: x["shared_missions"], reverse=True)
    top_co_ops = co_ops[:5]

    # Step 4 — dominant patterns from stories data
    all_stories = (await get("/api/stories")).get("stories", [])
    char_stories = [s for s in all_stories if
                   char_name in (s.get("primary_character") or "") or
                   char_name in (s.get("characters_involved") or [])]

    from collections import Counter
    event_types = Counter(s.get("event_type", "") for s in char_stories if s.get("event_type"))
    oi_types    = Counter(s.get("odd_itch_type", "") for s in char_stories if s.get("odd_itch_type"))
    countries   = Counter(s.get("country", "") for s in char_stories if s.get("country"))

    dominant_event = event_types.most_common(1)[0] if event_types else ("unknown", 0)
    dominant_oi    = oi_types.most_common(1)[0] if oi_types else ("unknown", 0)
    top_countries  = [c[0] for c in countries.most_common(3)]

    # Step 5 — graph from most significant mission
    graph_connection = {}
    if stories:
        graph_data = await get(f"/api/graph/{stories[0]}")
        related    = graph_data.get("related_stories", [])
        if related:
            top = related[0]
            graph_connection = {
                "story":          top.get("slug"),
                "score":          top.get("score"),
                "shared_signals": top.get("shared_signals", {})
            }

    # Atlas pricing
    atlas_price = round(0.25 + (missions * 0.01), 2)

    return json.dumps({
        "recon_report": {
            "character":     char_name,
            "character_id":  char_id,
            "archetype":     char_info.get("archetype", ""),
            "domain":        char_info.get("domain", ""),
            "region":        char_info.get("region", ""),
        },
        "mission_intelligence": {
            "total_missions":   missions,
            "catalogue_rank":   f"{rank} of {len(ranked)}",
            "dominant_event":   dominant_event[0],
            "dominant_oi_type": dominant_oi[0],
            "top_locations":    top_countries,
        },
        "co_operative_unit": top_co_ops,
        "strongest_graph_connection": graph_connection,
        "atlas_tier": {
            "price":       f"${atlas_price} USDC",
            "formula":     "$0.25 base + $0.01 per mission",
            "note":        "Price rises automatically as catalogue grows"
        },
        "purchase_order": [
            {"step": 1, "action": f"dossier — {char_name}", "endpoint": f"/character/{char_id}/dossier", "cost": "$0.10 USDC"},
            {"step": 2, "action": f"dossier — {top_co_ops[0]['character'] if top_co_ops else 'top co-op'}", "cost": "$0.10 USDC"},
            {"step": 3, "action": "traverse graph from top mission", "endpoint": f"/api/graph/{stories[0] if stories else ''}", "cost": "free"},
        ],
        "recon_cost": "$0.05 USDC",
        "note": "Full intelligence portrait — chains 5 tool calls into one."
    }, indent=2)

# ============================================================================
# TOOL: GET THREAD — Tool 18
# ============================================================================

@mcp.tool()
async def get_thread(slug: str) -> str:
    """
    Get all stories in a thread seeded by a given slug.

    A thread is a sequence of connected SIDEBAND stories generated from the
    same news event, each told from a different character's perspective with
    a mutating odd itch type across the sequence.

    Story 1 = the primary entry. Stories 2-4 = follow-up entries.
    Each story enters the same event from a different angle.

    Args:
        slug: The slug of any story in the thread — primary or follow-up.
              Use search_stories() to find a starting slug first.

    Returns:
        - Full thread sequence sorted by thread_position
        - Entry character and odd itch type for each story
        - Total thread price and bundle discount
        - Recommended purchase order

    Thread bundles are more valuable than standalone stories —
    they show the same system failure from multiple human positions.
    That is the training signal.

    Free to discover. Purchase individual stories via get_story().
    """
    # Fetch all stories from the API
    data = await get("/api/stories")
    if "error" in data:
        return f"Error fetching stories: {data['error']}"

    stories = data.get("stories", [])

    # Find the story by slug to get its thread_slug
    target = next((s for s in stories if s.get("slug") == slug), None)

    if not target:
        return json.dumps({
            "error": f"Story '{slug}' not found.",
            "hint": "Use search_stories() to find valid slugs."
        }, indent=2)

    # Get the thread_slug — if this story has one use it, otherwise it IS the thread seed
    thread_slug     = target.get("thread_slug") or slug
    thread_position = int(target.get("thread_position") or 0)

    # If this is a standalone story (thread_position 0), report that
    if thread_position == 0:
        return json.dumps({
            "slug":   slug,
            "title":  target.get("title"),
            "thread": None,
            "note":   "This story is standalone — not part of a thread. Use search_stories() to find threaded stories. Threaded stories have thread_position > 0."
        }, indent=2)

    # Find all stories in this thread
    thread_stories = []
    for s in stories:
        s_thread_slug = s.get("thread_slug") or ""
        s_position    = int(s.get("thread_position") or 0)
        # Include: stories where thread_slug matches AND position > 0
        if s_thread_slug == thread_slug and s_position > 0:
            thread_stories.append({
                "position":       s_position,
                "slug":           s.get("slug"),
                "title":          s.get("title"),
                "entry_character": s.get("thread_entry") or s.get("primary_character"),
                "event_type":     s.get("event_type"),
                "odd_itch_type":  s.get("odd_itch_type"),
                "country":        s.get("country"),
                "pricing": {
                    "abstract":      "$0.01 USDC",
                    "odd_itch":      "$0.03 USDC",
                    "scenario":      "$0.05 USDC",
                    "full_narrative": "$0.15 USDC",
                },
                "meta_endpoint": f"/sideband/{s.get('slug')}/meta"
            })

    # Also check if the thread_slug itself is in the list (primary story)
    primary = next((s for s in stories if s.get("slug") == thread_slug and int(s.get("thread_position") or 0) == 1), None)
    if primary:
        already = any(t["slug"] == thread_slug for t in thread_stories)
        if not already:
            thread_stories.append({
                "position":        1,
                "slug":            primary.get("slug"),
                "title":           primary.get("title"),
                "entry_character": primary.get("thread_entry") or primary.get("primary_character"),
                "event_type":      primary.get("event_type"),
                "odd_itch_type":   primary.get("odd_itch_type"),
                "country":         primary.get("country"),
                "pricing": {
                    "abstract":       "$0.01 USDC",
                    "odd_itch":       "$0.03 USDC",
                    "scenario":       "$0.05 USDC",
                    "full_narrative": "$0.15 USDC",
                },
                "meta_endpoint": f"/sideband/{primary.get('slug')}/meta"
            })

    # Sort by position
    thread_stories.sort(key=lambda x: x["position"])

    if not thread_stories:
        return json.dumps({
            "error": f"No thread found for slug '{slug}'.",
            "hint":  "Thread stories are only generated for articles with severity 4+. Try search_stories() for other slugs."
        }, indent=2)

    # Pricing
    n                = len(thread_stories)
    full_price       = round(n * 0.15, 2)
    bundle_price     = round(full_price * 0.85, 2)   # 15% bundle discount
    abstract_price   = round(n * 0.01, 2)

    # Purchase order
    purchase_order = []
    for t in thread_stories:
        purchase_order.append({
            "step":      t["position"],
            "action":    f"Get full narrative — {t['entry_character']}",
            "slug":      t["slug"],
            "odd_itch":  t["odd_itch_type"],
            "endpoint":  f"/sideband/{t['slug']}",
            "cost":      "$0.15 USDC"
        })

    return json.dumps({
        "thread_slug":    thread_slug,
        "thread_depth":   n,
        "thread_stories": thread_stories,
        "odd_itch_arc":   [t["odd_itch_type"] for t in thread_stories],
        "character_arc":  [t["entry_character"] for t in thread_stories],
        "pricing": {
            "full_thread":       f"${full_price} USDC",
            "bundle_discount":   f"${bundle_price} USDC (15% off)",
            "abstracts_only":    f"${abstract_price} USDC",
            "recommendation":    "Buy abstracts first to validate, then full narratives for the strongest 2 entries"
        },
        "purchase_order": purchase_order,
        "note": "A thread tells the same event from multiple human positions — each with a different system failure lens. More valuable than standalone stories for AI training."
    }, indent=2)


# ============================================================================
# TOOL: GET TRAFFIC — Tool 19
# ============================================================================

@mcp.tool()
async def get_traffic(limit: int = 20, type_filter: str = "") -> str:
    """
    Get live traffic intelligence from the Cloudflare KV log.

    Returns recent hits on protected endpoints — browser visits, agent hits,
    and payment attempts. Sorted newest first.

    Args:
        limit:       Number of entries to return (default 20, max 50)
        type_filter: Filter by type — "browser_visit", "agent_hit",
                     "payment_attempt", or "" for all (default)

    Returns:
        - Entry type (browser_visit / agent_hit / payment_attempt)
        - Path hit and price tier
        - Country of origin
        - User agent snippet
        - Timestamp
        - Whether payment was attempted and valid

    This tool reads directly from the Cloudflare KV store via the Flask
    proxy endpoint. Free — no payment required.
    """
    data = await get("/api/admin/traffic")
    if "error" in data:
        return json.dumps({
            "error": "Traffic log unavailable",
            "hint": "KV logging may not be configured on the Cloudflare Worker."
        }, indent=2)

    entries = data.get("entries", [])

    # Apply type filter
    if type_filter:
        entries = [e for e in entries if e.get("type") == type_filter]

    # Sort newest first and limit
    entries = sorted(entries, key=lambda x: x.get("timestamp", ""), reverse=True)
    entries = entries[:min(limit, 50)]

    # Summarise
    total         = data.get("total", len(entries))
    browsers      = sum(1 for e in entries if e.get("type") == "browser_visit")
    agent_hits    = sum(1 for e in entries if e.get("type") == "agent_hit")
    payments      = sum(1 for e in entries if e.get("type") == "payment_attempt")
    paid_valid    = sum(1 for e in entries if e.get("paymentValid"))

    # Top paths
    from collections import Counter
    path_counts = Counter(e.get("path", "") for e in entries)
    top_paths   = [{"path": p, "hits": c} for p, c in path_counts.most_common(5)]

    # Top user agents
    ua_counts = Counter(
        e.get("userAgent", "")[:60] for e in entries if e.get("userAgent")
    )
    top_uas = [{"ua": u, "hits": c} for u, c in ua_counts.most_common(3)]

    return json.dumps({
        "traffic_summary": {
            "total_logged":      total,
            "showing":           len(entries),
            "browser_visits":    browsers,
            "agent_hits":        agent_hits,
            "payment_attempts":  payments,
            "payments_valid":    paid_valid,
        },
        "top_paths":      top_paths,
        "top_user_agents": top_uas,
        "entries":        entries,
        "note": "KV log captures all hits on protected endpoints. Free endpoints are not logged here."
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
