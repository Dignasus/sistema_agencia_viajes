import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import date
from persistencia.repositorio.paquete_repo import PaqueteRepo 

class ReservaView(tk.Toplevel):
    def __init__(self, parent, usuario, controller):
        super().__init__(parent)
        self.usuario = usuario
        self.controller = controller
        
        self.title("Nueva Reserva - Catálogo de Viajes")
        self.geometry("1100x650")
        self.configure(bg="#f3f4f6")

        self.header_frame = tk.Frame(self, bg="#2c3e50", height=80)
        self.header_frame.pack(fill="x")
        
        tk.Label(
            self.header_frame, 
            text="EXPLORA NUESTROS DESTINOS", 
            bg="#2c3e50", 
            fg="white",
            font=("Helvetica", 18, "bold")
        ).pack(pady=20)

        table_frame = tk.Frame(self, bg="white", padx=20, pady=20)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            table_frame, 
            text="Selecciona el paquete que deseas reservar:", 
            bg="white", fg="#7f8c8d", font=("Segoe UI", 10, "italic")
        ).pack(anchor="w", pady=(0, 10))

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

        columns = ("ID", "Paquete", "Precio", "Fecha Inicio", "Fecha Fin", "Tipo")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Paquete", text="PAQUETE TURÍSTICO")
        self.tree.heading("Precio", text="PRECIO")
        self.tree.heading("Fecha Inicio", text="FECHA INICIO")
        self.tree.heading("Fecha Fin", text="FECHA FIN")
        self.tree.heading("Tipo", text="TIPO")
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Paquete", width=300)
        self.tree.column("Precio", width=120, anchor="e")
        self.tree.column("Fecha Inicio", width=100, anchor="center")
        self.tree.column("Fecha Fin", width=100, anchor="center")
        self.tree.column("Tipo", width=100, anchor="center")
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.cargar_datos()

        footer_frame = tk.Frame(self, bg="white", pady=15, padx=20)
        footer_frame.pack(fill="x", side="bottom")

        tk.Button(
            footer_frame, 
            text="✓ CONFIRMAR RESERVA", 
            bg="#27ae60", fg="white", 
            font=("Segoe UI", 11, "bold"), relief="flat", cursor="hand2",
            padx=20, pady=8,
            command=self.guardar_reserva
        ).pack(side="right", padx=10)

        tk.Button(
            footer_frame, 
            text="Volver al Menú", 
            bg="#95a5a6", fg="white", 
            font=("Segoe UI", 10), relief="flat", cursor="hand2",
            padx=15, pady=8,
            command=self.destroy
        ).pack(side="right")

    def cargar_datos(self):
        try:
            repo = PaqueteRepo() 
            datos = repo.obtener_todos() 
            
            for p in datos:
                precio_fmt = f"${p.precio_total:,.0f}" if isinstance(p.precio_total, (int, float)) else p.precio_total

                self.tree.insert("", tk.END, values=(
                    p.id_paquete,
                    p.nombre_paquete,
                    precio_fmt,
                    p.fecha_inicio,
                    p.fecha_fin,
                    p.tipo
                ))
        except Exception as e:
            print(f"Error al cargar paquetes: {e}")
            messagebox.showerror("Error", "No se pudo cargar el catálogo.", parent=self)

    def guardar_reserva(self):
        seleccionado = self.tree.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Por favor, selecciona un paquete de la lista para reservar.", parent=self)
            return

        values = self.tree.item(seleccionado, "values")
        id_paquete = values[0]
        nombre_paquete = values[1]

        if messagebox.askyesno("Confirmar Reserva", f"¿Estás seguro de que deseas reservar el paquete '{nombre_paquete}'?", parent=self):
            hoy = date.today()
            try:
                self.controller.crear_reserva(self.usuario.id, id_paquete, hoy, "Reservado")
                messagebox.showinfo("¡Felicidades!", "Tu reserva ha sido creada exitosamente.", parent=self)
                self.destroy() 
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo procesar la reserva: {e}", parent=self)