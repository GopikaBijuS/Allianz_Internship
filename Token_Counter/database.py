import sqlite3


def init_db():

    conn = sqlite3.connect(
        "token_history.db"
    )

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            model TEXT,
            token_count INTEGER,
            cost_usd REAL
                )""")
    
    conn.commit()
    conn.close()

def save_analysis(text,model,token_count,cost_usd):

    conn = sqlite3.connect("token_history.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT *
        FROM history
        WHERE text = ?
        AND model = ?
        ORDER BY id DESC
        LIMIT 1
        """, (text, model))
    result = cursor.fetchall()
    if not result:
        cursor.execute("""
            INSERT INTO history(text,model,token_count,cost_usd)VALUES (?, ?, ?, ?)""", 
            (text,model,token_count,cost_usd))
    conn.commit()
    conn.close()

def get_history():

    conn = sqlite3.connect(
        "token_history.db"
    )
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM history"
    )

    rows = cursor.fetchall()
    conn.close()

    return rows