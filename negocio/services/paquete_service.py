from persistencia.repositorio.paquete_repo import PaqueteRepo
from negocio.models.paquete import Paquete

class PaqueteService:
    def __init__(self):
        self.repo = PaqueteRepo()

    # OBTENER DATOS
    def obtener_paquetes(self, tipo=None):
        if tipo == 'oficial':
            return self.repo.obtener_por_tipo('oficial')
        elif tipo == 'personalizado':
            return self.repo.obtener_por_tipo('personalizado')
        else:
            return self.repo.obtener_todos()

    def obtener_por_id(self, id_paquete):
        return self.repo.obtener_por_id(id_paquete)

    # Crear admin
    def crear_paquete_admin(self, nombre, precio, inicio, fin, id_admin, destinos=None):
        # Creamos el objeto Paquete (Versión Limpia)
        nuevo_paquete = Paquete(
            id_paquete=0,
            nombre_paquete=nombre,
            precio_total=float(precio),
            fecha_inicio=inicio,
            fecha_fin=fin,
            tipo='oficial',
            id_admin_creador=id_admin,
            id_cliente_creador=None,
            destinos=destinos if destinos else []
        )
        return self.repo.crear(nuevo_paquete)

    # Crear cliente
    def crear_paquete_cliente(self, nombre, precio, inicio, fin, id_cliente, destinos):
        nuevo_paquete = Paquete(
            id_paquete=0,
            nombre_paquete=nombre,
            precio_total=float(precio),
            fecha_inicio=inicio,
            fecha_fin=fin,
            tipo='personalizado',
            id_admin_creador=None,
            id_cliente_creador=id_cliente,
            destinos=destinos
        )
        return self.repo.crear(nuevo_paquete)

    # Actualizar
    def actualizar_paquete(self, id_paquete, nombre, precio, inicio, fin, id_admin):
        # Validaciones
        try:
            precio_float = float(precio)
            if precio_float < 0: raise ValueError
        except:
            raise ValueError("El precio debe ser un número positivo.")

        # 1. Recuperar el paquete original para no perder sus destinos
        paquete_original = self.repo.obtener_por_id(id_paquete)
        destinos_actuales = paquete_original.destinos if paquete_original else []

        # 2. Crear objeto actualizado
        paquete_editado = Paquete(
            id_paquete=id_paquete,
            nombre_paquete=nombre,
            precio_total=precio_float,
            fecha_inicio=inicio,
            fecha_fin=fin,
            tipo='oficial',
            id_admin_creador=id_admin,
            id_cliente_creador=None,
            destinos=destinos_actuales
        )
        
        self.repo.actualizar(paquete_editado)
        return True

    # Eliminar
    def eliminar_paquete(self, id_paquete):
        self.repo.eliminar(id_paquete)