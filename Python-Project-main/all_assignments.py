import streamlit as st
from assignments import get_all_assignments, mark_completed, delete_assignment

PRIORITY_COLOR = {"High": "#f38ba8", "Medium": "#f9e2af", "Low": "#a6e3a1"}
STATUS_BADGE = {
    "Pending":   ("⏳", "#313244", "#cdd6f4"),
    "Completed": ("✅", "#1e3a2e", "#a6e3a1"),
    "Overdue":   ("🚨", "#3a1e1e", "#f38ba8"),
}


def show_all_assignments_page():
    """Show all assignments across subjects with sort/filter."""
    user = st.session_state.user

    col_back, col_title = st.columns([1, 5])
    with col_back:
        if st.button("← Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()
    with col_title:
        st.markdown("## 📋 All Assignments")

    st.markdown("---")

    # ── Filters ───────────────────────────────────────────────────────────────
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        filter_status = st.selectbox(
            "Filter by status",
            ["All", "Pending", "Completed", "Overdue"],
            key="all_filter_status"
        )
    with col_f2:
        sort_by = st.selectbox(
            "Sort by",
            ["priority_score", "deadline", "title", "created_at", "status"],
            format_func=lambda x: {
                "priority_score": "Priority",
                "deadline": "Deadline",
                "title": "Title (A-Z)",
                "created_at": "Date Added",
                "status": "Status"
            }[x],
            key="all_sort_by"
        )
    with col_f3:
        priority_filter = st.selectbox(
            "Filter by priority",
            ["All", "High", "Medium", "Low"],
            key="all_priority_filter"
        )

    assignments = get_all_assignments(user["id"], sort_by, filter_status)

    # Apply priority filter (client-side)
    if priority_filter != "All":
        assignments = [a for a in assignments if a["priority"] == priority_filter]

    st.markdown(f"**{len(assignments)} assignment(s) found**")
    st.markdown("<br>", unsafe_allow_html=True)

    if not assignments:
        st.info("No assignments match your filters.")
        return

    for a in assignments:
        _card(a, user["id"])


def _card(a: dict, user_id: int):
    from datetime import date

    priority     = a["priority"]
    status       = a["status"]
    p_color      = PRIORITY_COLOR.get(priority, "#cdd6f4")
    s_emoji, s_bg, s_fg = STATUS_BADGE.get(status, ("", "#313244", "#cdd6f4"))

    days_text = ""
    try:
        dl   = date.fromisoformat(a["deadline"])
        diff = (dl - date.today()).days
        if diff < 0:
            days_text = f"<span style='color:#f38ba8;'>({abs(diff)}d overdue)</span>"
        elif diff == 0:
            days_text = "<span style='color:#f9e2af;'>(Due today!)</span>"
        else:
            days_text = f"<span style='color:#a6adc8;'>({diff}d left)</span>"
    except Exception:
        pass

    subj_color = a.get("subject_color", "#6366f1")

    st.markdown(
        f"""
        <div style="
            background: #1e1e2e;
            border: 1px solid #313244;
            border-left: 5px solid {p_color};
            border-radius: 10px;
            padding: 1rem 1.2rem;
            margin-bottom: 0.6rem;
        ">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div>
                    <span style="
                        background:{subj_color}22; color:{subj_color};
                        padding:1px 8px; border-radius:20px; font-size:0.75rem;
                        margin-right:6px;
                    ">{a['subject_name']}</span>
                    <span style="font-size:1.05rem; font-weight:600; color:#cdd6f4;">{a['title']}</span>
                    &nbsp;
                    <span style="
                        background:{s_bg}; color:{s_fg};
                        padding:2px 8px; border-radius:20px; font-size:0.78rem;
                    ">{s_emoji} {status}</span>
                </div>
                <div style="text-align:right; font-size:0.82rem; color:#a6adc8;">
                    🗓 {a['deadline']} {days_text}
                </div>
            </div>
            <div style="margin-top:0.4rem; font-size:0.82rem; color:#a6adc8;">
                ⏱ {a['length_hours']}h &nbsp;|&nbsp;
                Priority: <span style="color:{p_color}; font-weight:600;">{priority}</span>
                (score: {a['priority_score']})
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_done, col_del, col_spacer = st.columns([2, 1, 5])
    with col_done:
        if a["status"] != "Completed":
            if st.button("✅ Mark Done", key=f"allDone_{a['id']}", use_container_width=True):
                mark_completed(a["id"], user_id)
                st.rerun()
    with col_del:
        if st.button("🗑 Delete", key=f"allDel_{a['id']}", use_container_width=True):
            delete_assignment(a["id"], user_id)
            st.rerun()
