import customtkinter as ctk

class LeftActions(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master, fg_color="transparent")
        self.controller = controller
        self.pack(fill="both", expand=True)

        ctk.CTkLabel(self, text="ACCIONES", text_color='green',
                     font=("Arial", 24, "bold")).pack(anchor="w", padx=16, pady=(16, 8))

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", padx=16)

        ctk.CTkButton(actions, text="Nuevo", height=48,
                      command=self.controller._on_new).pack(fill="x", pady=6)
        ctk.CTkButton(actions, text="Guardar", height=48,
                      command=self.controller._on_save).pack(fill="x", pady=6)
        ctk.CTkButton(actions, text="Actualizar", height=48,
                      command=self.controller._on_update).pack(fill="x", pady=6)
        ctk.CTkButton(actions, text="Borrar", height=48,
                      fg_color="#a33", hover_color="#c55",
                      command=self.controller._on_delete).pack(fill="x", pady=6)
