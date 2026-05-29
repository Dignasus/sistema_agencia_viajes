from utils.password_encryptor import PasswordEncryptor
from negocio.models.cliente import Cliente

class AuthService:
    def __init__(self, usuario_repository):
        self.repo = usuario_repository

    def login(self, email, password_plana):
        # (Este método queda igual)
        usuario = self.repo.obtener_por_email(email)
        if not usuario:
            return None, "Usuario no encontrado."
        if PasswordEncryptor.verify_password(password_plana, usuario.contrasena):
            return usuario, "Inicio de sesión exitoso."
        else:
            return None, "Contraseña incorrecta."

    def registrar_cliente(self, nombre, apellido, email, contrasena, direccion, telefono):
        # Verificar duplicados
        if self.repo.obtener_por_email(email):
            raise ValueError("El correo ya está registrado.")
        
        # Guardar
        nuevo_cliente = Cliente(0, nombre, apellido, email, contrasena, direccion, telefono, False)
        self.repo.crear(nuevo_cliente)
        
        return True, "Registro exitoso."