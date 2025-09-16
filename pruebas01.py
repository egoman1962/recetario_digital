import customtkinter as ctk

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

APP_TITLE = "Recetario Digital"
WIDTH, HEIGHT = 1920, 1080

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Colocar en esquina superior izquierda (0,0)
        self.geometry(f"{WIDTH}x{HEIGHT}+0+0")

        # Tamaño fijo
        self.minsize(WIDTH, HEIGHT)
        self.maxsize(WIDTH, HEIGHT)
        self.resizable(False, False)

        # Bloquear movimiento de la ventana
        self.bind("<Configure>", self._fix_position)

    def _fix_position(self, event=None):
        """Impide que la ventana se mueva de (0,0)."""
        self.geometry(f"{WIDTH}x{HEIGHT}+0+0")

if __name__ == "__main__":
    app = App()
    app.mainloop()
