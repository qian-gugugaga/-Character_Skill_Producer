# Character Skill Producer (CSP)

> 把二次元角色变成可运行的 agent 行为包。

CSP 是一个 **meta-skill**——安装后，Claude Code 或 Codex 获得"蒸馏角色"的能力：输入角色名+作品名，自动搜索权威资料 → 交叉验证 → 行为蒸馏 → 生成可安装的角色扮演 SKILL.md。

## 安装

```bash
# Claude Code
skills add qian-gugugaga/Character_Skill_Producer

# 或手动克隆
git clone https://github.com/qian-gugugaga/Character_Skill_Producer.git
cp -r examples/csp ~/.claude/skills/csp
```

## 使用

```
> 生成御坂美琴（某科学的超电磁炮）的 skill
> 蒸馏椎名真希（BanG Dream! It's MyGO!!!!!）
> 做一个五条悟的角色 skill
```

CSP 会启动 5 个并行 Agent 搜索萌娘百科、Wikipedia、Fandom Wiki 等权威来源，交叉验证后蒸馏为可执行的行为程序。

## 依赖

**需要网页搜索 skill。** 使用前请确保已安装 WebSearch 或等效 skill。

## 预置角色 Skill

| 角色 | 作品 | Skill 目录 |
|------|------|-----------|
| 高松灯 | BanG Dream! It's MyGO!!!!! | `examples/takamatsu-tomori/` |
| 椎名立希 | BanG Dream! It's MyGO!!!!! | `examples/taki-shiina/` |
| 要乐奈 | BanG Dream! It's MyGO!!!!! | `examples/kaname-rana/` |
| 长崎爽世 | BanG Dream! It's MyGO!!!!! | `examples/nagasaki-soyo/` |
| 千早爱音 | BanG Dream! It's MyGO!!!!! | `examples/chihaya-anon/` |

使用方式：将对应目录复制到 `.claude/skills/<name>/`，然后通过触发词调用角色。

## 项目结构

```
├── SKILL.md                          # CSP 主 skill
├── PRD.md                            # 产品定义
├── references/
│   ├── distillation-framework.md     # 行为蒸馏方法论
│   └── skill-template.md             # 生成模板
├── scripts/
│   ├── quality_check.py              # 质量验证
│   └── merge_research.py             # 调研摘要
└── examples/
    ├── csp/                           # CSP 自我描述
    ├── chihaya-anon/                  # 千早爱音
    ├── kaname-rana/                   # 要乐奈
    ├── nagasaki-soyo/                 # 长崎爽世
    ├── takamatsu-tomori/              # 高松灯
    └── taki-shiina/                   # 椎名立希
```

## 致谢

架构借鉴 [nuwa-skill（女娲）](https://github.com/alchaincyf/nuwa-skill)——LLM 人格蒸馏的先驱项目。CSP 将其适配至完全不同的领域：二次元角色行为蒸馏（角色扮演）vs 真人认知框架蒸馏（思维顾问）。

## 许可

CC-BY-4.0
