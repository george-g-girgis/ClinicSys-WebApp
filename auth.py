"""
auth.py — Authentication helpers for ClinicSys.

Keeps all credential-verification logic in one place,
separate from both the database layer and the UI.
"""

import bcrypt
from database import get_connection


def verify_login(username: str, password: str) -> tuple[bool, str | None]:
    """Check *username* / *password* against the Admin_Users table.

    Returns (True, role) on success, (False, None) on failure.
    All comparisons use bcrypt — plain-text passwords are never stored or logged.
    """
    conn = get_connection()
    try:
        cursor = conn.execute(
            "SELECT PasswordHash, Role FROM Admin_Users WHERE Username = ?;",
            (username,),
        )
        row = cursor.fetchone()

        if row is None:
            return False, None

        stored_hash = row["PasswordHash"].encode("utf-8")
        if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
            return True, row["Role"]
        return False, None
    finally:
        conn.close()
