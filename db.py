import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("recetario.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS recetas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    categoria TEXT,
    tiempo TEXT,
    ingredientes TEXT,
    instrucciones TEXT,
    foto TEXT
);
"""


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute(SCHEMA)
        conn.commit()


def add_recipe(nombre, categoria, tiempo, ingredientes, instrucciones, foto):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO recetas (nombre, categoria, tiempo, ingredientes, instrucciones, foto)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (nombre, categoria, tiempo, ingredientes, instrucciones, foto),
        )
        conn.commit()
        return cur.lastrowid


def update_recipe(recipe_id, nombre, categoria, tiempo, ingredientes, instrucciones, foto):
    with get_conn() as conn:
        conn.execute(
            """
            UPDATE recetas
               SET nombre=?, categoria=?, tiempo=?, ingredientes=?, instrucciones=?, foto=?
             WHERE id=?
            """,
            (nombre, categoria, tiempo, ingredientes, instrucciones, foto, recipe_id),
        )
        conn.commit()


def delete_recipe(recipe_id):
    with get_conn() as conn:
        conn.execute("DELETE FROM recetas WHERE id=?", (recipe_id,))
        conn.commit()


def get_all_recipes():
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT id, nombre, categoria, tiempo, ingredientes, instrucciones, foto FROM recetas ORDER BY id DESC"
        )
        return cur.fetchall()


def search_recipes(query_text):
    like = f"%{query_text.strip()}%"
    with get_conn() as conn:
        cur = conn.execute(
            """
            SELECT id, nombre, categoria, tiempo, ingredientes, instrucciones, foto
              FROM recetas
             WHERE nombre LIKE ? OR categoria LIKE ? OR ingredientes LIKE ?
             ORDER BY id DESC
            """,
            (like, like, like),
        )
        return cur.fetchall()


def get_recipe_by_id(recipe_id):
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT id, nombre, categoria, tiempo, ingredientes, instrucciones, foto FROM recetas WHERE id=?",
            (recipe_id,),
        )
        return cur.fetchone()


if __name__ == "__main__":
    init_db()
    print(f"Base de datos lista en: {DB_PATH}")