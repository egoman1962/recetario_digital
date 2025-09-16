import customtkinter as ctk

# Nitidez en Windows (opcional)
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

APP_TITLE = "Recetario Digital"
FULL_W, FULL_H = 1920, 1080
SCALE = 0.80
INIT_W, INIT_H = int(FULL_W * SCALE), int(FULL_H * SCALE)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Calcular centro del monitor principal
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        pos_x = int((screen_w // 2) - (INIT_W // 2))
        pos_y = int((screen_h // 2) - (INIT_H // 2))

        # Estado inicial: 65% centrado
        self.geometry(f"{INIT_W}x{INIT_H}+{pos_x}+{pos_y}")

        # Permitimos maximizar y restaurar
        self.minsize(INIT_W, INIT_H)
        self.resizable(True, True)

if __name__ == "__main__":
    app = App()
    app.mainloop()
