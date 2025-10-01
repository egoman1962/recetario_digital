import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from pathlib import Path
import db

# Panels
from panels.left_panel import LeftActions
from panels.foto_panel import FotoPanel
from panels.datos_panel import DatosPanel
from panels.ingredientes_panel import IngredientesPanel
from panels.preparacion_panel import PreparacionPanel
from panels.tabla_panel import TablaPanel

APP_TITLE = "Recetario Digital"
ASSETS_DIR = Path(__file__).with_name("fotos")
ASSETS_DIR.mkdir(exist_ok=True)


class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color='gray6')

        # Estado / DB
        db.init_db()
        self.selected_id = None

        # Ventana
        self.title(APP_TITLE)
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('blue')
        self.state("zoomed")
        self.resizable(True, True)

        # --- Frames contenedores (como ya los tenías) ---
        self.frame_izquierdo  = ctk.CTkFrame(self, fg_color='gray12', width=360,  height=984)
        self.frame_izquierdo.place(x=12, y=12)

        self.frame_derecho    = ctk.CTkFrame(self, fg_color='gray12', width=1518, height=984)
        self.frame_derecho.place(x=388, y=12)

        self.frame_foto       = ctk.CTkFrame(self.frame_derecho, fg_color='gray6', width=456, height=456)
        self.frame_foto.place(x=24, y=24)
        self.frame_foto.pack_propagate(False)
        self.frame_foto.configure(border_width=6, border_color='#1F6AA5')

        self.frame_datos      = ctk.CTkFrame(self.frame_derecho, fg_color='gray6', width=456, height=456)
        self.frame_datos.place(x=504, y=24)
        self.frame_datos.pack_propagate(False)
        self.frame_datos.configure(border_width=6, border_color='#1F6AA5')

        self.frame_ingred     = ctk.CTkFrame(self.frame_derecho, fg_color='gray6', width=510, height=456)
        self.frame_ingred.place(x=984, y=24)
        self.frame_ingred.pack_propagate(False)

        self.frame_prep       = ctk.CTkFrame(self.frame_derecho, fg_color='gray6', width=510, height=456)
        self.frame_prep.place(x=984, y=504)
        self.frame_prep.pack_propagate(False)

        self.frame_tabla      = ctk.CTkFrame(self.frame_derecho, fg_color='gray6', width=936, height=456)
        self.frame_tabla.place(x=24, y=504)
        self.frame_tabla.pack_propagate(False)

        # --- Instanciar paneles ---
        self.left_actions = LeftActions(self.frame_izquierdo, controller=self)
        self.foto         = FotoPanel(self.frame_foto, controller=self, assets_dir=ASSETS_DIR)
        self.datos        = DatosPanel(self.frame_datos, controller=self)
        self.ingredientes = IngredientesPanel(self.frame_ingred, controller=self)
        self.preparacion  = PreparacionPanel(self.frame_prep, controller=self)
        self.tabla        = TablaPanel(self.frame_tabla, controller=self)

        # Cargar tabla
        self._refresh_table()

    # ----------------- Controlador: helpers de formulario -----------------
    def _collect_form(self):
        nombre = self.datos.entry_nombre.get().strip()
        categoria = self.datos.option_categoria.get().strip() if self.datos.option_categoria.get() else None
        tiempo = self.datos.entry_tiempo.get().strip() or None
        ingredientes = self.ingredientes.txt.get("1.0", "end").strip() or None
        instrucciones = self.preparacion.txt.get("1.0", "end").strip() or None
        foto = self.foto.get_photo_path()
        return nombre, categoria, tiempo, ingredientes, instrucciones, foto

    def _fill_form(self, rec: dict):
        self.selected_id = rec["id"]
        # Datos
        self.datos.entry_nombre.delete(0, "end"); self.datos.entry_nombre.insert(0, rec.get("nombre",""))
        self.datos.option_categoria.set(rec.get("categoria") or "Desayuno")
        self.datos.entry_tiempo.delete(0, "end"); self.datos.entry_tiempo.insert(0, rec.get("tiempo",""))
        # Textos
        self.ingredientes.txt.delete("1.0", "end")
        self.ingredientes.txt.insert("1.0", (rec.get("ingredientes") or "● "))
        self.preparacion.txt.delete("1.0", "end")
        self.preparacion.txt.insert("1.0", (rec.get("instrucciones") or "1. "))
        self.preparacion.reset_step_number_from_content()
        # Foto
        self.foto.render_photo(rec.get("foto"))

    def _clear_form(self):
        self.selected_id = None
        self.datos.entry_nombre.delete(0, "end")
        self.datos.option_categoria.set("Desayuno")
        self.datos.entry_tiempo.delete(0, "end")
        self.ingredientes.txt.delete("1.0", "end"); self.ingredientes.txt.insert("1.0", "● ")
        self.preparacion.txt.delete("1.0", "end"); self.preparacion.reset(1); self.preparacion.txt.insert("1.0","1. ")
        self.foto.clear()

    # ----------------- Controlador: tabla / CRUD / búsqueda --------------
    def _refresh_table(self, rows=None):
        data = rows if rows is not None else db.get_all_recipes()
        self.tabla.populate(data)

    def _on_select_row(self, rid: int):
        rec = db.get_recipe_by_id(int(rid))
        if isinstance(rec, dict):
            self._fill_form(rec)
        else:
            keys = ["id","nombre","categoria","tiempo","ingredientes","instrucciones","foto"]
            self._fill_form(dict(zip(keys, rec)))

    def _on_new(self):
        self._clear_form()

    def _on_save(self):
        nombre, categoria, tiempo, ingredientes, instrucciones, foto = self._collect_form()
        if not nombre:
            CTkMessagebox(title="Validación", message="El nombre es obligatorio.", icon="warning"); return
        rid = db.add_recipe(nombre, categoria, tiempo, ingredientes, instrucciones, foto)
        self.selected_id = rid
        self._refresh_table()
        CTkMessagebox(title="Éxito", message="Receta guardada.", icon="check")

    def _on_update(self):
        if not self.selected_id:
            CTkMessagebox(title="Actualizar", message="Selecciona una receta en la tabla.", icon="info"); return
        nombre, categoria, tiempo, ingredientes, instrucciones, foto = self._collect_form()
        if not nombre:
            CTkMessagebox(title="Validación", message="El nombre es obligatorio.", icon="warning"); return
        db.update_recipe(self.selected_id, nombre, categoria, tiempo, ingredientes, instrucciones, foto)
        self._refresh_table()
        CTkMessagebox(title="Éxito", message="Receta actualizada.", icon="check")

    def _on_delete(self):
        if not self.selected_id:
            CTkMessagebox(title="Borrar", message="Selecciona una receta en la tabla.", icon="info"); return
        ask = CTkMessagebox(title="Confirmar", message="¿Borrar la receta seleccionada?", icon="warning",
                            option_1="Cancelar", option_2="Borrar")
        if ask.get() == "Borrar":
            db.delete_recipe(self.selected_id)
            self._clear_form()
            self._refresh_table()
            CTkMessagebox(title="Éxito", message="Receta borrada.", icon="check")

    def _on_search(self):
        text = self.tabla.get_search_text().strip()
        if not text:
            self._refresh_table(db.get_all_recipes())
        else:
            rows = db.search_recipes(text)
            self._refresh_table(rows)

    def _on_search_clear(self):
        self.tabla.clear_search()
        self._refresh_table(db.get_all_recipes())


if __name__ == "__main__":
    app = App()
    app.mainloop()
