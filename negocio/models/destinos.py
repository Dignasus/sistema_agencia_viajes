class Destino:
    def __init__(self, id_destino, nombre, descripcion, actividades, costo_base):
        self.id_destino = id_destino
        self.nombre = nombre
        self.descripcion = descripcion
        self.actividades = actividades # Lista de actividades disponibles en el destino
        self.costo_base = costo_base 

    def crear_destino(self):
        return {
            "id_destino": self.id_destino,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "actividades": self.actividades,
            "costo_base": self.costo_base
        }
    def editar_destino():
        pass

    def eliminar_destino():
        pass

    