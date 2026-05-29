import tkinter as tk
from tkinter import ttk, messagebox
from persistencia.repositorio.reserva_repo import ReservaRepository

class ReservasAdminView(tk.Toplevel):
    def __init__(self, parent, usuario):
        super().__init__(parent)
        self.usuario = usuario
        self.repo = ReservaRepository() 
        
        # Configuración de la ventana
        self.title("Gestión de Reservas (ADMIN) - Viajes Aventura")
        self.geometry("1000x600")
        self.configure(bg="#f3f4f6")

        # 1. ENCABEZADO (Header) - Azul Oscuro
        self.header_frame = tk.Frame(self, bg="#2c3e50", height=80)
        self.header_frame.pack(fill="x")
        
        # Título
        tk.Label(
            self.header_frame, 
            text="PANEL DE CONTROL DE RESERVAS", 
            bg="#2c3e50", 
            fg="white",
            font=("Helvetica", 18, "bold")
        ).pack(pady=20)

        # 2. ESTILOS DE LA TABLA (Moderno)
        style = ttk.Style()
        style.theme_use("clam") # Necesario para personalizar colores de cabecera

        # Estilo Cabeceras
        style.configure(
            "Treeview.Heading", 
            background="#2c3e50", 
            foreground="white", 
            font=("Segoe UI", 10, "bold"),
            relief="flat"
        )
        # Estilo Filas
        style.configure(
            "Treeview", 
            background="white",
            fieldbackground="white",
            foreground="#333333",
            rowheight=30,
            font=("Segoe UI", 10)
        )
        # Color de selección
        style.map("Treeview", background=[('selected', '#2980b9')])

        # 3. TABLA DE DATOS
        frame_tabla = tk.Frame(self, bg="#f3f4f6", padx=20, pady=20)
        frame_tabla.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "Cliente", "Paquete", "Fecha", "Estado")
        self.tree = ttk.Treeview(frame_tabla, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("ID", text="ID")
        self.tree.heading("Cliente", text="CLIENTE")
        self.tree.heading("Paquete", text="PAQUETE")
        self.tree.heading("Fecha", text="FECHA")
        self.tree.heading("Estado", text="ESTADO")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Cliente", width=150)
        self.tree.column("Paquete", width=250)
        self.tree.column("Fecha", width=100, anchor="center")
        self.tree.column("Estado", width=100, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 4. BARRA DE ACCIONES (Botones Planos)
        frame_botones = tk.Frame(self, bg="white", pady=15, padx=20)
        frame_botones.pack(fill=tk.X, side="bottom")

        # Etiqueta Acciones
        tk.Label(frame_botones, text="Acciones:", bg="white", fg="#7f8c8d", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))

        # Botón CONFIRMAR (Verde y plano)
        tk.Button(
            frame_botones, 
            text="✓ CONFIRMAR", 
            bg="#27ae60", fg="white", 
            font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2",
            padx=15, pady=5,
            command=self.confirmar_reserva
        ).pack(side=tk.LEFT, padx=5)

        # Botón CANCELAR (Rojo y plano)
        tk.Button(
            frame_botones, 
            text="✕ CANCELAR", 
            bg="#c0392b", fg="white", 
            font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2",
            padx=15, pady=5,
            command=self.cancelar_reserva
        ).pack(side=tk.LEFT, padx=5)

        # Botón REFRESCAR (Gris claro)
        tk.Button(
            frame_botones, 
            text="↻ Refrescar", 
            bg="#ecf0f1", fg="#2c3e50", 
            font=("Segoe UI", 9), relief="flat", cursor="hand2",
            padx=10, pady=5,
            command=self.cargar_datos
        ).pack(side=tk.LEFT, padx=20)

        # Botón CERRAR (Derecha)
        tk.Button(
            frame_botones, 
            text="Cerrar", 
            bg="#95a5a6", fg="white", 
            font=("Segoe UI", 9), relief="flat", cursor="hand2",
            padx=10, pady=5,
            command=self.destroy
        ).pack(side=tk.RIGHT)

        # Cargar datos al iniciar
        self.cargar_datos()

        # logica negocio
    def cargar_datos(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            datos = self.repo.obtener_todas_detalladas()
            for fila in datos:
                # fila = (id_reserva, nombre_cliente, nombre_paquete, fecha, estado)
                self.tree.insert("", tk.END, values=fila)

        except Exception as e:
            print(f"Error cargando reservas admin: {e}")
            messagebox.showerror("Error", "No se pudo cargar el historial.")

    def cambiar_estado_seleccion(self, nuevo_estado):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, selecciona una reserva de la lista.")
            return

        item = self.tree.item(seleccion)
        id_reserva = item['values'][0]
        estado_actual = item['values'][4]

        # Evitar cambiar si ya está en ese estado
        if estado_actual == nuevo_estado:
            messagebox.showinfo("Info", f"Esta reserva ya está '{nuevo_estado}'.")
            return

        if messagebox.askyesno("Confirmar", f"¿Cambiar estado de reserva #{id_reserva} a '{nuevo_estado}'?"):
            try:
                self.repo.cambiar_estado(id_reserva, nuevo_estado)
                messagebox.showinfo("Éxito", f"Reserva actualizada a {nuevo_estado}.")
                self.cargar_datos() 
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar: {e}")

    def confirmar_reserva(self):
        self.cambiar_estado_seleccion("Confirmada")

    def cancelar_reserva(self):
        self.cambiar_estado_seleccion("Cancelada")