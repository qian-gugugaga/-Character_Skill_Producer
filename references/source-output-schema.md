# 来源与 metadata 结构规范

CSP 的生成结果必须可追溯、可复查、可更新。本文件定义 `references/sources.json`、`manifest.json` 和质量报告的最低结构。

## sources.json

位置：

```text
<skill_dir>/references/sources.json
```

类型：数组。每个对象表示一次成功或失败的来源检索。

### 必填字段

```json
{
  "id": "moegirl-character-title",
  "source": "moegirl",
  "title": "条目标题",
  "url": "https://example.com/page",
  "query": "原始查询词",
  "work": "作品名",
  "source_tier": "high",
  "officiality": "secondary",
  "media_type": "wiki",
  "language": "zh",
  "retrieved_at": "YYYY-MM-DD",
  "status": "ok",
  "warnings": []
}
```

### 推荐字段

```json
{
  "resolved_title": "实际命中的标题",
  "pageid": 12345,
  "used_in": ["01-setting.md", "02-personality.md"],
  "content_hash": "sha256:...",
  "source_last_modified": null,
  "retrieved_by": "scripts/source_search.py",
  "attempted_modes": ["intro", "search", "full"],
  "error": null,
  "extract_chars": 1200
}
```

### `source_tier`

可用值：

- `highest`：用户提供的官方材料、官方设定集、访谈原文、BD 特典、官方字幕、官方剧情文本。
- `high`：官方网站、官方角色介绍、萌娘百科、Wikipedia、作品 Fandom Wiki。
- `medium`：Bangumi、AniDB、游戏数据库、Bilibili 高质量专栏、Anime News Network、Bestdori。
- `low`：粉丝讨论、社区解读，必须标注为推测。
- `excluded`：知乎、微信公众号、百度百科等不可用来源。

### `officiality`

可用值：

- `official`
- `semi_official`
- `secondary`
- `fan_interpretation`
- `user_provided`
- `excluded`

### `media_type`

可用值示例：

- `official_profile`
- `anime`
- `game_story`
- `event_story`
- `card_story`
- `interview`
- `wiki`
- `database`
- `article`
- `video`
- `subtitle`
- `user_material`

### 失败记录

失败也必须写入：

```json
{
  "id": "fandom-character-failed",
  "source": "fandom",
  "title": null,
  "url": null,
  "query": "角色名 作品名",
  "work": "作品名",
  "source_tier": "high",
  "officiality": "secondary",
  "media_type": "wiki",
  "language": "en",
  "retrieved_at": "YYYY-MM-DD",
  "status": "failed",
  "error": "not_found",
  "warnings": ["No exact title match"],
  "attempted_modes": ["search"]
}
```

失败记录用于证明 CSP 查过该来源，也用于后续更新。

## manifest.json

位置：

```text
<skill_dir>/manifest.json
```

最低结构：

```json
{
  "schema_version": "1.0",
  "name": "character-slug",
  "character": "角色名",
  "work": "作品名",
  "aliases": [],
  "generated_at": "YYYY-MM-DD",
  "research_started_at": "YYYY-MM-DD",
  "research_completed_at": "YYYY-MM-DD",
  "latest_source_checked_at": "YYYY-MM-DD",
  "covered_until": {
    "date": "YYYY-MM-DD",
    "description": "截至该日期可检索到的公开资料和用户提供材料"
  },
  "covered_media": [],
  "not_covered": [
    "YYYY-MM-DD 后发布的新剧情、新活动、新访谈、新设定修订"
  ],
  "source_count": 0,
  "source_tiers": {},
  "quality_score": null,
  "honesty_boundary": "",
  "csp_version": "unknown"
}
```

`latest_source_checked_at` 是面向用户解释资料边界的核心字段。用户说「最新剧情不是这样」时，角色 Skill 必须引用这个日期。

## quality-report.json

位置：

```text
<skill_dir>/references/quality-report.json
```

推荐结构：

```json
{
  "checked_at": "YYYY-MM-DD",
  "score": 0.0,
  "passed": false,
  "checks": {
    "behavior_patterns": "pass",
    "expression_texture": "pass",
    "contradictions": "pass",
    "role_play_rules": "pass",
    "behavior_examples": "pass",
    "honesty_boundary": "pass",
    "source_attribution": "pass",
    "manifest": "pass",
    "sources_json": "pass",
    "research_dates": "pass",
    "update_response": "pass"
  },
  "warnings": [],
  "failed_checks": []
}
```

## 黑名单

以下来源不得作为证据使用：

- `zhihu.com`
- `weixin.qq.com`
- `baike.baidu.com`

如果检索结果命中这些域名，`source_tier` 必须标为 `excluded`，且不得写入核心结论。
