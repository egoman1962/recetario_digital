import customtkinter as ctk

class DatosPanel(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master, fg_color='gray6')
        self.controller = controller
        self.pack(fill="both", expand=True)
        self.configure(border_width=6, border_color='#1F6AA5')

        pad = {'padx': 45, 'pady': 6}
        ctk.CTkLabel(self, text="RECETA", text_color='green',
                     font=("Arial", 24, "bold")).pack(anchor="w", **pad)

        # Nombre
        ctk.CTkLabel(self, text="NOMBRE:", font=("Arial", 21, "bold"),
                     fg_color='gray6').place(x=90, y=72)
        self.entry_nombre = ctk.CTkEntry(self, width=300, font=("Arial", 18, "bold"),
                                         fg_color='#1F6AA5', border_color='#144870')
        self.entry_nombre.place(x=54, y=120)

        # Categoría
        ctk.CTkLabel(self, text="CATEGORIA:", font=("Arial", 21, "bold"),
                     fg_color='gray6').place(x=90, y=180)
        self.option_categoria = ctk.CTkOptionMenu(self,
            values=["Desayuno","Comida","Cena","Snack","Postre","Bebida"],
            width=300, font=("Arial", 18, "bold"), button_color='#144870')
        self.option_categoria.place(x=54, y=228)
        self.option_categoria.set("Desayuno")

        # Tiempo
        ctk.CTkLabel(self, text="TIEMPO:", font=("Arial", 21, "bold"),
                     fg_color='gray6').place(x=90, y=288)
        self.entry_tiempo = ctk.CTkEntry(self, width=300, font=("Arial", 18, "bold"),
                                         fg_color='#1F6AA5', border_color='#144870')
        self.entry_tiempo.place(x=54, y=336)
