# Character Skill Producer (CSP)

## 1. Product Definition

CSP is an open-source **meta-skill** (a SKILL.md file) that enables LLM-based agents (Claude Code, Codex) to generate, edit, and share anime/game character role-playing skills.

CSP itself is installable as a skill — once loaded, the agent gains the ability to produce new character skills on demand.

---

## 2. Core Goal

Transform anime/game fictional characters into:

> **executable agent behavior packages** — not static character profiles, not taxonomic labels.

A character skill, when loaded by an agent, must make the agent *think, decide, speak, and perceive* like that character.

---

## 3. Domain Focus

**Anime, manga, and game fictional characters only.**

This is not a general-purpose character tool. CSP is laser-focused on the 二次元 domain to achieve authoritative depth rather than superficial breadth.

---

## 4. What is a Character Skill?

A character skill is a standard SKILL.md file (YAML frontmatter + Markdown body) containing executable behavioral instructions:

- **Identity & world context** — who they are, what world they inhabit
- **Behavioral dynamics** — how they act under different conditions (NOT archetype labels like "tsundere")
- **Decision logic** — what they optimize for, decision priorities, hard constraints
- **Expression texture** — how they construct sentences, vocabulary range, pace, how emotion leaks through word choice
- **Social cognition** — how they perceive others, what they notice vs. miss, relationship templates
- **Knowledge boundaries** — what they know and don't know in-world

### Design Principle: Executable, Not Taxonomic

Every section must be an **actionable behavioral instruction** the LLM can directly execute.

**Bad** (label-based):
```yaml
archetype: tsundere
speech_quirk: desu-wa
```

**Good** (executable):
```markdown
- Default mode: maintains emotional distance; deflects personal topics with sarcasm
- When target of affection is in genuine trouble: drops facade instantly, acts decisively,
  then later rationalizes it as "the obvious thing anyone would do"
- Never admits affection directly; shows it through actions the target is unlikely to notice
```

Tags exist only for discoverability, never to drive behavior.

---

## 5. Key Differentiators

### 5.1 Web-Search-First Pipeline

CSP **requires a web search skill** as a dependency. Before generating any skill:

1. Search authoritative sources (Moegirl Wiki, Wikipedia, Bangumi, AniDB, Fandom)
2. Cross-validate across at least 2 independent sources
3. Classify all evidence: CONFIRMED / DISPUTED / FANON
4. Only then distill into a skill

This ensures generated skills are grounded in canonical material, not LLM hallucination.

### 5.2 Anime Domain Authority

Deep understanding of anime character conventions — not through hard-coded tag dictionaries, but through search-verified source material and domain-aware distillation.

### 5.3 Community-Ready Output

Generated skills are single-file SKILL.md files following the AgentSkills standard. They are:
- Git-friendly and diffable
- Installable by any Claude Code / Codex user
- Forkable, modifiable, recombinable
- Ready for GitHub community sharing

---

## 6. Competitive Landscape

Two ecosystems exist, and CSP serves the Agent Skills ecosystem:

| Ecosystem | Format | Use Case | Representative |
|-----------|--------|----------|----------------|
| Roleplay Chat | V2/V3 JSON/PNG character cards | Chat frontends (SillyTavern, Chub) | SillyTavern (25K⭐) |
| Agent Skills | SKILL.md (YAML + Markdown) | Agent reasoning (Claude Code, Codex) | AgentSkills standard |

**Gaps CSP fills:**

| Gap | Existing State | CSP Approach |
|-----|---------------|---------------|
| Fictional character distillation | Most projects target real people | Anime/game characters only |
| Source-driven generation | Relies on LLM training data | Web search required as pipeline step 1 |
| Executable behavioral format | Character cards use taxonomic tags | Behavioral descriptions the LLM can directly execute |

---

## 7. System Components

### 7.1 CSP Meta-Skill

The CSP skill is a SKILL.md file with supporting references:

```
csp/
├── SKILL.md                              # Main entry point — full pipeline
├── PRD.md                                # Product definition (this file)
├── references/
│   ├── distillation-framework.md         # Behavioral distillation methodology
│   └── skill-template.md                 # Output template for generated skills
└── scripts/
    ├── quality_check.py                  # Quality validation (7 checks)
    └── merge_research.py                 # Research summary generator
```

When installed, the agent gains a character skill generation capability triggered by phrases like "generate a skill for X" or "distill X character."

**Dependency**: User must have a web search skill installed.

### 7.2 Skill Generator (Distiller)

Pipeline:
```
User input (character name + series)
  → Step 1: Requirement confirmation
  → Step 2: Create skill directory structure
  → Step 3: 5 parallel research agents (Setting / Personality / Expression / Relationships / Key Scenes)
  → Step 4: Research quality checkpoint (user confirms)
  → Step 5: Behavioral distillation (synthesis with dual verification)
  → Step 6: Distillation confirmation checkpoint
  → Step 7: SKILL.md assembly (using skill-template.md)
  → Step 8: Quality verification (known scene replay + edge case inference)
  → Deliver
```

Generation is powered by the host agent's LLM, guided by CSP instructions. Source priority: Moegirl Wiki > Wikipedia > Bangumi > AniDB > Fandom. Zhihu, WeChat public accounts, and Baidu Baike are permanently excluded.

### 7.3 Skill Editor

Natural language modification of existing character skills:
- "Make them more sarcastic" → updates Expression Texture section
- "Add their backstory with their rival" → updates Identity + Social Cognition
- "They wouldn't say that, they'd stay silent" → updates Behavioral Dynamics

System updates the skill incrementally, preserving version history through git.

### 7.4 Storage Format

```
<character-slug>/
  ├── SKILL.md                    # Single file output
  └── references/
      └── research/               # Research artifacts (kept for transparency)
```

Generated skill is single-file for maximum shareability. Follows AgentSkills standard exactly.

---

## 8. Generated Skill Schema

### YAML Frontmatter

```yaml
name: <slug>
description: <one-line character summary with source series, Chinese>
license: CC-BY-4.0
compatibility: claude-code, codex
metadata:
  source_series: <canonical name>
  source_series_en: <English name>
  confidence: high | medium
  evidence_sources:
    - <URL>
  tags: [<discoverability only>]
```

### Markdown Body Sections

1. **角色扮演规则（Role-Playing Rules）** — First-person immersion, exit triggers, one-time disclaimer
2. **身份卡（Identity Card）** — Who they are, world context, first impression, in their own voice
3. **行为动态（Behavioral Dynamics）** — Default state, under stress, around different people, core contradictions
4. **表达质感（Expression Texture）** — Sentence construction, vocabulary, language markers, pace, emotional leakage, canonical lines
5. **社会认知（Social Cognition）** — Perception defaults, what they notice/miss, relationship templates
6. **决策逻辑（Decision Logic）** — Core motivation, value priorities, hard constraints
7. **知识边界（Knowledge Boundaries）** — In-world knowns and unknowns, uncertainty handling
8. **行为示例（Behavioral Examples）** — 3-5 scenarios: context → internal thought → external action
9. **诚实边界（Honesty Boundary）** — Specific limitations, research date
10. **调研来源（Research Sources）** — Attribution and source links

---

## 9. Non-Goals

This project does NOT include:
- Game runtime system
- Multi-agent simulation world
- Narrative engine
- Player interaction system
- Character card (V2/V3 PNG) generation — focus is SKILL.md only
- Real-person distillation — focus is anime/game fictional characters

---

## 10. Future Vision

Skill becomes the standard way to share anime character agents:
- A GitHub repo is a character marketplace
- Fork a character, tweak their personality, share your version
- Characters are composable — load multiple for multi-character scenarios
- Zero-friction install: one `skills add` command and the character is alive in your agent

---

## 11. Language Strategy

Three-tier approach:

| Tier | Scope | Language | Reason |
|------|-------|----------|--------|
| 1 | PRD & planning docs | English | Precision, no translation ambiguity |
| 2 | CSP meta-skill body | **Chinese** | Target users are Chinese-speaking |
| 3 | Generated character skills | **Chinese** (primary), JP/EN adaptive | LLMs handle multi-language naturally |

CSP is built for Chinese users first. The meta-skill instructions and generated character behavior descriptions default to Chinese. Japanese and English character names, source materials, and canonical lines are preserved in their original language where appropriate.

Source research prioritizes Chinese wikis (Moegirl Wiki) for Chinese-speaking character communities, but searches across languages when needed.

---

## 12. Acknowledgements

CSP's architecture — multi-agent parallel research, phased checkpoints, and quality verification — is inspired by [nuwa-skill](https://github.com/alchaincyf/nuwa-skill) (女娲·Skill造人术), the pioneering work in LLM-based persona distillation. CSP adapts these patterns to a fundamentally different domain: anime character behavioral distillation (role-playing) vs. real-person cognitive framework distillation (thinking advisor).
