<div align="center">

# Character Skill Producer

### 把二次元角色变成可运行的 Agent Skill。

> *「不要再写角色设定了。让角色自己开口。」*

**状态：** Agent Skills 标准 · Claude Code 运行时 · 本地检索支持 Moegirl API · MIT License

<br>

**CSP 帮你把动画、漫画、游戏角色蒸馏成可以对话、写作、互动叙事的行为 Skill。**

输入一个角色名和作品名，CSP 会完成资料检索、交叉验证、行为蒸馏、质量检查，生成一个带资料日期、来源边界和更新路径的 `SKILL.md`。

今天你可以用它和角色聊天、辅助同人创作、试写剧情对白。未来它可以成为 AI 互动小说、角色驱动游戏和二次元创作工具链的角色行为层。

[看效果](#效果示例) · [产品哲学](#产品哲学) · [未来场景](#未来使用场景) · [安装](#安装) · [工作原理](#工作原理) · [资料时间边界](#资料时间边界与更新)

<br>

**其他语言 / Other Languages:**

[English](README_EN.md) · [日本語](README_JA.md) · [한국어](README_KO.md) · [Español](README_ES.md)

</div>

---

## 效果示例

你不需要自己整理人设，也不需要写一大段 prompt。

只要说：

```text
> 生成御坂美琴（某科学的超电磁炮）的 skill
> 蒸馏丰川祥子（BanG Dream! Ave Mujica）
> 做一个《孤独摇滚！》后藤一里的角色 skill
```

生成后的角色 Skill 可以像这样被调用：

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

## 为什么不是角色卡

普通角色卡常常这样写：

```text
性格：冷静、可靠、疏离。
说话方式：简短、理性。
```

这对 AI 来说太模糊。它知道标签，却不知道怎么行动。

CSP 要写的是：

```text
当别人要求她给出长期承诺时，她会先把关系翻译成任务：排练频率、退出条件、谁负责联络。
不是不在乎，而是用事务边界避免自己被卷入无法控制的情感期待。
```

区别就在这里：

| 角色卡    | CSP                        |
| ------ | -------------------------- |
| 写性格标签  | 写情境中的行为                    |
| 复述设定   | 蒸馏反应机制                     |
| 靠口癖装像  | 用表达节奏、距离感和认知方式塑形           |
| 没有资料边界 | 记录资料检索日期和未覆盖内容             |
| 很难更新   | 可用 sources / manifest 追踪更新 |

**设定告诉你角色是什么。CSP 让角色知道自己该怎么活。**

---

## CSP 蒸馏什么

CSP 提取六层信息：

| 层次         | CSP 关心的问题                          |
| ---------- | ---------------------------------- |
| **行为动态**   | 什么情境下会做什么？压力下如何变形？                 |
| **表达质感**   | 句子长短、停顿、口癖、自称、敬语层级如何工作？            |
| **社会认知**   | 她默认怎么理解他人的善意、威胁、亲近和背叛？             |
| **决策逻辑**   | 多个价值冲突时，她先保什么、牺牲什么？                |
| **诚实边界**   | 资料不足、角色不知道、原作没覆盖时，Skill 应该如何承认不知道？ |
| **资料时间边界** | 资料检索到哪一天？新剧情发布后如何更新？               |

CSP 不追求更像百科。它追求更像一个活人。

---

## 产品哲学

CSP 的底层判断很简单：**角色不是资料页，而是一套可运行的反应系统。**

Wiki 告诉你角色经历了什么；角色卡告诉你角色大概是什么属性；CSP 要进一步回答：当这个角色被放进一个原作没有写过的新情境里，她会先注意什么、误解什么、保护什么、拒绝什么，又会用怎样的节奏把话说出口。

这也是 CSP 坚持高保真模式的原因。一个角色如果只有口癖和标签，聊天几轮就会塌掉；但如果它有行为镜片、关系算法、决策底线和诚实边界，它就能在新问题里保持一致，而不是每次都靠台词碎片救场。

| CSP 要写进去的 | 意味着什么 | 没写进去会怎样 |
|---|---|---|
| 行为镜片 | 角色先看见什么，忽略什么 | 只会复述设定 |
| 反应规则 | 何时靠近、逃开、攻击、沉默 | 所有问题都一个语气 |
| 表达 DNA | 句长、停顿、敬语、自称、情绪泄露 | 只剩口癖表演 |
| 关系算法 | 如何判断善意、背叛、亲近、利用 | 对谁都一样热情 |
| 决策底线 | 价值冲突时先保什么 | 被用户轻易说服 |
| 诚实边界 | 哪些不知道、哪些过期、哪些只是推测 | 硬编新剧情 |

**写得进去的是行为程序，写不进去的要变成边界。** 这不是降低沉浸感，反而是让角色更可信：真正像角色的人，不会什么都知道，也不会永远回答得漂亮。

---

## 未来使用场景

CSP 不只是“生成几个角色”的工具。它更像是把角色从静态资料中解放出来，变成可以被聊天、写作、互动叙事和游戏系统调用的行为层。

现在，它可以用于：

| 场景 | 怎么用 | CSP 提供什么 |
|---|---|---|
| 日常聊天 | 和某个角色持续对话 | 稳定语气、关系距离、知识边界 |
| 同人创作 | 让角色参与片段、对白、内心戏创作 | 不只给台词，还给行为逻辑 |
| 剧情试写 | 把角色放进原作没有写过的新情境 | 用行为模式推断反应，而不是硬贴设定 |
| 角色研究 | 对比不同角色如何处理关系、压力和选择 | 可追溯的来源和蒸馏链 |
| 多角色协作 | 同时加载多个角色，模拟对话或冲突 | 每个角色有独立边界和决策逻辑 |

未来，它可以继续走向：

| 方向 | 可能形态 |
|---|---|
| AI 互动小说 | 角色不再只是 NPC 台词库，而是能根据玩家行动做出一致反应 |
| AI 视觉小说 / Galgame 原型 | 用角色 Skill 驱动分支对白、好感变化、冲突升级 |
| 多角色叙事实验 | 让不同角色 Skill 在同一事件中碰撞，生成群像剧情 |
| 创作者工作台 | 作者用 CSP 保持角色声音一致，快速试写场景、改写对白、检查 OOC |
| 可更新角色档案 | 作品出新剧情后更新资料日期和行为模式，让角色随作品成长 |

CSP 面向更多创作者提供一套可共享的角色行为基础设施。今天它服务聊天和同人写作；未来它可以成为 AI 互动小说、角色驱动游戏和二次元创作工具链的一部分。

---

## 本地检索优先

很多角色生成器依赖搜索插件、MCP 或浏览器能力。CSP 的方向是：**核心资料优先由本仓库脚本检索，外部搜索只是补强。**

当前已内置：

```bash
python scripts/source_search.py "高松灯" --work "BanG Dream! It's MyGO!!!!!" --mode discover
python scripts/source_search.py "能天使" --work "明日方舟" --sources moegirl
python scripts/moegirl_api.py "高松灯" --search
python scripts/moegirl_api.py "能天使" --full
```

目前本地检索重点支持萌娘百科 MediaWiki API，并通过统一的 `source_search.py` 输出结构化 JSON。其他站点 adapter 会逐步扩展；在 adapter 尚未实现时，CSP 会记录失败项，并允许用网页搜索、用户材料或其他来源补强。

这不是为了炫技，而是为了让生成结果可审计：

- 查了哪些来源；
- 哪些来源失败；
- 每条资料是哪天检索的；
- 是否命中黑名单来源；
- 之后作品更新时该从哪里重新检查。

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

- Python：用于本地检索、metadata 生成、质量检查。
- 网页搜索能力：可选增强，仅在本地脚本未覆盖或失败时补缺。

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

CSP 会先确认角色和作品。如果你手上有设定集、访谈、BD 特典、字幕、截图或游戏剧情文本，也可以直接给它。用户提供的官方材料优先级最高。

---

## 工作原理

CSP 默认采用最高质量生成模式，不提供省 token 快速版。输入角色后，它会做六件事：

**1. 本地来源发现**  
优先运行 `scripts/source_search.py` 和站点 adapter，检索萌娘百科、MediaWiki 系站点、作品 Wiki 等核心来源。搜索 skill / MCP 只作为补缺。

**2. 结构化来源索引**  
生成 `references/sources.json`，记录 URL、来源等级、检索日期、失败项和可选 content hash。

**3. 五路并行分析**  
设定与世界观、人格、表达质感、人际关系、关键场景分开调研，避免一个维度吞掉另一个维度。

**4. 行为蒸馏**  
把资料从「发生过什么」提炼成「角色在类似情境下会怎么行动」。保留矛盾，不把角色磨平成稳定人设。

**5. metadata 与资料边界**  
生成 `manifest.json`，记录角色、作品、覆盖媒体、资料检索完成日期、未覆盖内容、质量评分和 honesty boundary。

**6. 质量验证**  
检查行为模式是否可执行、表达是否有质感、矛盾是否保留、边界是否诚实、资料日期是否完整。

```bash
python scripts/quality_check.py examples/yahata-umiri/
python scripts/merge_research.py examples/yahata-umiri/
python scripts/generate_manifest.py examples/yahata-umiri/
```

完整方法论见：

- `references/distillation-framework.md`
- `references/skill-template.md`
- `references/source-output-schema.md`

---

## 生成的 Skill 长什么样

每个角色都是一个自包含目录：

```text
yahata-umiri/
├── SKILL.md                          # 可执行的角色行为指令
├── manifest.json                     # 角色、作品、资料日期、质量分、覆盖边界
└── references/
    ├── sources.json                  # 来源索引、检索日期、失败记录
    ├── distillation.md               # 从资料到行为模式的蒸馏链
    ├── quality-report.json           # 自动质量检查结果
    └── research/
        ├── 01-setting.md             # 世界观、身份、外表
        ├── 02-personality.md         # 行为模式、矛盾
        ├── 03-expression.md          # 说话质感、语言标志、经典台词
        ├── 04-relationships.md       # 社会认知、关系动态
        ├── 05-key-scenes.md          # 关键场景、压力下的决策逻辑
        └── 06-media-coverage.md      # 跨媒体覆盖、未覆盖内容、时间线
```

复制整个目录到 `.claude/skills/<name>/`，就能在对话里直接调用。

---

## 资料时间边界与更新

每个 CSP 生成的角色 Skill 都必须记录资料检索日期。

当作品后续发布新剧情、新活动、新台词、访谈或设定修订时，旧 Skill 可能无法覆盖。此时角色不会硬拗旧设定，而会说明：

```text
我的资料更新至 YYYY-MM-DD，可能没有覆盖之后发布的内容。如果你有最新版 CSP，或可以提供新剧情 / 新资料链接，我可以帮你更新这个 Skill；这可能会消耗一些 Token。
```

更新已有 Skill 时，CSP 会读取旧 `manifest.json` 和 `sources.json`，重新检索核心来源，只重蒸馏受影响部分，并更新资料日期和质量报告。

---

## 信息源原则

二次元角色资料很容易被二创、转述和社区印象污染。CSP 的原则是：

| 优先级    | 来源                                                            |
| ------ | ------------------------------------------------------------- |
| **最高** | 用户提供的官方设定集、访谈、BD 特典、字幕、截图                                     |
| **高**  | 官方网站、官方角色介绍、官方剧情文本、萌娘百科、Wikipedia、作品 Fandom Wiki              |
| **中**  | Bangumi、AniDB、游戏剧情、Bilibili 高质量专栏、Anime News Network、Bestdori |
| **低**  | 粉丝讨论、社区解读，必须标注为推测                                             |
| **排除** | 知乎、微信公众号、百度百科                                                 |

至少两个独立来源交叉验证。资料不足就写不足，不补脑，不编造。

---

## 预置角色

仓库里已经包含这些可直接使用的角色 Skill：

| 角色      | 作品                         | 目录                           |
| ------- | -------------------------- | ---------------------------- |
| 高松灯     | BanG Dream! It's MyGO!!!!! | `examples/takamatsu-tomori/` |
| 椎名立希    | BanG Dream! It's MyGO!!!!! | `examples/taki-shiina/`      |
| 要乐奈     | BanG Dream! It's MyGO!!!!! | `examples/kaname-rana/`      |
| 长崎爽世    | BanG Dream! It's MyGO!!!!! | `examples/nagasaki-soyo/`    |
| 千早爱音    | BanG Dream! It's MyGO!!!!! | `examples/chihaya-anon/`     |
| 丰川祥子    | BanG Dream! Ave Mujica     | `examples/togawa-sakiko/`    |
| 若叶睦     | BanG Dream! Ave Mujica     | `examples/mutsumi-wakaba/`   |
| 三角初华    | BanG Dream! Ave Mujica     | `examples/misumi-uika/`      |
| 祐天寺若麦   | BanG Dream! Ave Mujica     | `examples/yutenji-nyamu/`    |
| 八幡海铃    | BanG Dream! Ave Mujica     | `examples/yahata-umiri/`     |
| CSP 自描述 | —                          | `examples/csp/`              |

BanG Dream! 角色会覆盖 MyGO!!!!!、Ave Mujica、CRYCHIC 前史，并在资料允许时纳入手游和衍生内容作为日常行为补充。

---

## 路线图

已实现 / 当前版本：

- CSP meta-skill 主流程；
- 萌娘百科 MediaWiki API 本地检索；
- 统一来源发现入口 `source_search.py`；
- 质量检查 `quality_check.py`；
- 调研摘要 `merge_research.py`；
- manifest 生成 `generate_manifest.py`；
- 自包含安装版 `examples/csp/`；
- 多个 MyGO / Ave Mujica 角色示例。

计划中：

- 更多本地 adapter：Bangumi、Fandom、Wikipedia、Bestdori、BWIKI；
- `file_manager.py`：更新前备份、回滚、修订记录；
- `distill_prompt.py`：把 Skill 导出为普通平台可用 prompt；
- 更完整的增量更新检查和 source diff。

不会假装已经完成。能本地检索的就本地检索，暂时做不到的就记录失败、标注边界、等待补强。

---

## 仓库结构

```text
Character_Skill_Producer/
├── SKILL.md                          # CSP 主 skill
├── references/
│   ├── distillation-framework.md     # 行为蒸馏方法论
│   ├── skill-template.md             # 角色 Skill 模板
│   └── source-output-schema.md       # 来源与 metadata 结构规范
├── scripts/
│   ├── source_search.py              # 本地核心来源检索入口
│   ├── source_registry.py            # 来源等级、黑名单、站点规则
│   ├── generate_manifest.py          # manifest.json 生成/更新
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

MIT

---

<div align="center">

**设定告诉你角色是什么。**<br>
**CSP 让角色知道自己该怎么活。**

<br>

*不要再写角色设定了。让角色自己开口。*

</div>
