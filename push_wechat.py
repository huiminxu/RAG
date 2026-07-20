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

SERVERCHAN_KEYS = [k.strip() for k in os.getenv("SERVERCHAN_KEY", "").split(",") if k.strip()]
SERVERCHAN_URL = "https://sctapi.ftqq.com/{key}.send"


def generate_weekly_digest(language: str = "") -> str:
    """聚合技术趋势数据，生成 Markdown 摘要。"""
    from trends import get_all_trends

    data = get_all_trends(language=language, since="weekly", limit=8)
    today = date.today().isoformat()
    keyword_label = language if language else "全栈"

    lines = [
        f"## 📊 本周技术热点（{keyword_label}）",
        f"> 生成日期：{today}",
        "",
    ]

    # GitHub
    github = data.get("github", [])
    if github:
        lines.append("### 🐙 GitHub 热门项目")
        lines.append("")
        for i, r in enumerate(github[:6], 1):
            stars = r.get("stars", 0)
            star_label = f"{stars/1000:.1f}k" if stars >= 1000 else str(stars)
            desc = r.get("description", "")[:60]
            lines.append(f"{i}. [{r['name']}]({r['url']}) ⭐{star_label} — {desc}")
        lines.append("")

    # HackerNews
    hn = data.get("hackernews", [])
    if hn:
        lines.append("### 📰 HackerNews 热议")
        lines.append("")
        for i, h in enumerate(hn[:6], 1):
            lines.append(f"{i}. [{h['title']}]({h['url']}) ({h.get('score', 0)} points)")
        lines.append("")

    # Dev.to
    devto = data.get("devto", [])
    if devto:
        lines.append("### ✍️ Dev.to 精选")
        lines.append("")
        for i, a in enumerate(devto[:5], 1):
            lines.append(f"{i}. [{a['title']}]({a['url']}) ❤️{a.get('reactions', 0)}")
        lines.append("")

    # YouTube
    yt = data.get("youtube", [])
    if yt:
        lines.append("### 🎬 YouTube 推荐")
        lines.append("")
        for i, v in enumerate(yt[:5], 1):
            lines.append(f"{i}. [{v.get('title', '')}]({v.get('url', '')}) — {v.get('channel', '')}")
        lines.append("")

    # Bilibili
    bili = data.get("bilibili", [])
    if bili:
        lines.append("### 📺 B站技术视频")
        lines.append("")
        for i, b in enumerate(bili[:5], 1):
            play = b.get("play", 0)
            lines.append(f"{i}. [{b.get('title', '')}]({b.get('url', '')}) ▶️{play}")
        lines.append("")

    lines.append("---")
    lines.append("*由 RAG 学习助手自动生成*")
    return "\n".join(lines)


def push_to_wechat(title: str, content: str) -> dict:
    """通过 Server酱 推送消息到微信（支持多人）。"""
    if not SERVERCHAN_KEYS:
        return {"success": False, "msg": "未配置 SERVERCHAN_KEY，请在 .env 中添加（多人用逗号分隔）"}

    success_count = 0
    errors = []

    for key in SERVERCHAN_KEYS:
        url = SERVERCHAN_URL.format(key=key)
        payload = {"title": title, "desp": content}
        try:
            resp = requests.post(url, json=payload, timeout=15)
            resp.raise_for_status()
            result = resp.json()
            if result.get("code") == 0:
                success_count += 1
            else:
                errors.append(result.get("message", "未知错误"))
        except Exception as e:
            errors.append(str(e))

    if success_count == len(SERVERCHAN_KEYS):
        return {"success": True, "msg": f"推送成功，已发送给 {success_count} 人"}
    elif success_count > 0:
        return {"success": True, "msg": f"部分成功：{success_count}/{len(SERVERCHAN_KEYS)} 人"}
    else:
        return {"success": False, "msg": f"推送失败：{'; '.join(errors)}"}


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
