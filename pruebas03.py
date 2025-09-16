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

        self.frame_tabla = ctk.CTkFrame(self.frame_derecho, fg_color='gray6', width=936, height=456)
        self.frame_tabla.place(x=24, y=504)

        self.frame_ingredientes = ctk.CTkFrame(self.frame_derecho, fg_color='gray6', width=510, height=456)
        self.frame_ingredientes.place(x=984, y=24)

        self.frame_preparacion = ctk.CTkFrame(self.frame_derecho, fg_color='gray6', width=510, height=456)
        self.frame_preparacion.place(x=984, y=504)

if __name__ == "__main__":
    app = App()
    app.mainloop()
