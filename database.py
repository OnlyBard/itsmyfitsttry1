import sqlite3

DB_NAME = "tookam.db"

def connect():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tookakkar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        unique_no TEXT UNIQUE,
        name TEXT,
        type TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS karakkar (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        karakkar_id INTEGER,
        tookakkar_id INTEGER,
        order_no INTEGER
    )
    """)

    conn.commit()
    conn.close()

def get_next_tk_number():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT unique_no FROM tookakkar ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    conn.close()

    if row:
        num = int(row[0].split("-")[1]) + 1
        return f"TK-{num:03d}"
    return "TK-001"


def add_tookakkar(name, ttype):
    uid = get_next_tk_number()
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tookakkar (unique_no, name, type) VALUES (?, ?, ?)",
        (uid, name, ttype)
    )
    conn.commit()
    conn.close()


def fetch_tookakkar():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, unique_no, name, type FROM tookakkar")
    rows = cur.fetchall()
    conn.close()
    return rows

def save_karakkar(kid, name):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO karakkar (id, name)
    VALUES (?, ?)
    ON CONFLICT(id) DO UPDATE SET name=excluded.name
    """, (kid, name))
    conn.commit()
    conn.close()


def fetch_karakkar():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM karakkar ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return rows
def add_assignment(kar_id, tk_id, order_no):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO assignments (karakkar_id, tookakkar_id, order_no) VALUES (?, ?, ?)",
        (kar_id, tk_id, order_no)
    )
    conn.commit()
    conn.close()


def fetch_assignments():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
    SELECT a.id, a.order_no,
           t.unique_no, t.name,
           k.id, k.name
    FROM assignments a
    JOIN tookakkar t ON a.tookakkar_id = t.id
    JOIN karakkar k ON a.karakkar_id = k.id
    ORDER BY a.order_no
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

