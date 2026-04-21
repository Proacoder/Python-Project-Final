import streamlit as st
from subjects import get_subjects, add_subject, delete_subject
from assignments import get_dashboard_stats

PRIORITY_EMOJI = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
STATUS_EMOJI = {"Pending": "⏳", "Completed": "✅", "Overdue": "🚨"}


def show_dashboard():
    """Render the main dashboard page."""
    user = st.session_state.user

    # ── Top bar ──────────────────────────────────────────────────────────────
    col_title, col_logout = st.columns([5, 1])
    with col_title:
        st.markdown(f"## 👋 Hello, **{user['username']}**!")
    with col_logout:
        if st.button("Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    st.markdown("---")

    # ── Stats row ────────────────────────────────────────────────────────────
    stats = get_dashboard_stats(user["id"])
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("📋 Total", stats["total"] or 0)
    c2.metric("⏳ Pending", stats["pending"] or 0)
    c3.metric("✅ Completed", stats["completed"] or 0)
    c4.metric("🚨 Overdue", stats["overdue"] or 0)
    c5.metric("🔴 High Priority", stats["high_priority"] or 0)

    st.markdown("---")

    # ── All assignments quick view ────────────────────────────────────────────
    col_subj, col_view = st.columns([3, 1])
    with col_subj:
        st.markdown("### 📚 My Subjects")
    with col_view:
        if st.button("📋 View All Assignments", use_container_width=True):
            st.session_state.page = "all_assignments"
            st.rerun()
        if st.button("🤖 Chatbot", use_container_width=True):
            st.session_state.page = "chatbot"
            st.rerun()

    # ── Add subject form ─────────────────────────────────────────────────────
    with st.expander("➕ Add New Subject", expanded=False):
        with st.form("add_subject_form", clear_on_submit=True):
            new_subject = st.text_input("Subject Name", placeholder="e.g. Mathematics, History…")
            color = st.color_picker("Pick a colour", "#6366f1")
            if st.form_submit_button("Add Subject", type="primary"):
                if new_subject.strip():
                    ok, msg = add_subject(user["id"], new_subject.strip(), color)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                else:
                    st.error("Subject name cannot be empty.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Subject cards ─────────────────────────────────────────────────────────
    subjects = get_subjects(user["id"])

    if not subjects:
        st.info("No subjects yet. Add your first subject above! 🎓")
        return

    # Display in a 3-column grid
    cols = st.columns(3)
    for idx, subj in enumerate(subjects):
        with cols[idx % 3]:
            _subject_card(subj, user["id"])


def _subject_card(subj: dict, user_id: int):
    color = subj.get("color", "#6366f1")
    pending  = subj["pending"]  or 0
    overdue  = subj["overdue"]  or 0
    completed = subj["completed"] or 0
    total    = subj["total_assignments"] or 0

    st.markdown(
        f"""
        <div style="
            display: block;
            width: 100%;
            border-left: 5px solid {color};
            background: #1e1e2e;
            border-radius: 10px;
            padding: 1rem 1.2rem;
            margin-bottom: 0.75rem;
            border: 1px solid #313244;
            border-left: 5px solid {color};
        ">
            <h4 style="margin:0; color:#cdd6f4;">{subj['name']}</h4>
            <div style="color:#a6adc8; font-size:0.85rem; margin-top:0.4rem;">
                📋 {total} assignments &nbsp;|&nbsp;
                ⏳ {pending} pending &nbsp;|&nbsp;
                🚨 {overdue} overdue
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_open, col_del = st.columns([3, 1])
    with col_open:
        if st.button("Open", key=f"open_{subj['id']}", use_container_width=True, type="primary"):
            st.session_state.selected_subject = subj
            st.session_state.page = "subject"
            st.rerun()
    with col_del:
        if st.button("🗑", key=f"del_{subj['id']}", use_container_width=True):
            ok, msg = delete_subject(subj["id"], user_id)
            if ok:
                st.rerun()
            else:
                st.error(msg)
