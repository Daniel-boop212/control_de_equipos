from datetime import datetime


class Mantenimiento:
    def __init__(self, fecha, tipo, descripcion):
        self.fecha = fecha
        self.tipo = tipo
        self.descripcion = descripcion

    @staticmethod
    def calcular_estado(fecha_proxima, realizado=False):
        if realizado:
            return "🔵"

        try:
            fecha = datetime.strptime(
                fecha_proxima,
                "%Y-%m-%d"
            ).date()
        except ValueError:
            return "⚪"

        hoy = datetime.now().date()
        dias = (fecha - hoy).days

        if dias < 0:
            return "🔴"
        elif dias <= 30:
            return "🟡"
        else:
            return "🟢"