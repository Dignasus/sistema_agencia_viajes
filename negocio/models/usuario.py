from abc import ABC
from utils.password_encryptor import PasswordEncryptor
import re

class Usuario(ABC):
    def __init__(self, id_usuario, nombre, apellido, email, contrasena, rol, direccion, telefono, hashed = False):
        self._id_usuario = id_usuario
        self._nombre = nombre
        self._apellido = apellido
        self._email = email
        if hashed:
            self._contrasena = contrasena
        else: 
            self._contrasena = self.verificar_contrasena(contrasena)
        self._rol = rol
        self._direccion = direccion
        self._telefono = telefono

    @property
    def es_admin(self):
        return self._rol == "admin"

    @staticmethod
    def verificar_contrasena(contrasena):

        # Validar longitud
        if len(contrasena) < 8:
            raise ValueError("La contraseña es muy débil: debe tener al menos 8 caracteres.")
        # Validar que tenga números
        elif not re.search(r"\d", contrasena):
            raise ValueError("La contraseña debe incluir al menos un número (0-9).")
        # Validar que tenga mayúsculas (Opcional, pero recomendado)
        elif not re.search(r"[A-Z]", contrasena):
            raise ValueError("La contraseña debe incluir al menos una letra mayúscula.")
        else: 
            return PasswordEncryptor.hash_password(contrasena)

    @property
    def id(self):
        return self._id_usuario

    @id.setter
    def id(self, valor):
        self._id_usuario = valor

    @property
    def id_usuario(self): 
        return self._id_usuario

    @property
    def nombre(self):
        return self._nombre

    @property
    def apellido(self):
        return self._apellido
    
    @property
    def email(self):
        return self._email

    @property
    def contrasena(self):
        return self._contrasena

    @property
    def rol(self):
        return self._rol
        
    @property
    def direccion(self):
        return self._direccion

    @property
    def telefono(self):
        return self._telefono