<div align="center">

# Character Skill Producer

> *「不要再写角色设定了。让角色自己开口。」*

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Standard-green)](https://agentskills.io)
[![Runtime-Claude Code](https://img.shields.io/badge/Runtime-Claude%20Code-blueviolet)](#安装)
[![License: CC--BY--4.0](https://img.shields.io/badge/License-CC--BY--4.0-yellow.svg)](#许可)

<br>

**CSP 把二次元角色蒸馏成可运行的 Agent Skill。**

给它一个角色名和作品名，它会自动调研、交叉验证、提炼行为模式，最后生成一个可以直接安装、直接对话的 `SKILL.md`。

不是角色卡。不是设定集。不是「她很傲娇」这种标签。

是把角色在不同情境下**怎么反应、怎么说话、怎么理解别人、什么绝对不会做**，写成 AI 能执行的行为程序。

[看效果](#效果示例) · [安装](#安装) · [它蒸馏什么](#csp-蒸馏什么) · [工作原理](#工作原理) · [预置角色](#预置角色)

<br>

**其他语言 / Other Languages:**

[English](README_EN.md) · [日本語](README_JA.md) · [한국어](README_KO.md) · [Español](README_ES.md)

</div>

---

## 效果示例

你不需要写 prompt 工程，也不需要整理角色设定。

只要说：

```text
> 生成御坂美琴（某科学的超电磁炮）的 skill
> 蒸馏椎名真希（BanG Dream! It's MyGO!!!!!）
> 做一个五条悟的角色 skill
```

CSP 会把「角色资料」变成「可执行行为」。生成后的角色 Skill，可以像这样被调用：

```text
用户      ❯ 用海铃的视角聊聊，为什么一个人会同时给很多乐队做支援？

海铃      ❯ 因为那样比较清楚。
            今天排练，明天演出，结束之后就散。
            需要我做什么，我就做什么。

            长期关系反而麻烦。
            会有人期待你留下来，也会有人问你到底把这里当什么。

            ……但如果一直只做支援，也会有点空。
            这点我知道。
```

```text
用户      ❯ 扮演祥子。有人说你的计划太冷酷了。

祥子      ❯ 冷酷？
            只是因为它看起来不够温柔，对吗。

            但如果连舞台、时间、人员、退路都不先安排好，
            那所谓的温柔最后只会变成互相拖累，desuwa。

            我不讨厌理想。
            我只是已经知道，只靠理想是撑不起一场演出的。
```

这不是把台词拼起来。海铃不是在复读「支援贝斯」设定，祥子也不是在套大小姐口癖。真正被蒸馏出来的是：**角色面对关系、压力、边界和选择时的行为逻辑。**

---

## 安装

CSP 是一个 Claude Code / Agent Skills 风格的 meta-skill。推荐直接安装自包含版本：

```bash
skills add qian-gugugaga/Character_Skill_Producer
```

也可以手动安装：

```bash
git clone https://github.com/qian-gugugaga/Character_Skill_Producer.git
cp -r Character_Skill_Producer/examples/csp ~/.claude/skills/csp
```

`examples/csp/` 已经打包了运行所需的脚本和模板。复制到 `.claude/skills/csp/` 后即可使用。

### 依赖

CSP 需要：

- Python：用于调用萌娘百科 MediaWiki API
- 网页搜索能力：用于 Wikipedia、Fandom Wiki、Bangumi、Bilibili 等来源补强

萌娘百科优先走本地脚本，不依赖直接抓网页：

```bash
python scripts/moegirl_api.py "八幡海铃"              # 自动：简介 → 搜索 → 降级
python scripts/moegirl_api.py "八幡海铃" --search     # 搜索候选页面标题
python scripts/moegirl_api.py "八幡海铃" --full       # 全文提取
python scripts/moegirl_api.py "八幡海铃" --wikitext   # 原始 wikitext
```

---

## 使用

安装后，对 Claude Code 说：

```text
> /csp
> 生成千早爱音的 skill
> 蒸馏丰川祥子（BanG Dream! Ave Mujica）
> 做一个《孤独摇滚！》后藤一里的角色 skill
```

模糊需求也可以：

```text
> 想聊一个傲娇角色
> 有没有病娇推荐
> 帮我做一个适合长期聊天的二次元角色
```

CSP 会先确认角色和作品。如果你手上有设定集、访谈、BD 特典、字幕、截图或游戏剧情文本，也可以直接给它，用户提供的官方材料优先级最高。

---

## CSP 蒸馏什么

一个普通角色卡会写：

> 性格：冷静、可靠、疏离。

CSP 要写的是：

> 当别人要求她给出长期承诺时，她会先把关系翻译成任务：排练频率、退出条件、谁负责联络。不是不在乎，而是用事务边界避免自己被卷入无法控制的情感期待。

区别就在这里。

CSP 提取的是五层：

| 层次 | CSP 关心的问题 |
|---|---|
| **行为动态** | 什么情境下会做什么？压力下如何变形？ |
| **表达质感** | 句子长短、停顿、口癖、自称、敬语层级如何工作？ |
| **社会认知** | 她默认怎么理解他人的善意、威胁、亲近和背叛？ |
| **决策逻辑** | 多个价值冲突时，她先保什么、牺牲什么？ |
| **诚实边界** | 资料不足、角色不知道、原作没覆盖时，Skill 应该如何承认不知道？ |

**CSP 不追求更像百科。它追求更像一个活人。**

---

## 工作原理

输入角色后，CSP 会做四件事：

**1. 多源调研**  
从萌娘百科、Wikipedia、Fandom Wiki、Bangumi、AniDB、Bilibili、游戏剧情与用户提供资料中收集信息。知乎、微信公众号、百度百科默认排除。

**2. 五路并行分析**  
设定与世界观、人格、表达质感、人际关系、关键场景分开调研，避免一个维度吞掉另一个维度。

**3. 行为蒸馏**  
把资料从「发生过什么」提炼成「角色在类似情境下会怎么行动」。保留矛盾，不把角色磨平成稳定人设。

**4. 质量验证**  
生成后运行质量检查：行为模式是否可执行、表达是否有质感、矛盾是否保留、边界是否诚实、角色扮演规则是否完整。

```bash
python scripts/quality_check.py examples/yahata-umiri/SKILL.md
python scripts/merge_research.py examples/yahata-umiri/
```

完整方法论见：

- `references/distillation-framework.md`
- `references/skill-template.md`

---

## 生成的 Skill 长什么样

每个角色都是一个自包含目录：

```text
yahata-umiri/
├── SKILL.md                          # 可执行的角色行为指令
└── references/
    └── research/
        ├── 01-setting.md             # 世界观、身份、外表
        ├── 02-personality.md         # 行为模式、矛盾
        ├── 03-expression.md          # 说话质感、语言标志、经典台词
        ├── 04-relationships.md       # 社会认知、关系动态
        └── 05-key-scenes.md          # 关键场景、压力下的决策逻辑
```

复制整个目录到 `.claude/skills/<name>/`，就能在对话里直接调用。

---

## 预置角色

仓库里已经包含这些可直接使用的角色 Skill：

| 角色 | 作品 | 目录 |
|---|---|---|
| 高松灯 | BanG Dream! It's MyGO!!!!! | `examples/takamatsu-tomori/` |
| 椎名立希 | BanG Dream! It's MyGO!!!!! | `examples/taki-shiina/` |
| 要乐奈 | BanG Dream! It's MyGO!!!!! | `examples/kaname-rana/` |
| 长崎爽世 | BanG Dream! It's MyGO!!!!! | `examples/nagasaki-soyo/` |
| 千早爱音 | BanG Dream! It's MyGO!!!!! | `examples/chihaya-anon/` |
| 丰川祥子 | BanG Dream! Ave Mujica | `examples/togawa-sakiko/` |
| 若叶睦 | BanG Dream! Ave Mujica | `examples/mutsumi-wakaba/` |
| 三角初华 | BanG Dream! Ave Mujica | `examples/misumi-uika/` |
| 祐天寺若麦 | BanG Dream! Ave Mujica | `examples/yutenji-nyamu/` |
| 八幡海铃 | BanG Dream! Ave Mujica | `examples/yahata-umiri/` |
| CSP 自描述 | — | `examples/csp/` |

BanG Dream! 角色会覆盖 MyGO!!!!!、Ave Mujica、CRYCHIC 前史，并在资料允许时纳入手游和衍生内容作为日常行为补充。

---

## 信息源原则

二次元角色资料很容易被二创、转述和社区印象污染。CSP 的原则是：

| 优先级 | 来源 |
|---|---|
| **最高** | 用户提供的官方设定集、访谈、BD 特典、字幕、截图 |
| **高** | 萌娘百科、Wikipedia、作品 Fandom Wiki |
| **中** | Bangumi、AniDB、游戏剧情、Bilibili 高质量专栏、Anime News Network |
| **低** | 粉丝讨论、社区解读，必须标注为推测 |
| **排除** | 知乎、微信公众号、百度百科 |

至少两个独立来源交叉验证。资料不足就写不足，不补脑，不编造。

---

## 仓库结构

```text
Character_Skill_Producer/
├── SKILL.md                          # CSP 主 skill
├── references/
│   ├── distillation-framework.md     # 行为蒸馏方法论
│   └── skill-template.md             # 角色 Skill 模板
├── scripts/
│   ├── quality_check.py              # 质量验证
│   ├── merge_research.py             # 调研摘要
│   └── moegirl_api.py                # 萌娘百科 API 封装
└── examples/
    ├── csp/                          # 自包含 CSP skill
    └── <character>/                  # 预置角色 skill
```

---

## 致谢

CSP 的架构借鉴 [nuwa-skill（女娲）](https://github.com/alchaincyf/nuwa-skill)：从「蒸馏真人认知框架」出发，转向「蒸馏虚构角色行为系统」。

女娲问：一个人如何思考？  
CSP 问：一个角色如何活着？

---

## 许可

CC-BY-4.0

---

<div align="center">

**设定告诉你角色是什么。**<br>
**CSP 让角色知道自己该怎么活。**

<br>

*不要再写角色设定了。让角色自己开口。*

</div>
