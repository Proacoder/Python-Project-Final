"""
Assignment database operations module.
Handles CRUD operations for assignments.
"""
import os
import sqlite3
from datetime import date, datetime
from database import get_connection

UPLOADS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)


def calculate_priority(deadline: str, length_hours: float) -> tuple[str, float]:
    """
    Calculate priority level and score based on deadline and task length.
    
    Returns:
        (priority_level: str, priority_score: float)
    """
    try:
        dl = date.fromisoformat(deadline)
        days_until = (dl - date.today()).days
    except (ValueError, TypeError):
        days_until = 10  # default
    
    # Score: higher is more urgent
    # Factors: days remaining, hours required
    days_factor = max(0, 10 - days_until)  # More urgent as deadline approaches
    hours_factor = min(length_hours / 10, 3)  # Cap hours factor at 3
    score = days_factor * 2 + hours_factor
    
    if score >= 12:
        priority = "High"
    elif score >= 6:
        priority = "Medium"
    else:
        priority = "Low"
    
    return priority, round(score, 2)


def get_assignments(subject_id: int, user_id: int, sort_by: str = "deadline", filter_status: str = "All") -> list[dict]:
    """
    Fetch assignments for a subject with filtering and sorting.
    
    Args:
        subject_id: ID of the subject
        user_id: ID of the user
        sort_by: Field to sort by ('deadline', 'priority_score', 'title', 'created_at', 'status')
        filter_status: Status filter ('All', 'Pending', 'Completed', 'Overdue')
    
    Returns:
        List of assignment dictionaries
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Build WHERE clause
    where_parts = ["subject_id = ? AND user_id = ?"]
    params = [subject_id, user_id]
    
    if filter_status != "All":
        if filter_status == "Overdue":
            where_parts.append(f"status = 'Pending' AND deadline < date('now')")
        else:
            where_parts.append(f"status = ?")
            params.append(filter_status)
    
    where_clause = " AND ".join(where_parts)
    
    # Map sort_by to SQL column
    sort_map = {
        "deadline": "deadline ASC",
        "priority_score": "priority_score DESC",
        "title": "title ASC",
        "created_at": "created_at DESC",
        "status": "status ASC"
    }
    order_by = sort_map.get(sort_by, "deadline ASC")
    
    query = f"""
        SELECT 
            id, subject_id, user_id, title, description,
            deadline, length_hours, status, priority, priority_score,
            file_path, file_name, file_size, created_at, completed_at
        FROM assignments
        WHERE {where_clause}
        ORDER BY {order_by}
    """
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def add_assignment(subject_id: int, user_id: int, title: str, description: str,
                   deadline: str, length_hours: float, uploaded_file=None) -> tuple[bool, str]:
    """
    Add a new assignment.
    
    Args:
        subject_id: ID of the subject
        user_id: ID of the user
        title: Assignment title
        description: Assignment description
        deadline: Deadline date (YYYY-MM-DD)
        length_hours: Estimated hours to complete
        uploaded_file: Optional uploaded file object (Streamlit UploadedFile)
    
    Returns:
        (success: bool, message: str)
    """
    # Validation
    if not title or not title.strip():
        return False, "Title is required."
    
    if not deadline:
        return False, "Deadline is required."
    
    try:
        deadline_date = date.fromisoformat(deadline)
    except (ValueError, TypeError):
        return False, "Invalid deadline format."
    
    if deadline_date < date.today():
        return False, "Deadline cannot be in the past."
    
    if length_hours <= 0:
        return False, "Hours must be greater than 0."
    
    # Calculate priority
    priority, priority_score = calculate_priority(deadline, length_hours)
    
    # Handle file upload
    file_path = None
    file_name = None
    file_size = None
    
    if uploaded_file is not None:
        try:
            # Save file
            file_name = uploaded_file.name
            file_path = os.path.join(UPLOADS_DIR, f"{user_id}_{subject_id}_{file_name}")
            file_size = len(uploaded_file.getbuffer())
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        except Exception as e:
            return False, f"File upload failed: {str(e)}"
    
    # Insert into database
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO assignments (
                subject_id, user_id, title, description,
                deadline, length_hours, status, priority, priority_score,
                file_path, file_name, file_size, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            subject_id, user_id, title.strip(), description.strip(),
            deadline, length_hours, "Pending", priority, priority_score,
            file_path, file_name, file_size
        ))
        
        conn.commit()
        conn.close()
        
        return True, f"Assignment '{title}' added successfully!"
    
    except sqlite3.IntegrityError:
        return False, "Database error: integrity constraint violated."
    except Exception as e:
        return False, f"Database error: {str(e)}"


def mark_completed(assignment_id: int, user_id: int) -> tuple[bool, str]:
    """
    Mark an assignment as completed.
    
    Args:
        assignment_id: ID of the assignment
        user_id: ID of the user (for verification)
    
    Returns:
        (success: bool, message: str)
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verify user owns this assignment
        cursor.execute("SELECT user_id FROM assignments WHERE id = ?", (assignment_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return False, "Assignment not found."
        
        if row["user_id"] != user_id:
            conn.close()
            return False, "Unauthorized: you don't own this assignment."
        
        # Update status
        cursor.execute("""
            UPDATE assignments
            SET status = ?, completed_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, ("Completed", assignment_id))
        
        conn.commit()
        conn.close()
        
        return True, "Assignment marked as completed!"
    
    except Exception as e:
        return False, f"Error: {str(e)}"


def delete_assignment(assignment_id: int, user_id: int) -> tuple[bool, str]:
    """
    Delete an assignment (and its associated file if exists).
    
    Args:
        assignment_id: ID of the assignment
        user_id: ID of the user (for verification)
    
    Returns:
        (success: bool, message: str)
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Fetch the assignment to get file info
        cursor.execute(
            "SELECT user_id, file_path FROM assignments WHERE id = ?",
            (assignment_id,)
        )
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return False, "Assignment not found."
        
        if row["user_id"] != user_id:
            conn.close()
            return False, "Unauthorized: you don't own this assignment."
        
        # Delete file if exists
        if row["file_path"] and os.path.exists(row["file_path"]):
            try:
                os.remove(row["file_path"])
            except Exception as e:
                print(f"Warning: Could not delete file {row['file_path']}: {e}")
        
        # Delete from database
        cursor.execute("DELETE FROM assignments WHERE id = ?", (assignment_id,))
        conn.commit()
        conn.close()
        
        return True, "Assignment deleted successfully!"
    
    except Exception as e:
        return False, f"Error: {str(e)}"


def get_dashboard_stats(user_id: int) -> dict:
    """
    Get dashboard statistics for a user.
    
    Returns:
        dict with keys: total, pending, completed, overdue, high_priority
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Get total assignments
        cursor.execute("SELECT COUNT(*) FROM assignments WHERE user_id = ?", (user_id,))
        total = cursor.fetchone()[0]
        
        # Get pending assignments
        cursor.execute("SELECT COUNT(*) FROM assignments WHERE user_id = ? AND status = 'Pending'", (user_id,))
        pending = cursor.fetchone()[0]
        
        # Get completed assignments
        cursor.execute("SELECT COUNT(*) FROM assignments WHERE user_id = ? AND status = 'Completed'", (user_id,))
        completed = cursor.fetchone()[0]
        
        # Get overdue assignments (pending assignments past deadline)
        cursor.execute("""
            SELECT COUNT(*) FROM assignments 
            WHERE user_id = ? AND status = 'Pending' AND deadline < date('now')
        """, (user_id,))
        overdue = cursor.fetchone()[0]
        
        # Get high priority assignments
        cursor.execute("SELECT COUNT(*) FROM assignments WHERE user_id = ? AND priority = 'High'", (user_id,))
        high_priority = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total": total,
            "pending": pending,
            "completed": completed,
            "overdue": overdue,
            "high_priority": high_priority
        }
    
    except Exception as e:
        conn.close()
        # Return zeros on error
        return {
            "total": 0,
            "pending": 0,
            "completed": 0,
            "overdue": 0,
            "high_priority": 0
        }


def get_all_assignments(user_id: int, sort_by: str = "deadline", filter_status: str = "All") -> list[dict]:
    """
    Fetch all assignments for a user across all subjects with filtering and sorting.
    
    Args:
        user_id: ID of the user
        sort_by: Field to sort by ('deadline', 'priority_score', 'title', 'created_at', 'status')  
        filter_status: Filter by status ('All', 'Pending', 'Completed', 'Overdue')
    
    Returns:
        List of assignment dictionaries
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Build query based on filter
        query = """
            SELECT a.*, s.name as subject_name, s.color as subject_color
            FROM assignments a
            JOIN subjects s ON a.subject_id = s.id
            WHERE a.user_id = ?
        """
        params = [user_id]
        
        if filter_status != "All":
            if filter_status == "Overdue":
                query += " AND a.status = 'Pending' AND a.deadline < date('now')"
            else:
                query += " AND a.status = ?"
                params.append(filter_status)
        
        # Add sorting
        sort_mapping = {
            "deadline": "a.deadline ASC",
            "priority_score": "a.priority_score DESC",
            "title": "a.title ASC", 
            "created_at": "a.created_at DESC",
            "status": "a.status ASC"
        }
        query += f" ORDER BY {sort_mapping.get(sort_by, 'a.deadline ASC')}"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        assignments = []
        for row in rows:
            assignment = dict(row)
            
            # Calculate if overdue
            if assignment["status"] == "Pending" and assignment["deadline"] < date.today().isoformat():
                assignment["status"] = "Overdue"
            
            assignments.append(assignment)
        
        conn.close()
        return assignments
    
    except Exception as e:
        conn.close()
        return []


def mark_overdue(assignment_id: int, user_id: int) -> tuple[bool, str]:
    """
    Mark an assignment as overdue (for assignments that are past deadline but still pending).
    
    Args:
        assignment_id: ID of the assignment
        user_id: ID of the user (for authorization)
    
    Returns:
        (success: bool, message: str)
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Check if assignment exists and belongs to user
        cursor.execute(
            "SELECT user_id, status, deadline FROM assignments WHERE id = ?",
            (assignment_id,)
        )
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return False, "Assignment not found."
        
        if row["user_id"] != user_id:
            conn.close()
            return False, "Unauthorized: you don't own this assignment."
        
        # Only mark as overdue if it's pending and past deadline
        if row["status"] == "Pending" and row["deadline"] < date.today().isoformat():
            # Update status to Overdue
            cursor.execute(
                "UPDATE assignments SET status = 'Overdue' WHERE id = ?",
                (assignment_id,)
            )
            conn.commit()
            conn.close()
            return True, "Assignment marked as overdue."
        else:
            conn.close()
            return False, "Assignment is not eligible to be marked as overdue."
    
    except Exception as e:
        conn.close()
        return False, f"Error: {str(e)}"
