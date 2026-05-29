from database.db_connection import conectar
from negocio.models.reserva import Reserva

class ReservaRepository:

    # Crear reserva
    def crear(self, reserva: Reserva):
        conn = conectar("agencia_viajes")
        cursor = conn.cursor()
        sql = """
        INSERT INTO reservas (
            id_cliente, id_paquete, fecha_reserva,
            estado
        )
        VALUES (%s, %s, %s, %s)
        """

        valores = (
            reserva.id_cliente,
            reserva.id_paquete,
            reserva.fecha_reserva,
            reserva.estado
        )

        cursor.execute(sql, valores)
        conn.commit()

        reserva.id_reserva = cursor.lastrowid

        cursor.close()
        conn.close()
        return reserva

    # -Obtener por cliente
    def obtener_por_cliente(self, id_cliente):
        conn = conectar("agencia_viajes")
        cursor = conn.cursor()

        # Hacemos JOIN con la tabla 'paquetes' para traer el nombre real
        sql = """
            SELECT 
                r.id_reserva, 
                p.nombre_paquete, 
                r.fecha_reserva, 
                r.estado
            FROM reservas r
            JOIN paquetes p ON r.id_paquete = p.id_paquete
            WHERE r.id_cliente = %s
            ORDER BY r.id_reserva DESC
        """

        try:
            cursor.execute(sql, (id_cliente,))
            rows = cursor.fetchall()
        except Exception as e:
            print(f"Error SQL al obtener reservas: {e}")
            rows = []

        cursor.close()
        conn.close()

        return rows

    # Obtener por id
    def obtener_por_id(self, id_reserva):
        conn = conectar("agencia_viajes")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id_reserva, id_cliente, id_paquete, fecha_reserva,
                   cantidad_personas, estado
            FROM reservas
            WHERE id_reserva = %s
        """, (id_reserva,))

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if not row:
            return None

        return Reserva(*row)

    # Obtener todas
    def obtener_todas(self):
        conn = conectar("agencia_viajes")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id_reserva, id_cliente, id_paquete, fecha_reserva,
                   cantidad_personas, estado
            FROM reservas
        """)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return [Reserva(*row) for row in rows]
    
    def obtener_todas_detalladas(self):
        conn = conectar("agencia_viajes")
        cursor = conn.cursor()

        # CORRECCIÓN: Cambiamos 'u.id_usuario' por 'u.id'
        # (Asumiendo que la llave primaria de usuarios es 'id')
        sql = """
            SELECT 
                r.id_reserva, 
                u.nombre, 
                p.nombre_paquete, 
                r.fecha_reserva, 
                r.estado
            FROM reservas r
            JOIN usuarios u ON r.id_cliente = u.id  -- <--- CAMBIO AQUÍ (u.id)
            JOIN paquetes p ON r.id_paquete = p.id_paquete
            ORDER BY r.id_reserva DESC
        """

        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
        except Exception as e:
            print(f"Error SQL Admin: {e}")
            rows = []

        cursor.close()
        conn.close()
        return rows

    # Actualizar
    def actualizar(self, reserva: Reserva):
        conn = conectar("agencia_viajes")
        cursor = conn.cursor()

        sql = """
        UPDATE reservas
        SET id_cliente = %s,
            id_paquete = %s,
            fecha_reserva = %s,
            cantidad_personas = %s,
            estado = %s
        WHERE id_reserva = %s
        """

        valores = (
            reserva.id_cliente,
            reserva.id_paquete,
            reserva.fecha_reserva,
            reserva.cantidad_personas,
            reserva.estado,
            reserva.id_reserva
        )

        cursor.execute(sql, valores)
        conn.commit()

        cursor.close()
        conn.close()

    # Eliinar
    def eliminar(self, id_reserva):
        conn = conectar("agencia_viajes")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM reservas WHERE id_reserva = %s", (id_reserva,))
        conn.commit()

        cursor.close()
        conn.close()

    # Cambiar estado
    def cambiar_estado(self, id_reserva, nuevo_estado):
        conn = conectar("agencia_viajes")
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE reservas
            SET estado = %s
            WHERE id_reserva = %s
        """, (nuevo_estado, id_reserva))

        conn.commit()
        cursor.close()
        conn.close()