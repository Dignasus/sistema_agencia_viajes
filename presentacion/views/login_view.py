import tkinter as tk
from tkinter import messagebox

class LoginView(tk.Frame):
    def __init__(self, master, controller, reserva_controller=None):
        super().__init__(master)
        self.controller = controller
        self.reserva_controller = reserva_controller
        self.master = master
        
        # Configuración de la ventana principal
        self.master.geometry("1000x600") 
        self.master.resizable(False, False)
        self.master.title("Viajes Aventura - Acceso")
        
        # Configuración del frame actual
        self.pack(fill="both", expand=True)

        # COLORES
        COLOR_SIDEBAR = "#2c3e50"
        COLOR_TEXT_SIDEBAR = "white"
        COLOR_FONDO_DERECHA = "#f3f4f6"
        COLOR_BOTON = "#2980b9"
        
        
        # 1. PANEL IZQUIERDO (BRANDING)
        
        self.sidebar = tk.Frame(self, bg=COLOR_SIDEBAR, width=280)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False) 

        self.brand_frame = tk.Frame(self.sidebar, bg=COLOR_SIDEBAR)
        self.brand_frame.place(relx=0.5, rely=0.5, anchor="center")

        lbl_brand_1 = tk.Label(self.brand_frame, text="VIAJES", bg=COLOR_SIDEBAR, fg=COLOR_TEXT_SIDEBAR, font=("Helvetica", 28, "bold"))
        lbl_brand_1.pack()

        lbl_brand_2 = tk.Label(self.brand_frame, text="AVENTURA", bg=COLOR_SIDEBAR, fg="#bdc3c7", font=("Helvetica", 16, "bold"))
        lbl_brand_2.pack(pady=(5, 0))

        
        # 2. PANEL DERECHO (FORMULARIO)
        
        self.main_area = tk.Frame(self, bg=COLOR_FONDO_DERECHA)
        self.main_area.pack(side="right", fill="both", expand=True)

        self.form_frame = tk.Frame(self.main_area, bg=COLOR_FONDO_DERECHA)
        self.form_frame.place(relx=0.5, rely=0.5, anchor="center", width=350)

        # Títulos
        lbl_bienvenido = tk.Label(self.form_frame, text="Bienvenido", bg=COLOR_FONDO_DERECHA, fg="#333333", font=("Segoe UI", 24, "bold"))
        lbl_bienvenido.pack(pady=(0, 10), anchor="w")

        lbl_subtitulo = tk.Label(self.form_frame, text="Ingresa tus credenciales para continuar", bg=COLOR_FONDO_DERECHA, fg="#7f8c8d", font=("Segoe UI", 10))
        lbl_subtitulo.pack(pady=(0, 30), anchor="w")

        # INPUT EMAIL
        tk.Label(self.form_frame, text="CORREO ELECTRÓNICO", bg=COLOR_FONDO_DERECHA, fg="#7f8c8d", font=("Segoe UI", 8, "bold"), anchor="w").pack(fill="x")
        
        self.entry_email = tk.Entry(self.form_frame, font=("Segoe UI", 11), bd=0, bg="white", relief="flat")
        self.entry_email.pack(fill="x", ipady=8, pady=(5, 15))
        
        tk.Frame(self.form_frame, bg="#dcdcdc", height=1).pack(fill="x", pady=(0, 15))

        # INPUT PASSWORD
        tk.Label(self.form_frame, text="CONTRASEÑA", bg=COLOR_FONDO_DERECHA, fg="#7f8c8d", font=("Segoe UI", 8, "bold"), anchor="w").pack(fill="x")

        self.entry_password = tk.Entry(self.form_frame, font=("Segoe UI", 11), show="•", bd=0, bg="white", relief="flat")
        self.entry_password.pack(fill="x", ipady=8, pady=(5, 15))
        
        tk.Frame(self.form_frame, bg="#dcdcdc", height=1).pack(fill="x", pady=(0, 25))

        # BOTÓN INGRESAR
        self.btn_login = tk.Button(
            self.form_frame,
            text="INICIAR SESIÓN",
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_BOTON,
            fg="white",
            activebackground="#1a5276",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.validar_login
        )
        self.btn_login.pack(fill="x", ipady=8)

        # BOTÓN REGISTRARSE
        self.btn_registro = tk.Button(
            self.form_frame,
            text="¿No tienes cuenta? Regístrate aquí",
            font=("Segoe UI", 9),
            bg=COLOR_FONDO_DERECHA,
            fg="#2980b9",
            activebackground=COLOR_FONDO_DERECHA,
            activeforeground="#1a5276",
            relief="flat",
            cursor="hand2",
            command=self.ir_a_registro
        )
        self.btn_registro.pack(fill="x", pady=(15, 0))

    def validar_login(self):
        usuario_input = self.entry_email.get()
        password_input = self.entry_password.get()

        try:
            usuario = self.controller.autenticar(usuario_input, password_input)
            if usuario:
                from presentacion.views.main_menu_view import MainMenuView
                
                # Limpiamos la ventana raíz de forma segura
                root = self.master
                for widget in root.winfo_children():
                    widget.destroy()
                
                # Cargamos el menú
                MainMenuView(root, usuario, self.controller, self.reserva_controller)
            else:
                messagebox.showerror("Acceso Denegado", "Usuario o contraseña incorrectos.", parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}", parent=self)

    def ir_a_registro(self):
        # Lógica para ir a la pantalla de registro
        try:
            # Importamos aquí para evitar errores circulares
            from presentacion.views.registro_view import RegistroView 
            
            # Limpiamos la ventana actual
            root = self.master
            for widget in root.winfo_children():
                widget.destroy()
                
            # Cargamos la vista de registro
            # Nota: RegistroView necesita (master, controller) usualmente
            RegistroView(root, self.controller)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el registro: {e}", parent=self)