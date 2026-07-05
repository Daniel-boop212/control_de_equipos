class Equipo:
    def __init__(self, nombre, categoria, servicio, datos_hoja_vida):
        self.nombre = nombre
        self.categoria = categoria
        self.servicio = servicio
        self.datos_hoja_vida = datos_hoja_vida
        self.mantenimientos = []
        self.estado = "azul"

    def agregar_mantenimiento(self, mantenimiento):
        self.mantenimientos.append(mantenimiento)