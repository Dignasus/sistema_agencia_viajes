import tkinter as tk
from tkinter import messagebox
# Importamos las vistas necesarias
from presentacion.views.gestion_paquetes_view import GestionPaquetesView
from presentacion.views.paquetes_clientes_view import PaquetesClientesView
from presentacion.views.reservas_admin_view import ReservasAdminView
from presentacion.views.reservas_cliente_view import ReservasClienteView
from presentacion.views.reserva_view import ReservaView

# CAMBIO 1: Heredamos de Frame, no de Tk
class MainMenuView(tk.Frame):

    def __init__(self, parent, usuario, controller, reserva_controller):
        # CAMBIO 2: Pasamos el parent al constructor del Frame
        super().__init__(parent)
        self.usuario = usuario
        self.controller = controller
        self.reserva_controller = reserva_controller 
        self.master = parent # Guardamos la referencia a la ventana raíz
        
        # Nos empaquetamos para llenar la ventana
        self.pack(fill="both", expand=True)
        
        # CONFIGURACIÓN DE VENTANA (Usamos self.master porque somos un Frame)
        self.master.title(f"Agencia de Viajes - Bienvenido {usuario.nombre}")
        self.master.geometry("1000x650")
        self.configure(bg="#ECF0F1") 
        
        # Estilos (Colores)
        self.COLOR_BARRA = "#2C3E50"      # Azul Oscuro
        self.COLOR_HEADER = "#FFFFFF"     # Blanco
        self.COLOR_BTN = "#3498DB"        # Azul
        self.COLOR_BTN_HOVER = "#2980B9"  # Azul oscuro
        self.COLOR_TEXTO = "#333333"

        # LAYOUT PRINCIPAL
        
        # 1. BARRA LATERAL (Izquierda)
        self.sidebar = tk.Frame(self, bg=self.COLOR_BARRA, width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # Logo / Título
        tk.Label(
            self.sidebar, 
            text="AGENCIA", 
            bg=self.COLOR_BARRA, 
            fg="white", 
            font=("Segoe UI", 20, "bold")
        ).pack(pady=(40, 10))
        
        tk.Label(
            self.sidebar, 
            text="DE VIAJES", 
            bg=self.COLOR_BARRA, 
            fg="#BDC3C7", 
            font=("Segoe UI", 12)
        ).pack(pady=(0, 40))

        # 2. ÁREA DE CONTENIDO (Derecha)
        self.content = tk.Frame(self, bg="#ECF0F1")
        self.content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Encabezado Superior
        self.header = tk.Frame(self.content, bg=self.COLOR_HEADER, height=80)
        self.header.pack(fill=tk.X, padx=20, pady=20)
        self.header.pack_propagate(False)

        # Texto de Bienvenida
        rol_texto = "Administrador" if self.usuario.es_admin else "Cliente"
        
        tk.Label(
            self.header, 
            text=f"Hola, {self.usuario.nombre}", 
            bg=self.COLOR_HEADER, 
            fg=self.COLOR_TEXTO,
            font=("Segoe UI", 18, "bold")
        ).pack(side=tk.LEFT, padx=20)
        
        tk.Label(
            self.header, 
            text=f"Rol: {rol_texto}", 
            bg=self.COLOR_HEADER, 
            fg="#7F8C8D",
            font=("Segoe UI", 10, "italic")
        ).pack(side=tk.LEFT, padx=5, pady=5)

        # Botón Cerrar Sesión
        btn_logout = tk.Button(
            self.header, 
            text="Cerrar Sesión", 
            bg="#E74C3C", 
            fg="white", 
            font=("Segoe UI", 9, "bold"), 
            relief="flat", 
            padx=15, pady=5,
            command=self.cerrar_sesion, 
            cursor="hand2"
        )
        btn_logout.pack(side=tk.RIGHT, padx=20)

        # BOTONES DEL MENÚ
        self.crear_menu_opciones()

    def crear_menu_opciones(self):
        menu_frame = tk.Frame(self.sidebar, bg=self.COLOR_BARRA)
        menu_frame.pack(fill=tk.X, padx=20)

        if self.usuario.es_admin:
            self.crear_boton_menu(menu_frame, " Gestionar Paquetes", self.abrir_gestion_paquetes)
            self.crear_boton_menu(menu_frame, " Ver Todas las Reservas", self.abrir_reservas_admin)
        else:
            self.crear_boton_menu(menu_frame, " Ver Catálogo / Reservar", self.crear_reserva)
            self.crear_boton_menu(menu_frame, " Crear Paquete Propio", self.abrir_catalogo)
            self.crear_boton_menu(menu_frame, " Mis Reservas", self.abrir_mis_reservas)

        # Info pie de página
        tk.Label(self.sidebar, text="v1.0.0", bg=self.COLOR_BARRA, fg="#7F8C8D", 
                 font=("Arial", 8)).pack(side=tk.BOTTOM, pady=20)

    def crear_boton_menu(self, parent, texto, comando):
        btn = tk.Button(
            parent, 
            text=texto, 
            bg=self.COLOR_BTN, 
            fg="white", 
            font=("Segoe UI", 11), 
            relief="flat", 
            bd=0,
            padx=20, pady=10, 
            cursor="hand2", 
            anchor="w",
            command=comando
        )
        btn.pack(fill=tk.X, pady=5)
        
        # Efecto Hover
        btn.bind("<Enter>", lambda e: btn.config(bg=self.COLOR_BTN_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.COLOR_BTN))

    # MÉTODOS DE ACCIÓN
    def cerrar_sesion(self):
        if messagebox.askyesno("Salir", "¿Deseas cerrar sesión?", parent=self):
            # Limpiamos la ventana raíz de forma segura
            root = self.winfo_toplevel()
            controller_temp = self.controller # Guardamos el auth controller
            
            for widget in root.winfo_children():
                widget.destroy()
            
            # Volvemos al Login
            from presentacion.views.login_view import LoginView
            LoginView(root, controller_temp)

    def abrir_gestion_paquetes(self):
        GestionPaquetesView(self, self.usuario)

    def abrir_reservas_admin(self):
        ReservasAdminView(self, self.usuario)

    def crear_reserva(self):
        # Aquí pasamos el reserva_controller correctamente
        if self.reserva_controller:
            ReservaView(self, self.usuario, self.reserva_controller)
        else:
            messagebox.showerror("Error", "Error de conexión: Controlador de reservas no encontrado.", parent=self)

    def abrir_catalogo(self):
        PaquetesClientesView(self, self.usuario)

    def abrir_mis_reservas(self):
        ReservasClienteView(self, self.usuario)