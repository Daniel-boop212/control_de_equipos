from .equipo import Equipo

class EquipoRefrigeracion(Equipo):
    def __init__(self, id_equipo, nombre, servicio, capacidad, refrigerante):
        super().__init__(id_equipo, nombre, servicio, "Refrigeracion")
        self.capacidad = capacidad
        self.refrigerante = refrigerante