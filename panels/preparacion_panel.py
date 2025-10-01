import customtkinter as ctk

class PreparacionPanel(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master, fg_color='gray6')
        self.controller = controller
        self.pack(fill="both", expand=True)

        pad = {'padx': 45, 'pady': 6}
        ctk.CTkLabel(self, text="PREPARACIÓN", text_color='green',
                     font=("Arial", 24, "bold")).pack(anchor="w", **pad)

        self.txt = ctk.CTkTextbox(self, wrap="word", fg_color='gray6', font=("Arial", 21, "bold"), height=15)
        self.txt.pack(fill="both", expand=True, padx=6, pady=(0, 6))

        self.step_number = 1
        self.txt.insert("1.0", f"{self.step_number}. ")
        self.txt.bind("<Return>", self._add_step)

    def _add_step(self, event=None):
        self.step_number += 1
        self.txt.insert("insert", f"\n{self.step_number}. ")
        return "break"

    def reset(self, n: int = 1):
        self.step_number = n

    def reset_step_number_from_content(self):
        try:
            last_num = 0
            for line in self.txt.get("1.0", "end").splitlines():
                s = line.strip()
                if s and s[0].isdigit():
                    n = ""
                    for ch in s:
                        if ch.isdigit(): n += ch
                        else: break
                    if n:
                        last_num = max(last_num, int(n))
            self.step_number = max(1, last_num)
        except Exception:
            self.step_number = 1
