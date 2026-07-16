"""Tech trends aggregator — GitHub, Hacker News, Dev.to, Bilibili."""
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests


SINCE_MAP = {"daily": 1, "weekly": 7, "monthly": 30}


GITHUB_KEYWORD_MAP = {
    "ai": "AI machine-learning",
    "agent": "\"AI agent\"",
    "llm": "LLM \"large language model\"",
    "大模型": "LLM \"large language model\"",
    "英语": "\"english learning\" OR \"learn english\"",
}
GITHUB_LANG_SET = {"javascript", "typescript", "python", "vue", "react", "go", "rust"}


def fetch_github_trending(language: str = "", since: str = "weekly", limit: int = 10) -> list[dict]:
    """Fetch trending repos from GitHub Search API."""
    days = SINCE_MAP.get(since, 7)
    date_threshold = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")

    q = f"created:>{date_threshold}"
    lang_lower = language.lower() if language else ""
    if lang_lower in GITHUB_LANG_SET:
        q += f" language:{language}"
    elif lang_lower in GITHUB_KEYWORD_MAP:
        q += f" {GITHUB_KEYWORD_MAP[lang_lower]}"
    elif language:
        q += f" {language}"

    params = {"q": q, "sort": "stars", "order": "desc", "per_page": limit}
    try:
        resp = requests.get("https://api.github.com/search/repositories", params=params, timeout=15)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        return [
            {
                "name": r["full_name"],
                "description": r.get("description") or "",
                "stars": r["stargazers_count"],
                "forks": r["forks_count"],
                "language": r.get("language") or "N/A",
                "url": r["html_url"],
                "topics": r.get("topics", [])[:5],
            }
            for r in items[:limit]
        ]
    except Exception:
        return []


def fetch_hackernews_top(limit: int = 10) -> list[dict]:
    """Fetch top stories from Hacker News."""
    try:
        resp = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10)
        resp.raise_for_status()
        ids = resp.json()[:limit]

        results = []
        for story_id in ids:
            item = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json", timeout=5).json()
            if item and item.get("type") == "story":
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                    "score": item.get("score", 0),
                    "comments": item.get("descendants", 0),
                    "time": datetime.fromtimestamp(item.get("time", 0)).strftime("%Y-%m-%d %H:%M"),
                })
        return results
    except Exception:
        return []


def fetch_devto_trending(tag: str = "", limit: int = 10) -> list[dict]:
    """Fetch trending articles from Dev.to."""
    params = {"top": 7, "per_page": limit}
    if tag:
        params["tag"] = tag

    try:
        resp = requests.get("https://dev.to/api/articles", params=params, timeout=10)
        resp.raise_for_status()
        articles = resp.json()
        return [
            {
                "title": a["title"],
                "url": a["url"],
                "description": a.get("description", ""),
                "reactions": a.get("positive_reactions_count", 0),
                "comments": a.get("comments_count", 0),
                "tags": a.get("tag_list", []),
                "published_at": a.get("readable_publish_date", ""),
            }
            for a in articles[:limit]
        ]
    except Exception:
        return []


def fetch_bilibili_tech(limit: int = 10, keyword: str = "") -> list[dict]:
    """Fetch videos from Bilibili via WBI-signed search API."""
    import re
    import hashlib
    import time
    import urllib.parse

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://search.bilibili.com",
    }
    session = requests.Session()
    session.headers.update(headers)

    try:
        # Get buvid cookie
        spi = session.get("https://api.bilibili.com/x/frontend/finger/spi", timeout=10).json().get("data", {})
        session.cookies.set("buvid3", spi.get("b_3", ""), domain=".bilibili.com")
        session.cookies.set("buvid4", spi.get("b_4", ""), domain=".bilibili.com")

        # Get WBI keys
        nav = session.get("https://api.bilibili.com/x/web-interface/nav", timeout=10).json()
        wbi_img = nav.get("data", {}).get("wbi_img", {})
        img_key = wbi_img.get("img_url", "").split("/")[-1].split(".")[0]
        sub_key = wbi_img.get("sub_url", "").split("/")[-1].split(".")[0]

        # WBI sign
        MIXIN_KEY_ENC_TAB = [
            46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35,
            27, 43, 5, 49, 33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13,
            37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4,
            22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11, 36, 20, 34, 44, 52,
        ]
        mixin_key = "".join((img_key + sub_key)[i] for i in MIXIN_KEY_ENC_TAB)[:32]

        search_kw = keyword if keyword else "编程 开发"
        params = {"keyword": search_kw, "search_type": "video", "order": "totalrank", "page": 1, "pagesize": limit}
        params["wts"] = int(time.time())
        params = dict(sorted(params.items()))
        query = urllib.parse.urlencode(params)
        params["w_rid"] = hashlib.md5((query + mixin_key).encode()).hexdigest()

        # Search
        resp = session.get("https://api.bilibili.com/x/web-interface/wbi/search/type", params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            return []

        results = data.get("data", {}).get("result", [])
        return [
            {
                "title": re.sub(r"<[^>]+>", "", item.get("title", "")),
                "url": f"https://www.bilibili.com/video/{item.get('bvid', '')}",
                "author": item.get("author", ""),
                "play": item.get("play", 0),
                "danmaku": item.get("video_review", 0),
                "duration": item.get("duration", ""),
                "published": item.get("pubdate_str", "") or _ts_to_date(item.get("pubdate", 0)),
                "thumbnail": ("https:" + item["pic"]) if item.get("pic", "").startswith("//") else item.get("pic", ""),
            }
            for item in results[:limit]
            if item.get("bvid")
        ]
    except Exception:
        return []


def fetch_youtube_tech(keyword: str = "", limit: int = 10) -> list[dict]:
    """Fetch tech videos from YouTube via Invidious API (no API key needed)."""
    INVIDIOUS_INSTANCES = [
        "https://vid.puffyan.us",
        "https://invidious.fdn.fr",
        "https://invidious.privacyredirect.com",
    ]

    search_kw = keyword if keyword else "programming tutorial"
    params = {"q": search_kw, "sort_by": "upload_date", "type": "video", "page": 1}

    for instance in INVIDIOUS_INSTANCES:
        try:
            resp = requests.get(f"{instance}/api/v1/search", params=params, timeout=15)
            resp.raise_for_status()
            items = resp.json()
            results = []
            for item in items[:limit]:
                if item.get("type") != "video":
                    continue
                vid_id = item.get("videoId", "")
                results.append({
                    "title": item.get("title", ""),
                    "url": f"https://www.youtube.com/watch?v={vid_id}",
                    "author": item.get("author", ""),
                    "views": item.get("viewCount", 0),
                    "published": item.get("publishedText", ""),
                    "duration": _format_duration(item.get("lengthSeconds", 0)),
                    "thumbnail": f"https://i.ytimg.com/vi/{vid_id}/mqdefault.jpg" if vid_id else "",
                })
            return results
        except Exception:
            continue
    return []


def _format_duration(seconds: int) -> str:
    if not seconds:
        return ""
    h, m, s = seconds // 3600, (seconds % 3600) // 60, seconds % 60
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def _ts_to_date(ts) -> str:
    if not ts:
        return ""
    try:
        if isinstance(ts, str):
            return ts[:10]
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
    except Exception:
        return ""


def get_all_trends(language: str = "", since: str = "weekly", limit: int = 10) -> dict:
    """Aggregate all sources concurrently."""
    tag_map = {"javascript": "javascript", "typescript": "typescript", "python": "python",
               "vue": "vue", "react": "react", "go": "go", "rust": "rust",
               "ai": "ai", "agent": "ai", "llm": "ai", "大模型": "ai", "英语": ""}
    devto_tag = tag_map.get(language.lower(), "")
    bili_map = {"ai": "AI 人工智能", "agent": "AI Agent 智能体", "llm": "大模型 LLM", "大模型": "大模型 LLM", "英语": "英语学习"}
    bili_kw = bili_map.get(language.lower(), language) if language else ""

    yt_map = {"ai": "AI machine learning tutorial", "agent": "AI agent development", "llm": "LLM tutorial",
              "大模型": "LLM 大模型 tutorial", "英语": "English learning programming"}
    yt_kw = yt_map.get(language.lower(), f"{language} programming") if language else ""

    with ThreadPoolExecutor(max_workers=5) as executor:
        f_github = executor.submit(fetch_github_trending, language, since, limit)
        f_hn = executor.submit(fetch_hackernews_top, limit)
        f_devto = executor.submit(fetch_devto_trending, devto_tag, limit)
        f_bili = executor.submit(fetch_bilibili_tech, limit, bili_kw)
        f_yt = executor.submit(fetch_youtube_tech, yt_kw, limit)

    return {
        "github": f_github.result(),
        "hackernews": f_hn.result(),
        "devto": f_devto.result(),
        "bilibili": f_bili.result(),
        "youtube": f_yt.result(),
    }
