import sqlite3

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_NAME = os.path.join(
    BASE_DIR,
    "llm_history.db"
)


def init_db():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS llm_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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

    conn.commit()
    conn.close()


def save_chat(prompt,response,model,temperature,top_p,top_k,max_tokens,input_tokens,output_tokens,elapsed_time,cost):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO llm_history(
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
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
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

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM llm_history
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def delete_chat(chat_id):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM llm_history
        WHERE id = ?
    """, (chat_id,))

    conn.commit()
    conn.close()

def update_chat(chat_id, prompt, response, model, temperature, top_p, top_k, max_tokens, input_tokens, output_tokens, elapsed_time, cost):
    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()

    cursor.execute("""
        UPDATE llm_history
        SET prompt = ?, response = ?, model = ?, temperature = ?, top_p = ?, top_k = ?, max_tokens = ?, input_tokens = ?, output_tokens = ?, elapsed_time = ?, cost = ?
        WHERE id = ? """,
        (prompt, response, model, temperature, top_p, top_k, max_tokens, input_tokens, output_tokens, elapsed_time, cost, chat_id))

    conn.commit()
    conn.close()
