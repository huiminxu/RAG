"""Tech trends aggregator — GitHub, Hacker News, Dev.to, Bilibili."""
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

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


def fetch_hackernews_top(limit: int = 10, keyword: str = "") -> list[dict]:
    """Fetch from Hacker News. Uses Algolia search API when keyword is provided."""
    try:
        if keyword:
            params = {"query": keyword, "tags": "story", "hitsPerPage": limit}
            resp = requests.get("https://hn.algolia.com/api/v1/search", params=params, timeout=10)
            resp.raise_for_status()
            hits = resp.json().get("hits", [])
            return [
                {
                    "title": h.get("title", ""),
                    "url": h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID', '')}",
                    "score": h.get("points", 0),
                    "comments": h.get("num_comments", 0),
                    "time": datetime.fromtimestamp(h.get("created_at_i", 0)).strftime("%Y-%m-%d %H:%M"),
                }
                for h in hits[:limit]
            ]

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


def fetch_devto_trending(tag: str = "", limit: int = 10, keyword: str = "") -> list[dict]:
    """Fetch from Dev.to. Uses search when keyword is provided."""
    try:
        if keyword:
            params = {"q": keyword, "per_page": limit}
            resp = requests.get("https://dev.to/api/articles", params=params, timeout=10)
        else:
            params = {"top": 7, "per_page": limit}
            if tag:
                params["tag"] = tag
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
    """Fetch tech videos from YouTube Data API v3 (requires YOUTUBE_API_KEY)."""
    import os
    api_key = os.getenv("YOUTUBE_API_KEY", "")
    if not api_key:
        return []

    search_kw = keyword if keyword else "programming tutorial"
    params = {
        "part": "snippet",
        "q": search_kw,
        "type": "video",
        "order": "date",
        "relevanceLanguage": "en",
        "maxResults": limit,
        "key": api_key,
    }

    try:
        resp = requests.get("https://www.googleapis.com/youtube/v3/search", params=params, timeout=15)
        resp.raise_for_status()
        items = resp.json().get("items", [])

        video_ids = [item["id"]["videoId"] for item in items if item.get("id", {}).get("videoId")]
        stats = _fetch_youtube_stats(video_ids, api_key) if video_ids else {}

        results = []
        for item in items:
            vid_id = item.get("id", {}).get("videoId", "")
            if not vid_id:
                continue
            snippet = item.get("snippet", {})
            stat = stats.get(vid_id, {})
            results.append({
                "title": snippet.get("title", ""),
                "url": f"https://www.youtube.com/watch?v={vid_id}",
                "author": snippet.get("channelTitle", ""),
                "views": int(stat.get("viewCount", 0)),
                "published": snippet.get("publishedAt", "")[:10],
                "duration": stat.get("duration_fmt", ""),
                "thumbnail": f"https://i.ytimg.com/vi/{vid_id}/mqdefault.jpg",
            })
        return results
    except Exception:
        return []


def _fetch_youtube_stats(video_ids: list, api_key: str) -> dict:
    """Fetch view counts and durations for a list of video IDs."""
    params = {
        "part": "statistics,contentDetails",
        "id": ",".join(video_ids),
        "key": api_key,
    }
    try:
        resp = requests.get("https://www.googleapis.com/youtube/v3/videos", params=params, timeout=10)
        resp.raise_for_status()
        result = {}
        for item in resp.json().get("items", []):
            vid_id = item["id"]
            stats = item.get("statistics", {})
            duration_iso = item.get("contentDetails", {}).get("duration", "")
            result[vid_id] = {
                "viewCount": stats.get("viewCount", "0"),
                "duration_fmt": _parse_iso_duration(duration_iso),
            }
        return result
    except Exception:
        return {}


def _parse_iso_duration(iso: str) -> str:
    """Convert ISO 8601 duration (PT1H2M3S) to readable format."""
    import re
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso)
    if not m:
        return ""
    h, mi, s = m.group(1), m.group(2), m.group(3)
    h, mi, s = int(h or 0), int(mi or 0), int(s or 0)
    if h:
        return f"{h}:{mi:02d}:{s:02d}"
    return f"{mi}:{s:02d}"


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
    """Aggregate all sources concurrently. All sources use the same keyword for search."""
    keyword = language

    with ThreadPoolExecutor(max_workers=5) as executor:
        f_github = executor.submit(fetch_github_trending, keyword, since, limit)
        f_hn = executor.submit(fetch_hackernews_top, limit, keyword)
        f_devto = executor.submit(fetch_devto_trending, "", limit, keyword)
        f_bili = executor.submit(fetch_bilibili_tech, limit, keyword)
        f_yt = executor.submit(fetch_youtube_tech, keyword, limit)

    return {
        "github": f_github.result(),
        "hackernews": f_hn.result(),
        "devto": f_devto.result(),
        "bilibili": f_bili.result(),
        "youtube": f_yt.result(),
    }
