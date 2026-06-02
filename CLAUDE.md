# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

CSP (Character Skill Producer) is an open-source **meta-skill** — a SKILL.md file that gives Claude Code the ability to generate anime/game character role-playing skills. When loaded, the agent can search authoritative sources (Moegirl Wiki, Wikipedia, Fandom Wiki, Bangumi), cross-validate findings, distill behavior patterns, and produce executable character SKILL.md files.

The repo is at `github.com/qian-gugugaga/Character_Skill_Producer`. Generated skills follow the AgentSkills standard (YAML frontmatter + Markdown body).

## Platform Notes

- Shell is bash on Windows (Git Bash / MSYS). Use Unix-style syntax: `/dev/null` not `NUL`, forward slashes in paths.
- `python3` is not aliased on this machine — invoke `python` for the scripts below. The CSP `SKILL.md` examples sometimes show `python3`; treat that as a Linux convention and substitute `python` here.

## Commands

```bash
# Quality-check a generated skill (7 checks: behavior patterns, expression, contradictions, etc.)
python scripts/quality_check.py <path/to/SKILL.md>

# Summarize research results from references/research/ directory
python scripts/merge_research.py <skill_directory>

# Fetch Moegirl Wiki entries via MediaWiki API (when WebFetch is blocked by safety verification)
python scripts/moegirl_api.py "角色名"              # auto: intro → search → fallback
python scripts/moegirl_api.py "角色名" --search     # search candidate page titles
python scripts/moegirl_api.py "角色名" --full       # full plaintext extract
python scripts/moegirl_api.py "角色名" --wikitext   # raw wikitext
```

There is no build step, test suite, or linting — this is a SKILL.md pipeline repo, not an application.

## Architecture

### CSP Meta-Skill Pipeline (8 steps)

When a user says "generate a skill for X character", CSP runs:

1. **Requirement confirmation** — character name, series, focus direction
2. **Directory creation** — `.claude/skills/<slug>/` with `references/research/` subdir
3. **5 parallel research agents** — Setting (01), Personality (02), Expression (03), Relationships (04), Key Scenes (05). Each writes its findings to `references/research/0X-*.md`
4. **Research quality checkpoint** — `merge_research.py` summarizes source counts, key findings, contradictions, missing dimensions
5. **Behavioral distillation** — extract behavior patterns (dual verification: cross-scene recurrence + executability), expression texture, social cognition, decision logic
6. **Distillation confirmation** — user reviews extracted patterns before assembly
7. **SKILL.md assembly** — fill `references/skill-template.md` from distillation results
8. **Quality verification** — `quality_check.py` runs 7 checks; spawn sub-agent for known-scene replay and edge-case inference

### Key Files

| File | Role |
|------|------|
| `SKILL.md` | The CSP meta-skill itself — triggers on `/csp` or "生成XX的skill" |
| `references/skill-template.md` | Template for generated character SKILL.md files |
| `references/distillation-framework.md` | Methodology for extracting behavior patterns from research |
| `scripts/quality_check.py` | Quality verification for generated skills (7 checks) |
| `scripts/merge_research.py` | Summarize research results from references/research/ directory |
| `scripts/moegirl_api.py` | Fetches Moegirl Wiki entries via MediaWiki API. Use when `WebFetch` is blocked by safety verification. Supports `--intro`, `--full`, `--search`, `--wikitext` modes. Outputs JSON to stdout. |

### Generated Skill Structure

Each character skill is a self-contained directory:

```
<character-slug>/
├── SKILL.md                    # Executable behavior instructions
└── references/
    └── research/
        ├── 01-setting.md       # World, identity, appearance
        ├── 02-personality.md   # Behavior patterns, contradictions
        ├── 03-expression.md    # Speech texture, language markers, canonical lines
        ├── 04-relationships.md # Social cognition, relationship dynamics
        └── 05-key-scenes.md    # Pivotal moments, decision logic under pressure
```

Skills must be **self-contained** — copying the directory is all that's needed to install.

### Design Principles

- **Executable, not taxonomic** — describe HOW a character behaves, not WHAT labels apply. "Deflects personal topics with sarcasm" not "archetype: tsundere"
- **Contradictions > consistency** — preserve inner conflicts; they're the source of depth
- **Behavior > adjectives** — every pattern answers "in what situation → does what → why"
- **Honest about limits** — never fabricate when sources are thin; label gaps explicitly
- **Source-grounded** — all research cites URLs; Moegirl Wiki > Wikipedia > Bangumi > AniDB > Fandom; Zhihu, WeChat, Baidu Baike permanently excluded

### Skill Deployment

Generated skills live in `examples/<slug>/` (source) and are copied to `.claude/skills/<slug>/` (installed). The `.claude/` directory is gitignored.

Pre-built examples currently in `examples/`:

- `csp/` — CSP's own self-skill (a CSP-distilled version of CSP). **Self-contained**: bundles its own copies of `scripts/` and `references/` so the skill works standalone when installed. When editing the canonical pipeline files at the repo root (`SKILL.md`, `references/*.md`, `scripts/*.py`), keep `examples/csp/` in sync — otherwise the installable CSP diverges from source. See commit `c8a9d68` for the self-containment fix.
- BanG Dream! It's MyGO!!!!! members: `takamatsu-tomori/`, `taki-shiina/`, `kaname-rana/`, `nagasaki-soyo/`, `chihaya-anon/`
- BanG Dream! Ave Mujica members (cross-media with MyGO via CRYCHIC backstory): `togawa-sakiko/`, `mutsumi-wakaba/`, `misumi-uika/`, `yutenji-nyamu/`, `yahata-umiri/`

### Cross-Media Franchises

`SKILL.md` has a dedicated branch for "跨作品/跨团角色" (cross-work / cross-band characters) — applies to BanG Dream!, Love Live!, Project Sekai, 少女☆歌剧, etc. For these characters the pipeline expands:

- Agent 1 (Setting) and Agent 4 (Relationships) must search across all related works the character appears in (anime + spinoff anime + mobile game + stage adaptations).
- Game/spinoff content (Garupa card stories, Bestdori event scripts, area dialogues) is a legitimate research source at "medium" priority — same tier as Bangumi/AniDB. It's often the richest source of *daily-life* behavior that the main anime doesn't have screen time for.
- The honesty boundary must declare which works/media the research covered and which it didn't (e.g., "anime only, no Garupa events").

This is a real architectural branch, not scope creep — Sakiko/Mutsumi skills explicitly span MyGO + Ave Mujica + CRYCHIC backstory, and stripping cross-media research would make them shallow. Don't simplify the pipeline by removing this when working in this domain.

### Language Strategy

CSP meta-skill body and generated character skills are in **Chinese** (target users are Chinese-speaking). PRD and planning docs are in English. Japanese and English names/lines are preserved in original where appropriate.
