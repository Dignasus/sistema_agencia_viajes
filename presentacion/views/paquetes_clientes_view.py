import tkinter as tk
from tkinter import ttk, messagebox
from negocio.services.paquete_service import PaqueteService
from persistencia.repositorio.destino_repo import DestinoRepository

class PaquetesClientesView(tk.Toplevel):
    def __init__(self, parent, usuario):
        super().__init__(parent)
        self.usuario = usuario
        self.service = PaqueteService()

        # 1. Configuración General
        self.title(f"Diseñador de Viajes - {self.usuario.nombre}")
        self.geometry("1100x700") 
        self.configure(bg="#f3f4f6") 

        # 2. ENCABEZADO (Header)
        self.header_frame = tk.Frame(self, bg="#2c3e50", height=80)
        self.header_frame.pack(fill="x")
        
        tk.Label(
            self.header_frame, 
            text="CREA TU PROPIA AVENTURA", 
            bg="#2c3e50", 
            fg="white",
            font=("Helvetica", 18, "bold")
        ).pack(pady=20)

        # 3. CONTENEDOR PRINCIPAL
        main_container = tk.Frame(self, bg="#f3f4f6")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # COLUMNA IZQUIERDA: FORMULARIO
        left_card = tk.Frame(main_container, bg="white", width=350, padx=20, pady=20)
        left_card.pack(side="left", fill="both", expand=False) 
        left_card.pack_propagate(False)

        # Título del Formulario
        tk.Label(left_card, text="1. Detalles del Viaje", bg="white", fg="#2c3e50", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0, 20))

        # Input Nombre
        tk.Label(left_card, text="NOMBRE DE TU AVENTURA", bg="white", fg="#7f8c8d", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.entry_nombre = tk.Entry(left_card, font=("Segoe UI", 11), bg="#f0f2f5", relief="flat")
        self.entry_nombre.pack(fill="x", ipady=8, pady=(5, 20))

        # Input Fecha Inicio
        tk.Label(left_card, text="FECHA INICIO (YYYY-MM-DD)", bg="white", fg="#7f8c8d", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.entry_inicio = tk.Entry(left_card, font=("Segoe UI", 11), bg="#f0f2f5", relief="flat")
        self.entry_inicio.pack(fill="x", ipady=8, pady=(5, 20))

        # Input Fecha Fin
        tk.Label(left_card, text="FECHA FIN (YYYY-MM-DD)", bg="white", fg="#7f8c8d", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.entry_fin = tk.Entry(left_card, font=("Segoe UI", 11), bg="#f0f2f5", relief="flat")
        self.entry_fin.pack(fill="x", ipady=8, pady=(5, 20))

        # Nota ayuda
        tk.Label(left_card, text="* Selecciona los destinos en la tabla de la derecha.", bg="white", fg="#95a5a6", font=("Segoe UI", 9, "italic"), wraplength=300, justify="left").pack(anchor="w", pady=(20, 0))

        # --- COLUMNA DERECHA: TABLA DE DESTINOS ---
        right_card = tk.Frame(main_container, bg="white", padx=20, pady=20)
        right_card.pack(side="left", fill="both", expand=True, padx=(20, 0)) 

        tk.Label(right_card, text="2. Selecciona tus Destinos", bg="white", fg="#2c3e50", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0, 10))
        tk.Label(right_card, text="Mantén presionada la tecla Ctrl para seleccionar varios.", bg="white", fg="#7f8c8d", font=("Segoe UI", 9)).pack(anchor="w", pady=(0, 10))

        # Estilos de Tabla
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="#2c3e50", foreground="white", font=("Segoe UI", 10, "bold"), relief="flat")
        style.configure("Treeview", background="white", fieldbackground="white", rowheight=30, font=("Segoe UI", 10))
        style.map("Treeview", background=[('selected', '#2980b9')])

        # Treeview
        columns = ("ID", "Nombre", "Descripcion", "Actividades", "Costo")
        self.tree = ttk.Treeview(right_card, columns=columns, show="headings", selectmode="extended")
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="DESTINO")
        self.tree.heading("Descripcion", text="DESCRIPCIÓN")
        self.tree.heading("Actividades", text="ACTIVIDADES")
        self.tree.heading("Costo", text="COSTO BASE")
        
        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Nombre", width=120)
        self.tree.column("Descripcion", width=200)
        self.tree.column("Actividades", width=200)
        self.tree.column("Costo", width=80, anchor="e")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(right_card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Cargar Destinos
        self.cargar_destinos()

        # ---------------------------------------------------------
        # 4. BARRA DE ACCIONES (Footer)
        # ---------------------------------------------------------
        footer_frame = tk.Frame(self, bg="white", pady=15, padx=20)
        footer_frame.pack(fill="x", side="bottom")

        # Botón Guardar
        tk.Button(
            footer_frame, 
            text="✓ GUARDAR PAQUETE", 
            bg="#27ae60", fg="white", 
            font=("Segoe UI", 11, "bold"), relief="flat", cursor="hand2",
            padx=20, pady=8,
            command=self.guardarPaquete
        ).pack(side="right", padx=10)

        # Botón Cancelar
        tk.Button(
            footer_frame, 
            text="Cancelar", 
            bg="#95a5a6", fg="white", 
            font=("Segoe UI", 10), relief="flat", cursor="hand2",
            padx=15, pady=8,
            command=self.destroy
        ).pack(side="right")

    def cargar_destinos(self):
        try:
            repo_destinos = DestinoRepository()
            datos = repo_destinos.obtener_todos()
            for d in datos:
                self.tree.insert("", tk.END, values=(d.id_destino, d.nombre, d.descripcion, d.actividades, d.costo_base))
        except Exception as e:
            print(f"Error cargando destinos: {e}")
            messagebox.showerror("Error", "No se pudieron cargar los destinos disponibles.", parent=self)

    def guardarPaquete(self):
        nombre = self.entry_nombre.get()
        inicio = self.entry_inicio.get()
        fin = self.entry_fin.get()
        
        if not hasattr(self.usuario, 'id'):
            messagebox.showerror("Error", "No se pudo identificar al usuario actual.", parent=self)
            return
        id_cliente = self.usuario.id

        if not nombre or not inicio or not fin:
            messagebox.showwarning("Faltan datos", "Por favor, completa todos los campos del formulario.", parent=self)
            return

        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Atención", "Debes seleccionar al menos un destino de la tabla.", parent=self)
            return

        destinos = []
        precios = 0.0

        try:
            for item in selected_items:
                values = self.tree.item(item, "values")
                destination_id = values[0]
                precio_unitario = float(values[4]) 
                destinos.append(destination_id)
                precios += precio_unitario
            
            self.service.crear_paquete_cliente(nombre, precios, inicio, fin, id_cliente, destinos)
            
            messagebox.showinfo("¡Felicidades!", "Tu paquete personalizado ha sido creado con éxito.", parent=self)
            self.destroy()

        except ValueError as e:
            messagebox.showerror("Error de Formato", f"Por favor verifica los datos ingresados.\n{e}", parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}", parent=self)