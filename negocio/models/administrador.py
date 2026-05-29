from negocio.models.usuario import Usuario

class Administrador(Usuario):
    def __init__(self, id_usuario, nombre, apellido, email, contraseña, direccion, telefono, hashed):
        super().__init__(id_usuario, nombre, apellido, email, contraseña, "admin", direccion, telefono, hashed)

