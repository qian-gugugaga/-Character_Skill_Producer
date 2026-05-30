#!/usr/bin/env python3
"""
Validate generated character SKILL.md against CASF Phase 4 quality standards.
Checks each criterion, outputs PASS/FAIL with details.

Usage:
    python3 quality_check.py <SKILL.md_path>

Example:
    python3 quality_check.py .claude/skills/takamatsu-tomori/SKILL.md
"""

import sys
import re
from pathlib import Path


def check_behavior_patterns(content: str) -> tuple[bool, str]:
    """Check behavior pattern count (3-7 core patterns with scenario evidence)."""
    patterns = re.findall(
        r'^###\s+', content, re.MULTILINE
    )
    # Count patterns more carefully: look for behavioral descriptions under ## 行为动态
    in_section = False
    pattern_clues = 0
    for line in content.split('\n'):
        if re.match(r'^##\s+.*行为动态|行为模式', line):
            in_section = True
            continue
        if in_section and re.match(r'^##\s+', line) and '行为' not in line:
            break
        if in_section and re.match(r'^###\s+', line):
            pattern_clues += 1

    if pattern_clues > 0:
        passed = 3 <= pattern_clues <= 7
        return passed, f"{pattern_clues} core behavior patterns {'PASS' if passed else 'FAIL (expected 3-7)'}"

    # Fallback: count pattern-like paragraphs
    scenario_refs = len(re.findall(r'场景|situation|trigger|压力|默认', content))
    passed = 3 <= scenario_refs <= 10
    return passed, f"~{scenario_refs} behavior references {'PASS' if passed else 'FAIL (expected 3-7 patterns)'}"


def check_expression_texture(content: str) -> tuple[bool, str]:
    """Check expression texture is specific and identifiable."""
    section = bool(re.search(r'表达质感|表达|说话方式', content))
    if not section:
        return False, "FAIL: no expression texture section"

    markers = [
        '句式', '词汇', '语尾', '自称', '敬语', '节奏', '沉默',
        '口癖', '语气', '停顿', '情绪',
    ]
    found = sum(1 for m in markers if re.search(m, content))
    passed = found >= 4
    return passed, f"expression markers: {found} {'PASS' if passed else 'FAIL (expected >=4)'}"


def check_honest_boundary(content: str) -> tuple[bool, str]:
    """Check honesty boundary section (at least 3 specific limits)."""
    boundary_match = re.search(
        r'(?:##\s+.*诚实边界|##\s+.*局限)(.*?)(?=\n##\s|\Z)',
        content, re.DOTALL
    )
    if not boundary_match:
        return False, "FAIL: no honesty boundary section"

    boundary_text = boundary_match.group(1)
    items = re.findall(r'^[-*]\s+', boundary_text, re.MULTILINE)
    count = len(items)
    passed = count >= 3
    return passed, f"honesty boundary: {count} items {'PASS' if passed else 'FAIL (expected >=3)'}"


def check_contradictions(content: str) -> tuple[bool, str]:
    """Check that character contradictions are preserved (at least 1 pair)."""
    tension_markers = len(re.findall(
        r'矛盾|张力|冲突|paradox|一方面.*另一方面|既.*又|虽然.*但是.*却',
        content
    ))
    passed = tension_markers >= 1
    return passed, f"contradictions preserved: {tension_markers} {'PASS' if passed else 'FAIL (expected >=1)'}"


def check_behavior_examples(content: str) -> tuple[bool, str]:
    """Check behavior examples (3-5 scenarios with context-thought-action)."""
    examples = re.findall(r'###\s+场景[一二三四五\d]', content)
    if not examples:
        examples = re.findall(r'场景[一二三四五\d]', content)

    count = len(examples)
    passed = 3 <= count <= 5
    return passed, f"behavior examples: {count} {'PASS' if passed else 'FAIL (expected 3-5)'}"

    # Also check for context/thought/action structure
    has_structure = all([
        bool(re.search(r'情境|背景|场景', content)),
        bool(re.search(r'内心|想法|思考', content)),
        bool(re.search(r'言行|说话|行动|回应', content)),
    ])
    return passed, f"examples: {count}, structure complete: {'yes' if has_structure else 'no'} {'PASS' if passed else 'FAIL'}"


def check_role_play_rules(content: str) -> tuple[bool, str]:
    """Check that role-playing rules section exists with exit trigger."""
    has_rules = bool(re.search(r'角色扮演规则|角色扮演', content))
    has_exit = bool(re.search(r'退出|exit', content, re.IGNORECASE))
    has_first_person = bool(re.search(r'用「我」|第一人称|直接以', content))

    passed = has_rules and has_exit
    detail = f"rules:{'yes' if has_rules else 'no'}, exit:{'yes' if has_exit else 'no'}, 1st-person:{'yes' if has_first_person else 'no'}"
    return passed, f"{detail} {'PASS' if passed else 'FAIL (need role-play rules + exit trigger)'}"


def check_source_attribution(content: str) -> tuple[bool, str]:
    """Check that sources are attributed."""
    has_urls = len(re.findall(r'https?://[^\s\)]+', content)) >= 1
    has_source_section = bool(re.search(r'调研来源|来源|source', content, re.IGNORECASE))
    passed = has_urls or has_source_section
    return passed, f"URLs: {'yes' if has_urls else 'none'}, source section: {'yes' if has_source_section else 'no'} {'PASS' if passed else 'FAIL'}"


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 quality_check.py <SKILL.md_path>")
        sys.exit(1)

    skill_path = Path(sys.argv[1])
    if not skill_path.exists():
        print(f"FAIL: file not found: {skill_path}")
        sys.exit(1)

    content = skill_path.read_text(encoding='utf-8')

    checks = [
        ("Behavior Patterns", check_behavior_patterns),
        ("Expression Texture", check_expression_texture),
        ("Contradictions", check_contradictions),
        ("Role-Play Rules", check_role_play_rules),
        ("Behavior Examples", check_behavior_examples),
        ("Honesty Boundary", check_honest_boundary),
        ("Source Attribution", check_source_attribution),
    ]

    print(f"Quality Check: {skill_path.name}")
    print("=" * 56)

    passed_count = 0
    total = len(checks)

    for name, check_fn in checks:
        passed, detail = check_fn(content)
        status = "PASS" if passed else "FAIL"
        print(f"  {name:<20} {status:<6} {detail}")
        if passed:
            passed_count += 1

    print("=" * 56)
    print(f"Result: {passed_count}/{total} passed")

    if passed_count == total:
        print("All checks passed — ready to deliver.")
    elif passed_count >= total - 1:
        print("Mostly passed — fix remaining issues before delivery.")
    elif passed_count >= total - 2:
        print("Several failures — consider iterating Phase 2.")
    else:
        print("Multiple failures — return to Phase 2 for rework.")

    sys.exit(0 if passed_count >= total - 1 else 1)


if __name__ == '__main__':
    main()
