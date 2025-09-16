# main.py
# Recetario Digital - Estructura base (solo UI)
# Requisitos: pip install customtkinter pillow

import os
from pathlib import Path
import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from PIL import Image

APP_TITLE = "Recetario Digital"
SIZE = (1920, 1080)          # Tamaño único fijo
LEFT_W = 360                 # Ancho del panel izquierdo

CATEGORIAS = [
    "Desayuno", "Comida", "Cena", "Snack", "Postre", "Bebida"
]

# -------- Utilidades de ventana (Windows: mejor nitidez) ----------
try:
    # Solo en Windows, mejora el escalado de fuentes/íconos
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

class RecetarioApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)

        # Tema e identidad visual básica
        ctk.set_appearance_mode("light")     # "dark" si prefieres
        ctk.set_default_color_theme("blue")

        # Geometría fija a 1920x1080, anclada a la pantalla (0,0)
        self.geometry(f"{SIZE[0]}x{SIZE[1]}+0+0")
        # Fijamos tamaño para que NO se pueda redimensionar (pero conserva minimizar/cerrar)
        self.minsize(*SIZE)
        self.maxsize(*SIZE)
        self.resizable(False, False)

        # Contenedor raíz
        self._build_root_layout()

        # Panel izquierdo (lista, búsqueda, botones)
        self._build_left_panel()

        # Panel derecho (4 cuadrantes)
        self._build_right_panel()

        # Estado inicial
        self._clear_fields()

    # ------------------- LAYOUT RAÍZ -------------------
    def _build_root_layout(self):
        # 2 columnas: izquierda fija, derecha expansible (aunque el tamaño esté fijo)
        self.grid_columnconfigure(0, minsize=LEFT_W, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    # ------------------- PANEL IZQUIERDO -------------------
    def _build_left_panel(self):
        self.left = ctk.CTkFrame(self, corner_radius=0)
        self.left.grid(row=0, column=0, sticky="nsew")

        # Estructura interna
        self.left.grid_rowconfigure(3, weight=1)
        self.left.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self.left, text="Recetas", font=ctk.CTkFont(size=22, weight="bold"))
        title.grid(row=0, column=0, padx=16, pady=(16, 8), sticky="w")

        # Búsqueda
        search_frame = ctk.CTkFrame(self.left)
        search_frame.grid(row=1, column=0, padx=12, pady=(0, 8), sticky="ew")
        search_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(search_frame, text="Buscar:").grid(row=0, column=0, padx=(12, 8), pady=12, sticky="w")
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, placeholder_text="Nombre o categoría…")
        search_entry.grid(row=0, column=1, padx=(0, 12), pady=12, sticky="ew")
        ctk.CTkButton(search_frame, text="Filtrar", command=self._on_filter).grid(row=0, column=2, padx=(0, 12), pady=12)

        # Lista (Treeview)
        tree_frame = ctk.CTkFrame(self.left)
        tree_frame.grid(row=2, column=0, padx=12, pady=8, sticky="nsew")

        columns = ("nombre", "categoria", "tiempo")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=25)
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("categoria", text="Categoría")
        self.tree.heading("tiempo", text="Tiempo")
        self.tree.column("nombre", width=160, anchor="w")
        self.tree.column("categoria", width=90, anchor="center")
        self.tree.column("tiempo", width=70, anchor="center")
        self.tree.bind("<<TreeviewSelect>>", self._on_select_recipe)
        self.tree.pack(fill="both", expand=True)

        # Botones CRUD (sin lógica de BD aún)
        btns = ctk.CTkFrame(self.left)
        btns.grid(row=4, column=0, padx=12, pady=12, sticky="ew")
        btns.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkButton(btns, text="Nuevo", command=self._on_new).grid(row=0, column=0, padx=6, pady=6, sticky="ew")
        ctk.CTkButton(btns, text="Guardar", command=self._on_save_dummy).grid(row=0, column=1, padx=6, pady=6, sticky="ew")
        ctk.CTkButton(btns, text="Borrar", fg_color="#d9534f", hover_color="#c9302c",
                      command=self._on_delete_dummy).grid(row=0, column=2, padx=6, pady=6, sticky="ew")
        ctk.CTkButton(btns, text="Cargar foto", command=self._on_load_photo).grid(row=0, column=3, padx=6, pady=6, sticky="ew")

        # Relleno de ejemplo (temporal)
        self._seed_demo_rows()

    # ------------------- PANEL DERECHO (4 CUADRANTES) -------------------
    def _build_right_panel(self):
        self.right = ctk.CTkFrame(self)
        self.right.grid(row=0, column=1, sticky="nsew", padx=(0, 0), pady=0)

        # Grid 2x2
        for r in range(2):
            self.right.grid_rowconfigure(r, weight=1, uniform="row")
        for c in range(2):
            self.right.grid_columnconfigure(c, weight=1, uniform="col")

        # TL: Datos básicos
        self.box_tl = self._labeled_frame(self.right, "Datos básicos")
        self.box_tl.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.box_tl.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.box_tl, text="Nombre:").grid(row=0, column=0, padx=12, pady=(12, 6), sticky="e")
        self.var_nombre = ctk.StringVar()
        ctk.CTkEntry(self.box_tl, textvariable=self.var_nombre, placeholder_text="Ej. Ensalada César").grid(
            row=0, column=1, padx=12, pady=(12, 6), sticky="ew"
        )

        ctk.CTkLabel(self.box_tl, text="Categoría:").grid(row=1, column=0, padx=12, pady=6, sticky="e")
        self.var_categoria = ctk.StringVar(value=CATEGORIAS[0])
        ctk.CTkOptionMenu(self.box_tl, variable=self.var_categoria, values=CATEGORIAS).grid(
            row=1, column=1, padx=12, pady=6, sticky="w"
        )

        ctk.CTkLabel(self.box_tl, text="Tiempo:").grid(row=2, column=0, padx=12, pady=6, sticky="e")
        self.var_tiempo = ctk.StringVar()
        ctk.CTkEntry(self.box_tl, textvariable=self.var_tiempo, placeholder_text='Ej. "30 min"').grid(
            row=2, column=1, padx=12, pady=6, sticky="ew"
        )

        # BL: Foto
        self.box_bl = self._labeled_frame(self.right, "Foto")
        self.box_bl.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.box_bl.grid_columnconfigure(0, weight=1)
        self.box_bl.grid_rowconfigure(0, weight=1)

        self.photo_label = ctk.CTkLabel(self.box_bl, text="Sin imagen")
        self.photo_label.grid(row=0, column=0, padx=12, pady=12, sticky="nsew")

        # TR: Ingredientes
        self.box_tr = self._labeled_frame(self.right, "Ingredientes")
        self.box_tr.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.box_tr.grid_rowconfigure(0, weight=1)
        self.box_tr.grid_columnconfigure(0, weight=1)

        self.txt_ingredientes = ctk.CTkTextbox(self.box_tr, wrap="word")
        self.txt_ingredientes.grid(row=0, column=0, padx=12, pady=12, sticky="nsew")

        # BR: Instrucciones
        self.box_br = self._labeled_frame(self.right, "Instrucciones")
        self.box_br.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.box_br.grid_rowconfigure(0, weight=1)
        self.box_br.grid_columnconfigure(0, weight=1)

        self.txt_instrucciones = ctk.CTkTextbox(self.box_br, wrap="word")
        self.txt_instrucciones.grid(row=0, column=0, padx=12, pady=12, sticky="nsew")

    # ------------------- HELPERS UI -------------------
    def _labeled_frame(self, parent, title: str):
        frame = ctk.CTkFrame(parent)
        header = ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=16, weight="bold"))
        header.grid(row=0, column=0, padx=12, pady=(12, 0), sticky="w")
        # Línea separadora
        sep = ctk.CTkFrame(frame, height=1, fg_color="#dddddd")
        sep.grid(row=1, column=0, padx=12, pady=(6, 6), sticky="ew")
        # Contenido debajo del separador
        content = ctk.CTkFrame(frame)
        content.grid(row=2, column=0, padx=0, pady=0, sticky="nsew")
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        # Para comodidad, retornamos el "frame" pero usaremos row>=2 como área de contenido
        # Para simplificar, haremos que los widgets hijos usen 'frame' directamente en otros métodos.
        return frame

    def _clear_fields(self):
        self.var_nombre.set("")
        self.var_categoria.set(CATEGORIAS[0])
        self.var_tiempo.set("")
        self.txt_ingredientes.delete("1.0", "end")
        self.txt_instrucciones.delete("1.0", "end")
        self._set_photo(None)

    def _set_photo(self, path: str | None):
        if not path or not Path(path).exists():
            self.photo_label.configure(text="Sin imagen", image=None)
            self.photo_label.image = None
            return
        try:
            img = Image.open(path)
            # Ajuste básico al espacio disponible
            target_w = int((SIZE[0] - LEFT_W) / 2) - 48
            target_h = int(SIZE[1] / 2) - 140
            img.thumbnail((target_w, target_h))
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            self.photo_label.configure(image=ctk_img, text="")
            self.photo_label.image = ctk_img
        except Exception as e:
            messagebox.showerror("Imagen", f"No se pudo cargar la imagen:\n{e}")

    # ------------------- EVENTOS & DUMMY LOGIC -------------------
    def _on_filter(self):
        query = self.search_var.get().strip().lower()
        # Demo: filtra solo las filas cargadas en memoria (aún sin BD)
        for i in self.tree.get_children():
            self.tree.delete(i)
        data = [
            ("Ensalada César", "Comida", "25 min"),
            ("Hotcakes", "Desayuno", "15 min"),
            ("Agua de limón", "Bebida", "5 min"),
        ]
        for nombre, categoria, tiempo in data:
            if (query in nombre.lower()) or (query in categoria.lower()):
                self.tree.insert("", "end", values=(nombre, categoria, tiempo))

    def _on_new(self):
        self._clear_fields()
        self.tree.selection_remove(self.tree.selection())

    def _on_save_dummy(self):
        # En la siguiente fase conectaremos a SQLite
        messagebox.showinfo("Guardar", "Guardado (demo). En la siguiente fase conectaremos SQLite.")

    def _on_delete_dummy(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Borrar", "Selecciona una receta en la lista.")
            return
        self.tree.delete(sel[0])
        self._clear_fields()

    def _on_load_photo(self):
        path = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.webp;*.bmp")]
        )
        if path:
            self._set_photo(path)

    def _on_select_recipe(self, _event=None):
        sel = self.tree.selection()
        if not sel:
            return
        nombre, categoria, tiempo = self.tree.item(sel[0], "values")
        self.var_nombre.set(nombre)
        self.var_categoria.set(categoria if categoria in CATEGORIAS else CATEGORIAS[0])
        self.var_tiempo.set(tiempo)
        # Demo: muestra ejemplo de texto
        self.txt_ingredientes.delete("1.0", "end")
        self.txt_instrucciones.delete("1.0", "end")
        self.txt_ingredientes.insert("1.0", "- Ingrediente 1\n- Ingrediente 2\n- Ingrediente 3")
        self.txt_instrucciones.insert("1.0", "1) Paso uno\n2) Paso dos\n3) Paso tres")
        self._set_photo(None)

    def _seed_demo_rows(self):
        self.tree.insert("", "end", values=("Ensalada César", "Comida", "25 min"))
        self.tree.insert("", "end", values=("Hotcakes", "Desayuno", "15 min"))
        self.tree.insert("", "end", values=("Agua de limón", "Bebida", "5 min"))

if __name__ == "__main__":
    app = RecetarioApp()
    app.mainloop()
