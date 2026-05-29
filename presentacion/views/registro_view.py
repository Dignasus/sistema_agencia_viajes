import tkinter as tk
from tkinter import messagebox

class RegistroView(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.master = master
        
        # 1. Configuración de la Ventana Principal
        self.master.title("Crear Nueva Cuenta - Viajes Aventura")
        self.master.geometry("1000x650") 
        self.master.resizable(False, False)
        
        # Nos empaquetamos para llenar la ventana
        self.pack(fill="both", expand=True)

        # PALETA DE COLORES (Idéntica al Login)
        COLOR_SIDEBAR = "#2c3e50"
        COLOR_TEXT_SIDEBAR = "white"
        COLOR_FONDO_DERECHA = "#f3f4f6"
        COLOR_BOTON = "#2980b9"
        COLOR_LABEL = "#7f8c8d"
        FONT_LABEL = ("Segoe UI", 9, "bold")
        FONT_ENTRY = ("Segoe UI", 11)

        
        # 2. PANEL IZQUIERDO (BRANDING)
        
        self.sidebar = tk.Frame(self, bg=COLOR_SIDEBAR, width=280)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False) 

        self.brand_frame = tk.Frame(self.sidebar, bg=COLOR_SIDEBAR)
        self.brand_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            self.brand_frame, 
            text="VIAJES", 
            bg=COLOR_SIDEBAR, 
            fg=COLOR_TEXT_SIDEBAR, 
            font=("Helvetica", 32, "bold")
        ).pack()
        
        tk.Label(
            self.brand_frame, 
            text="AVENTURA", 
            bg=COLOR_SIDEBAR, 
            fg="#bdc3c7", 
            font=("Helvetica", 18, "bold")
        ).pack(pady=(5, 0))
        
        tk.Label(
            self.brand_frame, 
            text="Únete a la experiencia", 
            bg=COLOR_SIDEBAR, 
            fg="#95a5a6", 
            font=("Segoe UI", 12)
        ).pack(pady=(30, 0))

        
        # 3. PANEL DERECHO (FORMULARIO)
        
        self.main_area = tk.Frame(self, bg=COLOR_FONDO_DERECHA, padx=40, pady=40)
        self.main_area.pack(side="right", fill="both", expand=True)

        # Títulos
        tk.Label(
            self.main_area, 
            text="Crear Cuenta", 
            bg=COLOR_FONDO_DERECHA, 
            fg="#333333", 
            font=("Segoe UI", 24, "bold")
        ).pack(anchor="w")
        
        tk.Label(
            self.main_area, 
            text="Completa tus datos para registrarte", 
            bg=COLOR_FONDO_DERECHA, 
            fg=COLOR_LABEL, 
            font=("Segoe UI", 11)
        ).pack(anchor="w", pady=(0, 20))

        # FRAME INTERNO PARA LOS CAMPOS (GRID)
        form_frame = tk.Frame(self.main_area, bg=COLOR_FONDO_DERECHA)
        form_frame.pack(fill="both", expand=True)
        
        # Configuración de columnas
        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=1)
        
        PAD_X = 15
        PAD_Y = (5, 20) # (arriba, abajo)

        # Columna izquierda
        
        # Nombre
        tk.Label(form_frame, text="NOMBRE", bg=COLOR_FONDO_DERECHA, fg=COLOR_LABEL, font=FONT_LABEL).grid(row=0, column=0, sticky="w", padx=(0, PAD_X))
        self.entry_nombre = tk.Entry(form_frame, font=FONT_ENTRY, bd=0, bg="white", relief="flat")
        self.entry_nombre.grid(row=1, column=0, sticky="ew", ipady=8, padx=(0, PAD_X), pady=PAD_Y)

        # Apellido
        tk.Label(form_frame, text="APELLIDO", bg=COLOR_FONDO_DERECHA, fg=COLOR_LABEL, font=FONT_LABEL).grid(row=0, column=1, sticky="w", padx=(PAD_X, 0))
        self.entry_apellido = tk.Entry(form_frame, font=FONT_ENTRY, bd=0, bg="white", relief="flat")
        self.entry_apellido.grid(row=1, column=1, sticky="ew", ipady=8, padx=(PAD_X, 0), pady=PAD_Y)

        # Email
        tk.Label(form_frame, text="CORREO ELECTRÓNICO", bg=COLOR_FONDO_DERECHA, fg=COLOR_LABEL, font=FONT_LABEL).grid(row=2, column=0, sticky="w", padx=(0, PAD_X))
        self.entry_email = tk.Entry(form_frame, font=FONT_ENTRY, bd=0, bg="white", relief="flat")
        self.entry_email.grid(row=3, column=0, sticky="ew", ipady=8, padx=(0, PAD_X), pady=PAD_Y)

        # Contraseña
        tk.Label(form_frame, text="CONTRASEÑA", bg=COLOR_FONDO_DERECHA, fg=COLOR_LABEL, font=FONT_LABEL).grid(row=2, column=1, sticky="w", padx=(PAD_X, 0))
        self.entry_pass = tk.Entry(form_frame, font=FONT_ENTRY, show="•", bd=0, bg="white", relief="flat")
        self.entry_pass.grid(row=3, column=1, sticky="ew", ipady=8, padx=(PAD_X, 0), pady=PAD_Y)

        # Dirección
        tk.Label(form_frame, text="DIRECCIÓN", bg=COLOR_FONDO_DERECHA, fg=COLOR_LABEL, font=FONT_LABEL).grid(row=4, column=0, sticky="w", padx=(0, PAD_X))
        self.entry_direccion = tk.Entry(form_frame, font=FONT_ENTRY, bd=0, bg="white", relief="flat")
        self.entry_direccion.grid(row=5, column=0, sticky="ew", ipady=8, padx=(0, PAD_X), pady=PAD_Y)

        # Teléfono
        tk.Label(form_frame, text="TELÉFONO", bg=COLOR_FONDO_DERECHA, fg=COLOR_LABEL, font=FONT_LABEL).grid(row=4, column=1, sticky="w", padx=(PAD_X, 0))
        self.entry_telefono = tk.Entry(form_frame, font=FONT_ENTRY, bd=0, bg="white", relief="flat")
        self.entry_telefono.grid(row=5, column=1, sticky="ew", ipady=8, padx=(PAD_X, 0), pady=PAD_Y)

        
        # 4. BOTONES
        
        btn_frame = tk.Frame(self.main_area, bg=COLOR_FONDO_DERECHA)
        btn_frame.pack(fill="x", pady=(20, 0))

        # Botón GUARDAR (Azul fuerte)
        self.btn_guardar = tk.Button(
            btn_frame,
            text="REGISTRARME",
            font=("Segoe UI", 11, "bold"),
            bg=COLOR_BOTON,
            fg="white",
            activebackground="#1a5276",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=20, pady=10,
            command=self.guardar_usuario
        )
        self.btn_guardar.pack(side="right")

        # Botón VOLVER (Gris suave)
        self.btn_volver = tk.Button(
            btn_frame,
            text="Volver",
            font=("Segoe UI", 10),
            bg="#bdc3c7", # Gris
            fg="#2c3e50", # Texto oscuro
            activebackground="#95a5a6",
            relief="flat",
            cursor="hand2",
            padx=15, pady=10,
            command=self.volver_login
        )
        self.btn_volver.pack(side="right", padx=(0, 15))

    def guardar_usuario(self):
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        direccion = self.entry_direccion.get()
        telefono = self.entry_telefono.get()
        email = self.entry_email.get()
        contraseña = self.entry_pass.get()

        if nombre and apellido and email and contraseña:
            try:
                # Llamamos al controlador
                self.controller.registrar_cliente(nombre, apellido, email, contraseña, direccion, telefono)
                
                # IMPORTANTE: parent=self para que no salga la ventana fantasma
                messagebox.showinfo("Éxito", "Usuario registrado correctamente", parent=self)
                self.volver_login()
                
            except ValueError as error:
                messagebox.showwarning("Error de Registro", str(error), parent=self)
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}", parent=self)
        else:
            messagebox.showwarning("Faltan datos", "Todos los campos son obligatorios", parent=self)

    def volver_login(self):
        # 1. Limpiamos la ventana raíz
        root = self.master
        for widget in root.winfo_children():
            widget.destroy()

        # 2. Cargamos el Login de nuevo
        from presentacion.views.login_view import LoginView
        LoginView(root, self.controller)