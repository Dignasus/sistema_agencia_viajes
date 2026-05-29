from persistencia.repositorio.reserva_repo import ReservaRepository
from negocio.services.reserva_service import ReservaService

class ReservaController:
    def __init__(self):
        self.repo = ReservaRepository()
        self.service = ReservaService(self.repo)
        self.usuario_actual = None

    def crear_reserva(self, id_cliente, id_paquete, fecha_reserva, estado):
        try:
            return self.service.crear_reserva(id_cliente, id_paquete, fecha_reserva, estado)
        except ValueError as e:
            raise ValueError(str(e))