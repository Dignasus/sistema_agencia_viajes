from negocio.services.auth_service import AuthService
from persistencia.repositorio.usuarios_repo import UsuarioRepository

class AuthController:
    def __init__(self):
        self.repo = UsuarioRepository()
        self.service = AuthService(self.repo)
        self.usuario_actual = None

    def autenticar(self, email, password):
        # Delegamos la lógica al servicio
        usuario, mensaje = self.service.login(email, password)
        
        if usuario:
            self.usuario_actual = usuario
            return usuario
        else:
            # Lanzamos error para que la Vista muestre la alerta roja
            raise ValueError(mensaje)

    def registrar_cliente(self, nombre, apellido, email, password, direccion, telefono):
        try:
            return self.service.registrar_cliente(nombre, apellido, email, password, direccion, telefono)
        except ValueError as e:
            raise ValueError(str(e))
    
    def get_usuario_actual(self):
        return self.usuario_actual