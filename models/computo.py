from .equipo import Equipo

class EquipoComputo(Equipo):
    def __init__(self, id_equipo, nombre, servicio, cpu, ram, disco):
        super().__init__(id_equipo, nombre, servicio, "Computo")
        self.cpu = cpu
        self.ram = ram
        self.disco = disco