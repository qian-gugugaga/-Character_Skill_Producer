# Character Skill Producer (CSP)

> 把二次元角色变成可运行的 agent 行为包。

CSP 是一个 Claude Code 的 meta-skill。安装之后，你的 agent 就多了一项能力：给它一个角色名和作品名，它会自动去萌娘百科、Wikipedia、Fandom Wiki 这些地方搜资料，交叉验证，蒸馏行为模式，最后生成一个可以直接运行的角色扮演 SKILL.md。

不是角色卡，不是设定集。是让 agent "像那个人一样思考、判断、说话"的行为程序。

## 安装

```bash
# Claude Code 用户
skills add qian-gugugaga/Character_Skill_Producer

# 或者手动
git clone https://github.com/qian-gugugaga/Character_Skill_Producer.git
cp -r examples/csp ~/.claude/skills/csp
```

CSP 是自包含的——`examples/csp/` 里打包了它需要的所有脚本和模板。复制到 `.claude/skills/csp/` 就能用，不用装别的东西。

## 怎么用

装好之后，跟 agent 说类似这样的话就行：

```
> 生成御坂美琴（某科学的超电磁炮）的 skill
> 蒸馏椎名真希（BanG Dream! It's MyGO!!!!!）
> 做一个五条悟的角色 skill
```

甚至模糊需求也行：

```
> 想聊一个傲娇角色
> 有没有病娇推荐
```

CSP 会启动 5 个并行 agent，分别负责设定、性格、表达质感、人际关系、关键场景这五个维度的调研。调研完成后交叉验证，蒸馏出行为模式，最后拼装成 SKILL.md。整个过程大概需要几分钟，取决于角色资料的丰富程度。

## 依赖

需要一个网页搜索 skill（比如 `multi-search-engine`）。CSP 用它来搜 Wikipedia、Fandom Wiki、Bangumi 这些来源。

萌娘百科走 MediaWiki API，不依赖网页搜索。本机需要有 Python，网络能访问 `zh.moegirl.org.cn`。

## 脚本工具

仓库里有三个 Python 脚本，`examples/csp/scripts/` 里有完整副本：

**`scripts/moegirl_api.py`** — 萌娘百科 MediaWiki API 封装。当 WebFetch 被安全验证拦截时用这个。

```bash
python scripts/moegirl_api.py "八幡海铃"              # 自动：简介 → 搜索 → 降级
python scripts/moegirl_api.py "八幡海铃" --search     # 搜索候选页面标题
python scripts/moegirl_api.py "八幡海铃" --full       # 全文提取
python scripts/moegirl_api.py "八幡海铃" --wikitext   # 原始 wikitext
```

**`scripts/quality_check.py`** — 生成的 SKILL.md 质量检查，7 项验证（行为模式、表达质感、矛盾保留、角色扮演规则等）。

```bash
python scripts/quality_check.py examples/yahata-umiri/SKILL.md
```

**`scripts/merge_research.py`** — 从 `references/research/` 目录汇总调研结果，生成来源统计和关键发现摘要。

```bash
python scripts/merge_research.py examples/yahata-umiri/
```

## 生成的 Skill 长什么样

每个角色 skill 是一个独立目录，复制到任何地方都能直接用：

```
yahata-umiri/
├── SKILL.md                          # 可执行的行为指令
└── references/
    └── research/
        ├── 01-setting.md             # 世界观、身份、外表
        ├── 02-personality.md         # 行为模式、矛盾
        ├── 03-expression.md          # 说话质感、语言标志、经典台词
        ├── 04-relationships.md       # 社会认知、关系动态
        └── 05-key-scenes.md          # 关键场景、压力下的决策逻辑
```

SKILL.md 里写的是"什么情况下做什么、为什么这样做"，不是"她是傲娇/病娇/天然呆"。标签给人类看，行为规则给 AI 执行。

## 预置角色

仓库里已经做好的角色 skill（都在 `examples/` 下）：

| 角色 | 作品 | 目录 |
|------|------|------|
| 高松灯 | BanG Dream! It's MyGO!!!!! | `takamatsu-tomori/` |
| 椎名立希 | BanG Dream! It's MyGO!!!!! | `taki-shiina/` |
| 要乐奈 | BanG Dream! It's MyGO!!!!! | `kaname-rana/` |
| 长崎爽世 | BanG Dream! It's MyGO!!!!! | `nagasaki-soyo/` |
| 千早爱音 | BanG Dream! It's MyGO!!!!! | `chihaya-anon/` |
| 丰川祥子 | BanG Dream! Ave Mujica | `togawa-sakiko/` |
| 若叶睦 | BanG Dream! Ave Mujica | `mutsumi-wakaba/` |
| 三角初华 | BanG Dream! Ave Mujica | `misumi-uika/` |
| 祐天寺若麦 | BanG Dream! Ave Mujica | `yutenji-nyamu/` |
| 八幡海铃 | BanG Dream! Ave Mujica | `yahata-umiri/` |
| CSP 自描述 | — | `csp/` |

使用方式：把目录复制到 `.claude/skills/<name>/`，然后用触发词调用。比如装好 `yahata-umiri` 之后，说"用海铃的视角"或"扮演海铃"就行。

BanG Dream! 的角色跨 MyGO!!!!! 和 Ave Mujica 两部动画，加上 CRYCHIC 的前史。调研时会同时覆盖动画、手游（Garupa）、Fandom Wiki 这些来源。

## 信息源优先级

二次元角色的资料来源质量差异很大。CSP 的处理方式：

- 用户提供的官方设定集/访谈/BD 特典（最高）
- 萌娘百科、维基百科、作品 Fandom Wiki（高）
- Bangumi、AniDB、游戏内容（中）
- B站高质量专栏、Anime News Network（中）
- 粉丝讨论、社区解读（低，标注为推测）
- 知乎、微信公众号、百度百科（永久排除，信息失真率太高）

中文源优先，日文/英文源补强。至少 2 个独立来源交叉验证。

## 设计原则

**可执行，不是分类学。** "用讽刺转移私人话题"比"傲娇"有用得多。

**矛盾比一致性重要。** 角色的内在冲突是深度的来源，不要调和它们。

**行为比形容词重要。** 每个模式都回答"什么情境 → 做什么 → 为什么"。

**对局限诚实。** 资料不足就说不足，不编造。每个 skill 都有"诚实边界"一节。

## 项目结构

```
├── SKILL.md                          # CSP 主 skill（触发词：/csp）
├── CLAUDE.md                         # 项目指南
├── README.md                         # 本文件
├── references/
│   ├── distillation-framework.md     # 行为蒸馏方法论
│   └── skill-template.md             # 生成模板
├── scripts/
│   ├── quality_check.py              # 质量验证（7 项检查）
│   ├── merge_research.py             # 调研摘要生成
│   └── moegirl_api.py                # 萌娘百科 API 封装
└── examples/
    ├── csp/                           # CSP 自描述（自包含）
    ├── takamatsu-tomori/              # 高松灯
    ├── taki-shiina/                   # 椎名立希
    ├── kaname-rana/                   # 要乐奈
    ├── nagasaki-soyo/                 # 长崎爽世
    ├── chihaya-anon/                  # 千早爱音
    ├── togawa-sakiko/                 # 丰川祥子
    ├── mutsumi-wakaba/                # 若叶睦
    ├── misumi-uika/                   # 三角初华
    ├── yutenji-nyamu/                 # 祐天寺若麦
    └── yahata-umiri/                  # 八幡海铃
```

## 致谢

架构借鉴 [nuwa-skill（女娲）](https://github.com/alchaincyf/nuwa-skill)——LLM 人格蒸馏的先驱项目。CSP 把它的思路适配到了二次元领域：真人认知框架蒸馏（思维顾问）→ 二次元角色行为蒸馏（角色扮演）。

## 许可

CC-BY-4.0
