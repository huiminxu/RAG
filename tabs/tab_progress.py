import streamlit as st
import pandas as pd
from rag_engine import generate_learning_report
from progress import get_stats, get_progress_summary, get_review_stats


def render():
    st.title("📈 学习进度")
    st.caption("追踪学习数据，AI 生成个性化报告")

    stats = get_stats()
    review_stats = get_review_stats()

    # --- 数据概览卡片 ---
    with st.container(border=True):
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            st.metric("🎯 模拟面试", f"{stats['total_interviews']} 次")
        with col2:
            avg = f"{stats['avg_score']} 分" if stats['avg_score'] else "暂无"
            st.metric("💯 平均分", avg)
        with col3:
            st.metric("📚 学习资源", f"{stats['total_resources']} 篇")
        with col4:
            st.metric("📖 精读篇数", f"{stats.get('files_read', 0)} 篇")
        with col5:
            st.metric("📝 笔记总数", f"{stats.get('total_notes', 0)} 条")
        with col6:
            st.metric("🧠 待复习", f"{review_stats['due_today']} 张")
        with col7:
            st.metric("🔥 学习天数", f"{stats['total_study_days']} 天")

    # --- 图表 ---
    col_left, col_right = st.columns([1, 1])

    with col_left:
        if stats["recent_scores"]:
            st.markdown("#### 📊 评分趋势")
            score_df = pd.DataFrame({
                "次数": list(range(1, len(stats["recent_scores"]) + 1)),
                "分数": stats["recent_scores"],
            })
            st.line_chart(score_df, x="次数", y="分数", height=200)
        else:
            st.markdown("#### 📊 评分趋势")
            st.info("完成面试后这里会显示评分趋势")

    with col_right:
        if stats["category_distribution"]:
            st.markdown("#### 📂 分类分布")
            cat_df = pd.DataFrame(
                list(stats["category_distribution"].items()),
                columns=["分类", "数量"],
            )
            st.bar_chart(cat_df, x="分类", y="数量", height=200)
        else:
            st.markdown("#### 📂 分类分布")
            st.info("导入资源后这里会显示分类分布")

    # --- 最近动态 ---
    if stats["total_interviews"] > 0 or stats["total_resources"] > 0:
        with st.expander("📋 最近学习动态", expanded=False):
            summary = get_progress_summary()
            st.markdown(summary)

    # --- AI 学习报告 ---
    st.divider()
    if st.button("🧠 生成 AI 学习报告", type="primary"):
        if stats["total_interviews"] == 0 and stats["total_resources"] == 0:
            st.warning("暂无学习数据，请先进行面试或导入资源后再生成报告")
        else:
            with st.spinner("正在分析学习数据..."):
                summary = get_progress_summary()
                report = generate_learning_report(summary)
            st.markdown(report)
