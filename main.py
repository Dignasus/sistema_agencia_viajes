import tkinter as tk
from presentacion.controllers.auth_controller import AuthController
from presentacion.controllers.reserva_controller import ReservaController
from presentacion.views.login_view import LoginView
from database.db_connection import crear_bd, crear_tablas, crear_admin_por_defecto, crear_paquetes_iniciales, crear_destinos_iniciales


def main():
    try:
        print("Verificar la base de datos")
        crear_bd()
        crear_tablas()
        crear_admin_por_defecto()
        crear_paquetes_iniciales()
        crear_destinos_iniciales()
        print("Base de datos Creada y Verificada correctamente.")
    except Exception as e:
        print(f"Error al conectar con la Base de Datos: {e}")

    root = tk.Tk()
    root.title("Viajes Aventura - Gestión")
    root.geometry("600x450")
    
    auth_controller = AuthController()
    reserva_controller = ReservaController()
    app = LoginView(root, auth_controller, reserva_controller)
    app.pack(expand=True, fill="both")

    root.mainloop()

if __name__ == "__main__":
    main()