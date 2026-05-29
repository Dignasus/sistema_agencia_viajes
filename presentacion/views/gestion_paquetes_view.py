import tkinter as tk
from tkinter import ttk, messagebox
from negocio.services.paquete_service import PaqueteService

# COLORES Y ESTILOS GLOBALES
COLOR_FONDO = "#ECF0F1"
COLOR_HEADER = "#2C3E50"
COLOR_TEXTO = "#2C3E50"
COLOR_BTN_VERDE = "#27AE60"  # Crear
COLOR_BTN_AMARILLO = "#F39C12" # Editar
COLOR_BTN_ROJO = "#C0392B"   # Eliminar
FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_LABEL = ("Segoe UI", 10)
FONT_BTN = ("Segoe UI", 10, "bold")

class GestionPaquetesView(tk.Toplevel):
    def __init__(self, parent, usuario_admin):
        super().__init__(parent)
        self.usuario = usuario_admin
        self.service = PaqueteService()

        # Configuración de Ventana
        self.title(f"Gestión de Paquetes - Admin: {self.usuario.nombre}")
        self.geometry("1000x650")
        self.configure(bg=COLOR_FONDO)

        # ESTILO DE LA TABLA (Treeview)
        style = ttk.Style()
        style.theme_use("clam")
        
        # Encabezados
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), 
                        background=COLOR_HEADER, foreground="white", relief="flat")
        # Filas
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=30, 
                        background="white", fieldbackground="white", borderwidth=0)
        # Selección
        style.map("Treeview", background=[('selected', '#3498DB')])

        # TÍTULO
        tk.Label(self, text="📦 Administración de Paquetes Turísticos", 
                 font=FONT_TITLE, bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=20)

        # BARRA DE HERRAMIENTAS (Filtro y Botones)
        toolbar = tk.Frame(self, bg=COLOR_FONDO)
        toolbar.pack(fill=tk.X, padx=30, pady=10)

        # SECCIÓN FILTRO (Izquierda)
        frame_filtro = tk.Frame(toolbar, bg=COLOR_FONDO)
        frame_filtro.pack(side=tk.LEFT)
        
        tk.Label(frame_filtro, text="Filtrar por tipo:", font=FONT_LABEL, bg=COLOR_FONDO).pack(side=tk.LEFT)
        
        self.combo_filtro = ttk.Combobox(frame_filtro, 
                                         values=["Solo Oficiales", "De Clientes (Personalizados)", "Todos"], 
                                         state="readonly", width=25, font=("Segoe UI", 10))
        self.combo_filtro.current(0)
        self.combo_filtro.pack(side=tk.LEFT, padx=10)
        self.combo_filtro.bind("<<ComboboxSelected>>", self.filtrar_tabla)

        # SECCIÓN BOTONES (Derecha)
        frame_botones = tk.Frame(toolbar, bg=COLOR_FONDO)
        frame_botones.pack(side=tk.RIGHT)

        self.crear_boton(frame_botones, "+ Nuevo Paquete", COLOR_BTN_VERDE, self.abrir_formulario_crear)
        self.crear_boton(frame_botones, "✏️ Editar", COLOR_BTN_AMARILLO, self.abrir_formulario_editar)
        self.crear_boton(frame_botones, "🗑 Eliminar", COLOR_BTN_ROJO, self.eliminar_paquete)

        # --- TABLA ---
        frame_tabla = tk.Frame(self, bg="white", bd=1, relief=tk.SOLID)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))

        columns = ("ID", "Nombre", "Precio", "Inicio", "Fin", "Tipo")
        self.tree = ttk.Treeview(frame_tabla, columns=columns, show="headings", style="Treeview")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configurar columnas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre del Paquete")
        self.tree.heading("Precio", text="Precio ($)")
        self.tree.heading("Inicio", text="F. Inicio")
        self.tree.heading("Fin", text="F. Fin")
        self.tree.heading("Tipo", text="Origen")
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nombre", width=350)
        self.tree.column("Precio", width=120, anchor="e")
        self.tree.column("Inicio", width=100, anchor="center")
        self.tree.column("Fin", width=100, anchor="center")
        self.tree.column("Tipo", width=100, anchor="center")
        
        self.cargar_datos()

        # Botón Cerrar
        tk.Button(self, text="Cerrar Ventana", font=("Segoe UI", 9), bg="#95A5A6", fg="white",
                  relief="flat", padx=10, pady=5, command=self.destroy).pack(pady=10)

    # MÉTODO HELPER
    def crear_boton(self, parent, texto, color, comando):
        btn = tk.Button(parent, text=texto, bg=color, fg="white", 
                        font=FONT_BTN, relief="flat", padx=15, pady=8, cursor="hand2",
                        command=comando)
        btn.pack(side=tk.LEFT, padx=5)
        # Hover effect simple
        btn.bind("<Enter>", lambda e: btn.config(bg=self.adjust_color_lightness(color, 0.9)))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))

    def adjust_color_lightness(self, color, factor):
        return color

    #LÓGICA DE NEGOCIO

    def filtrar_tabla(self, event=None):
        self.cargar_datos()

    def cargar_datos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        seleccion = self.combo_filtro.get()
        try:
            if seleccion == "Solo Oficiales":
                paquetes = self.service.obtener_paquetes(tipo='oficial')
            elif seleccion == "De Clientes (Personalizados)":
                paquetes = self.service.obtener_paquetes(tipo='personalizado')
            else:
                paquetes = self.service.obtener_paquetes() 
            
            for p in paquetes:
                tag = "par" if p.id_paquete % 2 == 0 else "impar"
                self.tree.insert("", tk.END, values=(
                    p.id_paquete, 
                    p.nombre_paquete, 
                    f"${p.precio_total:,.0f}", 
                    p.fecha_inicio, 
                    p.fecha_fin, 
                    p.tipo
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar: {e}")

    def abrir_formulario_crear(self):
        FormularioPaqueteView(self, self.service, self.usuario, paquete_a_editar=None)

    def abrir_formulario_editar(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un paquete para editar.")
            return
        
        item = self.tree.item(seleccion)
        id_paquete = item['values'][0]

        try:
            paquete_completo = self.service.obtener_por_id(id_paquete)
        except AttributeError:
             from persistencia.repositorio.paquete_repo import PaqueteRepo
             repo = PaqueteRepo()
             paquete_completo = repo.obtener_por_id(id_paquete)

        if paquete_completo:
            FormularioPaqueteView(self, self.service, self.usuario, paquete_a_editar=paquete_completo)
        else:
            messagebox.showerror("Error", "No se pudieron obtener los datos del paquete.")

    def eliminar_paquete(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un paquete para eliminar.")
            return

        if messagebox.askyesno("Confirmar", "¿Eliminar paquete permanentemente?"):
            try:
                item = self.tree.item(seleccion)
                id_paquete = item['values'][0]
                self.service.eliminar_paquete(id_paquete)
                messagebox.showinfo("Éxito", "Paquete eliminado.")
                self.cargar_datos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {e}")


# CLASE FORMULARIO
class FormularioPaqueteView(tk.Toplevel):
    def __init__(self, parent, service, usuario_admin, paquete_a_editar=None):
        super().__init__(parent)
        self.service = service
        self.usuario = usuario_admin
        self.parent_view = parent
        self.paquete = paquete_a_editar 
        
        # Config Ventana
        self.configure(bg=COLOR_FONDO)
        self.geometry("500x500")
        
        if self.paquete:
            titulo = f"Editar Paquete #{self.paquete.id_paquete}"
            texto_boton = "Guardar Cambios"
        else:
            titulo = "Crear Nuevo Paquete"
            texto_boton = "Crear Paquete"

        self.title(titulo)

        # Encabezado Formulario
        tk.Label(self, text=titulo, font=FONT_TITLE, bg=COLOR_FONDO, fg=COLOR_HEADER).pack(pady=20)

        # Contenedor para alinear campos
        frame_form = tk.Frame(self, bg=COLOR_FONDO)
        frame_form.pack(padx=40, pady=10, fill=tk.X)

        self.crear_campo(frame_form, "Nombre del Paquete:", "entry_nombre")
        self.crear_campo(frame_form, "Precio Total ($):", "entry_precio")
        self.crear_campo(frame_form, "Fecha Inicio (YYYY-MM-DD):", "entry_inicio")
        self.crear_campo(frame_form, "Fecha Fin (YYYY-MM-DD):", "entry_fin")

        # Rellenar datos
        if self.paquete:
            self.entry_nombre.insert(0, self.paquete.nombre_paquete)
            self.entry_precio.insert(0, str(int(self.paquete.precio_total)))
            self.entry_inicio.insert(0, str(self.paquete.fecha_inicio))
            self.entry_fin.insert(0, str(self.paquete.fecha_fin))
        else:
            self.entry_inicio.insert(0, "2024-06-01")
            self.entry_fin.insert(0, "2024-06-15")

        # Botón Guardar
        tk.Button(self, text=texto_boton, bg=COLOR_BTN_VERDE, fg="white", 
                  font=("Segoe UI", 12, "bold"), relief="flat", padx=20, pady=10, cursor="hand2",
                  command=self.guardar).pack(pady=30)

    def crear_campo(self, parent, texto, nombre_attr):
        # Helper para crear labels y entries alineados
        tk.Label(parent, text=texto, font=FONT_LABEL, bg=COLOR_FONDO, anchor="w").pack(fill=tk.X, pady=(10, 0))
        entry = tk.Entry(parent, font=("Segoe UI", 11), relief="flat", bd=1, highlightthickness=1)
        entry.config(highlightbackground="#BDC3C7", highlightcolor="#3498DB") # Borde gris que se pone azul al escribir
        entry.pack(fill=tk.X, pady=(2, 0), ipady=3) # ipady hace el input más alto y cómodo
        setattr(self, nombre_attr, entry)

    def guardar(self):
        nombre = self.entry_nombre.get()
        precio = self.entry_precio.get()
        inicio = self.entry_inicio.get()
        fin = self.entry_fin.get()
        id_admin = getattr(self.usuario, 'id', 1)

        try:
            if self.paquete:
                self.service.actualizar_paquete(
                    self.paquete.id_paquete, nombre, precio, inicio, fin, id_admin
                )
                mensaje = "Paquete actualizado correctamente."
            else:
                self.service.crear_paquete_admin(
                    nombre, precio, inicio, fin, id_admin
                )
                mensaje = "Paquete creado correctamente."

            messagebox.showinfo("Éxito", mensaje)
            self.parent_view.cargar_datos() 
            self.destroy()

        except ValueError as e:
            messagebox.showwarning("Datos Inválidos", str(e))
        except Exception as e:
            print(f"Error al guardar: {e}")
            messagebox.showerror("Error", f"Ocurrió un error: {e}")