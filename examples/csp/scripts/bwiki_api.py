#!/usr/bin/env python3
"""Fetch BWIKI (wiki.biligame.com) entries through the MediaWiki API.

BWIKI hosts per-game wikis.  Each game has its own sub-site:
    https://wiki.biligame.com/{game}/api.php

NOTE: BWIKI does NOT support the TextExtracts extension, so extract-style
queries (intro/full) fall back to fetching wikitext and parsing the
infobox |介绍= field.
"""

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

USER_AGENT = "CharacterSkillProducer/1.0 (+https://github.com/qian-gugugaga/Character_Skill_Producer)"

GAME_SLUG_MAP = {
    "原神": "ys",
    "Genshin Impact": "ys",
    "Genshin": "ys",
    "崩坏：星穹铁道": "sr",
    "崩坏星穹铁道": "sr",
    "星穹铁道": "sr",
    "Honkai: Star Rail": "sr",
    "Honkai Star Rail": "sr",
    "Star Rail": "sr",
    "明日方舟": "arknights",
    "Arknights": "arknights",
    "明日方舟：终末地": "arknightsendfield",
    "Arknights: Endfield": "arknightsendfield",
    "蔚蓝档案": "ba",
    "Blue Archive": "ba",
    "碧蓝航线": "blhx",
    "Azur Lane": "blhx",
    "崩坏3": "bh3",
    "崩坏3rd": "bh3",
    "Honkai Impact 3rd": "bh3",
    "FGO": "fgo",
    "Fate/Grand Order": "fgo",
    "少女前线": "gf",
    "Girls Frontline": "gf",
    "少女前线2：追放": "gf2",
    "尘白禁区": "snowbreak",
    "鸣潮": "wutheringwaves",
    "Wuthering Waves": "wutheringwaves",
}


def build_api_url(game):
    return f"https://wiki.biligame.com/{game}/api.php"


def build_page_url(game, title):
    return f"https://wiki.biligame.com/{game}/" + urllib.parse.quote(title.replace(" ", "_"))


def request_json(url, params, timeout, retries=2):
    full_url = url + "?" + urllib.parse.urlencode(params)
    last_err = None
    for attempt in range(retries + 1):
        if attempt > 0:
            time.sleep(1.5 * attempt)
        req = urllib.request.Request(full_url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            last_err = exc
            if exc.code in (429, 567) and attempt < retries:
                continue
            raise
    raise last_err


def resolve_game_slug(game):
    """Resolve a game name/slug to a BWIKI URL slug."""
    if not game:
        return None
    # Direct slug match (e.g. user passed "sr" or "arknights")
    if game.lower() in GAME_SLUG_MAP.values():
        return game.lower()
    # Name lookup
    for name, slug in GAME_SLUG_MAP.items():
        if name.lower() in game.lower() or game.lower() in name.lower():
            return slug
    return game.lower()


def fallback_error(query, error, message, attempted_modes):
    return {
        "ok": False,
        "source": "bwiki_mediawiki_api",
        "query": query,
        "error": error,
        "message": message,
        "attempted_modes": attempted_modes,
        "fallbacks": [
            "retry with --search to find candidate page titles",
            "retry with --wikitext if extracts are incomplete",
            "verify the --game slug is correct for this BWIKI sub-site",
            "cross-check with Moegirl Wiki, Wikipedia, or official sources",
        ],
    }


# ---------------------------------------------------------------------------
# Search (opensearch)
# ---------------------------------------------------------------------------

def search_titles(query, game, timeout):
    api_url = build_api_url(game)
    params = {
        "action": "opensearch",
        "search": query,
        "limit": "10",
        "namespace": "0",
        "format": "json",
        "origin": "*",
    }
    data = request_json(api_url, params, timeout)
    titles = data[1] if len(data) > 1 else []
    descriptions = data[2] if len(data) > 2 else []
    urls = data[3] if len(data) > 3 else []
    candidates = []
    for index, title in enumerate(titles):
        candidates.append({
            "title": title,
            "description": descriptions[index] if index < len(descriptions) else "",
            "url": urls[index] if index < len(urls) else build_page_url(game, title),
        })

    return {
        "ok": bool(candidates),
        "source": "bwiki_mediawiki_api",
        "mode": "search",
        "query": query,
        "query_title": query,
        "resolved_title": candidates[0]["title"] if candidates else None,
        "pageid": None,
        "page_url": candidates[0]["url"] if candidates else None,
        "extract": candidates[0]["description"] if candidates else "",
        "extract_chars": len(candidates[0]["description"]) if candidates else 0,
        "candidates": candidates,
        "game": game,
        "error": None if candidates else "no_candidates",
        "message": None if candidates else "No search candidates returned",
        "warnings": [] if candidates else ["no search candidates returned"],
        "fallbacks": [] if candidates else [
            "retry with the Chinese title, Japanese title, alias, or series name plus character name",
            "verify the --game slug matches the correct BWIKI sub-site",
            "cross-check with Moegirl Wiki, Wikipedia, or official sources",
        ],
    }, data


# ---------------------------------------------------------------------------
# Wikitext fetch + intro extraction
# ---------------------------------------------------------------------------

def fetch_wikitext(title, game, timeout):
    """Fetch raw wikitext via revisions API.  Returns (page_dict, raw_data) or (None, raw_data)."""
    api_url = build_api_url(game)
    params = {
        "action": "query",
        "prop": "revisions",
        "titles": title,
        "rvprop": "content",
        "rvslots": "main",
        "format": "json",
        "redirects": "1",
        "origin": "*",
    }
    data = request_json(api_url, params, timeout)
    if "error" in data:
        return None, data

    query_data = data.get("query", {})
    pages = query_data.get("pages", {})
    if not pages:
        return None, data

    page = next(iter(pages.values()))
    if page.get("missing") is not None or str(page.get("pageid", "")) == "-1":
        return None, data

    resolved_title = page.get("title", title)
    revisions = page.get("revisions", [])
    content = ""
    if revisions:
        slots = revisions[0].get("slots", {})
        main_slot = slots.get("main", {})
        content = main_slot.get("*", "") or main_slot.get("content", "") or ""

    return {
        "resolved_title": resolved_title,
        "pageid": page.get("pageid"),
        "content": content,
    }, data


def extract_intro_from_wikitext(wikitext):
    """Extract a character introduction from BWIKI wikitext.

    Strategy:
    1. Look for |介绍= or similar fields in infobox templates.
    2. Fallback: extract the first non-template paragraph after the first {{ }} block.
    """
    if not wikitext:
        return ""

    # Strategy 1: look for |介绍= or similar fields in infobox templates
    # Fields are tried in order of preference
    for field in ("介绍", "介绍2", "角色介绍", "描述", "临床诊断分析", "晋升记录"):
        pattern = r"\|" + field + r"\s*=\s*(.*?)(?=\n\s*\||\n\s*\}\})"
        match = re.search(pattern, wikitext, re.DOTALL)
        if match:
            intro = _clean_wikitext(match.group(1))
            if intro:
                return intro

    # Strategy 2: extract first non-template paragraph after the first {{ }} block
    closing = re.search(r"\n\}\}\s*\n", wikitext)
    if closing:
        after = wikitext[closing.end():]
        # Collect lines until we hit another template or end
        collected = []
        for line in after.split("\n"):
            stripped = line.strip()
            if not stripped:
                if collected:
                    break
                continue
            if stripped.startswith("{{") or stripped.startswith("{|"):
                if collected:
                    break
                continue
            if stripped.startswith("|"):
                if collected:
                    break
                continue
            collected.append(stripped)
        if collected:
            intro = _clean_wikitext(" ".join(collected))
            if intro and len(intro) > 10:
                return intro
    return ""


def _clean_wikitext(text):
    """Strip wiki markup from text."""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\{\{[^}]*\}\}", "", text)
    text = re.sub(r"\[\[([^\]|]*\|)?([^\]]*)\]\]", r"\2", text)
    text = re.sub(r"<ref[^>]*>.*?</ref>", "", text, flags=re.DOTALL)
    text = re.sub(r"<ref[^/]*/?>", "", text)
    return text.strip()


def query_extract(title, game, timeout):
    """Fetch intro extract by getting wikitext and parsing infobox |介绍= field."""
    page, raw = fetch_wikitext(title, game, timeout)
    if page is None:
        return None, raw

    wikitext = page["content"]
    intro = extract_intro_from_wikitext(wikitext)
    warnings = []
    if not intro:
        warnings.append("empty intro from wikitext; |介绍= field not found; try --wikitext for full content")

    return {
        "ok": bool(intro),
        "source": "bwiki_mediawiki_api",
        "mode": "intro",
        "query": title,
        "query_title": title,
        "resolved_title": page["resolved_title"],
        "pageid": page["pageid"],
        "page_url": build_page_url(game, page["resolved_title"]),
        "extract": intro,
        "extract_chars": len(intro),
        "candidates": [],
        "game": game,
        "warnings": warnings,
    }, raw


def query_full(title, game, timeout):
    """Fetch full wikitext content."""
    page, raw = fetch_wikitext(title, game, timeout)
    if page is None:
        return None, raw

    wikitext = page["content"]
    warnings = []
    if not wikitext.strip():
        warnings.append("empty wikitext")

    return {
        "ok": bool(wikitext.strip()),
        "source": "bwiki_mediawiki_api",
        "mode": "full",
        "query": title,
        "query_title": title,
        "resolved_title": page["resolved_title"],
        "pageid": page["pageid"],
        "page_url": build_page_url(game, page["resolved_title"]),
        "extract": wikitext,
        "extract_chars": len(wikitext),
        "candidates": [],
        "game": game,
        "warnings": warnings,
    }, raw


def query_wikitext(title, game, timeout):
    """Fetch raw wikitext through revisions API."""
    page, raw = fetch_wikitext(title, game, timeout)
    if page is None:
        error = raw.get("error", {}) if isinstance(raw, dict) else {}
        return fallback_error(
            title,
            error.get("code", "api_error"),
            error.get("info", "MediaWiki API error"),
            ["wikitext"],
        ), raw

    wikitext = page["content"]
    return {
        "ok": bool(wikitext.strip()),
        "source": "bwiki_mediawiki_api",
        "mode": "wikitext",
        "query": title,
        "query_title": title,
        "resolved_title": page["resolved_title"],
        "pageid": page["pageid"],
        "page_url": build_page_url(game, page["resolved_title"]),
        "extract": wikitext,
        "extract_chars": len(wikitext),
        "candidates": [],
        "game": game,
        "warnings": [] if wikitext.strip() else ["empty wikitext"],
    }, raw


# ---------------------------------------------------------------------------
# Auto query
# ---------------------------------------------------------------------------

def auto_query(query, game, timeout):
    attempted = []

    # Try search first to find the right page title
    attempted.append("search")
    search_result, _ = search_titles(query, game, timeout)
    if not search_result.get("ok"):
        return fallback_error(query, "missing_page", "No search candidates returned", attempted)

    first_title = search_result["candidates"][0]["title"]

    # Try intro on the first search result
    attempted.append("intro:first_search_candidate")
    intro_result, _ = query_extract(first_title, game, timeout)
    if intro_result and intro_result.get("ok"):
        intro_result["candidates"] = search_result["candidates"]
        intro_result["attempted_modes"] = attempted
        return intro_result

    # Fallback: return search result with wikitext extract
    attempted.append("wikitext:first_search_candidate")
    wikitext_result, _ = query_wikitext(first_title, game, timeout)
    if wikitext_result and wikitext_result.get("ok"):
        wikitext_result["candidates"] = search_result["candidates"]
        wikitext_result["attempted_modes"] = attempted
        return wikitext_result

    # Last resort: return search candidates
    search_result["attempted_modes"] = attempted
    return search_result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(description="Fetch BWIKI entries through MediaWiki API")
    parser.add_argument("query", help="page title, character name, alias, or search query")
    parser.add_argument("--game", default="", help="BWIKI game slug (e.g. sr, arknights, ba) or game name")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--intro", action="store_true", help="fetch intro extract from infobox |介绍= field")
    mode.add_argument("--full", action="store_true", help="fetch full wikitext content")
    mode.add_argument("--search", action="store_true", help="search candidate page titles")
    mode.add_argument("--wikitext", action="store_true", help="fetch raw wikitext through revisions API")
    parser.add_argument("--raw", action="store_true", help="include raw API response")
    parser.add_argument("--timeout", type=int, default=20, help="request timeout in seconds")
    return parser.parse_args()


def emit_json(payload):
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    sys.stdout.buffer.write(text.encode("utf-8"))


def main():
    args = parse_args()
    attempted_modes = []

    game = resolve_game_slug(args.game)
    if not game:
        result = fallback_error(args.query, "missing_game", "No --game specified and could not infer from query", [])
        emit_json(result)
        return 1

    try:
        raw = None
        if args.search:
            attempted_modes.append("search")
            result, raw = search_titles(args.query, game, args.timeout)
        elif args.full:
            attempted_modes.append("full")
            result, raw = query_full(args.query, game, args.timeout)
            if result is None:
                result = fallback_error(args.query, "missing_page", "Page title not found", attempted_modes)
        elif args.wikitext:
            attempted_modes.append("wikitext")
            result, raw = query_wikitext(args.query, game, args.timeout)
            if isinstance(result, dict) and result.get("error"):
                pass  # already a fallback_error
            elif result is None:
                result = fallback_error(args.query, "missing_page", "Page title not found", attempted_modes)
        elif args.intro:
            attempted_modes.append("intro")
            result, raw = query_extract(args.query, game, args.timeout)
            if result is None or not result.get("ok"):
                attempted_modes.append("search")
                search_result, search_raw = search_titles(args.query, game, args.timeout)
                raw = {"extract_response": raw, "search_response": search_raw}
                if search_result.get("ok"):
                    first_title = search_result["candidates"][0]["title"]
                    attempted_modes.append("intro:first_search_candidate")
                    intro_result, intro_raw = query_extract(first_title, game, args.timeout)
                    if intro_result and intro_result.get("ok"):
                        intro_result["candidates"] = search_result["candidates"]
                        intro_result["attempted_modes"] = attempted_modes
                        result = intro_result
                    else:
                        search_result["attempted_modes"] = attempted_modes
                        result = search_result
                else:
                    result = fallback_error(args.query, "missing_page", "Page title not found and search returned no candidates", attempted_modes)
        else:
            result = auto_query(args.query, game, args.timeout)

        if args.raw:
            result["raw"] = raw

        emit_json(result)
        return 0 if result.get("ok") else 1
    except urllib.error.HTTPError as exc:
        result = fallback_error(args.query, "http_error", f"HTTP {exc.code}: {exc.reason}", attempted_modes)
    except urllib.error.URLError as exc:
        result = fallback_error(args.query, "url_error", str(exc.reason), attempted_modes)
    except TimeoutError as exc:
        result = fallback_error(args.query, "timeout", str(exc), attempted_modes)
    except json.JSONDecodeError as exc:
        result = fallback_error(args.query, "json_decode_error", str(exc), attempted_modes)

    emit_json(result)
    return 1


if __name__ == "__main__":
    sys.exit(main())
