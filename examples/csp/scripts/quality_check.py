#!/usr/bin/env python3
"""Validate generated CSP character skills."""

import json
import re
import sys
from datetime import date
from pathlib import Path

BLACKLISTED_DOMAINS = ["zhihu.com", "weixin.qq.com", "baike.baidu.com"]


def read_text(path):
    return path.read_text(encoding="utf-8") if path.exists() else ""


def load_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def resolve_paths(target):
    path = Path(target)
    if path.is_dir():
        return path, path / "SKILL.md"
    return path.parent, path


def check_behavior_patterns(content):
    in_section = False
    pattern_clues = 0
    for line in content.split("\n"):
        if re.match(r"^##\s+.*行为动态|行为模式", line):
            in_section = True
            continue
        if in_section and re.match(r"^##\s+", line) and "行为" not in line:
            break
        if in_section and re.match(r"^###\s+", line):
            pattern_clues += 1
    passed = 3 <= pattern_clues <= 8
    return passed, f"{pattern_clues} behavior subsections {'PASS' if passed else 'FAIL (expected 3-8)'}"


def check_expression_texture(content):
    markers = ["句式", "词汇", "语尾", "自称", "敬语", "节奏", "沉默", "口癖", "语气", "停顿", "情绪"]
    found = sum(1 for marker in markers if marker in content)
    passed = "表达质感" in content and found >= 4
    return passed, f"expression markers: {found} {'PASS' if passed else 'FAIL (expected section + >=4 markers)'}"


def check_honest_boundary(content):
    match = re.search(r"(?:##\s+.*诚实边界|##\s+.*局限)(.*?)(?=\n##\s|\Z)", content, re.DOTALL)
    if not match:
        return False, "FAIL: no honesty boundary section"
    count = len(re.findall(r"^[-*]\s+", match.group(1), re.MULTILINE))
    passed = count >= 3
    return passed, f"honesty boundary: {count} items {'PASS' if passed else 'FAIL (expected >=3)'}"


def check_contradictions(content):
    count = len(re.findall(r"矛盾|张力|冲突|paradox|一方面.*另一方面|既.*又|虽然.*但是", content))
    passed = count >= 1
    return passed, f"contradictions preserved: {count} {'PASS' if passed else 'FAIL (expected >=1)'}"


def check_behavior_examples(content):
    examples = re.findall(r"###\s+场景[一二三四五六七八九十\d]", content)
    if not examples:
        examples = re.findall(r"场景[一二三四五六七八九十\d]", content)
    count = len(examples)
    passed = 3 <= count <= 8
    return passed, f"behavior examples: {count} {'PASS' if passed else 'FAIL (expected 3-8)'}"


def check_role_play_rules(content):
    has_rules = "角色扮演规则" in content
    has_exit = bool(re.search(r"退出|exit", content, re.IGNORECASE))
    has_first_person = bool(re.search(r"用「我」|第一人称|直接以", content))
    passed = has_rules and has_exit and has_first_person
    return passed, f"rules:{has_rules}, exit:{has_exit}, 1st-person:{has_first_person} {'PASS' if passed else 'FAIL'}"


def check_source_attribution(content, skill_dir):
    has_urls = bool(re.search(r"https?://[^\s\)]+", content))
    has_source_section = bool(re.search(r"调研来源|来源|source", content, re.IGNORECASE))
    has_sources_json = (skill_dir / "references" / "sources.json").exists()
    passed = has_urls or has_source_section or has_sources_json
    return passed, f"URLs:{has_urls}, source section:{has_source_section}, sources.json:{has_sources_json} {'PASS' if passed else 'FAIL'}"


def check_manifest(skill_dir):
    path = skill_dir / "manifest.json"
    data = load_json(path, {})
    required = ["schema_version", "name", "character", "work", "generated_at", "research_completed_at", "latest_source_checked_at", "covered_until", "source_count"]
    missing = [key for key in required if key not in data or data.get(key) in (None, "")]
    return not missing, f"manifest {'PASS' if not missing else 'FAIL missing ' + ', '.join(missing)}"


def source_records(skill_dir):
    data = load_json(skill_dir / "references" / "sources.json", [])
    if isinstance(data, dict) and "records" in data:
        return data["records"]
    if isinstance(data, list):
        return data
    return []


def check_sources_json(skill_dir):
    path = skill_dir / "references" / "sources.json"
    if not path.exists():
        return False, "FAIL: missing references/sources.json"
    records = source_records(skill_dir)
    if not records:
        return False, "FAIL: sources.json has no records"
    missing_dates = [record.get("id", record.get("source", "unknown")) for record in records if not record.get("retrieved_at")]
    blacklisted = []
    for record in records:
        url = (record.get("url") or "").lower()
        if any(domain in url for domain in BLACKLISTED_DOMAINS) and record.get("source_tier") != "excluded":
            blacklisted.append(url)
    passed = not missing_dates and not blacklisted
    detail = f"records:{len(records)}, missing_dates:{len(missing_dates)}, blacklisted:{len(blacklisted)}"
    return passed, f"{detail} {'PASS' if passed else 'FAIL'}"


def check_research_dates(content):
    has_date_section = "资料时间边界" in content
    has_update_phrase = "我的资料更新至" in content and "这可能会消耗一些 Token" in content
    date_like = bool(re.search(r"20\d{2}-\d{2}-\d{2}|YYYY-MM-DD", content))
    passed = has_date_section and has_update_phrase and date_like
    return passed, f"date section:{has_date_section}, update response:{has_update_phrase}, date:{date_like} {'PASS' if passed else 'FAIL'}"


def check_research_files(skill_dir):
    research_dir = skill_dir / "references" / "research"
    required = ["01-setting.md", "02-personality.md", "03-expression.md", "04-relationships.md", "05-key-scenes.md"]
    missing = [name for name in required if not (research_dir / name).exists()]
    media = (research_dir / "06-media-coverage.md").exists()
    passed = not missing
    return passed, f"missing:{missing or 'none'}, media_coverage:{media} {'PASS' if passed else 'FAIL'}"


def write_report(skill_dir, results):
    report_dir = skill_dir / "references"
    if not report_dir.exists():
        return
    passed_count = sum(1 for result in results if result[1])
    score = round(passed_count / len(results), 3) if results else 0
    report = {
        "checked_at": date.today().isoformat(),
        "score": score,
        "passed": passed_count >= len(results) - 1,
        "checks": {name: "pass" if passed else "fail" for name, passed, _ in results},
        "warnings": [detail for _, passed, detail in results if not passed],
        "failed_checks": [name for name, passed, _ in results if not passed],
    }
    (report_dir / "quality-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    if len(sys.argv) < 2:
        print("Usage: python quality_check.py <skill_directory_or_SKILL.md_path>")
        sys.exit(1)

    skill_dir, skill_path = resolve_paths(sys.argv[1])
    if not skill_path.exists():
        print(f"FAIL: SKILL.md not found: {skill_path}")
        sys.exit(1)

    content = read_text(skill_path)
    checks = [
        ("Behavior Patterns", lambda: check_behavior_patterns(content)),
        ("Expression Texture", lambda: check_expression_texture(content)),
        ("Contradictions", lambda: check_contradictions(content)),
        ("Role-Play Rules", lambda: check_role_play_rules(content)),
        ("Behavior Examples", lambda: check_behavior_examples(content)),
        ("Honesty Boundary", lambda: check_honest_boundary(content)),
        ("Source Attribution", lambda: check_source_attribution(content, skill_dir)),
        ("Manifest", lambda: check_manifest(skill_dir)),
        ("Sources JSON", lambda: check_sources_json(skill_dir)),
        ("Research Dates", lambda: check_research_dates(content)),
        ("Research Files", lambda: check_research_files(skill_dir)),
    ]

    print(f"Quality Check: {skill_path}")
    print("=" * 72)
    results = []
    for name, fn in checks:
        passed, detail = fn()
        results.append((name, passed, detail))
        print(f"  {name:<22} {'PASS' if passed else 'FAIL':<6} {detail}")
    print("=" * 72)

    passed_count = sum(1 for _, passed, _ in results if passed)
    print(f"Result: {passed_count}/{len(results)} passed")
    write_report(skill_dir, results)

    if passed_count == len(results):
        print("All checks passed — ready to deliver.")
    elif passed_count >= len(results) - 1:
        print("Mostly passed — fix remaining issue before delivery.")
    else:
        print("Failures found — iterate before delivery.")

    sys.exit(0 if passed_count >= len(results) - 1 else 1)


if __name__ == "__main__":
    main()
