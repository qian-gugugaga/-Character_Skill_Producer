#!/usr/bin/env python3
"""Source registry for CSP local source discovery."""

EXCLUDED_DOMAINS = [
    "zhihu.com",
    "weixin.qq.com",
    "baike.baidu.com",
]

SOURCE_TIERS = {
    "official": "highest",
    "user_material": "highest",
    "moegirl": "high",
    "mediawiki": "high",
    "wikipedia": "high",
    "fandom": "high",
    "bangumi": "medium",
    "anidb": "medium",
    "bestdori": "medium",
    "bwiki": "medium",  # 萌娘百科中文源补充：BWIKI 为 B 站游戏 Wiki，覆盖米哈游系等手游角色数据
    "bilibili_column": "medium",
    "fan_discussion": "low",
}

WORK_SOURCE_HINTS = {
    "BanG Dream!": ["official", "moegirl", "fandom", "bangumi", "bestdori"],
    "BanG Dream": ["official", "moegirl", "fandom", "bangumi", "bestdori"],
    "MyGO": ["official", "moegirl", "fandom", "bangumi", "bestdori"],
    "Ave Mujica": ["official", "moegirl", "fandom", "bangumi", "bestdori"],
    "原神": ["official", "moegirl", "bwiki", "fandom"],
    "Genshin Impact": ["official", "moegirl", "bwiki", "fandom"],
    "崩坏：星穹铁道": ["official", "moegirl", "bwiki", "fandom"],
    "Honkai: Star Rail": ["official", "moegirl", "bwiki", "fandom"],
    "明日方舟": ["official", "moegirl", "bwiki"],
    "Arknights": ["official", "moegirl", "bwiki"],
    "蔚蓝档案": ["official", "moegirl", "bwiki"],
    "Blue Archive": ["official", "moegirl", "bwiki"],
    "碧蓝航线": ["official", "moegirl", "bwiki"],
    "Azur Lane": ["official", "moegirl", "bwiki"],
    "鸣潮": ["official", "moegirl", "bwiki"],
    "Wuthering Waves": ["official", "moegirl", "bwiki"],
}

CROSS_MEDIA_WORKS = [
    "BanG Dream!",
    "BanG Dream",
    "MyGO",
    "Ave Mujica",
    "Love Live!",
    "Project Sekai",
    "プロジェクトセカイ",
    "少女☆歌剧",
    "少女歌劇",
]


def source_tier(source):
    return SOURCE_TIERS.get(source, "medium")


def source_hints_for_work(work):
    if not work:
        return ["moegirl", "mediawiki"]
    for key, sources in WORK_SOURCE_HINTS.items():
        if key.lower() in work.lower() or work.lower() in key.lower():
            return sources
    return ["moegirl", "mediawiki"]


def is_cross_media_work(work):
    if not work:
        return False
    return any(key.lower() in work.lower() for key in CROSS_MEDIA_WORKS)


def is_excluded_url(url):
    if not url:
        return False
    lower = url.lower()
    return any(domain in lower for domain in EXCLUDED_DOMAINS)
