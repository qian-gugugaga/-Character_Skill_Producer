# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

CSP (Character Skill Producer) is an open-source **meta-skill** that turns anime/game fictional characters into executable Agent Skills. Given a character name and series, it researches authoritative sources, cross-validates evidence, distills behavior patterns, and outputs a runnable `SKILL.md` character role-playing skill.

This repo is `github.com/qian-gugugaga/Character_Skill_Producer`. Generated skills follow the AgentSkills convention: YAML frontmatter plus Markdown body, with research artifacts kept under `references/research/` for transparency.

CSP is not a character-card generator and does not target real-person distillation. The project is focused on 二次元 anime/manga/game characters and executable behavior instructions rather than static profiles or archetype labels.

## Platform Notes

- Shell is bash on Windows (Git Bash / MSYS). Use Unix-style syntax: `/dev/null` not `NUL`, forward slashes in paths.
- `python3` is not aliased on this machine. Use `python` for local commands, even when docs or script headers show `python3`.
- `package.json` currently only declares the `docx` dependency; there is no Node build/test script for CSP itself.

## Commands

```bash
# Install package dependencies if needed by local tooling
npm install

# Quality-check a generated skill (7 checks: behavior patterns, expression, contradictions, etc.)
python scripts/quality_check.py <path/to/SKILL.md>

# Summarize research results from references/research/ under a generated skill directory
python scripts/merge_research.py <skill_directory>

# Fetch Moegirl Wiki entries through the MediaWiki API
python scripts/moegirl_api.py "角色名"              # auto: intro → search → fallback
python scripts/moegirl_api.py "角色名" --intro      # intro extract for a known title
python scripts/moegirl_api.py "角色名" --search     # candidate page titles
python scripts/moegirl_api.py "角色名" --full       # full plaintext extract
python scripts/moegirl_api.py "角色名" --wikitext   # raw wikitext fallback
```

There is no build step, lint command, or test suite for this repo. The closest validations are `quality_check.py` for generated skills and `merge_research.py` for research completeness.

## Architecture

### Canonical Source vs Installable Skill

The root files are the canonical source for CSP development:

| File | Role |
|------|------|
| `SKILL.md` | Main CSP meta-skill and pipeline instructions |
| `references/skill-template.md` | Template used to assemble generated character skills |
| `references/distillation-framework.md` | Methodology for extracting behavior patterns from research |
| `scripts/quality_check.py` | Quality gate for generated character skills |
| `scripts/merge_research.py` | Research-summary/checkpoint generator |
| `scripts/moegirl_api.py` | Moegirlpedia MediaWiki API wrapper |
| `PRD.md` | Product definition and long-term scope, in English |

`examples/csp/` is the self-contained installable CSP skill. It bundles its own copies of `SKILL.md`, `references/`, and `scripts/` so users can copy or install it independently. When changing root `SKILL.md`, `references/*.md`, or `scripts/*.py`, keep the corresponding files in `examples/csp/` in sync or the published skill will diverge from the source.

Generated character examples live in `examples/<slug>/`. Installed local skills live in `.claude/skills/<slug>/`; `.claude/` is gitignored and should not be treated as source.

### CSP Meta-Skill Pipeline

When a user asks to generate a character skill, CSP follows this staged flow:

1. **Requirement confirmation** — character name, series, optional focus, and whether the user has official local materials.
2. **Directory creation** — create the skill directory and `references/research/` before research begins.
3. **5 parallel research agents** — Setting (`01-setting.md`), Personality (`02-personality.md`), Expression (`03-expression.md`), Relationships (`04-relationships.md`), Key Scenes (`05-key-scenes.md`). Each agent must write its findings to the corresponding file.
4. **Research quality checkpoint** — use `merge_research.py` or an equivalent summary to report source count, key findings, contradictions, and missing dimensions before distillation.
5. **Behavioral distillation** — extract behavior patterns, expression texture, social cognition, decision logic, hard constraints, and honesty boundaries. Core behavior patterns should pass both cross-scene recurrence and executability checks.
6. **Distillation confirmation** — summarize the extracted patterns and limits for user confirmation before assembly.
7. **SKILL.md assembly** — fill `references/skill-template.md` from the distilled material.
8. **Quality verification** — run `quality_check.py` and use independent known-scene replay / edge-case inference where appropriate. Show verification results before calling the work complete.

### Generated Skill Structure

Each character skill is a self-contained directory:

```text
<character-slug>/
├── SKILL.md
└── references/
    └── research/
        ├── 01-setting.md
        ├── 02-personality.md
        ├── 03-expression.md
        ├── 04-relationships.md
        └── 05-key-scenes.md
```

Copying the whole directory should be enough to install/share the character skill.

## Source and Research Rules

CSP is source-grounded. Prefer user-provided official materials first, then public sources:

| Priority | Sources |
|---|---|
| Highest | User-provided official books, interviews, BD extras, subtitles, screenshots, transcripts |
| High | Moegirl Wiki, Wikipedia, official or franchise Fandom Wiki |
| Medium | Bangumi, AniDB, game stories, Bilibili high-quality columns, Anime News Network |
| Low | Fan discussion/community interpretation, clearly marked as speculation |
| Excluded | Zhihu, WeChat public accounts, Baidu Baike |

Use at least two independent sources for important claims. Preserve conflicts instead of smoothing them over. If public information is thin, label the gap explicitly rather than inventing behavior.

For Moegirlpedia, use `scripts/moegirl_api.py` before trying direct page fetches. Record the command, resolved title, page URL, and any API failure in research files.

## Cross-Media Franchises

`SKILL.md` has a dedicated branch for cross-work/cross-band characters, including BanG Dream!, Love Live!, Project Sekai, and 少女☆歌剧.

For these characters:

- Setting and relationship research must cover all relevant works the character appears in, not only one anime season.
- Game/spinoff material such as Garupa card stories, Bestdori event scripts, and area dialogue is valid medium-priority evidence, especially for daily-life behavior.
- The honesty boundary must say which media were covered and which were not.

Do not remove or simplify this branch as “scope creep”; it is necessary for characters whose behavior depends on cross-media context.

## Writing Standards for Skills

- Write CSP meta-skill body and generated character skills in Chinese. PRD/planning docs may be English.
- Preserve Japanese/English names and canonical lines where appropriate.
- Describe **how the character behaves** in situations, not taxonomy labels like “tsundere”.
- Preserve contradictions and developmental changes; they are behavior signals, not bugs.
- Every core behavior pattern should answer: in what situation → does what → why.
- Generated role-play instructions should sound like natural speech, not essays or PPT outlines. Avoid overusing bold text, dash-linked sentences, and rigid three-part structures in character voice.
