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
        super().__init__()
        self.title(APP_TITLE)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Abrir directamente maximizada al 100%
        self.state("zoomed")

        # Permitir botones del sistema
        self.resizable(True, True)

        # Frame 1
        self.frame1 = ctk.CTkFrame(self, fg_color="teal", width=360, height=984)
        self.frame1.place(x=12, y=12)

        # Frame 2
        self.frame2 = ctk.CTkFrame(self, fg_color="purple", width=1518, height=984)
        self.frame2.place(x=388, y=12)

if __name__ == "__main__":
    app = App()
    app.mainloop()
