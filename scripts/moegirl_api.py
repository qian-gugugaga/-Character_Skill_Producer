#!/usr/bin/env python3
"""Fetch public Moegirlpedia entries through the MediaWiki API."""

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

API_URL = "https://zh.moegirl.org.cn/api.php"
PAGE_BASE_URL = "https://zh.moegirl.org.cn/"
USER_AGENT = "CharacterSkillProducer/1.0 (+https://github.com/qian-gugugaga/Character_Skill_Producer)"


def build_page_url(title):
    return PAGE_BASE_URL + urllib.parse.quote(title.replace(" ", "_"))


def request_json(params, timeout):
    url = API_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def fallback_error(query, error, message, attempted_modes):
    return {
        "ok": False,
        "source": "moegirl_mediawiki_api",
        "query": query,
        "error": error,
        "message": message,
        "attempted_modes": attempted_modes,
        "fallbacks": [
            "retry with --search to find candidate page titles",
            "retry with --full or --wikitext if extracts are incomplete",
            "use WebSearch/WebFetch only as a fallback and record Moegirl API failure",
            "cross-check with Wikipedia, Fandom Wiki, Bangumi, AniDB, or official sources",
        ],
    }


def normalize_query_response(data, query, mode):
    query_data = data.get("query", {})
    pages = query_data.get("pages", {})
    if not pages:
        return None

    page = next(iter(pages.values()))
    if page.get("missing") is not None or str(page.get("pageid", "")) == "-1":
        return None

    resolved_title = page.get("title", query)
    extract = page.get("extract", "") or ""
    warnings = []
    if not extract.strip():
        warnings.append("empty extract; try --search, --full, or --wikitext")

    normalized = query_data.get("normalized", [])
    redirects = query_data.get("redirects", [])

    return {
        "ok": bool(extract.strip()),
        "source": "moegirl_mediawiki_api",
        "mode": mode,
        "query": query,
        "query_title": query,
        "resolved_title": resolved_title,
        "pageid": page.get("pageid"),
        "page_url": build_page_url(resolved_title),
        "extract": extract,
        "extract_chars": len(extract),
        "candidates": [],
        "normalized": normalized,
        "redirected": redirects,
        "warnings": warnings,
    }


def query_extract(title, intro, timeout):
    params = {
        "action": "query",
        "prop": "extracts",
        "titles": title,
        "format": "json",
        "explaintext": "1",
        "redirects": "1",
        "origin": "*",
    }
    if intro:
        params["exintro"] = "1"

    data = request_json(params, timeout)
    result = normalize_query_response(data, title, "intro" if intro else "full")
    return result, data


def search_titles(query, timeout):
    params = {
        "action": "opensearch",
        "search": query,
        "limit": "10",
        "namespace": "0",
        "format": "json",
        "origin": "*",
    }
    data = request_json(params, timeout)
    titles = data[1] if len(data) > 1 else []
    descriptions = data[2] if len(data) > 2 else []
    urls = data[3] if len(data) > 3 else []
    candidates = []
    for index, title in enumerate(titles):
        candidates.append(
            {
                "title": title,
                "description": descriptions[index] if index < len(descriptions) else "",
                "url": urls[index] if index < len(urls) else build_page_url(title),
            }
        )

    return {
        "ok": bool(candidates),
        "source": "moegirl_mediawiki_api",
        "mode": "search",
        "query": query,
        "query_title": query,
        "resolved_title": candidates[0]["title"] if candidates else None,
        "pageid": None,
        "page_url": candidates[0]["url"] if candidates else None,
        "extract": candidates[0]["description"] if candidates else "",
        "extract_chars": len(candidates[0]["description"]) if candidates else 0,
        "candidates": candidates,
        "error": None if candidates else "no_candidates",
        "message": None if candidates else "No search candidates returned",
        "warnings": [] if candidates else ["no search candidates returned"],
        "fallbacks": [] if candidates else [
            "retry with the Chinese title, Japanese title, alias, or series name plus character name",
            "use --intro if the exact page title is known",
            "cross-check with Wikipedia, Fandom Wiki, Bangumi, AniDB, or official sources",
        ],
    }, data


def query_wikitext(title, timeout):
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
    data = request_json(params, timeout)
    if "error" in data:
        error = data["error"]
        return fallback_error(title, error.get("code", "api_error"), error.get("info", "MediaWiki API error"), ["wikitext"]), data

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
        "ok": bool(content.strip()),
        "source": "moegirl_mediawiki_api",
        "mode": "wikitext",
        "query": title,
        "query_title": title,
        "resolved_title": resolved_title,
        "pageid": page.get("pageid"),
        "page_url": build_page_url(resolved_title),
        "extract": content,
        "extract_chars": len(content),
        "candidates": [],
        "warnings": [] if content.strip() else ["empty wikitext"],
    }, data


def auto_query(query, timeout):
    attempted = []

    attempted.append("intro")
    intro_result, _ = query_extract(query, True, timeout)
    if intro_result and intro_result.get("ok"):
        return intro_result

    attempted.append("search")
    search_result, _ = search_titles(query, timeout)
    if search_result.get("ok"):
        first_title = search_result["candidates"][0]["title"]
        attempted.append("intro:first_search_candidate")
        candidate_result, _ = query_extract(first_title, True, timeout)
        if candidate_result and candidate_result.get("ok"):
            candidate_result["candidates"] = search_result["candidates"]
            candidate_result["attempted_modes"] = attempted
            return candidate_result
        search_result["attempted_modes"] = attempted
        return search_result

    return fallback_error(query, "missing_page", "No extract or search candidates returned", attempted)


def parse_args():
    parser = argparse.ArgumentParser(description="Fetch Moegirlpedia entries through MediaWiki API")
    parser.add_argument("query", help="Moegirlpedia page title, character name, alias, or search query")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--intro", action="store_true", help="fetch intro extract for a page title")
    mode.add_argument("--full", action="store_true", help="fetch full plaintext extract for a page title")
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

    try:
        raw = None
        if args.search:
            attempted_modes.append("search")
            result, raw = search_titles(args.query, args.timeout)
        elif args.full:
            attempted_modes.append("full")
            result, raw = query_extract(args.query, False, args.timeout)
            if result is None:
                result = fallback_error(args.query, "missing_page", "Page title not found", attempted_modes)
        elif args.wikitext:
            attempted_modes.append("wikitext")
            result, raw = query_wikitext(args.query, args.timeout)
            if result is None:
                result = fallback_error(args.query, "missing_page", "Page title not found", attempted_modes)
        elif args.intro:
            attempted_modes.append("intro")
            result, raw = query_extract(args.query, True, args.timeout)
            if result is None or not result.get("ok"):
                attempted_modes.append("search")
                search_result, search_raw = search_titles(args.query, args.timeout)
                raw = {"extract_response": raw, "search_response": search_raw}
                if search_result.get("ok"):
                    search_result["attempted_modes"] = attempted_modes
                    result = search_result
                else:
                    result = fallback_error(args.query, "missing_page", "Page title not found and search returned no candidates", attempted_modes)
        else:
            result = auto_query(args.query, args.timeout)

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
