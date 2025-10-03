import customtkinter as ctk
from tkinter import ttk

class TablaPanel(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master, fg_color='gray6')
        self.controller = controller
        self.pack(fill="both", expand=True)

        pad = {'padx': 45, 'pady': 6}
        ctk.CTkLabel(self, text="TABLA", text_color='green',
                     font=("Arial", 24, "bold")).pack(anchor="w", **pad)

        # Barra de búsqueda
        search_bar = ctk.CTkFrame(self, fg_color="transparent")
        search_bar.pack(fill="x", padx=16)
        self.entry_search = ctk.CTkEntry(search_bar, placeholder_text="Buscar nombre, categoría o ingrediente…")
        self.entry_search.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(search_bar, text="Buscar",  width=100,
                      command=self.controller._on_search).pack(side="left", padx=6)
        ctk.CTkButton(search_bar, text="Limpiar", width=100,
                      command=self.controller._on_search_clear).pack(side="left")

        # Tabla con estilo
        wrap = ctk.CTkFrame(self, fg_color='gray10')
        wrap.pack(fill="both", expand=True, padx=16, pady=12)

        style = ttk.Style(self)
        try:
            style.theme_use('clam')
        except Exception:
            pass
        style.configure("Treeview",
                        background="#1e1e1e", foreground="#e6e6e6", font=("Arial", 12, "bold"),
                        fieldbackground="#1e1e1e", rowheight=30, borderwidth=0)
        style.map("Treeview", background=[("selected", "gray40")])

        style.configure("Treeview.Heading",
                        background='green', foreground='white',
                        font=("Arial", 15, "bold"), relief="flat")
        # Hover y click en encabezados
        style.map(
            "Treeview.Heading",
            background=[("active", "gray75"), ("pressed", "#0E3D66")],
            foreground=[("active", "black")],
            relief=[("pressed", "sunken"), ("!pressed", "flat")]
        )

        # Sin columna ID visible
        self.tree = ttk.Treeview(wrap, columns=("nombre","categoria","tiempo"), show="headings")
        self.tree.heading("nombre", text="NOMBRE")
        self.tree.heading("categoria", text="CATEGORIA")
        self.tree.heading("tiempo", text="TIEMPO")
        self.tree.column("nombre", width=330, anchor="w")
        self.tree.column("categoria", width=150, anchor="center")
        self.tree.column("tiempo", width=120, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

        self.tree.bind("<<TreeviewSelect>>", self._on_select_row)

        # Tags zebra
        self.tree.tag_configure("even", background='gray50', foreground='black')
        self.tree.tag_configure("odd",  background='gray75', foreground='black')

        # API de interacción
    def get_search_text(self):
        return self.entry_search.get()

    def clear_search(self):
        self.entry_search.delete(0, "end")

    def populate(self, data):
        # limpiar
        for i in self.tree.get_children():
            self.tree.delete(i)
        # llenar con zebra (usando iid = id)
        for idx, r in enumerate(data):
            tag = "even" if idx % 2 == 0 else "odd"
            if isinstance(r, dict):
                rid, nombre, categoria, tiempo = r["id"], r.get("nombre"), r.get("categoria"), r.get("tiempo")
            else:
                rid, nombre, categoria, tiempo = r[0], r[1], r[2], r[3]
            # guardamos el id como iid, no en columnas visibles
            self.tree.insert("", "end", iid=str(rid),
                             values=(nombre, categoria, tiempo), tags=(tag,))

        # Selección
    def _on_select_row(self, _evt=None):
        sel = self.tree.selection()
        if not sel:
            return
        # id viene del iid del item
        rid = int(sel[0])
        self.controller._on_select_row(rid)
