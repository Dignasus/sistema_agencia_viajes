from database.db_connection import conectar
from negocio.models.usuario import Usuario
from negocio.models.administrador import Administrador
from negocio.models.cliente import Cliente


class UsuarioRepository:

    # -------------------------
    # CREAR
    # -------------------------
    def crear(self, usuario: Usuario):
        conn = conectar("agencia_viajes")
        cursor = conn.cursor()

        sql = """
        INSERT INTO usuarios 
        (nombre, apellido, email, telefono, direccion, contraseña_hash, rol)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        valores = (
            usuario.nombre,
            usuario.apellido,
            usuario.email,
            usuario.telefono,
            usuario.direccion,
            usuario.contrasena,
            usuario.rol
        )

        cursor.execute(sql, valores)
        conn.commit()

        usuario.id = cursor.lastrowid  # asignar ID al modelo

        cursor.close()
        conn.close()
        return usuario

    # -------------------------
    # LEER - por id
    # -------------------------
    def obtener_por_id(self, id_usuario: int):
        conn = conectar("agencia_viajes")
        cursor = conn.cursor()

        sql = """
        SELECT id, nombre, email, telefono, direccion, contraseña_hash, rol
        FROM usuarios WHERE id = %s
        """

        cursor.execute(sql, (id_usuario,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return Usuario(*row)  # mapeo automático
        return None

    # -------------------------
    # LEER - por email (login)
    # -------------------------
    def obtener_por_email(self, email):
        conn = conectar("agencia_viajes")
        cursor = conn.cursor()

        sql = """
        SELECT id, nombre, email, telefono, direccion, contraseña_hash, rol
        FROM usuarios WHERE email = %s
        """
        cursor.execute(sql, (email,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            # Desempaquetamos los datos de la BD
            id_u, nom, mail, tel, dire, pas, rol = row
            
            #Decidir qué clase instanciar
            if rol == "admin":
                # Asumimos apellido vacío "" si no está en tu consulta SQL
                return Administrador(id_u, nom, "", mail, pas, dire, tel, True)
            else:
                return Cliente(id_u, nom, "", mail, pas, dire, tel, True)
        
        return None

    # -------------------------
    # LEER - todos
    # -------------------------
    def obtener_todos(self):
        conn = conectar("agencia_viajes")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id, nombre, email, telefono, direccion, contraseña_hash, rol
        FROM usuarios
        """)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return [Usuario(*row) for row in rows]

    # -------------------------
    # ACTUALIZAR
    # -------------------------
    def actualizar(self, usuario: Usuario):
        conn = conectar("agencia_viajes")
        cursor = conn.cursor()

        sql = """
        UPDATE usuarios
        SET nombre=%s, email=%s, telefono=%s, direccion=%s,
            contraseña_hash=%s, rol=%s
        WHERE id=%s
        """

        valores = (
            usuario.nombre,
            usuario.email,
            usuario.telefono,
            usuario.direccion,
            usuario.contraseña,
            usuario.rol,
            usuario.id
        )

        cursor.execute(sql, valores)
        conn.commit()

        cursor.close()
        conn.close()

    # -------------------------
    # ELIMINAR
    # -------------------------
    def eliminar(self, id_usuario: int):
        conn = conectar("agencia_viajes")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM usuarios WHERE id=%s", (id_usuario,))
        conn.commit()

        cursor.close()
        conn.close()
