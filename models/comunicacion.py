from .equipo import Equipo


class EquipoComunicacion(Equipo):
    def __init__(self, id_equipo, nombre, servicio, cpu, ram, disco):
        super().__init__(id_equipo, nombre, servicio, "Comunicacion")
        self.cpu = cpu
        self.ram = ram
        self.disco = disco


EquipoCompunicaciones = EquipoComunicacion
