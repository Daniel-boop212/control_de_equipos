from base_form import BaseForm

class ComputoForm(BaseForm):
    def __init__(self, datos_existentes=None):
        super().__init__("Equipo de cómputo")
        self.agregar_seccion("Imagen")
        self.agregar_selector_imagen("imagen_equipo")

        self.agregar_seccion("Información general")
        self.agregar_input("Nombre")
        self.agregar_input("Marca")
        self.agregar_input("Modelo")
        self.agregar_input("Serie")

        self.agregar_seccion("Compra")
        self.agregar_fecha("Fecha compra")
        self.agregar_input("Garantía")
        self.agregar_input("Proveedor")

        self.agregar_seccion("Hardware")
        self.agregar_input("Procesador")
        self.agregar_input("Marca monitor")
        self.agregar_input("Serie monitor")

        self.agregar_combo("Tipo", [
            "Computador",
            "Televisor",
            "Impresora",
            "Scanner",
            "Servidor"
        ])

        self.btn_guardar.clicked.connect(self.guardar)

        if datos_existentes:
            self.cargar_datos_existentes(datos_existentes)

    def guardar(self):
        self.datos_guardados = self.obtener_datos()
        self.accept()