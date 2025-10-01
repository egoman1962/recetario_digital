import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import filedialog
from PIL import Image
from pathlib import Path
import shutil

class FotoPanel(ctk.CTkFrame):
    def __init__(self, master, controller, assets_dir: Path):
        super().__init__(master, fg_color="gray6")
        self.controller = controller
        self.assets_dir = assets_dir
        self._img_path = None

        self.pack(fill="both", expand=True)
        self.configure(border_width=6, border_color='#1F6AA5')

        pad = {'padx': 45, 'pady': 6}
        ctk.CTkLabel(self, text="FOTOGRAFÍA", text_color='green',
                     font=("Arial", 24, "bold")).pack(anchor="w", **pad)

        self.lbl = ctk.CTkLabel(self, text="Sin foto", width=330, height=330,
                                fg_color='gray6', text_color='BLUE',
                                corner_radius=12, anchor="center")
        self.lbl.pack(padx=16, pady=(0, 12))

        # Botones
        ctk.CTkButton(self, text="Cargar foto", font=("Arial", 18, "bold"),
                      width=150, height=45, command=self._cargar_foto).place(x=40, y=390)
        ctk.CTkButton(self, text="Quitar foto", font=("Arial", 18, "bold"),
                      width=150, height=45, command=self._quitar_foto).place(x=250, y=390)

    # --- API pública del panel ---
    def get_photo_path(self):
        return self._img_path

    def render_photo(self, path: str | None):
        try:
            if path and Path(path).exists():
                img = Image.open(path).resize((318, 318), Image.LANCZOS)
                ctki = ctk.CTkImage(light_image=img, dark_image=img, size=(318, 318))
                self.lbl.configure(image=ctki, text="")
                self.lbl.image = ctki
                self._img_path = str(path)
            else:
                self.lbl.configure(image=None, text="Sin foto")
                self.lbl.image = None
                self._img_path = None
        except Exception as e:
            CTkMessagebox(title="Error", message=f"No se pudo renderizar la imagen:\n{e}", icon="cancel")

    def clear(self):
        self.render_photo(None)

    # --- Handlers internos ---
    def _cargar_foto(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar fotografía",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        if not file_path:
            return
        try:
            src = Path(file_path)
            dst = self.assets_dir / src.name
            if src.resolve() != dst.resolve():
                shutil.copyfile(src, dst)
            self.render_photo(str(dst))
            CTkMessagebox(title="Fotografía", message="La foto se cargó correctamente.", icon="check")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"No se pudo cargar la imagen:\n{e}", icon="cancel")

    def _quitar_foto(self):
        self.clear()
        CTkMessagebox(title="Fotografía", message="Se quitó la foto correctamente.", icon="check")
