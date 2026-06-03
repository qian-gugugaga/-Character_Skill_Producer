<div align="center">

# Character Skill Producer

> *"Stop writing character profiles. Let the character speak."*

**Status:** Agent Skills standard · Claude Code runtime · MIT License

<br>

**CSP turns anime and game characters into runnable Agent Skills.**

Give it a character name and a series. It researches, cross-validates, distills behavior patterns, and generates an installable `SKILL.md` you can talk to directly.

Not a character card. Not a lore sheet. Not a pile of labels like "tsundere" or "cool and distant".

It captures **how the character reacts, speaks, reads other people, makes decisions, and where they must admit they do not know.**

[Examples](#examples) · [Install](#install) · [What CSP Distills](#what-csp-distills) · [How It Works](#how-it-works) · [Included Characters](#included-characters)

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
> Distill Maki Shiina from BanG Dream! It's MyGO!!!!!
> Make a Gojo Satoru character skill
```

CSP turns character information into executable behavior. Once generated, a character skill can be invoked like this:

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

This is not quote stitching. CSP distills the behavioral logic underneath the character.

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

- Python, for the Moegirl Wiki MediaWiki API helper
- Web search capability, for Wikipedia, Fandom Wiki, Bangumi, Bilibili, and fallback sources

```bash
python scripts/moegirl_api.py "Yahata Umiri"
python scripts/moegirl_api.py "Yahata Umiri" --search
python scripts/moegirl_api.py "Yahata Umiri" --full
```

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

## What CSP Distills

A normal character card says:

> Personality: calm, reliable, distant.

CSP writes something executable:

> When asked for a long-term commitment, she translates the relationship into tasks first: rehearsal frequency, exit conditions, who coordinates. Not because she does not care, but because operational boundaries protect her from emotional expectations she cannot control.

CSP extracts five layers:

| Layer | Question |
|---|---|
| **Behavior dynamics** | What does the character do in which situation? How do they change under pressure? |
| **Expression texture** | Sentence length, pauses, pronouns, speech markers, honorific distance |
| **Social cognition** | How do they read kindness, threat, closeness, and betrayal? |
| **Decision logic** | What do they protect first when values collide? |
| **Honest limits** | What does the character not know? What does the source material not support? |

**CSP is not trying to be a better wiki. It is trying to make the character feel alive.**

---

## How It Works

**1. Multi-source research** — Moegirl Wiki, Wikipedia, Fandom Wiki, Bangumi, AniDB, Bilibili, game stories, and user-provided materials. Zhihu, WeChat articles, and Baidu Baike are excluded by default.

**2. Five parallel research tracks** — setting, personality, expression, relationships, and key scenes are investigated separately.

**3. Behavioral distillation** — raw events become reusable behavior patterns. Contradictions are preserved instead of flattened.

**4. Quality validation** — the generated skill is checked for executability, expression texture, preserved contradictions, honest limits, and complete role-play rules.

```bash
python scripts/quality_check.py examples/yahata-umiri/SKILL.md
python scripts/merge_research.py examples/yahata-umiri/
```

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
