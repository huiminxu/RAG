import streamlit as st
from progress import load_meeting_rooms, save_meeting_room, delete_meeting_room


def render():
    st.title("📹 自习室")
    st.caption("与学习伙伴视频连线，一起专注学习")
    render_content()


def render_content():
    tab_jitsi, tab_tencent = st.tabs(["🌐 在线视频（免安装）", "📱 腾讯会议"])

    with tab_jitsi:
        st.markdown("输入相同房间名即可和伙伴进入同一自习室，无需安装任何软件。")
        col_input, col_btn = st.columns([4, 1])
        with col_input:
            room_name = st.text_input(
                "房间名",
                placeholder="输入房间名（如：huimin-study）",
                key="jitsi_room_name",
                label_visibility="collapsed",
            )
        with col_btn:
            join_clicked = st.button("🚀 进入", key="join_jitsi", use_container_width=True)

        if join_clicked and room_name.strip():
            st.session_state.jitsi_room = room_name.strip().replace(" ", "-")
        elif join_clicked:
            st.warning("请输入房间名")

        if st.session_state.get("jitsi_room"):
            room = st.session_state.jitsi_room
            jitsi_url = f"https://meet.jit.si/{room}"

            with st.container(border=True):
                st.markdown(f"**当前房间：** `{room}`")
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.link_button(
                        "🚀 打开视频自习室",
                        jitsi_url,
                        use_container_width=True,
                    )
                with col2:
                    if st.button("❌ 离开", key="leave_jitsi", use_container_width=True):
                        st.session_state.pop("jitsi_room", None)
                        st.rerun()

            st.info("💡 首次使用需 Google 账号登录（免费）。分享房间名给伙伴，对方输入相同名字即可加入。")

    with tab_tencent:
        st.markdown("保存常用腾讯会议链接，一键加入。")
        col_name, col_url, col_btn = st.columns([2, 4, 1])
        with col_name:
            t_name = st.text_input(
                "名称",
                placeholder="会议名称",
                key="room_name_input",
                label_visibility="collapsed",
            )
        with col_url:
            t_url = st.text_input(
                "链接",
                placeholder="粘贴腾讯会议链接...",
                key="room_url_input",
                label_visibility="collapsed",
            )
        with col_btn:
            if st.button("➕", key="add_room", use_container_width=True):
                if t_name.strip() and t_url.strip():
                    save_meeting_room(t_name.strip(), t_url.strip())
                    st.rerun()

        rooms = load_meeting_rooms()
        if not rooms:
            st.caption("暂无保存的会议，添加一个试试")
        else:
            for room in rooms:
                with st.container(border=True):
                    col_info, col_join, col_del = st.columns([5, 2, 1])
                    with col_info:
                        st.markdown(f"**{room['name']}**")
                    with col_join:
                        st.link_button("🚀 加入", room["url"], use_container_width=True)
                    with col_del:
                        if st.button("🗑️", key=f"del_room_{room['id']}"):
                            delete_meeting_room(room["id"])
                            st.rerun()
