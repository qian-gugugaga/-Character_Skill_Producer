#!/usr/bin/env python3
"""Unified local source discovery entrypoint for CSP."""

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

from source_registry import is_cross_media_work, is_excluded_url, source_hints_for_work, source_tier

ROOT = Path(__file__).resolve().parent
TODAY = date.today().isoformat()

# BWIKI game slug mapping — mirrors bwiki_api.py GAME_SLUG_MAP
BWIKI_GAME_SLUGS = {
    "原神": "ys", "Genshin": "ys",
    "星穹铁道": "sr", "Star Rail": "sr",
    "明日方舟": "arknights", "Arknights": "arknights",
    "蔚蓝档案": "ba", "Blue Archive": "ba",
    "碧蓝航线": "blhx", "Azur Lane": "blhx",
    "崩坏3": "bh3", "Honkai Impact": "bh3",
    "鸣潮": "wutheringwaves", "Wuthering Waves": "wutheringwaves",
}


def sha256_text(text):
    if not text:
        return None
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def run_python_script(script, args, timeout):
    cmd = [sys.executable, str(ROOT / script), *args, "--timeout", str(timeout)]
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=timeout + 5)
        stdout = proc.stdout.decode("utf-8", errors="replace") if proc.stdout else ""
        stderr = proc.stderr.decode("utf-8", errors="replace") if proc.stderr else ""
        payload = json.loads(stdout) if stdout.strip() else {}
        payload["retrieved_by"] = " ".join(cmd)
        payload["command_status"] = proc.returncode
        if stderr.strip():
            payload.setdefault("warnings", []).append(stderr.strip())
        return payload
    except subprocess.TimeoutExpired as exc:
        return {
            "ok": False,
            "source": script,
            "status": "failed",
            "error": "timeout",
            "message": str(exc),
            "retrieved_by": " ".join(cmd),
        }
    except json.JSONDecodeError as exc:
        return {
            "ok": False,
            "source": script,
            "status": "failed",
            "error": "json_decode_error",
            "message": str(exc),
            "retrieved_by": " ".join(cmd),
        }


def normalize_moegirl(raw, query, work):
    url = raw.get("page_url") or raw.get("url")
    excluded = is_excluded_url(url)
    extract = raw.get("extract", "") or ""
    status = "ok" if raw.get("ok") and not excluded else "failed"
    return {
        "id": f"moegirl-{raw.get('resolved_title') or query}".replace(" ", "-"),
        "source": "moegirl",
        "title": raw.get("resolved_title"),
        "resolved_title": raw.get("resolved_title"),
        "url": url,
        "query": query,
        "work": work,
        "source_tier": "excluded" if excluded else source_tier("moegirl"),
        "officiality": "excluded" if excluded else "secondary",
        "media_type": "wiki",
        "language": "zh",
        "retrieved_at": TODAY,
        "status": status,
        "warnings": raw.get("warnings", []),
        "attempted_modes": raw.get("attempted_modes") or [raw.get("mode")],
        "retrieved_by": raw.get("retrieved_by"),
        "pageid": raw.get("pageid"),
        "extract_chars": raw.get("extract_chars", len(extract)),
        "content_hash": sha256_text(extract),
        "error": raw.get("error"),
    }


def discover_moegirl(query, work, timeout):
    raw = run_python_script("moegirl_api.py", [query], timeout)
    return normalize_moegirl(raw, query, work)


def resolve_bwiki_game(work):
    """Resolve a work name to a BWIKI game slug."""
    if not work:
        return None
    for name, slug in BWIKI_GAME_SLUGS.items():
        if name.lower() in work.lower() or work.lower() in name.lower():
            return slug
    return None


def normalize_bwiki(raw, query, work):
    url = raw.get("page_url") or raw.get("url")
    excluded = is_excluded_url(url)
    extract = raw.get("extract", "") or ""
    status = "ok" if raw.get("ok") and not excluded else "failed"
    return {
        "id": f"bwiki-{raw.get('resolved_title') or query}".replace(" ", "-"),
        "source": "bwiki",
        "title": raw.get("resolved_title"),
        "resolved_title": raw.get("resolved_title"),
        "url": url,
        "query": query,
        "work": work,
        "source_tier": "excluded" if excluded else source_tier("bwiki"),
        "officiality": "excluded" if excluded else "secondary",
        "media_type": "wiki",
        "language": "zh",
        "retrieved_at": TODAY,
        "status": status,
        "warnings": raw.get("warnings", []),
        "attempted_modes": raw.get("attempted_modes") or [raw.get("mode")],
        "retrieved_by": raw.get("retrieved_by"),
        "pageid": raw.get("pageid"),
        "extract_chars": raw.get("extract_chars", len(extract)),
        "content_hash": sha256_text(extract),
        "error": raw.get("error"),
    }


def discover_bwiki(query, work, timeout):
    game = resolve_bwiki_game(work)
    if not game:
        return {
            "id": f"bwiki-{query}".replace(" ", "-"),
            "source": "bwiki",
            "title": None,
            "url": None,
            "query": query,
            "work": work,
            "source_tier": source_tier("bwiki"),
            "officiality": "secondary",
            "media_type": "wiki",
            "language": "zh",
            "retrieved_at": TODAY,
            "status": "failed",
            "error": "unknown_game",
            "warnings": [f"could not resolve BWIKI game slug from work '{work}'; pass --sources bwiki with a known game name"],
            "attempted_modes": ["discover"],
        }
    raw = run_python_script("bwiki_api.py", [query, "--game", game], timeout)
    return normalize_bwiki(raw, query, work)


def placeholder_source(source, query, work, reason="adapter_not_implemented"):
    return {
        "id": f"{source}-{query}".replace(" ", "-"),
        "source": source,
        "title": None,
        "url": None,
        "query": query,
        "work": work,
        "source_tier": source_tier(source),
        "officiality": "secondary",
        "media_type": "wiki" if source in {"mediawiki", "fandom", "wikipedia", "bwiki"} else "database",
        "language": None,
        "retrieved_at": TODAY,
        "status": "failed",
        "error": reason,
        "warnings": [f"{source} adapter is not implemented yet; use search skill or user material as fallback and record results"],
        "attempted_modes": ["placeholder"],
    }


def parse_sources(value, work):
    if value:
        return [part.strip() for part in value.split(",") if part.strip()]
    return source_hints_for_work(work)


def emit_json(payload):
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    sys.stdout.buffer.write(text.encode("utf-8"))


def main():
    parser = argparse.ArgumentParser(description="Discover CSP character sources through local adapters")
    parser.add_argument("query", help="character name, alias, or page title")
    parser.add_argument("--work", default="", help="work/franchise name")
    parser.add_argument("--mode", default="discover", choices=["discover"], help="discovery mode")
    parser.add_argument("--sources", help="comma-separated source adapters, e.g. moegirl,mediawiki")
    parser.add_argument("--timeout", type=int, default=20, help="per-adapter timeout seconds")
    args = parser.parse_args()

    requested_sources = parse_sources(args.sources, args.work)
    records = []

    for source in requested_sources:
        if source == "moegirl":
            records.append(discover_moegirl(args.query, args.work, args.timeout))
        elif source == "bwiki":
            records.append(discover_bwiki(args.query, args.work, args.timeout))
        elif source == "official":
            records.append(placeholder_source(source, args.query, args.work, "manual_or_official_material_required"))
        else:
            records.append(placeholder_source(source, args.query, args.work))

    result = {
        "ok": any(record.get("status") == "ok" for record in records),
        "query": args.query,
        "work": args.work,
        "mode": args.mode,
        "retrieved_at": TODAY,
        "cross_media_hint": is_cross_media_work(args.work),
        "sources_requested": requested_sources,
        "records": records,
        "warnings": [] if any(record.get("status") == "ok" for record in records) else ["no local adapter returned a successful source"],
    }

    emit_json(result)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
