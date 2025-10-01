import sqlite3
from pathlib import Path
from contextlib import contextmanager
from typing import Iterable, List, Optional, Tuple, Dict, Any

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

-- Índices sencillos para acelerar búsquedas por nombre y categoría
CREATE INDEX IF NOT EXISTS idx_recetas_nombre ON recetas(nombre);
CREATE INDEX IF NOT EXISTS idx_recetas_categoria ON recetas(categoria);
"""

PRAGMAS = (
    "PRAGMA foreign_keys = ON;",
    "PRAGMA journal_mode = WAL;",
    "PRAGMA synchronous = NORMAL;",
)


@contextmanager
def get_conn():
    """Context manager que abre una conexión con ajustes seguros y la cierra automáticamente.

    Nota: row_factory=sqlite3.Row permite acceder por nombre de columna.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.row_factory = sqlite3.Row
        for p in PRAGMAS:
            conn.execute(p)
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    with get_conn() as conn:
        conn.executescript(SCHEMA)


# --------------------------- Utilidades --------------------------- #

def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    return {k: row[k] for k in row.keys()}


# ----------------------------- CRUD ------------------------------- #

def add_recipe(nombre: str, categoria: Optional[str], tiempo: Optional[str],
               ingredientes: Optional[str], instrucciones: Optional[str],
               foto: Optional[str]) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO recetas (nombre, categoria, tiempo, ingredientes, instrucciones, foto)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (nombre, categoria, tiempo, ingredientes, instrucciones, foto),
        )
        return cur.lastrowid


def update_recipe(recipe_id: int, nombre: str, categoria: Optional[str], tiempo: Optional[str],
                  ingredientes: Optional[str], instrucciones: Optional[str],
                  foto: Optional[str]) -> None:
    with get_conn() as conn:
        conn.execute(
            """
            UPDATE recetas
               SET nombre = ?,
                   categoria = ?,
                   tiempo = ?,
                   ingredientes = ?,
                   instrucciones = ?,
                   foto = ?
             WHERE id = ?
            """,
            (nombre, categoria, tiempo, ingredientes, instrucciones, foto, recipe_id),
        )


def delete_recipe(recipe_id: int) -> None:
    with get_conn() as conn:
        conn.execute("DELETE FROM recetas WHERE id = ?", (recipe_id,))


# -------------------------- Lecturas ------------------------------ #

def get_all_recipes(as_dict: bool = True) -> List[Any]:
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT id, nombre, categoria, tiempo, ingredientes, instrucciones, foto\n             FROM recetas\n             ORDER BY id DESC"
        )
        rows = cur.fetchall()
        if as_dict:
            return [_row_to_dict(r) for r in rows]
        return rows


def search_recipes(query_text: str, as_dict: bool = True) -> List[Any]:
    like = f"%{query_text.strip()}%"
    with get_conn() as conn:
        cur = conn.execute(
            """
            SELECT id, nombre, categoria, tiempo, ingredientes, instrucciones, foto
              FROM recetas
             WHERE nombre LIKE ? ESCAPE '\\' COLLATE NOCASE
                OR categoria LIKE ? ESCAPE '\\' COLLATE NOCASE
                OR ingredientes LIKE ? ESCAPE '\\' COLLATE NOCASE
             ORDER BY id DESC
            """,
            (like, like, like),
        )
        rows = cur.fetchall()
        return [_row_to_dict(r) for r in rows] if as_dict else rows


def get_recipe_by_id(recipe_id: int, as_dict: bool = True) -> Optional[Any]:
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT id, nombre, categoria, tiempo, ingredientes, instrucciones, foto\n             FROM recetas WHERE id = ?",
            (recipe_id,),
        )
        row = cur.fetchone()
        return _row_to_dict(row) if (row and as_dict) else row


# ------------------------ Mantenimiento --------------------------- #

def integrity_check() -> bool:
    """Devuelve True si la BD pasa PRAGMA integrity_check."""
    with get_conn() as conn:
        res = conn.execute("PRAGMA integrity_check;").fetchone()
        return bool(res and res[0] == "ok")


def vacuum() -> None:
    with get_conn() as conn:
        conn.execute("VACUUM;")


if __name__ == "__main__":
    init_db()
    print(f"Base de datos lista en: {DB_PATH}")
