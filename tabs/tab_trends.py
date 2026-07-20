import html as html_lib
import streamlit as st
from trends import get_all_trends


CARD_CSS_DARK = """
<style>
.trend-card {
    border: 1px solid #4a2d6b;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
    background: linear-gradient(135deg, #2a1a3e 0%, #3d2060 100%);
    transition: box-shadow 0.2s, transform 0.2s;
}
.trend-card:hover {
    box-shadow: 0 4px 16px rgba(168,85,247,0.2);
    transform: translateY(-1px);
}
.trend-card h4 {
    margin: 0 0 8px 0;
    font-size: 15px;
}
.trend-card h4 a {
    color: #c084fc;
    text-decoration: none;
}
.trend-card h4 a:hover {
    color: #e9d5ff;
}
.trend-card .desc {
    color: #c8b0e8;
    font-size: 13px;
    margin-bottom: 8px;
}
.trend-card .meta {
    color: #9080b0;
    font-size: 12px;
}
.trend-card .meta span {
    margin-right: 12px;
}
.trend-card .tags {
    margin-top: 6px;
}
.trend-card .tags code {
    background: #3d2060;
    color: #d8b4fe;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 11px;
    margin-right: 4px;
    border: 1px solid #6b21a8;
}
.bili-card {
    display: flex;
    gap: 12px;
    align-items: flex-start;
}
.bili-card img {
    width: 160px;
    border-radius: 8px;
    flex-shrink: 0;
    border: 1px solid #4a2d6b;
}
</style>
"""

CARD_CSS_LIGHT = """
<style>
.trend-card {
    border: 1px solid #c8e6c9;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
    background: linear-gradient(135deg, #f1f8e9 0%, #e8f5e9 100%);
    transition: box-shadow 0.2s, transform 0.2s;
}
.trend-card:hover {
    box-shadow: 0 4px 16px rgba(76,175,80,0.15);
    transform: translateY(-1px);
}
.trend-card h4 {
    margin: 0 0 8px 0;
    font-size: 15px;
}
.trend-card h4 a {
    color: #2e7d32;
    text-decoration: none;
}
.trend-card h4 a:hover {
    color: #1b5e20;
}
.trend-card .desc {
    color: #4e6e4e;
    font-size: 13px;
    margin-bottom: 8px;
}
.trend-card .meta {
    color: #6d9b6d;
    font-size: 12px;
}
.trend-card .meta span {
    margin-right: 12px;
}
.trend-card .tags {
    margin-top: 6px;
}
.trend-card .tags code {
    background: #e8f5e9;
    color: #2e7d32;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 11px;
    margin-right: 4px;
    border: 1px solid #a5d6a7;
}
.bili-card {
    display: flex;
    gap: 12px;
    align-items: flex-start;
}
.bili-card img {
    width: 160px;
    border-radius: 8px;
    flex-shrink: 0;
    border: 1px solid #c8e6c9;
}
</style>
"""


def render():
    import os

    st.title("🌺 技术趋势")
    st.caption("聚合 GitHub / Hacker News / Dev.to / B站 热门资源，快速了解技术前沿")

    col_lang, col_custom, col_since, col_refresh = st.columns([2, 2, 2, 1])
    with col_lang:
        trend_language = st.selectbox(
            "语言/领域",
            ["", "JavaScript", "TypeScript", "Python", "Vue", "React", "Go", "Rust", "AI", "Agent", "LLM", "大模型", "英语", "__custom__"],
            format_func=lambda x: {"": "全部", "__custom__": "🔍 自定义..."}.get(x, x),
            key="trend_lang",
        )
    with col_custom:
        if trend_language == "__custom__":
            custom_kw = st.text_input("关键词", placeholder="Docker、微服务、GPT...", key="trend_custom")
        else:
            custom_kw = ""
            st.text_input("关键词", placeholder="选择「自定义」后输入", disabled=True, key="trend_custom_disabled")
    with col_since:
        trend_since = st.selectbox(
            "时间范围",
            ["daily", "weekly", "monthly"],
            index=1,
            format_func=lambda x: {"daily": "今天", "weekly": "本周", "monthly": "本月"}[x],
            key="trend_since",
        )
    with col_refresh:
        st.write("")
        st.write("")
        refresh = st.button("🔄 刷新", key="trend_refresh")

    trend_keyword = custom_kw.strip() if trend_language == "__custom__" else trend_language
    if trend_language == "__custom__" and not trend_keyword:
        st.info("请输入关键词后查看结果")
        st.stop()

    @st.cache_data(ttl=3600, show_spinner=False)
    def _cached_trends(language, since):
        return get_all_trends(language=language, since=since, limit=10)

    if refresh:
        _cached_trends.clear()

    CARD_CSS = CARD_CSS_DARK if st.session_state.dark_mode else CARD_CSS_LIGHT

    col_load, col_push = st.columns([1, 1])
    with col_load:
        load_clicked = st.button("📡 加载趋势数据", type="primary", key="trend_load", use_container_width=True)
    with col_push:
        push_clicked = st.button("📬 推送本周资讯到微信", key="push_wechat_btn", use_container_width=True)

    if push_clicked:
        from push_wechat import weekly_push
        with st.spinner("正在获取数据并推送到微信..."):
            result = weekly_push(trend_keyword)
        if result["success"]:
            st.success(result["msg"])
        else:
            st.error(result["msg"])

    if load_clicked or st.session_state.get("trends_loaded"):
        st.session_state.trends_loaded = True
        with st.spinner("🌺 正在获取最新技术趋势..."):
            trends = _cached_trends(trend_keyword, trend_since)

        st.markdown(CARD_CSS, unsafe_allow_html=True)

        row1_left, row1_mid, row1_right = st.columns(3)
        row2_left, row2_mid, row2_right = st.columns(3)

        with row1_left:
            st.markdown("#### ⭐ GitHub 热门项目")
            with st.container(height=420):
                if trends["github"]:
                    for repo in trends["github"]:
                        desc = html_lib.escape(repo['description'][:80]) if repo['description'] else ""
                        topics_html = "".join(f"<code>{html_lib.escape(t)}</code>" for t in repo["topics"]) if repo["topics"] else ""
                        parts = [
                            '<div class="trend-card">',
                            f'<h4><a href="{repo["url"]}" target="_blank">{html_lib.escape(repo["name"])}</a></h4>',
                        ]
                        if desc:
                            parts.append(f'<div class="desc">{desc}</div>')
                        parts.append(f'<div class="meta"><span>⭐ {repo["stars"]:,}</span><span>🍴 {repo["forks"]:,}</span><span>🏷️ {repo["language"]}</span></div>')
                        if topics_html:
                            parts.append(f'<div class="tags">{topics_html}</div>')
                        parts.append('</div>')
                        st.markdown("".join(parts), unsafe_allow_html=True)
                else:
                    st.info("暂无数据")

        with row1_mid:
            st.markdown("#### 📰 Hacker News 热门")
            with st.container(height=420):
                if trends["hackernews"]:
                    for item in trends["hackernews"]:
                        title = html_lib.escape(item['title'])
                        card = f'<div class="trend-card"><h4><a href="{item["url"]}" target="_blank">{title}</a></h4><div class="meta"><span>🔥 {item["score"]}</span><span>💬 {item["comments"]} 评论</span><span>🕐 {item["time"]}</span></div></div>'
                        st.markdown(card, unsafe_allow_html=True)
                else:
                    st.info("暂无数据")

        with row1_right:
            st.markdown("#### ▶️ YouTube 技术视频")
            with st.container(height=420):
                if trends.get("youtube"):
                    for video in trends["youtube"]:
                        title = html_lib.escape(video['title'])
                        author = html_lib.escape(video.get('author', ''))
                        views = f"{video['views']:,}" if isinstance(video.get("views"), int) else str(video.get("views", 0))
                        thumb = f'<img src="{video["thumbnail"]}" referrerpolicy="no-referrer" style="width:120px;border-radius:6px;margin-right:10px;float:left;" />' if video.get("thumbnail") else ""
                        card = f'<div class="trend-card">{thumb}<h4><a href="{video["url"]}" target="_blank">{title}</a></h4><div class="meta"><span>👤 {author}</span><span>👁️ {views}</span><span>⏱️ {video.get("duration", "")}</span><span>📅 {video.get("published", "")}</span></div><div style="clear:both;"></div></div>'
                        st.markdown(card, unsafe_allow_html=True)
                else:
                    if not os.getenv("YOUTUBE_API_KEY"):
                        st.info("需配置 YOUTUBE_API_KEY\n\n[获取 Key →](https://console.cloud.google.com/apis/library/youtube.googleapis.com)")
                    else:
                        st.info("暂无 YouTube 数据")

        with row2_left:
            st.markdown("#### 📝 Dev.to 热门文章")
            with st.container(height=420):
                if trends["devto"]:
                    for article in trends["devto"]:
                        title = html_lib.escape(article['title'])
                        desc = html_lib.escape(article.get('description', '')[:80])
                        tags_html = "".join(f"<code>{html_lib.escape(t)}</code>" for t in article["tags"][:4]) if article["tags"] else ""
                        parts = [
                            '<div class="trend-card">',
                            f'<h4><a href="{article["url"]}" target="_blank">{title}</a></h4>',
                        ]
                        if desc:
                            parts.append(f'<div class="desc">{desc}</div>')
                        parts.append(f'<div class="meta"><span>❤️ {article["reactions"]}</span><span>💬 {article["comments"]}</span><span>📅 {article["published_at"]}</span></div>')
                        if tags_html:
                            parts.append(f'<div class="tags">{tags_html}</div>')
                        parts.append('</div>')
                        st.markdown("".join(parts), unsafe_allow_html=True)
                else:
                    st.info("暂无数据")

        with row2_mid:
            st.markdown("#### 📺 B站技术视频")
            with st.container(height=420):
                if trends["bilibili"]:
                    for video in trends["bilibili"]:
                        play_str = f"{video['play']:,}" if isinstance(video.get("play"), int) else str(video.get("play", 0))
                        title = html_lib.escape(video['title'])
                        author = html_lib.escape(video.get('author', ''))
                        thumb = f'<img src="{video["thumbnail"]}" referrerpolicy="no-referrer" style="width:120px;border-radius:6px;margin-right:10px;float:left;" />' if video.get("thumbnail") else ""
                        card = f'<div class="trend-card">{thumb}<h4><a href="{video["url"]}" target="_blank">{title}</a></h4><div class="meta"><span>👤 {author}</span><span>▶️ {play_str}</span><span>💬 {video.get("danmaku", 0)}</span><span>⏱️ {video.get("duration", "")}</span></div><div style="clear:both;"></div></div>'
                        st.markdown(card, unsafe_allow_html=True)
                else:
                    st.info("暂无 B站 数据")

