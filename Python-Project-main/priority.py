from datetime import date, datetime


def calculate_priority(deadline_str: str, length_hours: float, status: str) -> tuple[str, float]:
    """
    Calculate assignment priority based on deadline proximity and length.

    Returns:
        (priority_label, priority_score)
        priority_label: 'High', 'Medium', or 'Low'
        priority_score: float 0.0 - 100.0
    """
    if status == "Completed":
        return "Low", 0.0

    try:
        if isinstance(deadline_str, str):
            deadline = date.fromisoformat(deadline_str)
        else:
            deadline = deadline_str
    except Exception:
        return "Low", 0.0

    today = date.today()
    days_remaining = (deadline - today).days

    # --- Time urgency score (0-70 points) ---
    if days_remaining < 0:
        time_score = 70.0  # Overdue: max time score
    elif days_remaining == 0:
        time_score = 68.0  # Due today
    elif days_remaining <= 1:
        time_score = 62.0
    elif days_remaining <= 3:
        time_score = 52.0
    elif days_remaining <= 7:
        time_score = 38.0
    elif days_remaining <= 14:
        time_score = 22.0
    elif days_remaining <= 30:
        time_score = 12.0
    else:
        time_score = 4.0

    # --- Length/complexity score (0-30 points) ---
    # Normalise: 1h=3pts, 3h=10pts, 5h=16pts, 10h=24pts, 20h+=30pts
    length_hours = max(0.5, float(length_hours))
    if length_hours >= 20:
        length_score = 30.0
    elif length_hours >= 10:
        length_score = 24.0 + (length_hours - 10) / 10 * 6
    elif length_hours >= 5:
        length_score = 16.0 + (length_hours - 5) / 5 * 8
    elif length_hours >= 3:
        length_score = 10.0 + (length_hours - 3) / 2 * 6
    elif length_hours >= 1:
        length_score = 3.0 + (length_hours - 1) / 2 * 7
    else:
        length_score = 1.0

    priority_score = round(time_score + length_score, 2)

    # Label thresholds
    if priority_score >= 55:
        label = "High"
    elif priority_score >= 28:
        label = "Medium"
    else:
        label = "Low"

    return label, priority_score


def determine_status(current_status: str, deadline_str: str) -> str:
    """
    Automatically determine assignment status.
    - Completed stays Completed.
    - Past deadline → Overdue.
    - Otherwise → Pending.
    """
    if current_status == "Completed":
        return "Completed"

    try:
        if isinstance(deadline_str, str):
            deadline = date.fromisoformat(deadline_str)
        else:
            deadline = deadline_str
    except Exception:
        return current_status

    if date.today() > deadline:
        return "Overdue"
    return "Pending"


def recalculate_all(conn, user_id: int):
    """Recalculate priority and status for all non-completed assignments of a user."""
    assignments = conn.execute(
        "SELECT id, deadline, length_hours, status FROM assignments WHERE user_id = ?",
        (user_id,)
    ).fetchall()

    for row in assignments:
        new_status = determine_status(row["status"], row["deadline"])
        new_priority, new_score = calculate_priority(row["deadline"], row["length_hours"], new_status)

        conn.execute(
            """UPDATE assignments
               SET status = ?, priority = ?, priority_score = ?
               WHERE id = ?""",
            (new_status, new_priority, new_score, row["id"])
        )
    conn.commit()
