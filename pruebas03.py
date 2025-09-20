import customtkinter as ctk

# Nitidez en Windows (opcional)
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

APP_TITLE = "Recetario Digital"

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color='gray6')
        self.title(APP_TITLE)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Abrir directamente maximizada al 100%
        self.state("zoomed")

        # Permitir botones del sistema
        self.resizable(True, True)

        # Frame izquierdo
        self.frame_izquierdo = ctk.CTkFrame(self, fg_color='gray12', width=360, height=984)
        self.frame_izquierdo.place(x=12, y=12)

        # Frame derecho
        self.frame_derecho = ctk.CTkFrame(self, fg_color='gray12', width=1518, height=984)
        self.frame_derecho.place(x=388, y=12)

        self.frame_foto = ctk.CTkFrame(self.frame_derecho , fg_color='gray6', width=456, height=456)
        self.frame_foto.place(x=24, y=24)

        self.frame_datos = ctk.CTkFrame(self.frame_derecho, fg_color='gray6', width=456, height=456)
        self.frame_datos.place(x=504, y=24)
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


    def _build_ingredientes(self):
        pad = {'padx': 45, 'pady': 6}
        title = ctk.CTkLabel(self.frame_ingredientes, text="Ingredientes", font=("Arial", 24, "bold"))
        title.pack(anchor="w", **pad)
        self.txt_ingredientes = ctk.CTkTextbox(self.frame_ingredientes, wrap="word")
        self.txt_ingredientes.pack(fill="both", expand=True, padx=6, pady=(0, 6))

    def _build_preparacion(self):
        pad = {'padx': 45, 'pady': 6}
        title = ctk.CTkLabel(self.frame_preparacion, text="Preparación", font=("Arial", 24, "bold"))
        title.pack(anchor="w", **pad)
        self.txt_preparacion = ctk.CTkTextbox(self.frame_preparacion, wrap="word")
        self.txt_preparacion.pack(fill="both", expand=True, padx=6, pady=(0, 6))

    def _build_frame_datos(self):
        # Título del frame
        lbl_titulo = ctk.CTkLabel(
            self.frame_datos,
            text="Receta",
            font=("Arial", 20, "bold")
        )
        lbl_titulo.grid(row=0, column=0, columnspan=2, pady=10)

        # Nombre
        lbl_nombre = ctk.CTkLabel(self.frame_datos, text="Nombre:")
        lbl_nombre.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        self.entry_nombre = ctk.CTkEntry(self.frame_datos, width=300)
        self.entry_nombre.grid(row=1, column=1, padx=10, pady=5)

        # Categoría
        lbl_categoria = ctk.CTkLabel(self.frame_datos, text="Categoría:")
        lbl_categoria.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        self.combo_categoria = ctk.CTkComboBox(
            self.frame_datos,
            values=["Desayuno", "Comida", "Cena", "Snack", "Postre", "Bebida"],
            width=300
        )
        self.combo_categoria.grid(row=2, column=1, padx=10, pady=5)

        # Tiempo
        lbl_tiempo = ctk.CTkLabel(self.frame_datos, text="Tiempo:")
        lbl_tiempo.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        self.entry_tiempo = ctk.CTkEntry(self.frame_datos, width=300)
        self.entry_tiempo.grid(row=3, column=1, padx=10, pady=5)

if __name__ == "__main__":
    app = App()
    app.mainloop()