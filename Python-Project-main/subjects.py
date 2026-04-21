from database import get_connection

SUBJECT_COLORS = [
    "#6366f1", "#ec4899", "#14b8a6", "#f59e0b",
    "#ef4444", "#8b5cf6", "#10b981", "#3b82f6",
    "#f97316", "#06b6d4"
]


def get_subjects(user_id: int) -> list[dict]:
    """Return all subjects for a user."""
    conn = get_connection()
    try:
        rows = conn.execute(
            """SELECT s.id, s.name, s.color, s.created_at,
                      COUNT(a.id) AS total_assignments,
                      SUM(CASE WHEN a.status = 'Pending' THEN 1 ELSE 0 END) AS pending,
                      SUM(CASE WHEN a.status = 'Completed' THEN 1 ELSE 0 END) AS completed,
                      SUM(CASE WHEN a.status = 'Overdue' THEN 1 ELSE 0 END) AS overdue
               FROM subjects s
               LEFT JOIN assignments a ON a.subject_id = s.id
               WHERE s.user_id = ?
               GROUP BY s.id
               ORDER BY s.created_at DESC""",
            (user_id,)
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def add_subject(user_id: int, name: str, color: str = None) -> tuple[bool, str]:
    name = name.strip()
    if not name:
        return False, "Subject name cannot be empty."
    if len(name) > 100:
        return False, "Subject name too long (max 100 chars)."

    conn = get_connection()
    try:
        existing = conn.execute(
            "SELECT id FROM subjects WHERE user_id = ? AND LOWER(name) = LOWER(?)",
            (user_id, name)
        ).fetchone()
        if existing:
            return False, "A subject with this name already exists."

        if not color:
            count = conn.execute(
                "SELECT COUNT(*) FROM subjects WHERE user_id = ?", (user_id,)
            ).fetchone()[0]
            color = SUBJECT_COLORS[count % len(SUBJECT_COLORS)]

        conn.execute(
            "INSERT INTO subjects (user_id, name, color) VALUES (?, ?, ?)",
            (user_id, name, color)
        )
        conn.commit()
        return True, "Subject added successfully."
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()


def delete_subject(subject_id: int, user_id: int) -> tuple[bool, str]:
    conn = get_connection()
    try:
        result = conn.execute(
            "DELETE FROM subjects WHERE id = ? AND user_id = ?",
            (subject_id, user_id)
        )
        conn.commit()
        if result.rowcount == 0:
            return False, "Subject not found."
        return True, "Subject deleted."
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()


def get_subject(subject_id: int, user_id: int) -> dict | None:
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM subjects WHERE id = ? AND user_id = ?",
            (subject_id, user_id)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()
