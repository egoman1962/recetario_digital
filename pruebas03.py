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

        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('blue')

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

    def _build_frame_foto(self):
        pad = {'padx': 45, 'pady': 6}

        # --- Título ---
        title = ctk.CTkLabel(
            self.frame_foto,
            text="FOTOGRAFÍA",
            text_color='green',
            font=("Arial", 24, "bold")
        )
        title.pack(anchor="w", **pad)

        # --- Recuadro para la imagen ---
        self.lbl_foto = ctk.CTkLabel(
            self.frame_foto,
            text="Sin foto",
            width=416,  # ajustado al tamaño del frame
            height=312,
            fg_color="gray10",
            text_color="gray70",
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
        self.btn_cargar.place(x=40, y=378)

        # Botón para quitar
        self.btn_quitar = ctk.CTkButton(self.frame_foto, text="Quitar foto", font=("Arial", 18, "bold"),
                                        width=150, command=self._quitar_foto, height=45)
        self.btn_quitar.place(x=250, y=378)

    def _cargar_foto(self):
        # Aquí luego pondremos el código para abrir el explorador y cargar la imagen
        print("Cargar foto presionado")

    def _quitar_foto(self):
        # Esto limpia el recuadro
        self.lbl_foto.configure(image=None, text="Sin foto")
        self.lbl_foto.image = None
        print("Foto quitada")

    def _build_ingredientes(self):
        pad = {'padx': 45, 'pady': 6}
        title = ctk.CTkLabel(self.frame_ingredientes, text="INGREDIENTES",
                             text_color='green', font=("Arial", 24, "bold"))
        title.pack(anchor="w", **pad)
        self.txt_ingredientes = ctk.CTkTextbox(self.frame_ingredientes, wrap="word")
        self.txt_ingredientes.pack(fill="both", expand=True, padx=6, pady=(0, 6))

    def _build_preparacion(self):
        pad = {'padx': 45, 'pady': 6}
        title = ctk.CTkLabel(self.frame_preparacion, text="PREPARACION",
                             text_color='green',  font=("Arial", 24, "bold"))
        title.pack(anchor="w", **pad)
        self.txt_preparacion = ctk.CTkTextbox(self.frame_preparacion, wrap="word")
        self.txt_preparacion.pack(fill="both", expand=True, padx=6, pady=(0, 6))

    def _build_frame_datos(self):
        pad = {'padx': 45, 'pady': 6}
        title = ctk.CTkLabel(self.frame_datos, text="RECETA",
                             text_color='green', font=("Arial", 24, "bold"))
        title.pack(anchor="w", **pad)
        self.txt_datos = ctk.CTkTextbox(self.frame_datos, wrap="word")
        self.txt_datos.pack(fill="both", expand=True, padx=6, pady=(0, 6))

        # Nombre
        lbl_nombre = ctk.CTkLabel(self.frame_datos, text="Nombre:",
                                  font=("Arial", 21, "bold"), fg_color='gray12')
        lbl_nombre.place(x=90, y=72)
        self.entry_nombre = ctk.CTkEntry(self.frame_datos, width=300,
                                         font=("Arial", 18, "bold"), fg_color='#1F6AA5', border_color='#144870')
        self.entry_nombre.place(x=54, y=120)

        # Categoría
        lbl_categoria = ctk.CTkLabel(self.frame_datos,text="Categoría:",
            font=("Arial", 21, "bold"),fg_color = 'gray12' )
        lbl_categoria.place(x=90, y=180)

        self.option_categoria = ctk.CTkOptionMenu(self.frame_datos,
            values=["Desayuno", "Comida", "Cena", "Snack", "Postre", "Bebida"], width=300,
            font=("Arial", 16, "bold"), button_color='#144870')
        self.option_categoria.place(x=54, y=228)
        # Valor inicial
        self.option_categoria.set("Desayuno")

        # Tiempo
        lbl_tiempo = ctk.CTkLabel(self.frame_datos, text="Tiempo:",
                                  font=("Arial", 21, "bold"), fg_color='gray12')
        lbl_tiempo.place(x=90, y=288)
        self.entry_tiempo = ctk.CTkEntry(self.frame_datos, width=300,
                                         fg_color='#1F6AA5', border_color='#144870')
        self.entry_tiempo.place(x=54, y=336)


if __name__ == "__main__":
    app = App()
    app.mainloop()