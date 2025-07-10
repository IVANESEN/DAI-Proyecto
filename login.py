import sys
import mysql.connector
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox
)

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panel Principal")
        self.setGeometry(100, 100, 300, 100)
        self.label = QLabel("¡Bienvenido al sistema!")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login ICI")
        self.setGeometry(100, 100, 300, 150)

        self.usuario_label = QLabel("Usuario:")
        self.usuario_input = QLineEdit()

        self.contrasena_label = QLabel("Contraseña:")
        self.contrasena_input = QLineEdit()
        self.contrasena_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.boton_login = QPushButton("Iniciar Sesión")
        self.boton_login.clicked.connect(self.verificar_credenciales)

        layout = QVBoxLayout()
        layout.addWidget(self.usuario_label)
        layout.addWidget(self.usuario_input)
        layout.addWidget(self.contrasena_label)
        layout.addWidget(self.contrasena_input)
        layout.addWidget(self.boton_login)

        self.setLayout(layout)

    def verificar_credenciales(self):
        usuario = self.usuario_input.text()
        contrasena = self.contrasena_input.text()

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",             
                password="1234",           
                database="sistema_ventas" 
            )
            cursor = conn.cursor()
            query = "SELECT * FROM usuarios WHERE usuario=%s AND contraseña=%s"
            cursor.execute(query, (usuario, contrasena))
            resultado = cursor.fetchone()
            conn.close()

            if resultado:
                self.ocultar_y_mostrar_ventana_principal()
            else:
                QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Error de conexión", f"No se pudo conectar a la base de datos:\n{err}")

    def ocultar_y_mostrar_ventana_principal(self):
        self.hide()
        self.ventana_principal = VentanaPrincipal()
        self.ventana_principal.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec())
