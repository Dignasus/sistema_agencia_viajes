class Reserva:
    def __init__(self, id_reserva, id_cliente, id_paquete, fecha_reserva, estado = "Pendiente"):
        self.id_resrva = id_reserva
        self.id_cliente = int(id_cliente)
        self.id_paquete = int(id_paquete)
        self.fecha_reserva = fecha_reserva
        self.estado = estado