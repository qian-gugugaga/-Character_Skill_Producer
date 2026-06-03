#!/usr/bin/env python3
"""Merge CSP research results and report source/date coverage."""

import json
import re
import sys
from collections import Counter
from pathlib import Path

AGENTS = {
    "01-setting": "Setting",
    "02-personality": "Personality",
    "03-expression": "Expression",
    "04-relationships": "Relationships",
    "05-key-scenes": "Key Scenes",
    "06-media-coverage": "Media Coverage",
}

BLACKLISTED_DOMAINS = ["zhihu.com", "weixin.qq.com", "baike.baidu.com"]


def load_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def source_records(skill_dir):
    data = load_json(skill_dir / "references" / "sources.json", [])
    if isinstance(data, dict) and "records" in data:
        return data["records"]
    if isinstance(data, list):
        return data
    return []


def count_sources(content):
    urls = re.findall(r"https?://[^\s\)]+", content)
    primary = len(re.findall(r"官方|primary|original|设定集|interview|访谈|transcript|原文|source material", content, re.IGNORECASE))
    secondary = len(re.findall(r"同人|fan|community|粉丝|解读|analysis|推测|speculation|转述", content, re.IGNORECASE))
    return {"unique_urls": len(set(urls)), "total_urls": len(urls), "primary": primary, "secondary": secondary}


def extract_key_findings(content, max_items=3):
    headings = re.findall(r"^##\s+(.+)$", content, re.MULTILINE)
    if headings:
        return headings[:max_items]
    bolds = re.findall(r"\*\*(.+?)\*\*", content)
    if bolds:
        return bolds[:max_items]
    lines = [line.strip() for line in content.split("\n") if line.strip() and not line.startswith("#")]
    return [(line[:50] + "...") if len(line) > 50 else line for line in lines[:max_items]]


def find_contradictions(files):
    contradictions = []
    for name, content in files.items():
        matches = re.findall(r"(?:矛盾|争议|contradiction|conflict|disputed|然而.*?不同|但.*?相反).{0,100}", content, re.IGNORECASE)
        for match in matches:
            contradictions.append(f"{AGENTS.get(name, name)}: {match[:80]}")
    return contradictions[:5]


def classify_confidence(unique_sources, primary, secondary, source_records_count):
    effective_sources = max(unique_sources, source_records_count)
    if effective_sources >= 10 and primary >= 2:
        return "HIGH"
    if effective_sources >= 5:
        return "MEDIUM"
    return "LOW"


def summarize_sources(records):
    ok_records = [record for record in records if record.get("status") == "ok"]
    failed = [record for record in records if record.get("status") != "ok"]
    missing_dates = [record for record in records if not record.get("retrieved_at")]
    tiers = Counter(record.get("source_tier", "unknown") for record in ok_records)
    blacklisted = []
    for record in records:
        url = (record.get("url") or "").lower()
        if any(domain in url for domain in BLACKLISTED_DOMAINS) and record.get("source_tier") != "excluded":
            blacklisted.append(url)
    latest = max([record.get("retrieved_at") for record in records if record.get("retrieved_at")] or ["N/A"])
    return {
        "ok": len(ok_records),
        "failed": len(failed),
        "missing_dates": len(missing_dates),
        "tiers": tiers,
        "blacklisted": blacklisted,
        "latest": latest,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python merge_research.py <skill_directory>")
        sys.exit(1)

    skill_dir = Path(sys.argv[1])
    research_dir = skill_dir / "references" / "research"
    if not research_dir.exists():
        print(f"FAIL: directory not found: {research_dir}")
        sys.exit(1)

    files = {}
    rows = []
    total_sources = 0
    total_primary = 0
    total_secondary = 0
    missing = []

    for key, label in AGENTS.items():
        md_file = research_dir / f"{key}.md"
        if not md_file.exists():
            missing.append(label)
            rows.append(f"│ {label:<16} │ {'MISSING':<8} │ {'—':<34} │")
            continue
        content = md_file.read_text(encoding="utf-8")
        files[key] = content
        stats = count_sources(content)
        findings = extract_key_findings(content)
        total_sources += stats["unique_urls"]
        total_primary += stats["primary"]
        total_secondary += stats["secondary"]
        findings_str = ", ".join(findings) if findings else "—"
        if len(findings_str) > 34:
            findings_str = findings_str[:31] + "..."
        rows.append(f"│ {label:<16} │ {stats['unique_urls']:<8} │ {findings_str:<34} │")

    records = source_records(skill_dir)
    source_summary = summarize_sources(records)
    contradictions = find_contradictions(files)
    confidence = classify_confidence(total_sources, total_primary, total_secondary, source_summary["ok"])

    print("┌──────────────────┬──────────┬────────────────────────────────────┐")
    print("│ Dimension        │ URLs     │ Key Findings                       │")
    print("├──────────────────┼──────────┼────────────────────────────────────┤")
    for row in rows:
        print(row)
    print("├──────────────────┼──────────┼────────────────────────────────────┤")
    print(f"│ Sources JSON OK  │ {source_summary['ok']:<8} │ failed: {source_summary['failed']:<25} │")
    print(f"│ Latest Checked   │ {'—':<8} │ {source_summary['latest']:<34} │")
    print(f"│ Missing Dates    │ {source_summary['missing_dates']:<8} │ {'must be 0':<34} │")
    print(f"│ Confidence       │ {confidence:<8} │ {'tiers: ' + dict(source_summary['tiers']).__repr__():<34.34} │")
    print(f"│ Contradictions   │ {len(contradictions):<8} │ {(contradictions[0][:34] if contradictions else '—'):<34} │")
    print(f"│ Missing Dims     │ {len(missing):<8} │ {(', '.join(missing) if missing else '—'):<34.34} │")
    print("└──────────────────┴──────────┴────────────────────────────────────┘")

    if source_summary["missing_dates"]:
        print("\nWARNING: some source records are missing retrieved_at.")
    if source_summary["blacklisted"]:
        print("\nFAIL: blacklisted sources used without excluded tier:")
        for url in source_summary["blacklisted"]:
            print(f"- {url}")
    if total_sources < 5 and source_summary["ok"] < 5:
        print("\nWARNING: low source count — supplement research before distillation.")
    if missing:
        print(f"\nWARNING: missing dimensions: {', '.join(missing)}")
    if confidence == "LOW":
        print("\nWARNING: LOW confidence — inform user before proceeding.")

    if source_summary["blacklisted"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
