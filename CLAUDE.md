# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

CSP (Character Skill Producer) is an open-source Claude Code / Agent Skills style **meta-skill** for turning anime, manga, and game fictional characters into executable character behavior skills.

Given a character name and series, CSP researches sources, cross-validates evidence, distills behavior patterns, runs quality checks, and outputs a runnable `SKILL.md` with research dates, source boundaries, and an update path. It is designed for character chat, fanfiction drafting, scene/dialogue prototyping, and future interactive-fiction or character-driven game workflows.

CSP is not a static character-card generator and does not target real-person distillation. The project focuses on 二次元 characters and executable behavioral instructions: how a character reacts in situations, not just trait labels or lore summaries.

## Platform Notes

- Shell is bash on Windows (Git Bash / MSYS). Use Unix-style syntax: `/dev/null` not `NUL`, forward slashes in paths.
- `python3` is not aliased on this machine. Use `python` for local commands, even when docs or script headers show `python3`.
- `package.json` currently only declares the `docx` dependency; there is no Node build/test script for CSP itself.
- There are no Cursor rules or Copilot instruction files in this repository at the time this file was checked.
- README translations (`README_EN.md`, `README_JA.md`, `README_KO.md`, `README_ES.md`) are product-facing docs; keep them aligned when changing core product messaging in `README.md`.

## Commands

```bash
# Install package dependencies if local tooling needs them
npm install

# Discover local sources through the repository search entrypoint
python scripts/source_search.py "高松灯" --work "BanG Dream! It's MyGO!!!!!" --mode discover
python scripts/source_search.py "能天使" --work "明日方舟" --sources moegirl

# Fetch Moegirl Wiki entries through the MediaWiki API
python scripts/moegirl_api.py "角色名"              # auto: intro → search → fallback
python scripts/moegirl_api.py "角色名" --intro      # intro extract for a known title
python scripts/moegirl_api.py "角色名" --search     # candidate page titles
python scripts/moegirl_api.py "角色名" --full       # full plaintext extract
python scripts/moegirl_api.py "角色名" --wikitext   # raw wikitext fallback

# Summarize research results from references/research/ under a generated skill directory
python scripts/merge_research.py <skill_directory>

# Generate or refresh manifest metadata for a generated skill directory
python scripts/generate_manifest.py <skill_directory>

# Quality-check a generated character skill directory or SKILL.md
python scripts/quality_check.py <skill_directory>
python scripts/quality_check.py <path/to/SKILL.md>
```

There is no build step, lint command, or conventional test suite for this repo. The closest validations are `quality_check.py` for generated character skills, `merge_research.py` for research completeness, and `generate_manifest.py` for metadata generation. `quality_check.py` writes/refreshes `references/quality-report.json` and exits non-zero when more than one check fails, so it is the main command to run before delivering a generated skill.

## Architecture

### Canonical Source vs Installable Skill

The root files are the canonical source for CSP development:

| File | Role |
|---|---|
| `SKILL.md` | Main CSP meta-skill and pipeline instructions |
| `references/skill-template.md` | Template used to assemble generated character skills |
| `references/distillation-framework.md` | Methodology for converting research into executable behavior patterns |
| `references/source-output-schema.md` | Expected structures for `sources.json`, `manifest.json`, and `quality-report.json` |
| `scripts/source_search.py` | Unified local source discovery entrypoint |
| `scripts/source_registry.py` | Source tiers, excluded domains, work-specific hints, and cross-media work rules |
| `scripts/moegirl_api.py` | Moegirlpedia MediaWiki API wrapper |
| `scripts/merge_research.py` | Research-summary/checkpoint generator |
| `scripts/generate_manifest.py` | Manifest generator/updater for generated skills |
| `scripts/quality_check.py` | Quality gate for generated character skills |

`examples/csp/` is the self-contained installable CSP skill. It bundles its own copies of `SKILL.md`, `references/`, and `scripts/` so users can copy or install it independently. When changing root `SKILL.md`, `references/*.md`, or `scripts/*.py`, keep the corresponding files in `examples/csp/` in sync or the published skill will diverge from the source.

`README.md` and the translated READMEs describe the same product promise for different audiences. If you change installation instructions, source policy, supported examples, or roadmap status in one README, update the translations or explicitly note that they are intentionally out of sync.

Generated character examples live in `examples/<slug>/`. Installed local skills live in `.claude/skills/<slug>/`; `.claude/` is gitignored and should not be treated as source.

### Generated Skill Structure

Each generated character skill is a self-contained directory:

```text
<character-slug>/
├── SKILL.md
├── manifest.json
└── references/
    ├── sources.json
    ├── distillation.md
    ├── quality-report.json
    └── research/
        ├── 01-setting.md
        ├── 02-personality.md
        ├── 03-expression.md
        ├── 04-relationships.md
        ├── 05-key-scenes.md
        └── 06-media-coverage.md
```

Copying the whole directory should be enough to install/share the character skill.

### CSP Meta-Skill Pipeline

When a user asks to generate a character skill, CSP follows this staged flow:

1. **Requirement confirmation** — character name, series, optional focus, and whether the user has official local materials.
2. **Local source discovery** — run `scripts/source_search.py` and site adapters before external web search. External search is a supplement, not the default first step.
3. **Directory and source index setup** — create the skill directory, `references/research/`, and `references/sources.json` with retrieval dates, source tiers, failures, and optional content hashes.
4. **Five research tracks** — setting/worldview, personality, expression, relationships, and key scenes are researched separately so one dimension does not swallow the others.
5. **Cross-media coverage** — for cross-work franchises, document covered and uncovered media in `06-media-coverage.md`.
6. **Research quality checkpoint** — use `merge_research.py` or an equivalent summary to report source count, key findings, contradictions, and missing dimensions before distillation.
7. **Behavioral distillation** — extract behavior dynamics, expression texture, social cognition, decision logic, hard constraints, contradictions, and honesty boundaries. Core behavior patterns should answer: in what situation → does what → why.
8. **Skill assembly** — fill `references/skill-template.md` from the distilled material.
9. **Metadata and quality verification** — generate `manifest.json`, run `quality_check.py`, and refresh `references/quality-report.json`.

## Source and Research Rules

CSP is source-grounded. Prefer user-provided official materials first, then public sources:

| Priority | Sources |
|---|---|
| Highest | User-provided official books, interviews, BD extras, subtitles, screenshots, transcripts |
| High | Official sites, official character profiles, official story text, Moegirl Wiki, Wikipedia, franchise Fandom Wiki |
| Medium | Bangumi, AniDB, game stories, Bilibili high-quality columns, Anime News Network, Bestdori, BWIKI |
| Low | Fan discussion/community interpretation, clearly marked as speculation |
| Excluded | Zhihu, WeChat public accounts, Baidu Baike |

Use at least two independent sources for important claims. Preserve conflicts instead of smoothing them over. If public information is thin, label the gap explicitly rather than inventing behavior.

For Moegirlpedia, use `scripts/moegirl_api.py` or `scripts/source_search.py` before trying direct page fetches. Record the command, resolved title, page URL, retrieval date, and any API failure in research/source files.

## Research Dates and Updates

Every generated skill must record research timing and coverage boundaries in `manifest.json` and `references/sources.json`, including fields such as retrieval dates, research completion date, covered media, uncovered material, and latest source checked date.

When a user says newer canon contradicts the skill, the character should acknowledge the boundary instead of inventing updates. The expected Chinese pattern is:

```text
我的资料更新至 YYYY-MM-DD，可能没有覆盖之后发布的内容。如果你有最新版 CSP，或可以提供新剧情 / 新资料链接，我可以帮你更新这个 Skill；这可能会消耗一些 Token。
```

Updating an old skill should read its existing `manifest.json` and `sources.json`, re-check core sources, re-distill only affected dimensions, and refresh research dates and quality reports.

## Cross-Media Franchises

`SKILL.md` has a dedicated branch for cross-work/cross-band characters, including BanG Dream!, Love Live!, Project Sekai, and 少女☆歌剧.

For these characters:

- Setting and relationship research must cover all relevant works the character appears in, not only one anime season.
- Game/spinoff material such as Garupa card stories, Bestdori event scripts, and area dialogue is valid medium-priority evidence, especially for daily-life behavior.
- The honesty boundary must say which media were covered and which were not.
- `06-media-coverage.md` should record cross-media coverage, uncovered content, and timeline boundaries.

Do not remove or simplify this branch as “scope creep”; it is necessary for characters whose behavior depends on cross-media context.

## Writing Standards for Skills

- Write CSP meta-skill body and generated character skills in Chinese. PRD/planning docs may be English.
- Preserve Japanese/English names and canonical lines where appropriate.
- Describe **how the character behaves** in situations, not taxonomy labels like “tsundere”.
- Preserve contradictions and developmental changes; they are behavior signals, not bugs.
- Every core behavior pattern should answer: in what situation → does what → why.
- Generated role-play instructions should sound like natural speech, not essays or PPT outlines. Avoid overusing bold text, dash-linked sentences, and rigid three-part structures in character voice.
