from .equipo import Equipo

class MuebleEnser(Equipo):
    def __init__(self, id_equipo, nombre, servicio, material, estado):
        super().__init__(id_equipo, nombre, servicio, "Mueble")
        self.material = material
        self.estado = estado