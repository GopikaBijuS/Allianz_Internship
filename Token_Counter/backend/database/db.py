import sqlite3
import os
import json

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DB_NAME = os.path.join(
    BASE_DIR,
    "llm_history.db"
)


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Existing chat history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS llm_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            prompt TEXT NOT NULL,
            response TEXT NOT NULL,
            model TEXT NOT NULL,
            temperature REAL,
            top_p REAL,
            top_k REAL,
            max_tokens INTEGER,
            input_tokens INTEGER,
            output_tokens INTEGER,
            elapsed_time REAL,
            cost TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Agent execution logs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agent_logs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            prompt TEXT,
            response TEXT,
            model TEXT,
            tools TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# ---------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------

def save_chat(
        session_id,
        prompt,
        response,
        model,
        temperature,
        top_p,
        top_k,
        max_tokens,
        input_tokens,
        output_tokens,
        elapsed_time,
        cost
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO llm_history(
            session_id,
            prompt,
            response,
            model,
            temperature,
            top_p,
            top_k,
            max_tokens,
            input_tokens,
            output_tokens,
            elapsed_time,
            cost
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        session_id,
        prompt,
        response,
        model,
        temperature,
        top_p,
        top_k,
        max_tokens,
        input_tokens,
        output_tokens,
        elapsed_time,
        cost
    ))

    conn.commit()
    conn.close()


def get_history():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM llm_history
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()
    return rows


def get_session_history(session_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM llm_history
        WHERE session_id = ?
        ORDER BY id ASC
    """, (session_id,))

    rows = cursor.fetchall()

    conn.close()
    return rows


def delete_chat(chat_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM llm_history
        WHERE id = ?
    """, (chat_id,))

    conn.commit()
    conn.close()


def delete_session(session_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM llm_history
        WHERE session_id = ?
    """, (session_id,))

    cursor.execute("""
        DELETE FROM agent_logs
        WHERE session_id = ?
    """, (session_id,))

    conn.commit()
    conn.close()


def update_chat(
        chat_id,
        session_id,
        prompt,
        response,
        model,
        temperature,
        top_p,
        top_k,
        max_tokens,
        input_tokens,
        output_tokens,
        elapsed_time,
        cost
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE llm_history
        SET
            session_id = ?,
            prompt = ?,
            response = ?,
            model = ?,
            temperature = ?,
            top_p = ?,
            top_k = ?,
            max_tokens = ?,
            input_tokens = ?,
            output_tokens = ?,
            elapsed_time = ?,
            cost = ?
        WHERE id = ?
    """,
    (
        session_id,
        prompt,
        response,
        model,
        temperature,
        top_p,
        top_k,
        max_tokens,
        input_tokens,
        output_tokens,
        elapsed_time,
        cost,
        chat_id
    ))

    conn.commit()
    conn.close()


# ---------------------------------------------------
# AGENT LOGS
# ---------------------------------------------------

def save_agent_log(
        session_id,
        prompt,
        response,
        model,
        tools
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO agent_logs(
            session_id,
            prompt,
            response,
            model,
            tools
        )
        VALUES (?, ?, ?, ?, ?)
    """,
    (
        session_id,
        prompt,
        response,
        model,
        json.dumps(tools)
    ))

    conn.commit()
    conn.close()


def get_agent_logs(session_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM agent_logs
        WHERE session_id = ?
        ORDER BY id DESC
    """, (session_id,))

    rows = cursor.fetchall()

    conn.close()
    return rows