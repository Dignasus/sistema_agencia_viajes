from datetime import datetime, date

class Paquete:
    def __init__(self, id_paquete, nombre_paquete, precio_total, fecha_inicio, fecha_fin, tipo, id_admin_creador, id_cliente_creador, destinos=None):
        self._id_paquete = id_paquete
        self._nombre_paquete = nombre_paquete
        self.precio_total = precio_total
        self.fecha_inicio = self.validar_fecha(fecha_inicio)
        self.fecha_fin = self.validar_fecha(fecha_fin)
        self.tipo = tipo
        self.id_admin_creador = id_admin_creador
        self.id_cliente_creador = id_cliente_creador
        self.destinos = destinos if destinos else []

    def validar_fecha(self, fecha):
        if isinstance(fecha, (date, datetime)): return fecha
        if isinstance(fecha, str):
            try:
                return datetime.strptime(fecha, "%Y-%m-%d").date()
            except ValueError:
                return fecha
        return fecha

    # Getters y Setters
    @property
    def id_paquete(self): return self._id_paquete
    @id_paquete.setter
    def id_paquete(self, value): self._id_paquete = value

    @property
    def nombre_paquete(self): return self._nombre_paquete
    @nombre_paquete.setter
    def nombre_paquete(self, value): self._nombre_paquete = value