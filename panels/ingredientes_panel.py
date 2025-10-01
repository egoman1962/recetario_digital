import customtkinter as ctk

class IngredientesPanel(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master, fg_color='gray6')
        self.controller = controller
        self.pack(fill="both", expand=True)

        pad = {'padx': 45, 'pady': 6}
        ctk.CTkLabel(self, text="INGREDIENTES", text_color='green',
                     font=("Arial", 24, "bold")).pack(anchor="w", **pad)

        self.txt = ctk.CTkTextbox(self, wrap="word", fg_color='gray6', font=("Arial", 21, "bold"), height=15)
        self.txt.pack(fill="both", expand=True, padx=6, pady=(0, 6))

        self.txt.insert("1.0", "● ")
        self.txt.bind("<Return>", self._add_bullet)

    def _add_bullet(self, event=None):
        self.txt.insert("insert", "\n●  ")
        return "break"
