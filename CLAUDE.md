# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

CSP (Character Skill Producer) is an open-source **meta-skill** — a SKILL.md file that gives Claude Code the ability to generate anime/game character role-playing skills. When loaded, the agent can search authoritative sources (Moegirl Wiki, Wikipedia, Fandom Wiki, Bangumi), cross-validate findings, distill behavior patterns, and produce executable character SKILL.md files.

The repo is at `github.com/qian-gugugaga/-Character_Skill_Producer`. Generated skills follow the AgentSkills standard (YAML frontmatter + Markdown body).

## Commands

```bash
# Quality-check a generated skill (7 checks: behavior patterns, expression, contradictions, etc.)
python scripts/quality_check.py <path/to/SKILL.md>

# Summarize research results from references/research/ directory
python scripts/merge_research.py <skill_directory>
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
| `PRD.md` | Product definition (English) — core goals, competitive landscape, schema |
| `references/skill-template.md` | Template for generated character SKILL.md files |
| `references/distillation-framework.md` | Methodology for extracting behavior patterns from research |
| `push_api.py` | One-off: push to GitHub via REST API when git protocol is blocked |

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

Generated skills live in `examples/<slug>/` (source) and are copied to `.claude/skills/<slug>/` (installed). The `.claude/` directory is gitignored. Pre-built examples include characters from BanG Dream! It's MyGO!!!!! (Tomori, Taki, Rana, Soyo, Anon).

### Language Strategy

CSP meta-skill body and generated character skills are in **Chinese** (target users are Chinese-speaking). PRD and planning docs are in English. Japanese and English names/lines are preserved in original where appropriate.
