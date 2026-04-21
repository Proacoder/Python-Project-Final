import streamlit as st
from datetime import date
from assignments import (
    get_assignments, add_assignment,
    mark_completed, delete_assignment
)

PRIORITY_COLOR = {"High": "#f38ba8", "Medium": "#f9e2af", "Low": "#a6e3a1"}
STATUS_BADGE = {
    "Pending":   ("⏳", "#313244", "#cdd6f4"),
    "Completed": ("✅", "#1e3a2e", "#a6e3a1"),
    "Overdue":   ("🚨", "#3a1e1e", "#f38ba8"),
}


def show_subject_page():
    """Render the Subject detail page."""
    user   = st.session_state.user
    subject = st.session_state.get("selected_subject")

    if not subject:
        st.error("No subject selected.")
        if st.button("← Back to Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()
        return

    # ── Breadcrumb / top nav ──────────────────────────────────────────────────
    col_back, col_title = st.columns([1, 5])
    with col_back:
        if st.button("← Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()
    with col_title:
        color = subject.get("color", "#6366f1")
        st.markdown(
            f"<h2 style='color:{color}; margin:0;'>📖 {subject['name']}</h2>",
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ── Add assignment form ───────────────────────────────────────────────────
    with st.expander("➕ Add New Assignment", expanded=False):
        with st.form("add_assignment_form", clear_on_submit=True):
            title       = st.text_input("Title *", placeholder="Assignment title")
            description = st.text_area("Description", placeholder="Optional notes…", height=80)

            col_dl, col_len = st.columns(2)
            with col_dl:
                deadline = st.date_input("Deadline *", min_value=date.today())
            with col_len:
                length_hours = st.number_input(
                    "Estimated hours *", min_value=0.5, max_value=200.0,
                    value=2.0, step=0.5,
                    help="Rough time required to complete. Affects priority."
                )

            uploaded = st.file_uploader(
                "Upload file (optional)",
                type=["pdf", "docx", "doc", "txt", "pptx", "xlsx", "zip", "png", "jpg", "jpeg"]
            )

            if st.form_submit_button("Add Assignment", type="primary"):
                ok, msg = add_assignment(
                    subject_id=subject["id"],
                    user_id=user["id"],
                    title=title,
                    description=description,
                    deadline=str(deadline),
                    length_hours=length_hours,
                    uploaded_file=uploaded
                )
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

    # ── Filters & sort ────────────────────────────────────────────────────────
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filter_status = st.selectbox(
            "Filter by status",
            ["All", "Pending", "Completed", "Overdue"],
            key="subj_filter_status"
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
            key="subj_sort_by"
        )

    st.markdown("---")

    # ── Assignment list ───────────────────────────────────────────────────────
    assignments = get_assignments(subject["id"], user["id"], sort_by, filter_status)

    if not assignments:
        st.info("No assignments found. Add one above!")
        return

    st.markdown(f"**{len(assignments)} assignment(s)**")
    st.markdown("<br>", unsafe_allow_html=True)

    for a in assignments:
        _assignment_card(a, user["id"])


def _assignment_card(a: dict, user_id: int):
    priority     = a["priority"]
    status       = a["status"]
    p_color      = PRIORITY_COLOR.get(priority, "#cdd6f4")
    s_emoji, s_bg, s_fg = STATUS_BADGE.get(status, ("", "#313244", "#cdd6f4"))

    days_text = ""
    try:
        from datetime import date
        dl = date.fromisoformat(a["deadline"])
        diff = (dl - date.today()).days
        if diff < 0:
            days_text = f"<span style='color:#f38ba8;'>({abs(diff)}d overdue)</span>"
        elif diff == 0:
            days_text = "<span style='color:#f9e2af;'>(Due today!)</span>"
        else:
            days_text = f"<span style='color:#a6adc8;'>({diff}d left)</span>"
    except Exception:
        pass

    file_badge = ""
    if a.get("file_name"):
        size_kb = round(a["file_size"] / 1024, 1) if a.get("file_size") else "?"
        file_badge = f"📎 <span style='color:#89b4fa;'>{a['file_name']}</span> <span style='color:#6c7086;'>({size_kb} KB)</span>"

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
                    <span style="font-size:1.1rem; font-weight:600; color:#cdd6f4;">{a['title']}</span>
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
            {'<div style="color:#a6adc8; font-size:0.88rem; margin-top:0.4rem;">'+a['description']+'</div>' if a.get('description') else ''}
            <div style="margin-top:0.5rem; font-size:0.82rem; color:#a6adc8;">
                ⏱ {a['length_hours']}h &nbsp;|&nbsp;
                Priority: <span style="color:{p_color}; font-weight:600;">{priority}</span>
                (score: {a['priority_score']})
                {'&nbsp;|&nbsp;' + file_badge if file_badge else ''}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_done, col_del, col_spacer = st.columns([2, 1, 5])
    with col_done:
        if a["status"] != "Completed":
            if st.button("✅ Mark Done", key=f"done_{a['id']}", use_container_width=True):
                mark_completed(a["id"], user_id)
                st.rerun()
    with col_del:
        if st.button("🗑 Delete", key=f"delA_{a['id']}", use_container_width=True):
            delete_assignment(a["id"], user_id)
            st.rerun()
