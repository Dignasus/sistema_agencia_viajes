from database.db_connection import conectar
from negocio.models.destinos import Destino 

class DestinoRepository:

    # Crear destino
    def crear(self, destino: Destino):
        conn = conectar("agencia_viajes")
        cursor = conn.cursor()
        sql = """
        INSERT INTO destinos (
            nombre, descripcion, actividades, costo_base
        )
        VALUES (%s, %s, %s, %s)
        """

        valores = (
            destino.nombre,
            destino.descripcion,
            destino.actividades,
            destino.costo_base,
        )

        cursor.execute(sql, valores)
        conn.commit()

        destino.id_destino = cursor.lastrowid

        cursor.close()
        conn.close()

        return destino

    # Obtener por id
    def obtener_por_id(self, id_destino):
        conn = conectar("agencia_viajes")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_destino, nombre, descripcion, actividades, costo_base
            FROM destinos
            WHERE id_destino = %s
        """, (id_destino,))

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if not row:
            return None

        return Destino(*row)

    # Obtener todos
    def obtener_todos(self):
        conn = conectar("agencia_viajes")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_destino, nombre, descripcion, actividades, costo_base
            FROM destinos
        """)

        rows = cursor.fetchall()
        
        # Convertimos las tuplas en OBJETOS
        destinos = []
        for row in rows:
            try:
                destino = Destino(*row)
                destinos.append(destino)
            except Exception as e:
                print(f"[ERROR Repo] No se pudo convertir destino: {e}")

        cursor.close()
        conn.close()

        return destinos # Devolvemos lista de objetos

    # Buscar por nombre
    def buscar_por_nombre(self, texto):
        conn = conectar("agencia_viajes")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_destino, nombre, descripcion, actividades, costo_base
            FROM destinos
            WHERE nombre LIKE %s
        """, (f"%{texto}%",))

        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        return [Destino(*row) for row in rows]

    # Actualizar Destino
    def actualizar(self, destino: Destino):
        conn = conectar("agencia_viajes")
        cursor = conn.cursor()

        sql = """
        UPDATE destinos
        SET nombre = %s,
            descripcion = %s,
            actividades = %s,
            costo_base = %s
        WHERE id_destino = %s
        """

        valores = (
            destino.nombre,
            destino.descripcion,
            destino.actividades,
            destino.costo_base,
            destino.id_destino
        )

        cursor.execute(sql, valores)
        conn.commit()

        cursor.close()
        conn.close()

    # Eliminar destino
    def eliminar(self, id_destino):
        conn = conectar("agencia_viajes")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM destinos WHERE id_destino = %s", (id_destino,))
        conn.commit()

        cursor.close()
        conn.close()