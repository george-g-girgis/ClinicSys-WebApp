"""
database.py — Database initialization and helper functions for ClinicSys.

Handles SQLite connection, table creation, and default admin seeding.
All queries use strict parameter binding to prevent SQL injection.
"""

import sqlite3
import os
import sys
import bcrypt

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
if getattr(sys, 'frozen', False):
    # Running in a PyInstaller bundle, store db next to the .exe
    DB_DIR = os.path.dirname(sys.executable)
else:
    # Running in normal Python environment
    DB_DIR = os.path.dirname(os.path.abspath(__file__))

DB_NAME = os.path.join(DB_DIR, "clinic.db")


# ---------------------------------------------------------------------------
# Connection helper
# ---------------------------------------------------------------------------
def get_connection():
    """Return a new SQLite connection with foreign-key enforcement enabled."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row          # allow dict-like access on rows
    return conn


# ---------------------------------------------------------------------------
# Table creation
# ---------------------------------------------------------------------------
def get_db_state_hash() -> str:
    """
    Returns a unified hash string representing the total rows and sums
    of the database across components. Useful for polling auto-updates.
    """
    conn = get_connection()
    try:
        c = conn.execute('''
            SELECT 
                (SELECT COUNT(*) FROM Patients) +
                (SELECT COUNT(*) FROM Doctors) +
                (SELECT COUNT(*) FROM Inventory) +
                (SELECT COUNT(*) FROM Billing) as cnt,
                IFNULL((SELECT SUM(Age) FROM Patients), 0) +
                IFNULL((SELECT SUM(Quantity) FROM Inventory), 0) +
                IFNULL((SELECT SUM(Amount) FROM Billing), 0) +
                IFNULL((SELECT SUM(LENGTH(Status)) FROM Billing), 0) +
                IFNULL((SELECT SUM(LENGTH(FullName)) FROM Patients), 0) as stats
        ''')
        row = c.fetchone()
        if row:
            return f"{row['cnt']}-{row['stats']}"
        return "0-0"
    finally:
        conn.close()

def _create_tables(conn: sqlite3.Connection):
    """Create every table defined in the PRD schema (idempotent)."""

    conn.execute("""
        CREATE TABLE IF NOT EXISTS Admin_Users (
            ID            INTEGER PRIMARY KEY AUTOINCREMENT,
            Username      TEXT    NOT NULL UNIQUE,
            PasswordHash  TEXT    NOT NULL,
            Role          TEXT    NOT NULL DEFAULT 'admin'
        );
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS Patients (
            ID              INTEGER PRIMARY KEY AUTOINCREMENT,
            FullName        TEXT    NOT NULL,
            Age             INTEGER,
            PhoneNumber     TEXT,
            MedicalHistory  TEXT,
            Allergies       TEXT,
            NextAppointment TEXT,
            DOB             TEXT
        );
    """)
    # Safely inject DOB column on legacy databases
    try:
        conn.execute("ALTER TABLE Patients ADD COLUMN DOB TEXT;")
    except sqlite3.OperationalError:
        pass  # Column already exists


    conn.execute("""
        CREATE TABLE IF NOT EXISTS Doctors (
            ID          INTEGER PRIMARY KEY AUTOINCREMENT,
            Name        TEXT    NOT NULL,
            Specialty   TEXT,
            PhoneNumber TEXT
        );
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS Inventory (
            ID          INTEGER PRIMARY KEY AUTOINCREMENT,
            ItemName    TEXT    NOT NULL,
            Quantity    INTEGER NOT NULL DEFAULT 0,
            ExpiryDate  TEXT,
            Price       REAL    NOT NULL DEFAULT 0.0
        );
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS Billing (
            ID          INTEGER PRIMARY KEY AUTOINCREMENT,
            Patient_ID  INTEGER NOT NULL,
            Amount      REAL    NOT NULL,
            Date        TEXT    NOT NULL,
            Status      TEXT    NOT NULL DEFAULT 'Pending'
                        CHECK (Status IN ('Paid', 'Pending')),
            Item_ID     INTEGER,
            Item_Qty    INTEGER DEFAULT 0,
            FOREIGN KEY (Patient_ID) REFERENCES Patients(ID),
            FOREIGN KEY (Item_ID) REFERENCES Inventory(ID)
        );
    """)

    # Backwards compatibility injection for previously created Billing tables
    try:
        conn.execute("ALTER TABLE Billing ADD COLUMN Item_ID INTEGER REFERENCES Inventory(ID);")
        conn.execute("ALTER TABLE Billing ADD COLUMN Item_Qty INTEGER DEFAULT 0;")
        conn.commit()
    except sqlite3.OperationalError:
        pass

    try:
        conn.execute("ALTER TABLE Inventory ADD COLUMN Price REAL NOT NULL DEFAULT 0.0;")
        conn.commit()
    except sqlite3.OperationalError:
        pass


def get_next_available_id(conn, table_name: str) -> int:
    """Finds the lowest missing positive integer ID in a specified table, returning the next logically skipped ID natively bridging AUTOINCREMENT boundaries."""
    rows = conn.execute(f"SELECT ID FROM {table_name} ORDER BY ID ASC").fetchall()
    ids = {r['ID'] for r in rows}
    
    next_id = 1
    while next_id in ids:
        next_id += 1
    return next_id


    # -----------------------------------------------------------------------
    # Indices for faster lookup/search operations on big data scales
    # -----------------------------------------------------------------------
    conn.execute("CREATE INDEX IF NOT EXISTS idx_patients_name ON Patients(FullName);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_doctors_name ON Doctors(Name);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_inventory_item ON Inventory(ItemName);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_billing_patient ON Billing(Patient_ID);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON Admin_Users(Username);")

    conn.commit()


# ---------------------------------------------------------------------------
# Default admin seeding
# ---------------------------------------------------------------------------
def _seed_default_admin(conn: sqlite3.Connection):
    """Insert a default admin user if the Admin_Users table is empty.

    Default credentials
    -------------------
    Username : admin
    Password : admin123   (stored as a bcrypt hash — NEVER plain text)
    """
    cursor = conn.execute("SELECT COUNT(*) FROM Admin_Users;")
    count = cursor.fetchone()[0]

    if count == 0:
        default_username = "admin"
        default_password = "admin123"

        # Hash the password with bcrypt (auto-generates a salt)
        hashed = bcrypt.hashpw(
            default_password.encode("utf-8"),
            bcrypt.gensalt(),
        )

        conn.execute(
            "INSERT INTO Admin_Users (Username, PasswordHash, Role) VALUES (?, ?, ?);",
            (default_username, hashed.decode("utf-8"), "admin"),
        )
        conn.commit()
        print("[database] Default admin user created  (username: admin)")
    else:
        print("[database] Admin user(s) already exist — skipping seed.")


# ---------------------------------------------------------------------------
# Public initialiser
# ---------------------------------------------------------------------------
def init_db():
    """Initialise the database: create tables and seed the default admin.

    Safe to call on every application start — all operations are idempotent.
    """
    conn = get_connection()
    try:
        _create_tables(conn)
        _seed_default_admin(conn)
        print(f"[database] Database ready  ({DB_NAME})")
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Quick smoke-test when run directly
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    init_db()
