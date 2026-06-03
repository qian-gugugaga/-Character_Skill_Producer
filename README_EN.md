<div align="center">

# Character Skill Producer

### Turn anime and game characters into runnable Agent Skills.

> *"Stop writing character profiles. Let the character speak."*

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Standard-green)](https://agentskills.io)
[![Runtime-Claude Code](https://img.shields.io/badge/Runtime-Claude%20Code-blueviolet)](#install)
[![Local Research](https://img.shields.io/badge/Local%20Research-Moegirl%20API-orange)](#local-research-first)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

<br>

**CSP distills anime, manga, and game characters into behavior skills for chat, writing, and interactive storytelling.**

Give it a character name and a series. CSP researches sources, cross-validates evidence, distills behavior patterns, runs quality checks, and generates a dated `SKILL.md` with source boundaries and an update path.

Use it today for character chat, fanfiction drafting, and scene/dialogue prototyping. In the future, it can become the character-behavior layer for AI interactive fiction, character-driven games, and anime/game creation workflows.

[Examples](#examples) · [Product Philosophy](#product-philosophy) · [Future Scenarios](#future-scenarios) · [Install](#install) · [How It Works](#how-it-works) · [Research Dates](#research-dates-and-updates)

<br>

**Other Languages:**

[中文](README.md) · [日本語](README_JA.md) · [한국어](README_KO.md) · [Español](README_ES.md)

</div>

---

## Examples

You do not need prompt engineering or a hand-written lore pack.

Just say:

```text
> Generate a Misaka Mikoto skill from A Certain Scientific Railgun
> Distill Togawa Sakiko from BanG Dream! Ave Mujica
> Make a Hitori Gotoh character skill from Bocchi the Rock!
```

Once generated, a character skill can be invoked like this:

```text
User    ❯ Talk from Umiri's perspective. Why would someone support so many bands?

Umiri  ❯ Because that makes things clear.
          Rehearsal today, show tomorrow, then it ends.
          I do what is needed.

          Long-term relationships are harder.
          People start expecting you to stay. They ask what this place means to you.

          ...But if you only ever support others, it gets a little empty.
          I know that.
```

This is not quote stitching. CSP distills the behavioral logic underneath the character: how they handle relationships, pressure, boundaries, and choices.

---

## Product Philosophy

CSP treats a character as **a runnable reaction system**, not a static profile page.

A wiki tells you what happened to a character. A character card tells you their rough traits. CSP goes further: when the character enters a situation the original work never wrote, what do they notice first, what do they misunderstand, what do they protect, what do they refuse, and what rhythm do they use to speak?

| What CSP encodes | What it means |
|---|---|
| Behavior lens | What the character notices and ignores |
| Reaction rules | When they approach, retreat, attack, or go silent |
| Expression DNA | Sentence length, pauses, honorific distance, pronouns, emotional leakage |
| Relationship algorithm | How they read kindness, betrayal, closeness, and being used |
| Decision boundary | What they protect first when values collide |
| Honest limits | What they do not know, what is outdated, what is only inference |

**What can be encoded becomes behavior. What cannot be encoded becomes a boundary.** That boundary is part of immersion: believable characters do not know everything and do not always answer beautifully.

---

## Future Scenarios

CSP provides a shared character-behavior infrastructure for creators.

Today, it can be used for:

| Scenario | Use | What CSP provides |
|---|---|---|
| Character chat | Talk with a character over time | Stable voice, relationship distance, knowledge boundary |
| Fanfiction writing | Draft dialogue, inner monologue, and short scenes | Behavioral logic, not just lines |
| Scene prototyping | Place a character in a new situation | Inferred reactions based on behavior patterns |
| Character study | Compare how characters handle pressure and relationships | Traceable sources and distillation chain |
| Multi-character scenes | Load multiple characters into one event | Independent boundaries and decision logic |

Future directions:

| Direction | Possible form |
|---|---|
| AI interactive fiction | Characters respond consistently to player actions |
| AI visual novel / galgame prototypes | Character skills drive branching dialogue, affection shifts, and conflict escalation |
| Multi-character narrative experiments | Several skills collide in one event to generate ensemble drama |
| Creator workbench | Writers test scenes, rewrite dialogue, and check OOC drift |
| Updatable character files | New story releases update research dates and behavior patterns |

CSP gives creators a reusable character behavior layer. It serves chat and fan writing today; it can become part of AI interactive fiction, character-driven games, and anime/game creation tooling.

---

## Local Research First

CSP's direction is: **core sources should be fetched by repository scripts first; external web search is a supplement.**

Current examples:

```bash
python scripts/source_search.py "高松灯" --work "BanG Dream! It's MyGO!!!!!" --mode discover
python scripts/source_search.py "能天使" --work "明日方舟" --sources moegirl
python scripts/moegirl_api.py "高松灯" --search
python scripts/moegirl_api.py "能天使" --full
```

Current local research focuses on the Moegirl Wiki MediaWiki API through `source_search.py`. More adapters such as Bangumi, Fandom, Wikipedia, Bestdori, and BWIKI can be added later. When an adapter is missing or fails, CSP records the failure and allows web search or user materials to fill the gap.

---

## Install

CSP is a Claude Code / Agent Skills style meta-skill. Install the self-contained version:

```bash
skills add qian-gugugaga/Character_Skill_Producer
```

Or install manually:

```bash
git clone https://github.com/qian-gugugaga/Character_Skill_Producer.git
cp -r Character_Skill_Producer/examples/csp ~/.claude/skills/csp
```

`examples/csp/` already includes the scripts and templates it needs.

### Requirements

- Python, for local research, metadata generation, and quality checks
- Web search capability as an optional fallback when local scripts cannot cover a source

---

## Usage

After installation, tell Claude Code:

```text
> /csp
> Generate a Chihaya Anon skill
> Distill Togawa Sakiko from BanG Dream! Ave Mujica
> Make a Bocchi character skill from Bocchi the Rock!
```

Vague requests work too:

```text
> I want to talk to a tsundere character
> Recommend a yandere character
> Make me a character suitable for long conversations
```

If you have official materials, interviews, subtitles, screenshots, or game story text, give them to CSP. User-provided official material has the highest priority.

---

## How It Works

CSP defaults to highest-fidelity generation.

**1. Local source discovery** — Run `scripts/source_search.py` and site adapters before using external search.

**2. Structured source index** — Write `references/sources.json` with URLs, source tiers, retrieval dates, failures, and optional content hashes.

**3. Five research tracks** — Setting, personality, expression, relationships, and key scenes are investigated separately.

**4. Behavioral distillation** — Raw events become reusable behavior patterns. Contradictions are preserved instead of flattened.

**5. Metadata and boundaries** — Generate `manifest.json` with research dates, covered media, uncovered material, quality score, and honesty boundary.

**6. Quality validation** — Check executability, expression texture, contradictions, honest limits, research dates, and role-play rules.

```bash
python scripts/quality_check.py examples/yahata-umiri/
python scripts/merge_research.py examples/yahata-umiri/
python scripts/generate_manifest.py examples/yahata-umiri/
```

---

## Research Dates and Updates

Every generated character skill records its research completion date.

When a new episode, game event, line, interview, or setting revision appears after that date, the old skill may not cover it. The character should then say:

```text
My materials are updated through YYYY-MM-DD, so I may not cover content released after that. If you have the latest CSP or can provide new story / source links, I can help update this Skill; this may consume some tokens.
```

CSP updates old skills by reading `manifest.json` and `sources.json`, re-checking core sources, re-distilling affected dimensions, and refreshing the research date and quality report.

---

## Included Characters

| Character | Series | Directory |
|---|---|---|
| Takamatsu Tomori | BanG Dream! It's MyGO!!!!! | `examples/takamatsu-tomori/` |
| Shiina Taki | BanG Dream! It's MyGO!!!!! | `examples/taki-shiina/` |
| Kaname Rana | BanG Dream! It's MyGO!!!!! | `examples/kaname-rana/` |
| Nagasaki Soyo | BanG Dream! It's MyGO!!!!! | `examples/nagasaki-soyo/` |
| Chihaya Anon | BanG Dream! It's MyGO!!!!! | `examples/chihaya-anon/` |
| Togawa Sakiko | BanG Dream! Ave Mujica | `examples/togawa-sakiko/` |
| Mutsumi Wakaba | BanG Dream! Ave Mujica | `examples/mutsumi-wakaba/` |
| Misumi Uika | BanG Dream! Ave Mujica | `examples/misumi-uika/` |
| Yutenji Nyamu | BanG Dream! Ave Mujica | `examples/yutenji-nyamu/` |
| Yahata Umiri | BanG Dream! Ave Mujica | `examples/yahata-umiri/` |
| CSP self-skill | — | `examples/csp/` |

---

## License

MIT

---

<div align="center">

**Lore tells you what a character is.**<br>
**CSP teaches the character how to live.**

<br>

*Stop writing character profiles. Let the character speak.*

</div>
