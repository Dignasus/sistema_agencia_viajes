import tkinter as tk
from tkinter import ttk, messagebox
from persistencia.repositorio.reserva_repo import ReservaRepository

class ReservasClienteView(tk.Toplevel):
    def __init__(self, parent, usuario):
        super().__init__(parent)
        self.usuario = usuario
        self.repo = ReservaRepository()
        
        # 1. Configuración de Ventana
        self.title(f"Mis Reservas - {usuario.nombre}")
        self.geometry("900x600")
        self.configure(bg="#f3f4f6")

        # 2. Encabezado
        self.header_frame = tk.Frame(self, bg="#2c3e50", height=80)
        self.header_frame.pack(fill="x")
        
        tk.Label(
            self.header_frame, 
            text="MIS VIAJES RESERVADOS", 
            bg="#2c3e50", 
            fg="white",
            font=("Helvetica", 18, "bold")
        ).pack(pady=20)

        # 3. Estilos de Tabla
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure(
            "Treeview.Heading", 
            background="#2c3e50", 
            foreground="white", 
            font=("Segoe UI", 10, "bold"), 
            relief="flat"
        )
        style.configure(
            "Treeview", 
            background="white", 
            fieldbackground="white", 
            rowheight=30, 
            font=("Segoe UI", 10)
        )
        style.map("Treeview", background=[('selected', '#2980b9')])

        # 4. Tabla
        frame_tabla = tk.Frame(self, bg="#f3f4f6", padx=20, pady=20)
        frame_tabla.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "Paquete", "Fecha Viaje", "Estado")
        self.tree = ttk.Treeview(frame_tabla, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Paquete", text="PAQUETE TURÍSTICO")
        self.tree.heading("Fecha Viaje", text="FECHA RESERVA")
        self.tree.heading("Estado", text="ESTADO ACTUAL")
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Paquete", width=300)
        self.tree.column("Fecha Viaje", width=120, anchor="center")
        self.tree.column("Estado", width=120, anchor="center")
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")

        # 5. Barra de Acciones
        frame_botones = tk.Frame(self, bg="white", pady=15, padx=20)
        frame_botones.pack(fill=tk.X, side="bottom")

        tk.Label(frame_botones, text="Opciones:", bg="white", fg="#7f8c8d", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            frame_botones, 
            text="✕ CANCELAR VIAJE", 
            bg="#c0392b", fg="white", 
            font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2",
            padx=15, pady=5,
            command=self.cancelar_reserva
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            frame_botones, 
            text="↻ Actualizar", 
            bg="#ecf0f1", fg="#2c3e50", 
            font=("Segoe UI", 9), relief="flat", cursor="hand2",
            padx=10, pady=5,
            command=self.cargar_datos_reales
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            frame_botones, 
            text="Cerrar", 
            bg="#95a5a6", fg="white", 
            font=("Segoe UI", 9), relief="flat", cursor="hand2",
            padx=10, pady=5,
            command=self.destroy
        ).pack(side=tk.RIGHT)

        self.cargar_datos_reales()

    def cargar_datos_reales(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            mis_reservas = self.repo.obtener_por_cliente(self.usuario.id)
            for reserva in mis_reservas:
                self.tree.insert("", tk.END, values=reserva)
        except Exception as e:
            print(f"No se pudieron cargar las reservas: {e}")
            messagebox.showerror("Error", "Ocurrió un error al cargar tus reservas.", parent=self)

    def cancelar_reserva(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Selecciona el viaje que deseas cancelar.", parent=self)
            return

        item = self.tree.item(selected)
        id_reserva = item['values'][0] 
        estado_actual = item['values'][3] 

        if estado_actual == "Cancelada":
            messagebox.showinfo("Información", "Esta reserva ya se encuentra cancelada.", parent=self)
            return

        if messagebox.askyesno("Confirmar Cancelación", "¿Estás seguro de que deseas cancelar este viaje?", parent=self):
            try:
                self.repo.cambiar_estado(id_reserva, "Cancelada")
                messagebox.showinfo("Éxito", "Tu reserva ha sido cancelada.", parent=self)
                self.cargar_datos_reales() 
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cancelar: {e}", parent=self)