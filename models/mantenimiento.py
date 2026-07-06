from datetime import datetime

class Mantenimiento:
    def __init__(self, fecha, tipo, descripcion):
        self.fecha = fecha
        self.tipo = tipo
        self.descripcion = descripcion

    @staticmethod
    def calcular_estado(fecha_proxima):
        if not fecha_proxima:
            return "⚪"

        try:
            fecha = datetime.strptime(
                fecha_proxima,
                "%d/%m/%Y"
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