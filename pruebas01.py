# import os
from pathlib import Path
import customtkinter as ctk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

import db

# ===================== CONSTANTES DE LAYOUT =====================
APP_TITLE = "Recetario Digital"
SIZE = (1920, 1080)  # Tamaño único fijo de la ventana

# Panel izquierdo (menú CRUD)
LEFT_W = 260  # ancho fijo del panel izquierdo

# Gaps (márgenes internos en el área derecha)
GAP = 8

# Panel derecho (cuadrantes y tabla)
# Medidas en píxeles. COL_DER se calcula automáticamente.
COL_IZQ = 620        # ancho de columna izquierda en el área derecha
FILA_SUP = 420       # alto de fila superior
FILA_INF = 420       # alto de fila inferior
TABLA_MIN_ALTO = 180 # alto mínimo para el contenedor de tabla (por si resta poco espacio)
# ================================================================

CATEGORIAS = [
    "Desayuno", "Comida", "Cena", "Snack", "Postre", "Bebida"
]


class RecetarioApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)

        # Decoraciones estándar y pantalla completa
        self.overrideredirect(False)
        self.state("zoomed")

        # Tamaño fijo y posicionado en 0,0
        self.minsize(*SIZE)
        self.maxsize(*SIZE)
        self.geometry(f"{SIZE[0]}x{SIZE[1]}+0+0")
        self.resizable(False, False)

        # Reatacha la barra de título si alguna vez usaste overrideredirect(True)
        self._restore_decorations()

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # DB
        db.init_db()

        # Estado
        self.selected_recipe_id = None
        self.current_photo_path = None

        # Construcción UI (ya NO usamos grid en raíz; todo con place)
        self._build_left_panel()
        self._build_right_panel()

    # ---------------- Layout Izquierdo (place) -----------------
    def _build_left_panel(self):
        self.left = ctk.CTkFrame(self, width=LEFT_W, height=SIZE[1])
        self.left.place(x=0, y=0)  # anchado a la izquierda, alto total

        title = ctk.CTkLabel(self.left, text=APP_TITLE, font=("Arial", 18, "bold"))
        title.pack(padx=12, pady=(16, 8))

        # Acciones CRUD
        ctk.CTkLabel(self.left, text="Acciones", anchor="w", font=("Arial", 14, "bold")).pack(fill="x", padx=12)
        self.btn_nuevo = ctk.CTkButton(self.left, text="Agregar receta", command=self.on_add)
        self.btn_nuevo.pack(fill="x", padx=12, pady=6)

        self.btn_mod = ctk.CTkButton(self.left, text="Modificar receta", command=self.on_update)
        self.btn_mod.pack(fill="x", padx=12, pady=6)

        self.btn_del = ctk.CTkButton(self.left, text="Eliminar receta", fg_color="#b3261e", hover_color="#8c1b15",
                                     command=self.on_delete)
        self.btn_del.pack(fill="x", padx=12, pady=6)

        # Buscar / Mostrar todas
        ctk.CTkLabel(self.left, text="Buscar", anchor="w", font=("Arial", 14, "bold")).pack(fill="x", padx=12, pady=(16, 0))
        self.ent_buscar = ctk.CTkEntry(self.left, placeholder_text="Nombre / categoría / ingrediente")
        self.ent_buscar.pack(fill="x", padx=12, pady=(6, 6))
        self.btn_buscar = ctk.CTkButton(self.left, text="Buscar receta", command=self.on_search)
        self.btn_buscar.pack(fill="x", padx=12, pady=6)

        self.btn_all = ctk.CTkButton(self.left, text="Mostrar todas", command=self.on_show_all)
        self.btn_all.pack(fill="x", padx=12, pady=(6, 16))

        # Barra de estado
        self.status = ctk.CTkLabel(self.left, text="Listo", anchor="w")
        self.status.pack(fill="x", padx=12, pady=(8, 12))

    # ---------------- Layout Derecho (place) -----------------
    def _build_right_panel(self):
        # Área derecha total
        RW = SIZE[0] - LEFT_W           # ancho del área derecha
        RH = SIZE[1]                     # alto total
        self.right = ctk.CTkFrame(self, width=RW, height=RH)
        self.right.place(x=LEFT_W, y=0)

        # Cálculo de columnas/filas internas
        col_der = RW - COL_IZQ - (GAP * 3)  # ancho derecha respetando gaps
        fila_tab = RH - (FILA_SUP + FILA_INF + GAP * 4)
        fila_tab = max(fila_tab, TABLA_MIN_ALTO)  # asegura mínimo para tabla

        # Coordenadas base
        x1 = GAP
        x2 = x1 + COL_IZQ + GAP
        y1 = GAP
        y2 = y1 + FILA_SUP + GAP
        y3 = y2 + FILA_INF + GAP  # inicio de la tabla

        # ---- Q1: Datos básicos (arriba izquierda) ----
        self.q1 = ctk.CTkFrame(self.right, width=COL_IZQ, height=FILA_SUP)
        self.q1.place(x=x1, y=y1)
        self._build_q1()

        # ---- Q2: Ingredientes (arriba derecha) ----
        self.q2 = ctk.CTkFrame(self.right, width=col_der, height=FILA_SUP)
        self.q2.place(x=x2, y=y1)
        self._build_q2()

        # ---- Q3: Foto (abajo izquierda) ----
        self.q3 = ctk.CTkFrame(self.right, width=COL_IZQ, height=FILA_INF)
        self.q3.place(x=x1, y=y2)
        self._build_q3()

        # ---- Q4: Instrucciones (abajo derecha) ----
        self.q4 = ctk.CTkFrame(self.right, width=col_der, height=FILA_INF)
        self.q4.place(x=x2, y=y2)
        self._build_q4()

        # ---- Tabla de resultados (abajo a lo ancho) ----
        container_w = RW - (GAP * 2)
        container_h = fila_tab
        container_x = GAP
        container_y = y3

        self.results_container = ctk.CTkFrame(self.right, width=container_w, height=container_h)
        self.results_container.place(x=container_x, y=container_y)

        # Construir tabla
        cols = ("id", "nombre", "categoria", "tiempo")
        self.tree = ttk.Treeview(self.results_container, columns=cols, show="headings", height=6)
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("categoria", text="Categoría")
        self.tree.heading("tiempo", text="Tiempo")
        self.tree.column("id", width=60, anchor="center")
        self.tree.column("nombre", width=300)
        self.tree.column("categoria", width=150)
        self.tree.column("tiempo", width=120, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=6, pady=6)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    # ----------- Q1: Datos básicos -----------
    def _build_q1(self):
        pad = {'padx': 8, 'pady': 6}
        title = ctk.CTkLabel(self.q1, text="Datos básicos", font=("Arial", 15, "bold"))
        title.grid(row=0, column=0, columnspan=2, sticky="w", **pad)

        ctk.CTkLabel(self.q1, text="Nombre:").grid(row=1, column=0, sticky="e", **pad)
        self.ent_nombre = ctk.CTkEntry(self.q1)
        self.ent_nombre.grid(row=1, column=1, sticky="ew", **pad)

        ctk.CTkLabel(self.q1, text="Categoría:").grid(row=2, column=0, sticky="e", **pad)
        self.cbo_categoria = ctk.CTkOptionMenu(self.q1, values=CATEGORIAS)
        self.cbo_categoria.set(CATEGORIAS[0])
        self.cbo_categoria.grid(row=2, column=1, sticky="ew", **pad)

        ctk.CTkLabel(self.q1, text="Tiempo (ej. 30 min):").grid(row=3, column=0, sticky="e", **pad)
        self.ent_tiempo = ctk.CTkEntry(self.q1)
        self.ent_tiempo.grid(row=3, column=1, sticky="ew", **pad)

        # Para que la columna de entradas se expanda dentro del frame (internamente)
        self.q1.grid_columnconfigure(0, weight=0)
        self.q1.grid_columnconfigure(1, weight=1)

    # ----------- Q2: Ingredientes -----------
    def _build_q2(self):
        pad = {'padx': 8, 'pady': 6}
        title = ctk.CTkLabel(self.q2, text="Ingredientes", font=("Arial", 15, "bold"))
        title.pack(anchor="w", **pad)

        self.txt_ingredientes = ctk.CTkTextbox(self.q2, wrap="word")
        self.txt_ingredientes.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    # ----------- Q3: Foto -----------
    def _build_q3(self):
        pad = {'padx': 8, 'pady': 6}
        title = ctk.CTkLabel(self.q3, text="Foto de la receta", font=("Arial", 15, "bold"))
        title.pack(anchor="w", **pad)

        self.photo_label = ctk.CTkLabel(self.q3, text="(Sin imagen)")
        self.photo_label.pack(fill="both", expand=True, padx=8, pady=8)

        btns = ctk.CTkFrame(self.q3)
        btns.pack(fill="x", padx=8, pady=(0, 8))
        ctk.CTkButton(btns, text="Cargar foto", command=self.load_photo).pack(side="left", padx=4)
        ctk.CTkButton(btns, text="Quitar foto", command=self.clear_photo).pack(side="left", padx=4)

    # ----------- Q4: Instrucciones -----------
    def _build_q4(self):
        pad = {'padx': 8, 'pady': 6}
        title = ctk.CTkLabel(self.q4, text="Instrucciones", font=("Arial", 15, "bold"))
        title.pack(anchor="w", **pad)

        self.txt_instrucciones = ctk.CTkTextbox(self.q4, wrap="word")
        self.txt_instrucciones.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    # ----------------- Utilidades UI -----------------
    def _restore_decorations(self):
        """Reaplica las decoraciones (título/botones) tras cualquier overrideredirect previo."""
        try:
            self.update_idletasks()
            self.withdraw()
            self.overrideredirect(False)
            self.after(10, self.deiconify)
        except Exception:
            pass

    def clear_form(self):
        self.selected_recipe_id = None
        self.ent_nombre.delete(0, "end")
        self.cbo_categoria.set(CATEGORIAS[0])
        self.ent_tiempo.delete(0, "end")
        self.txt_ingredientes.delete("1.0", "end")
        self.txt_instrucciones.delete("1.0", "end")
        self.clear_photo()
        self.status.configure(text="Listo")

    def load_photo(self):
        path = filedialog.askopenfilename(
            title="Selecciona una imagen",
            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.webp;*.bmp")],
        )
        if not path:
            return
        self.current_photo_path = path
        self._render_photo(path)

    def _render_photo(self, path):
        try:
            # Asegura que q3 ya tenga dimensiones reales antes de escalar
            self.q3.update_idletasks()
            im = Image.open(path)
            max_w = int(self.q3.winfo_width() * 0.9) or 400
            max_h = int(self.q3.winfo_height() * 0.7) or 250
            im.thumbnail((max_w, max_h))
            self._photo_imgtk = ImageTk.PhotoImage(im)
            self.photo_label.configure(image=self._photo_imgtk, text="")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen:\n{e}")

    def clear_photo(self):
        self.current_photo_path = None
        self.photo_label.configure(image=None, text="(Sin imagen)")

    # ----------------- Tabla de resultados -----------------
    def populate_tree(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for r in rows:
            rid, nombre, categoria, tiempo, *_ = r
            self.tree.insert("", "end", values=(rid, nombre, categoria, tiempo))

    def on_tree_select(self, event=None):
        sel = self.tree.selection()
        if not sel:
            return
        values = self.tree.item(sel[0], "values")
        recipe_id = int(values[0])
        data = db.get_recipe_by_id(recipe_id)
        if not data:
            return
        (rid, nombre, categoria, tiempo, ingredientes, instrucciones, foto) = data
        self.selected_recipe_id = rid
        self.ent_nombre.delete(0, "end")
        self.ent_nombre.insert(0, nombre)
        self.cbo_categoria.set(categoria if categoria else CATEGORIAS[0])
        self.ent_tiempo.delete(0, "end")
        self.ent_tiempo.insert(0, tiempo or "")
        self.txt_ingredientes.delete("1.0", "end")
        self.txt_ingredientes.insert("1.0", ingredientes or "")
        self.txt_instrucciones.delete("1.0", "end")
        self.txt_instrucciones.insert("1.0", instrucciones or "")
        self.current_photo_path = foto
        if foto and Path(foto).exists():
            self._render_photo(foto)
        else:
            self.clear_photo()
        self.status.configure(text=f"Seleccionado ID {rid}")

    # ----------------- Acciones CRUD -----------------
    def on_add(self):
        nombre = self.ent_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Validación", "El nombre es obligatorio")
            return
        categoria = self.cbo_categoria.get()
        tiempo = self.ent_tiempo.get().strip()
        ingredientes = self.txt_ingredientes.get("1.0", "end").strip()
        instrucciones = self.txt_instrucciones.get("1.0", "end").strip()
        foto = self.current_photo_path
        rid = db.add_recipe(nombre, categoria, tiempo, ingredientes, instrucciones, foto)
        self.status.configure(text=f"Receta agregada (ID {rid})")
        self.on_show_all()

    def on_update(self):
        if not self.selected_recipe_id:
            messagebox.showinfo("Modificar", "Selecciona una receta en la tabla")
            return
        nombre = self.ent_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Validación", "El nombre es obligatorio")
            return
        categoria = self.cbo_categoria.get()
        tiempo = self.ent_tiempo.get().strip()
        ingredientes = self.txt_ingredientes.get("1.0", "end").strip()
        instrucciones = self.txt_instrucciones.get("1.0", "end").strip()
        foto = self.current_photo_path
        db.update_recipe(self.selected_recipe_id, nombre, categoria, tiempo, ingredientes, instrucciones, foto)
        self.status.configure(text=f"Receta modificada (ID {self.selected_recipe_id})")
        self.on_show_all()

    def on_delete(self):
        if not self.selected_recipe_id:
            messagebox.showinfo("Eliminar", "Selecciona una receta en la tabla")
            return
        if messagebox.askyesno("Confirmar", f"¿Eliminar receta ID {self.selected_recipe_id}?"):
            db.delete_recipe(self.selected_recipe_id)
            self.clear_form()
            self.on_show_all()
            self.status.configure(text="Receta eliminada")

    def on_search(self):
        q = self.ent_buscar.get().strip()
        if not q:
            self.status.configure(text="Ingresa un texto para buscar")
            return
        rows = db.search_recipes(q)
        self.populate_tree(rows)
        self.status.configure(text=f"Coincidencias: {len(rows)}")

    def on_show_all(self):
        rows = db.get_all_recipes()
        self.populate_tree(rows)
        self.status.configure(text=f"Total: {len(rows)} recetas")


if __name__ == "__main__":
    app = RecetarioApp()
    app.mainloop()
