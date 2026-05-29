from database.db_connection import conectar
from negocio.models.paquete import Paquete

class PaqueteRepo:

    # Creacion paquete
    def crear(self, paquete: Paquete):
        conn = conectar("agencia_viajes")
        cursor = conn.cursor()
        sql = """
        INSERT INTO paquetes (
            nombre_paquete, fecha_inicio, fecha_fin, precio_total,
            tipo, id_admin_creador, id_cliente_creador
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        valores = (
            paquete.nombre_paquete,
            paquete.fecha_inicio,
            paquete.fecha_fin,
            paquete.precio_total,
            paquete.tipo,
            paquete.id_admin_creador,
            paquete.id_cliente_creador
        )

        cursor.execute(sql, valores)
        conn.commit()

        paquete.id_paquete = cursor.lastrowid

        # Guardar destinos relacionados
        if paquete.destinos:
            self._guardar_destinos(cursor, paquete.id_paquete, paquete.destinos)
            conn.commit()

        cursor.close()
        conn.close()
        return paquete

    # Obtener por id
    def obtener_por_id(self, id_paquete):
        conn = conectar("agencia_viajes")
        cursor = conn.cursor()
        sql = """
        SELECT 
            id_paquete, 
            nombre_paquete, 
            precio_total, 
            fecha_inicio, 
            fecha_fin, 
            tipo, 
            id_admin_creador, 
            id_cliente_creador
        FROM paquetes WHERE id_paquete=%s
        """
        cursor.execute(sql, (id_paquete,))
        row = cursor.fetchone()

        if not row:
            cursor.close()
            conn.close()
            return None

        # Desempaquetamos los 8 valores
        paquete = Paquete(*row)
        paquete.destinos = self._obtener_destinos(cursor, id_paquete)

        cursor.close()
        conn.close()
        return paquete

    # Obtener por todos
    def obtener_todos(self):
        conn = conectar("agencia_viajes")
        cursor = conn.cursor()

        sql = """
        SELECT 
            id_paquete, 
            nombre_paquete, 
            precio_total, 
            fecha_inicio, 
            fecha_fin, 
            tipo, 
            id_admin_creador, 
            id_cliente_creador
        FROM paquetes
        """

        cursor.execute(sql)

        rows = cursor.fetchall()
        paquetes = []
        for row in rows:
            paquete = Paquete(*row)
            paquete.destinos = self._obtener_destinos(cursor, paquete.id_paquete)
            paquetes.append(paquete)

        cursor.close()
        conn.close()
        return paquetes

    # OBTENER POR TIPO (Oficial / Personalizado)

    def obtener_por_tipo(self, tipo):
        conn = conectar("agencia_viajes")
        cursor = conn.cursor()
        cursor.execute("""
        SELECT 
            id_paquete, 
            nombre_paquete, 
            precio_total, 
            fecha_inicio, 
            fecha_fin,  
            tipo, 
            id_admin_creador, 
            id_cliente_creador
        FROM paquetes WHERE tipo=%s
        """, (tipo,))

        rows = cursor.fetchall()
        paquetes = []
        for row in rows:
            paquete = Paquete(*row)
            paquete.destinos = self._obtener_destinos(cursor, paquete.id_paquete)
            paquetes.append(paquete)

        cursor.close()
        conn.close()
        return paquetes

    # Obtener x clientes
    def obtener_por_cliente(self, id_cliente):
        conn = conectar("agencia_viajes")
        cursor = conn.cursor()
        cursor.execute("""
        SELECT 
            id_paquete, 
            nombre_paquete, 
            precio_total, 
            fecha_inicio, 
            fecha_fin,
            tipo, 
            id_admin_creador, 
            id_cliente_creador
        FROM paquetes WHERE id_cliente_creador=%s
        """, (id_cliente,))

        rows = cursor.fetchall()
        paquetes = []
        for row in rows:
            paquete = Paquete(*row)
            paquete.destinos = self._obtener_destinos(cursor, paquete.id_paquete)
            paquetes.append(paquete)

        cursor.close()
        conn.close()
        return paquetes

    # OBTENER POR ADMIN
    def obtener_por_admin(self, id_admin):
        conn = conectar("agencia_viajes")
        cursor = conn.cursor()
        cursor.execute("""
        SELECT 
            id_paquete, 
            nombre_paquete, 
            precio_total, 
            fecha_inicio, 
            fecha_fin, 
            tipo, 
            id_admin_creador, 
            id_cliente_creador
        FROM paquetes WHERE id_admin_creador=%s
        """, (id_admin,))

        rows = cursor.fetchall()
        paquetes = []
        for row in rows:
            paquete = Paquete(*row)
            paquete.destinos = self._obtener_destinos(cursor, paquete.id_paquete)
            paquetes.append(paquete)

        cursor.close()
        conn.close()
        return paquetes

    # ACTUALIZAR
    def actualizar(self, paquete: Paquete):
        conn = conectar("agencia_viajes")
        cursor = conn.cursor()
        sql = """
        UPDATE paquetes
        SET nombre_paquete=%s, fecha_inicio=%s, fecha_fin=%s, precio_total=%s,
            tipo=%s, id_admin_creador=%s, id_cliente_creador=%s
        WHERE id_paquete=%s
        """

        valores = (
            paquete.nombre_paquete,
            paquete.fecha_inicio,
            paquete.fecha_fin,
            paquete.precio_total,
            paquete.tipo,
            paquete.id_admin_creador,
            paquete.id_cliente_creador,
            paquete.id_paquete
        )

        cursor.execute(sql, valores)

        # Actualizar destinos (Borrar anteriores e insertar nuevos)
        cursor.execute("DELETE FROM paquetes_destinos WHERE id_paquete=%s", (paquete.id_paquete,))
        if paquete.destinos:
            self._guardar_destinos(cursor, paquete.id_paquete, paquete.destinos)

        conn.commit()
        cursor.close()
        conn.close()

    # Eliminar
    def eliminar(self, id_paquete):
        conn = conectar("agencia_viajes")
        cursor = conn.cursor()
        
        try:
            # 1. Primero borramos las RESERVAS de este paquete
            # (Esto soluciona el error de Foreign Key constraint)
            cursor.execute("DELETE FROM reservas WHERE id_paquete=%s", (id_paquete,))

            # 2. Luego borramos la relación con DESTINOS
            cursor.execute("DELETE FROM paquetes_destinos WHERE id_paquete=%s", (id_paquete,))

            # 3. Finalmente borramos el PAQUETE
            cursor.execute("DELETE FROM paquetes WHERE id_paquete=%s", (id_paquete,))
            
            conn.commit()
        except Exception as e:
            conn.rollback() # Si algo falla, deshacemos cambios
            raise e
        finally:
            cursor.close()
            conn.close()




    # MÉTODOS AUXILIARES
    def _guardar_destinos(self, cursor, id_paquete, destinos_ids):
        for id_destino in destinos_ids:
            cursor.execute(
                "INSERT INTO paquetes_destinos (id_paquete, id_destino) VALUES (%s,%s)",
                (id_paquete, id_destino)
            )

    def _obtener_destinos(self, cursor, id_paquete):
        cursor.execute(
            "SELECT id_destino FROM paquetes_destinos WHERE id_paquete=%s",
            (id_paquete,)
        )
        rows = cursor.fetchall()
        return [r[0] for r in rows]