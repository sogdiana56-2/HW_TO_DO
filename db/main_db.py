import sqlite3
import os

DB_PATH = "db/todo.db"

# Создание папки db, если её нет
if not os.path.exists("db"):
    os.makedirs("db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_text TEXT,
            completed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, task_text, completed FROM tasks")
    tasks = cur.fetchall()
    conn.close()
    return tasks

def add_task(task_text):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (task_text, completed) VALUES (?, 0)", (task_text,))
    task_id = cur.lastrowid
    conn.commit()
    conn.close()
    return task_id

def update_task(task_id, new_task):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET task_text = ? WHERE id = ?", (new_task, task_id))
    conn.commit()
    conn.close()

def update_task_completed(task_id, completed):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET completed = ? WHERE id = ?", (1 if completed else 0, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def delete_completed_tasks():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE completed = 1")
    conn.commit()
    conn.close()

