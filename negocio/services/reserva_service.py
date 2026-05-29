from negocio.models.reserva import Reserva

class ReservaService:
    def __init__(self, reserva_repository):
        self.repo = reserva_repository

    def crear_reserva(self, id_cliente, id_paquete, fecha_reserva, estado):
        # Guardar
        reserva = Reserva(0, id_cliente, id_paquete, fecha_reserva, estado)
        self.repo.crear(reserva)
        
        return True, "Reserva exitosa."