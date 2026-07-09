import sys
from PyQt6.QtWidgets import QApplication
from splash_screen import SplashScreen
from main_window import MainWindow

app = QApplication(sys.argv)

splash = SplashScreen()
splash.show()

window = MainWindow()

def abrir_main():
    window.show()

splash.timer.timeout.connect(
    lambda: abrir_main() if splash.valor == 100 else None
)

sys.exit(app.exec())