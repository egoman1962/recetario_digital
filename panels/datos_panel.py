import customtkinter as ctk
import tkinter as tk  # para StringVar

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

        # Tiempo (con sufijo ' min')
        ctk.CTkLabel(self, text="TIEMPO:", font=("Arial", 21, "bold"),
                     fg_color='gray6').place(x=90, y=288)

        self.tiempo_var = tk.StringVar()
        self.entry_tiempo = ctk.CTkEntry(
            self, width=300, font=("Arial", 18, "bold"),
            fg_color='#1F6AA5', border_color='#144870',
            textvariable=self.tiempo_var
        )
        self.entry_tiempo.place(x=54, y=336)

        # Eventos para mantener el sufijo y sólo dígitos
        self.entry_tiempo.bind("<KeyRelease>", self._on_tiempo_change)
        self.entry_tiempo.bind("<FocusOut>",  self._on_tiempo_change)

    # ---------- Helpers de tiempo con sufijo ---------- #
    def _format_tiempo(self, text: str) -> str:
        # conservar sólo dígitos
        digits = "".join(ch for ch in text if ch.isdigit())
        return f"{digits} min" if digits else ""

    def _on_tiempo_change(self, _evt=None):
        current = self.tiempo_var.get()
        formatted = self._format_tiempo(current)
        if current != formatted:
            # Actualiza el texto y coloca el cursor antes del sufijo
            self.tiempo_var.set(formatted)
            digits_len = len(formatted.replace(" min", ""))
            # mover el cursor al final de los dígitos
            self.entry_tiempo.after(0, lambda: self.entry_tiempo.icursor(digits_len))

    # Para que el controlador pueda leer/poner el valor fácilmente
    def get_tiempo_minutes(self) -> str | None:
        """Devuelve sólo los minutos (ej. '30') o None si vacío."""
        text = self.tiempo_var.get()
        digits = "".join(ch for ch in text if ch.isdigit())
        return digits or None

    def set_tiempo_minutes(self, minutes: int | str | None):
        """Asigna minutos y muestra 'NN min' o vacío si None."""
        if minutes is None or str(minutes).strip() == "":
            self.tiempo_var.set("")
        else:
            self.tiempo_var.set(f"{int(minutes)} min")
            self.entry_tiempo.icursor(len(str(int(minutes))))
