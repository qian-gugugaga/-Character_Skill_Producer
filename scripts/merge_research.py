#!/usr/bin/env python3
"""
Merge 5 CASF agent research results, generate Phase 1.5 research review summary.
Scans references/research/ directory for 01-05 md files,
counts sources and extracts key findings per dimension.

Usage:
    python3 merge_research.py <skill_directory>

Example:
    python3 merge_research.py .claude/skills/takamatsu-tomori

Output: prints markdown summary table to stdout.
"""

import sys
import re
from pathlib import Path

AGENTS = {
    '01-setting': 'Setting',
    '02-personality': 'Personality',
    '03-expression': 'Expression',
    '04-relationships': 'Relationships',
    '05-key-scenes': 'Key Scenes',
}


def count_sources(content: str) -> dict:
    """Count sources and classify primary vs secondary."""
    urls = re.findall(r'https?://[^\s\)]+', content)
    unique = len(set(urls))

    primary = len(re.findall(
        r'官方|primary|original|设定集|interview|访谈|transcript|原文|source material',
        content, re.IGNORECASE
    ))
    secondary = len(re.findall(
        r'同人|fan|community|粉丝|解读|analysis|推测|speculation|转述',
        content, re.IGNORECASE
    ))

    return {
        'unique_urls': unique,
        'total_urls': len(urls),
        'primary': primary,
        'secondary': secondary,
    }


def extract_key_findings(content: str, max_items: int = 3) -> list[str]:
    """Extract key findings from research file."""
    # Try ## headings first
    headings = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
    if headings:
        return headings[:max_items]

    # Fallback: bold text
    bolds = re.findall(r'\*\*(.+?)\*\*', content)
    if bolds:
        return bolds[:max_items]

    # Fallback: first non-empty non-heading lines
    lines = [
        l.strip() for l in content.split('\n')
        if l.strip() and not l.startswith('#')
    ]
    return [
        (l[:50] + '...') if len(l) > 50 else l
        for l in lines[:max_items]
    ]


def find_contradictions(files: dict) -> list[str]:
    """Detect cross-file contradictions."""
    contradictions = []
    for name, content in files.items():
        matches = re.findall(
            r'(?:矛盾|争议|contradiction|conflict|disputed|然而.*?不同|但.*?相反).{0,100}',
            content, re.IGNORECASE
        )
        for m in matches:
            contradictions.append(f"{AGENTS.get(name, name)}: {m[:80]}")
    return contradictions[:5]


def classify_confidence(unique_sources: int, primary: int, secondary: int) -> str:
    """Classify overall source confidence."""
    if unique_sources >= 5 and primary >= 2:
        return 'HIGH'
    elif unique_sources >= 3:
        return 'MEDIUM'
    else:
        return 'LOW'


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 merge_research.py <skill_directory>")
        sys.exit(1)

    skill_dir = Path(sys.argv[1])
    research_dir = skill_dir / 'references' / 'research'

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
            rows.append(f"│ {label:<14} │ {'MISSING':<8} │ {'—':<26} │")
            continue

        content = md_file.read_text(encoding='utf-8')
        files[key] = content
        stats = count_sources(content)
        findings = extract_key_findings(content)

        total_sources += stats['unique_urls']
        total_primary += stats['primary']
        total_secondary += stats['secondary']

        findings_str = ', '.join(findings) if findings else '—'
        if len(findings_str) > 38:
            findings_str = findings_str[:35] + '...'

        rows.append(
            f"│ {label:<14} │ {stats['unique_urls']:<8} │ {findings_str:<26} │"
        )

    contradictions = find_contradictions(files)
    confidence = classify_confidence(total_sources, total_primary, total_secondary)

    # Build output table
    print("┌────────────────┬──────────┬───────────────────────────┐")
    print("│ Agent          │ Sources   │ Key Findings              │")
    print("├────────────────┼──────────┼───────────────────────────┤")
    for row in rows:
        print(row)
    print("├────────────────┼──────────┼───────────────────────────┤")

    primary_ratio = (
        f"{total_primary}/{total_primary + total_secondary}"
        if (total_primary + total_secondary) > 0
        else "N/A"
    )
    print(f"│ Total Sources   │ {total_sources:<8} │ P/S ratio: {primary_ratio:<14} │")
    print(f"│ Confidence      │ {confidence:<8} │                           │")

    if contradictions:
        print(f"│ Contradictions  │ {len(contradictions)} found   │ {contradictions[0][:24]:<24} │")
    else:
        print(f"│ Contradictions  │ 0 found   │ {'—':<24} │")

    if missing:
        print(f"│ Missing Dims    │ {len(missing)} dims    │ {', '.join(missing):<24} │")
    else:
        print(f"│ Missing Dims    │ None      │ {'—':<24} │")

    print("└────────────────┴──────────┴───────────────────────────┘")

    # Summary
    if total_sources < 5:
        print("\n⚠️  Total sources < 5 — consider lowering expectations or supplementing research.")
    if missing:
        print(f"\n⚠️  Missing dimensions: {', '.join(missing)} — note in honesty boundary.")
    if confidence == 'LOW':
        print("\n⚠️  LOW confidence — inform user before proceeding to Phase 2.")


if __name__ == '__main__':
    main()
