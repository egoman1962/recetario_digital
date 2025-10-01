import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import filedialog
from tkinter import ttk
from PIL import Image
from pathlib import Path
import shutil

import db # Asegúrate de tener db.py en la misma carpeta

APP_TITLE = "Recetario Digital"
ASSETS_DIR = Path(__file__).with_name("fotos")
ASSETS_DIR.mkdir(exist_ok=True)




class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color='gray6')

        db.init_db()  # inicializa la BD
        self.selected_id = None
        self._img_path = None

        self.title(APP_TITLE)

        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('blue')

        # Abrir directamente maximizada al 100%
        self.state("zoomed")

        # Permitir botones del sistema
        self.resizable(True, True)

        # ---- Estado ----
        self.selected_id = None
        self._img_path = None  # ruta en ./fotos guardada en BD

        # ---- DB ----
        db.init_db()


        # Frame izquierdo
        self.frame_izquierdo = ctk.CTkFrame(self, fg_color='gray12', width=360, height=984)
        self.frame_izquierdo.place(x=12, y=12)
        self._build_left_actions()

        # Frame derecho
        self.frame_derecho = ctk.CTkFrame(self, fg_color='gray12', width=1518, height=984)
        self.frame_derecho.place(x=388, y=12)

        self.frame_foto = ctk.CTkFrame(self.frame_derecho , fg_color='gray6', width=456, height=456)
        self.frame_foto.place(x=24, y=24)
        self.frame_foto.pack_propagate(False)
        self.frame_foto.configure(border_width=6, border_color='#1F6AA5')
        self._build_frame_foto()

        self.frame_datos = ctk.CTkFrame(self.frame_derecho, fg_color='gray6', width=456, height=456)
        self.frame_datos.place(x=504, y=24)
        self.frame_datos.pack_propagate(False)
        self.frame_datos.configure(border_width=6, border_color='#1F6AA5')
        self._build_frame_datos()

        self.frame_ingredientes = ctk.CTkFrame(self.frame_derecho, fg_color='gray6', width=510, height=456)
        self.frame_ingredientes.place(x=984, y=24)
        self.frame_ingredientes.pack_propagate(False)
        self._build_ingredientes()

        self.frame_preparacion = ctk.CTkFrame(self.frame_derecho, fg_color='gray6', width=510, height=456)
        self.frame_preparacion.place(x=984, y=504)
        self.frame_preparacion.pack_propagate(False)
        self._build_preparacion()

        self.frame_tabla = ctk.CTkFrame(self.frame_derecho, fg_color='gray6', width=936, height=456)
        self.frame_tabla.place(x=24, y=504)
        self.frame_tabla.pack_propagate(False)
        self._build_tabla()

    # Refrescar listado al inicio
        self._refresh_table()

    def _build_left_actions(self):
        # Título
        ctk.CTkLabel(
            self.frame_izquierdo,
            text="ACCIONES",
            text_color='green',
            font=("Arial", 24, "bold")
        ).pack(anchor="w", padx=16, pady=(16, 8))

        # Contenedor de botones
        actions = ctk.CTkFrame(self.frame_izquierdo, fg_color="transparent")
        actions.pack(fill="x", padx=16)

        # Botones CRUD (a lo ancho, alto uniforme)
        ctk.CTkButton(actions, text="Nuevo", height=48,
                      command=self._on_new).pack(fill="x", pady=6)
        ctk.CTkButton(actions, text="Guardar", height=48,
                      command=self._on_save).pack(fill="x", pady=6)
        ctk.CTkButton(actions, text="Actualizar", height=48,
                      command=self._on_update).pack(fill="x", pady=6)
        ctk.CTkButton(actions, text="Borrar", height=48,
                      fg_color="#a33", hover_color="#c55",
                      command=self._on_delete).pack(fill="x", pady=6)

    # PANEL DE FOTO #######################################################################################

    def _build_frame_foto(self):
        pad = {'padx': 45, 'pady': 6}

        # --- Título ---
        title = ctk.CTkLabel(
            self.frame_foto,
            text="FOTOGRAFÍA",
            text_color='green',
            font=("Arial", 24, "bold"))
        title.pack(anchor="w", **pad)

        # --- Recuadro para la imagen ---
        self.lbl_foto = ctk.CTkLabel(
            self.frame_foto,
            text="Sin foto",
            width=330,  # ajustado al tamaño del frame
            height=330,
            fg_color='gray6',
            text_color='BLUE',
            corner_radius=12,
            anchor="center"
        )
        self.lbl_foto.pack(padx=16, pady=(0, 12))

        # --- Frame inferior para los botones ---
        btn_frame = ctk.CTkFrame(self.frame_foto, fg_color="transparent")
        btn_frame.pack(side="bottom", pady=10)

        # Botón para cargar
        self.btn_cargar = ctk.CTkButton(self.frame_foto, text="Cargar foto", font=("Arial", 18, "bold"),
                                        width=150, command=self._cargar_foto, height=45)
        self.btn_cargar.place(x=40, y=390)

        # Botón para quitar
        self.btn_quitar = ctk.CTkButton(self.frame_foto, text="Quitar foto", font=("Arial", 18, "bold"),
                                        width=150, command=self._quitar_foto, height=45)
        self.btn_quitar.place(x=250, y=390)

    def _render_photo(self, path: str | None):
        try:
            if path and Path(path).exists():
                img = Image.open(path)
                img = img.resize((318, 318), Image.LANCZOS)
                foto = ctk.CTkImage(light_image=img, dark_image=img, size=(318, 318))
                self.lbl_foto.configure(image=foto, text="")
                self.lbl_foto.image = foto
            else:
                self.lbl_foto.configure(image=None, text="Sin foto")
                self.lbl_foto.image = None
        except Exception as e:
            CTkMessagebox(title="Error", message=f"No se pudo renderizar la imagen:\n{e}", icon="cancel")

    def _cargar_foto(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar fotografía",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        if file_path:
            try:
                # Copiar a ./fotos para tener ruta estable
                src = Path(file_path)
                dst = ASSETS_DIR / src.name
                if src.resolve() != dst.resolve():
                    shutil.copyfile(src, dst)
                self._img_path = str(dst)
                self._render_photo(self._img_path)
                CTkMessagebox(title="Fotografía", message="La foto se cargó correctamente.", icon="check")
            except Exception as e:
                CTkMessagebox(title="Error", message=f"No se pudo cargar la imagen:\n{e}", icon="cancel")

    def _quitar_foto(self):
        self._img_path = None
        self._render_photo(None)
        CTkMessagebox(title="Fotografía", message="Se quitó la foto correctamente.", icon="check")

    # PANEL DE DATOS #######################################################################################

    def _build_frame_datos(self):
        pad = {'padx': 45, 'pady': 6}
        title = ctk.CTkLabel(self.frame_datos, text="RECETA",
                             text_color='green', font=("Arial", 24, "bold"))
        title.pack(anchor="w", **pad)
        # self.txt_datos = ctk.CTkTextbox(self.frame_datos, wrap="word")
        # self.txt_datos.pack(fill="both", expand=True, padx=6, pady=(0, 6))

        # Nombre
        lbl_nombre = ctk.CTkLabel(self.frame_datos, text="NOMBRE:",
                                  font=("Arial", 21, "bold"), fg_color='gray6')
        lbl_nombre.place(x=90, y=72)
        self.entry_nombre = ctk.CTkEntry(self.frame_datos, width=300,
                                         font=("Arial", 18, "bold"), fg_color='#1F6AA5', border_color='#144870')
        self.entry_nombre.place(x=54, y=120)

        # Categoría
        lbl_categoria = ctk.CTkLabel(self.frame_datos,text="CATEGORIA:",
            font=("Arial", 21, "bold"),fg_color = 'gray6' )
        lbl_categoria.place(x=90, y=180)

        self.option_categoria = ctk.CTkOptionMenu(self.frame_datos,
            values=["Desayuno", "Comida", "Cena", "Snack", "Postre", "Bebida"], width=300,
            font=("Arial", 18, "bold"), button_color='#144870')
        self.option_categoria.place(x=54, y=228)
        # Valor inicial
        self.option_categoria.set("Desayuno")

        # Tiempo
        lbl_tiempo = ctk.CTkLabel(self.frame_datos, text="TIEMPO:",
                                  font=("Arial", 21, "bold"), fg_color='gray6')
        lbl_tiempo.place(x=90, y=288)
        self.entry_tiempo = ctk.CTkEntry(self.frame_datos, width=300, font=("Arial", 18, "bold"),
                                         fg_color='#1F6AA5', border_color='#144870')
        self.entry_tiempo.place(x=54, y=336)

# PANEL DE INGREDIENTES #######################################################################################

    def _build_ingredientes(self):
        pad = {'padx': 45, 'pady': 6}
        title = ctk.CTkLabel(
            self.frame_ingredientes,
            text="INGREDIENTES",
            text_color='green',
            font=("Arial", 24, "bold")
        )
        title.pack(anchor="w", **pad)

        self.txt_ingredientes = ctk.CTkTextbox(
            self.frame_ingredientes,
            wrap="word",
            fg_color='gray6',
            font=("Arial", 21, "bold"),
            height=15
        )
        self.txt_ingredientes.pack(fill="both", expand=True, padx=6, pady=(0, 6))

        # Insertar la primera viñeta al inicio
        self.txt_ingredientes.insert("1.0", "● ")

        # Vincular tecla Enter para agregar viñeta en nueva línea
        self.txt_ingredientes.bind("<Return>", self._add_bullet)

    def _add_bullet(self, event=None):
        self.txt_ingredientes.insert("insert", "\n●  ")
        return "break"  # evita que Tkinter agregue un salto extra

    # PANEL DE PREPARACION #######################################################################################

    def _build_preparacion(self):
        pad = {'padx': 45, 'pady': 6}
        title = ctk.CTkLabel(
            self.frame_preparacion,
            text="PREPARACIÓN",
            text_color='green',
            font=("Arial", 24, "bold")
        )
        title.pack(anchor="w", **pad)

        self.txt_preparacion = ctk.CTkTextbox(
            self.frame_preparacion,
            wrap="word",
            fg_color='gray6',
            font=("Arial", 21, "bold"),
            height=15
        )
        self.txt_preparacion.pack(fill="both", expand=True, padx=6, pady=(0, 6))

        # Iniciar con el paso 1
        self.step_number = 1
        self.txt_preparacion.insert("1.0", f"{self.step_number}. ")

        # Vincular tecla Enter para insertar el siguiente número
        self.txt_preparacion.bind("<Return>", self._add_step)

    def _add_step(self, event=None):
        self.step_number += 1
        self.txt_preparacion.insert("insert", f"\n{self.step_number}. ")
        return "break"  # evita salto extra

    # PANEL DE TABLA #######################################################################################

    def _build_tabla(self):

        pad = {'padx': 45, 'pady': 6}
        title = ctk.CTkLabel(self.frame_tabla,
                     text="TABLA",
                     text_color='green',
                     font=("Arial", 24, "bold"))
        title.pack(anchor="w", **pad)

        # Barra de búsqueda
        search_bar = ctk.CTkFrame(self.frame_tabla, fg_color="transparent")
        search_bar.pack(fill="x", padx=16)
        self.entry_search = ctk.CTkEntry(search_bar, placeholder_text="Buscar nombre, categoría o ingrediente…")
        self.entry_search.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(search_bar, text="Buscar", width=100, command=self._on_search).pack(side="left", padx=6)
        ctk.CTkButton(search_bar, text="Limpiar", width=100, command=self._on_search_clear).pack(side="left")

        # Tabla (ttk.Treeview)
        table_wrap = ctk.CTkFrame(self.frame_tabla, fg_color='gray10')
        table_wrap.pack(fill="both", expand=True, padx=16, pady=12)

        columns = ("id", "nombre", "categoria", "tiempo")
        self.tree = ttk.Treeview(table_wrap, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("categoria", text="Categoría")
        self.tree.heading("tiempo", text="Tiempo")
        self.tree.column("id", width=60, anchor="center")
        self.tree.column("nombre", width=260)
        self.tree.column("categoria", width=150, anchor="center")
        self.tree.column("tiempo", width=120, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)
        self.tree.bind("<<TreeviewSelect>>", self._on_select_row)

        self.tree.bind("<<TreeviewSelect>>", self._on_select_row)

    # --------------------------- Helpers ------------------------------- #
    def _collect_form(self):
        nombre = self.entry_nombre.get().strip()
        categoria = self.option_categoria.get().strip() if self.option_categoria.get() else None
        tiempo = self.entry_tiempo.get().strip() or None
        ingredientes = self.txt_ingredientes.get("1.0", "end").strip() or None
        instrucciones = self.txt_preparacion.get("1.0", "end").strip() or None
        foto = self._img_path
        return nombre, categoria, tiempo, ingredientes, instrucciones, foto

    def _fill_form(self, rec: dict):
        self.selected_id = rec["id"]
        # Datos
        self.entry_nombre.delete(0, "end");
        self.entry_nombre.insert(0, rec.get("nombre", ""))
        self.option_categoria.set(rec.get("categoria") or "Desayuno")
        self.entry_tiempo.delete(0, "end");
        self.entry_tiempo.insert(0, rec.get("tiempo", ""))
        # Textos
        self.txt_ingredientes.delete("1.0", "end")
        ing = rec.get("ingredientes") or ""
        self.txt_ingredientes.insert("1.0", ing if ing else "● ")
        self.txt_preparacion.delete("1.0", "end")
        inst = rec.get("instrucciones") or "1. "
        self.txt_preparacion.insert("1.0", inst)
        # Foto
        self._img_path = rec.get("foto")
        self._render_photo(self._img_path)
        # Reiniciar numerador según contenido
        try:
            last_num = 0
            for line in self.txt_preparacion.get("1.0", "end").splitlines():
                line = line.strip()
                if line and line[0].isdigit():
                    n = ''
                    for ch in line:
                        if ch.isdigit():
                            n += ch
                        else:
                            break
                    if n:
                        last_num = max(last_num, int(n))
            self.step_number = max(1, last_num)
        except Exception:
            self.step_number = 1

    def _clear_form(self):
        self.selected_id = None
        self.entry_nombre.delete(0, "end")
        self.option_categoria.set("Desayuno")
        self.entry_tiempo.delete(0, "end")
        self.txt_ingredientes.delete("1.0", "end");
        self.txt_ingredientes.insert("1.0", "● ")
        self.txt_preparacion.delete("1.0", "end");
        self.step_number = 1;
        self.txt_preparacion.insert("1.0", "1. ")
        self._quitar_foto()

    # --------------------------- Tabla/CRUD ---------------------------- #
    def _refresh_table(self, rows=None):
        # obtener data
        data = rows if rows is not None else db.get_all_recipes()
        # limpiar
        for i in getattr(self, 'tree', []).get_children():
            self.tree.delete(i)
        # llenar
        for r in data:
            # r puede ser dict (db robusta) o tupla (si cambiaste algo); soportamos ambos
            if isinstance(r, dict):
                self.tree.insert("", "end", values=(r["id"], r.get("nombre"), r.get("categoria"), r.get("tiempo")))
            else:
                self.tree.insert("", "end", values=(r[0], r[1], r[2], r[3]))

        """
            Rellena la Treeview con rayado tipo 'zebra'.
            Soporta filas como dict (db.py robusto) o como tuplas.
            """
        # Asegura tags de estilo (las puedes ajustar a tu gusto)
        # Nota: si ya los configuraste antes, no pasa nada por reconfigurarlos aquí.
        self.tree.tag_configure("even", background='gray50', foreground='black')
        self.tree.tag_configure("odd", background='gray75', foreground='black')

        # (Opcional) preservar selección actual por ID
        selected_id = None
        sel = self.tree.selection()
        if sel:
            try:
                selected_id = int(self.tree.item(sel[0])["values"][0])
            except Exception:
                selected_id = None

        # Obtener datos (si no se pasaron)
        data = rows if rows is not None else db.get_all_recipes()

        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insertar filas alternando tags
        for idx, r in enumerate(data):
            tag = "even" if idx % 2 == 0 else "odd"

            if isinstance(r, dict):
                rid = r.get("id")
                nombre = r.get("nombre")
                categoria = r.get("categoria")
                tiempo = r.get("tiempo")
            else:
                # (id, nombre, categoria, tiempo, ingredientes, instrucciones, foto)
                rid, nombre, categoria, tiempo = r[0], r[1], r[2], r[3]

            self.tree.insert("", "end", values=(rid, nombre, categoria, tiempo), tags=(tag,))

        # (Opcional) volver a seleccionar la fila anterior si sigue visible
        if selected_id is not None:
            for iid in self.tree.get_children():
                try:
                    if int(self.tree.item(iid)["values"][0]) == selected_id:
                        self.tree.selection_set(iid)
                        self.tree.see(iid)
                        break
                except Exception:
                    pass


    def _on_select_row(self, _event=None):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])
        rid = int(item["values"][0])
        rec = db.get_recipe_by_id(rid)
        # rec puede venir como dict (db.py robusto)
        if isinstance(rec, dict):
            self._fill_form(rec)
        else:
            keys = ["id", "nombre", "categoria", "tiempo", "ingredientes", "instrucciones", "foto"]
            self._fill_form(dict(zip(keys, rec)))

    def _on_new(self):
        self._clear_form()

    def _on_save(self):
        nombre, categoria, tiempo, ingredientes, instrucciones, foto = self._collect_form()

        if not nombre:
            CTkMessagebox(title="Validación", message="El nombre es obligatorio.", icon="warning")
            return
        rid = db.add_recipe(nombre, categoria, tiempo, ingredientes, instrucciones, foto)
        self.selected_id = rid
        self._refresh_table()
        CTkMessagebox(title="Éxito", message="Receta guardada.", icon="check")

    def _on_update(self):
        if not self.selected_id:
            CTkMessagebox(title="Actualizar", message="Selecciona una receta en la tabla.", icon="info")
            return
        nombre, categoria, tiempo, ingredientes, instrucciones, foto = self._collect_form()
        if not nombre:
            CTkMessagebox(title="Validación", message="El nombre es obligatorio.", icon="warning")
            return
        db.update_recipe(self.selected_id, nombre, categoria, tiempo, ingredientes, instrucciones, foto)
        self._refresh_table()
        CTkMessagebox(title="Éxito", message="Receta actualizada.", icon="check")

    def _on_delete(self):
        if not self.selected_id:
            CTkMessagebox(title="Borrar", message="Selecciona una receta en la tabla.", icon="info")
            return
        confirm = CTkMessagebox(title="Confirmar", message="¿Borrar la receta seleccionada?", icon="warning", option_1="Cancelar", option_2="Borrar")
        if confirm.get() == "Borrar":
            db.delete_recipe(self.selected_id)
            self._clear_form()
            self._refresh_table()
            CTkMessagebox(title="Éxito", message="Receta borrada.", icon="check")

    # --------------------------- Búsqueda ------------------------------ #
    def _on_search(self):
        text = self.entry_search.get().strip()
        if not text:
            self._refresh_table(db.get_all_recipes())
        else:
            rows = db.search_recipes(text)
            self._refresh_table(rows)

    def _on_search_clear(self):
        self.entry_search.delete(0, "end")
        self._refresh_table(db.get_all_recipes())


if __name__ == "__main__":
    app = App()
    app.mainloop()