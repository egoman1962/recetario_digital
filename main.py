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
LEFT_W = 360  # ancho del panel izquierdo

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

        # Estado inicial: 80% centrado; permitir maximizar/restaurar
        self.geometry(f"{INIT_W}x{INIT_H}+{pos_x}+{pos_y}")
        self.minsize(INIT_W, INIT_H)
        self.resizable(True, True)

        # ====== LAYOUT RAÍZ (2 columnas) ======
        # Columna 0: izquierda fija; Columna 1: derecha expansible
        self.grid_columnconfigure(0, minsize=LEFT_W, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ----- Panel izquierdo -----
        self.left = ctk.CTkFrame(self, corner_radius=0)
        self.left.grid(row=0, column=0, sticky="nsew")
        self._build_left()

        # ----- Panel derecho (4 cuadrantes) -----
        self.right = ctk.CTkFrame(self)
        self.right.grid(row=0, column=1, sticky="nsew")
        self._build_right_quadrants()

    # ----------------- UI: Panel izquierdo -----------------
    def _build_left(self):
        # Estructura simple: título y espacio vacío (placeholder)
        self.left.grid_rowconfigure(1, weight=1)
        self.left.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self.left, text="Recetas", font=ctk.CTkFont(size=22, weight="bold"))
        title.grid(row=0, column=0, padx=16, pady=(16, 8), sticky="w")

        placeholder = ctk.CTkLabel(self.left, text="(Aquí irá la lista / búsqueda / botones)", text_color=("gray70", "gray60"))
        placeholder.grid(row=1, column=0, padx=16, pady=16, sticky="n")

    # --------- UI: Panel derecho con 4 cuadrantes ----------
    def _build_right_quadrants(self):
        # Grid 2x2 uniforme
        for r in range(2):
            self.right.grid_rowconfigure(r, weight=1, uniform="rows")
        for c in range(2):
            self.right.grid_columnconfigure(c, weight=1, uniform="cols")

        # Cuadrantes (frames con encabezado)
        self.box_tl = self._labeled_box(self.right, "Datos básicos")
        self.box_tl.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.box_tr = self._labeled_box(self.right, "Ingredientes")
        self.box_tr.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.box_bl = self._labeled_box(self.right, "Foto")
        self.box_bl.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.box_br = self._labeled_box(self.right, "Instrucciones")
        self.box_br.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        # Placeholders internos (para que veas el área)
        for box in (self.box_tl, self.box_tr, self.box_bl, self.box_br):
            box.grid_rowconfigure(1, weight=1)
            box.grid_columnconfigure(0, weight=1)
            ph = ctk.CTkLabel(box, text="(contenido)", text_color=("gray70", "gray60"))
            ph.grid(row=1, column=0, padx=12, pady=12, sticky="n")

    def _labeled_box(self, parent, title: str):
        """Crea un frame con título y una línea separadora"""
        frame = ctk.CTkFrame(parent)
        header = ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=16, weight="bold"))
        header.grid(row=0, column=0, padx=12, pady=(12, 6), sticky="w")
        sep = ctk.CTkFrame(frame, height=1, fg_color=("gray75", "gray30"))
        sep.grid(row=0, column=1, padx=12, pady=(12, 6), sticky="ew")
        frame.grid_columnconfigure(0, weight=0)
        frame.grid_columnconfigure(1, weight=1)
        return frame

if __name__ == "__main__":import customtkinter as ctk

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

    app = App()
    app.mainloop()
