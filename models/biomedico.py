from .equipo import Equipo

class EquipoBiomedico(Equipo):
    def __init__(self, id_equipo, nombre, servicio, marca, modelo, serie):
        super().__init__(id_equipo, nombre, servicio, "Biomedico")
        self.marca = marca
        self.modelo = modelo
        self.serie = serie