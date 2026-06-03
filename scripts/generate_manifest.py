#!/usr/bin/env python3
"""Generate or update manifest.json for a CSP character skill directory."""

import argparse
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path

TODAY = date.today().isoformat()


def load_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def extract_frontmatter_field(content, field):
    match = re.search(rf"^{re.escape(field)}:\s*(.+)$", content, re.MULTILINE)
    return match.group(1).strip() if match else None


def infer_character(skill_content):
    title = re.search(r"^#\s+(.+?)(?:\s+·|$)", skill_content, re.MULTILINE)
    if title:
        return title.group(1).strip()
    return ""


def source_records(skill_dir):
    sources_path = skill_dir / "references" / "sources.json"
    data = load_json(sources_path, [])
    if isinstance(data, dict) and "records" in data:
        return data["records"]
    if isinstance(data, list):
        return data
    return []


def latest_retrieved_at(records):
    dates = [record.get("retrieved_at") for record in records if record.get("retrieved_at")]
    return max(dates) if dates else TODAY


def source_tiers(records):
    return dict(Counter(record.get("source_tier", "unknown") for record in records if record.get("status") == "ok"))


def covered_media_from_files(skill_dir):
    media_file = skill_dir / "references" / "research" / "06-media-coverage.md"
    if not media_file.exists():
        return []
    content = media_file.read_text(encoding="utf-8")
    items = re.findall(r"^[-*]\s+(.+)$", content, re.MULTILINE)
    return items[:20]


def main():
    parser = argparse.ArgumentParser(description="Generate CSP manifest.json")
    parser.add_argument("skill_dir", help="character skill directory")
    parser.add_argument("--character", help="character display name")
    parser.add_argument("--work", help="work/franchise name")
    parser.add_argument("--csp-version", default="unknown")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir)
    skill_path = skill_dir / "SKILL.md"
    skill_content = skill_path.read_text(encoding="utf-8") if skill_path.exists() else ""
    records = source_records(skill_dir)
    latest = latest_retrieved_at(records)

    existing = load_json(skill_dir / "manifest.json", {})
    name = existing.get("name") or extract_frontmatter_field(skill_content, "name") or skill_dir.name
    character = args.character or existing.get("character") or infer_character(skill_content)
    work = args.work or existing.get("work") or ""
    covered_media = existing.get("covered_media") or covered_media_from_files(skill_dir)

    manifest = {
        "schema_version": "1.0",
        "name": name,
        "character": character,
        "work": work,
        "aliases": existing.get("aliases", []),
        "generated_at": existing.get("generated_at", TODAY),
        "research_started_at": existing.get("research_started_at", TODAY),
        "research_completed_at": existing.get("research_completed_at", latest),
        "latest_source_checked_at": existing.get("latest_source_checked_at", latest),
        "covered_until": existing.get("covered_until", {
            "date": latest,
            "description": "截至该日期可检索到的公开资料和用户提供材料",
        }),
        "covered_media": covered_media,
        "not_covered": existing.get("not_covered", [f"{latest} 后发布的新剧情、新活动、新访谈、新设定修订"]),
        "source_count": sum(1 for record in records if record.get("status") == "ok"),
        "source_tiers": source_tiers(records),
        "quality_score": existing.get("quality_score"),
        "honesty_boundary": existing.get("honesty_boundary", ""),
        "csp_version": args.csp_version,
    }

    output_path = skill_dir / "manifest.json"
    output_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
