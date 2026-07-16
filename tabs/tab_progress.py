import streamlit as st
import pandas as pd
from rag_engine import generate_learning_report
from progress import get_stats, get_progress_summary


def render():
    st.title("🌱 学习进度")
    st.caption("追踪学习数据，AI 生成个性化学习报告")

    stats = get_stats()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("模拟面试", f"{stats['total_interviews']} 次")
    with col2:
        st.metric("平均分", f"{stats['avg_score']}" if stats['avg_score'] else "暂无")
    with col3:
        st.metric("学习资源", f"{stats['total_resources']} 篇")
    with col4:
        st.metric("学习天数", f"{stats['total_study_days']} 天")

    if stats["recent_scores"]:
        st.subheader("📊 面试评分趋势")
        score_df = pd.DataFrame({
            "次数": list(range(1, len(stats["recent_scores"]) + 1)),
            "分数": stats["recent_scores"],
        })
        st.line_chart(score_df, x="次数", y="分数")

    if stats["category_distribution"]:
        st.subheader("📂 分类学习分布")
        cat_df = pd.DataFrame(
            list(stats["category_distribution"].items()),
            columns=["分类", "数量"],
        )
        st.bar_chart(cat_df, x="分类", y="数量")

    st.divider()

    if st.button("🧠 生成 AI 学习报告", type="primary"):
        if stats["total_interviews"] == 0 and stats["total_resources"] == 0:
            st.warning("暂无学习数据，请先进行面试或导入资源后再生成报告")
        else:
            with st.spinner("🌱 AI 正在分析你的学习数据..."):
                summary = get_progress_summary()
                report = generate_learning_report(summary)
            st.markdown(report)
