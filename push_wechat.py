"""
每周技术资讯推送到微信（via Server酱）

用法：
  1. 在 .env 中配置 SERVERCHAN_KEY（从 sct.ftqq.com 获取 SendKey）
  2. UI 内点击「推送到微信」按钮
  3. 或命令行：python push_wechat.py [关键词]
"""

import os
import requests
from datetime import date
from dotenv import load_dotenv

load_dotenv()

SERVERCHAN_KEY = os.getenv("SERVERCHAN_KEY", "")
SERVERCHAN_URL = "https://sctapi.ftqq.com/{key}.send"


def generate_weekly_digest(language: str = "") -> str:
    """聚合技术趋势数据，生成 HTML 摘要。"""
    from trends import get_all_trends

    data = get_all_trends(language=language, since="weekly", limit=8)
    today = date.today().isoformat()
    keyword_label = language if language else "全栈"

    html_parts = [
        f"<h2>📊 本周技术热点（{keyword_label}）</h2>",
        f"<p style='color:#888'>生成日期：{today}</p>",
    ]

    # GitHub
    github = data.get("github", [])
    if github:
        html_parts.append("<h3>🐙 GitHub 热门项目</h3><ol>")
        for r in github[:6]:
            stars = r.get("stars", 0)
            star_label = f"{stars/1000:.1f}k" if stars >= 1000 else str(stars)
            desc = r.get("description", "")[:60]
            html_parts.append(
                f"<li><a href=\"{r['url']}\">{r['name']}</a> ⭐{star_label} — {desc}</li>"
            )
        html_parts.append("</ol>")

    # HackerNews
    hn = data.get("hackernews", [])
    if hn:
        html_parts.append("<h3>📰 HackerNews 热议</h3><ol>")
        for h in hn[:6]:
            html_parts.append(
                f"<li><a href=\"{h['url']}\">{h['title']}</a> ({h.get('score', 0)} points)</li>"
            )
        html_parts.append("</ol>")

    # Dev.to
    devto = data.get("devto", [])
    if devto:
        html_parts.append("<h3>✍️ Dev.to 精选</h3><ol>")
        for a in devto[:5]:
            html_parts.append(
                f"<li><a href=\"{a['url']}\">{a['title']}</a> ❤️{a.get('reactions', 0)}</li>"
            )
        html_parts.append("</ol>")

    # YouTube
    yt = data.get("youtube", [])
    if yt:
        html_parts.append("<h3>🎬 YouTube 推荐</h3><ol>")
        for v in yt[:5]:
            html_parts.append(
                f"<li><a href=\"{v.get('url', '')}\">{v.get('title', '')}</a> — {v.get('channel', '')}</li>"
            )
        html_parts.append("</ol>")

    # Bilibili
    bili = data.get("bilibili", [])
    if bili:
        html_parts.append("<h3>📺 B站技术视频</h3><ol>")
        for b in bili[:5]:
            html_parts.append(
                f"<li><a href=\"{b.get('url', '')}\">{b.get('title', '')}</a> ▶️{b.get('play', 0)}</li>"
            )
        html_parts.append("</ol>")

    html_parts.append("<hr><p style='color:#aaa;font-size:12px'>由 RAG 学习助手自动生成</p>")
    return "\n".join(html_parts)


def push_to_wechat(title: str, content: str) -> dict:
    """通过 Server酱 推送消息到微信。"""
    if not SERVERCHAN_KEY:
        return {"success": False, "msg": "未配置 SERVERCHAN_KEY，请在 .env 中添加（从 sct.ftqq.com 获取）"}

    url = SERVERCHAN_URL.format(key=SERVERCHAN_KEY)
    payload = {
        "title": title,
        "desp": content,
    }

    try:
        resp = requests.post(url, json=payload, timeout=15)
        resp.raise_for_status()
        result = resp.json()
        if result.get("code") == 0:
            return {"success": True, "msg": "推送成功，请查看微信"}
        else:
            return {"success": False, "msg": result.get("message", "推送失败")}
    except Exception as e:
        return {"success": False, "msg": f"请求失败：{e}"}


def weekly_push(language: str = "") -> dict:
    """生成本周摘要并推送到微信。"""
    keyword_label = language if language else "全栈"
    title = f"📊 本周技术热点（{keyword_label}）— {date.today().isoformat()}"
    content = generate_weekly_digest(language)
    return push_to_wechat(title, content)


if __name__ == "__main__":
    import sys

    lang = sys.argv[1] if len(sys.argv) > 1 else ""
    print(f"正在获取技术趋势数据（关键词：{lang or '全部'}）...")
    result = weekly_push(lang)
    if result["success"]:
        print(f"✅ {result['msg']}")
    else:
        print(f"❌ {result['msg']}")
