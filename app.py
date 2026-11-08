import os

import psycopg
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


def connect_db():
    return psycopg.connect(
        host="db",
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        connect_timeout=5,
    )


with connect_db() as connection:
    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            title varchar(120) NOT NULL
        )
    """)


@app.get("/")
def index():
    with connect_db() as connection:
        tasks = connection.execute(
            "SELECT title FROM tasks ORDER BY id DESC"
        ).fetchall()
    return render_template("index.html", tasks=tasks)


@app.post("/tasks")
def add_task():
    title = request.form.get("title", "").strip()
    if not title or len(title) > 120:
        return "Judul tugas harus berisi 1 hingga 120 karakter.", 400

    with connect_db() as connection:
        connection.execute("INSERT INTO tasks (title) VALUES (%s)", (title,))
    return redirect(url_for("index"), code=303)
