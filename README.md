import sys
import mysql.connector
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QFrame, QLineEdit, QTableWidget, QTableWidgetItem, QSpacerItem, QSizePolicy,
    QGraphicsDropShadowEffect, QMessageBox, QMenu
)
from PyQt6.QtGui import QFont, QColor, QPixmap
from PyQt6.QtCore import Qt

# --- FUNCIONES BD ---
def obtener_clientes():
    try:
        conn = mysql.connector.connect(
            host="localhost", user="root", password="1234", database="sistema_ventas"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT nombre_cliente, fecha_registro FROM clientes")
        data = cursor.fetchall()
        conn.close()
        return data
    except mysql.connector.Error as e:
        print("Error al conectar con BD:", e)
        return []

def insertar_cliente(nombre, email, telefono, direccion):
    try:
        conn = mysql.connector.connect(
            host="localhost", user="root", password="1234", database="sistema_ventas"
        )
        cursor = conn.cursor()
        query = "INSERT INTO clientes (nombre_cliente, email_cliente, telefono_cliente, direccion) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (nombre, email, telefono, direccion))
        conn.commit()
        conn.close()
        return True
    except mysql.connector.Error as e:
        print("Error al insertar cliente:", e)
        return False

# --- LOGIN ---
class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login ICI")
        self.setGeometry(100, 100, 700, 400)
        self.setStyleSheet("background-color: #f0f2f5;")
        layout_principal = QHBoxLayout()
        layout_logo = QVBoxLayout()

        logo_label = QLabel()
        pixmap = QPixmap("proyecto/ICI_logo(login).png").scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_logo.addWidget(logo_label)
        layout_principal.addLayout(layout_logo)

        layout_login = QVBoxLayout()
        layout_login.setContentsMargins(40, 30, 40, 30)
        login_box = QWidget()
        login_box.setStyleSheet("background-color: #3c258c; border-radius: 5px;")
        login_layout = QVBoxLayout(login_box)

        titulo = QLabel("Login")
        titulo.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        titulo.setStyleSheet("color: white;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.usuario_input = QLineEdit()
        self.usuario_input.setPlaceholderText("Email o Usuario")
        self.usuario_input.setStyleSheet(
            "padding: 5px; color: white; background-color: transparent; border: none; border-bottom: 1px solid white;"
        )
        self.contrasena_input = QLineEdit()
        self.contrasena_input.setPlaceholderText("Password")
        self.contrasena_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.contrasena_input.setStyleSheet(
            "padding: 5px; color: white; background-color: transparent; border: none; border-bottom: 1px solid white;"
        )

        self.boton_login = QPushButton("Login")
        self.boton_login.setStyleSheet(
            """
            QPushButton {
                background-color: lightgray;
                color: #3c258c;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: white;
            }
        """
        )
        self.boton_login.clicked.connect(self.verificar_credenciales)

        enlaces = QHBoxLayout()
        crear = QLabel("<a href='#' style='color: white;'>Crear cuenta</a>")
        crear.setOpenExternalLinks(False)
        recuperar = QLabel("<a href='#' style='color: white;'>¿Olvidaste la contraseña?</a>")
        recuperar.setOpenExternalLinks(False)
        enlaces.addWidget(crear)
        enlaces.addSpacerItem(QSpacerItem(40, 10, QSizePolicy.Policy.Expanding))
        enlaces.addWidget(recuperar)

        login_layout.addWidget(titulo)
        login_layout.addSpacing(10)
        login_layout.addWidget(self.usuario_input)
        login_layout.addWidget(self.contrasena_input)
        login_layout.addSpacing(10)
        login_layout.addWidget(self.boton_login)
        login_layout.addSpacing(20)
        login_layout.addLayout(enlaces)

        layout_login.addWidget(login_box)
        layout_principal.addLayout(layout_login)
        self.setLayout(layout_principal)

    def verificar_credenciales(self):
        usuario = self.usuario_input.text()
        clave = self.contrasena_input.text()
        try:
            conn = mysql.connector.connect(
                host="localhost", user="root", password="1234", database="sistema_ventas"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE usuario=%s AND contraseña=%s", (usuario, clave))
            if cursor.fetchone():
                self.hide()
                self.dashboard = DashboardICI(self, usuario)
                self.dashboard.show()
            else:
                QMessageBox.warning(self, "Error", "Credenciales incorrectas.")
            conn.close()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Error de conexión", f"{err}")

class CardWidget(QFrame):
    """Card visual idéntica a Figma, con sombra y borde redondeado."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            """
            background: #FFF;
            border-radius: 18px;
        """
        )
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(80, 80, 120, 30))
        self.setGraphicsEffect(shadow)

class ProveedoresWidget(CardWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        titulo = QLabel("👥 Proveedores actuales")
        titulo.setStyleSheet("color: #888; font-size: 13px;")
        layout.addWidget(titulo)

        nombre = QLabel("Vidri\nFreund")
        nombre.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        nombre.setStyleSheet("color: #000; line-height: 1.2;")
        layout.addWidget(nombre)

        layout.addSpacing(6)

        boton = QPushButton("Agregar")
        boton.setStyleSheet(
            """
            background-color: #1e40ff;
            color: white;
            border-radius: 10px;
            padding: 7px 18px;
            font-weight: 600;
        """
        )
        boton.setFixedWidth(95)
        layout.addWidget(boton, alignment=Qt.AlignmentFlag.AlignRight)

class ClientesWidget(CardWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)

        titulo = QLabel("📋 Lista de Clientes")
        titulo.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(titulo)

        clientes = obtener_clientes()
        filas = len(clientes)

        tabla = QTableWidget(filas, 2)
        tabla.setHorizontalHeaderLabels(["Nombre del Cliente", "Fecha de Registro"])
        tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        tabla.verticalHeader().setVisible(False)
        tabla.horizontalHeader().setStretchLastSection(True)
        tabla.setShowGrid(False)
        tabla.setStyleSheet(
            """
            QTableWidget {
                border: none;
                background: transparent;
            }
            QHeaderView::section {
                background: transparent;
                font-size: 12px;
                font-weight: bold;
                color: #4B5563;
                border: none;
                padding: 4px;
            }
        """
        )

        for i, (nombre, fecha) in enumerate(clientes):
            tabla.setItem(i, 0, QTableWidgetItem(nombre))
            tabla.setItem(i, 1, QTableWidgetItem(fecha.strftime("%d/%m/%Y") if hasattr(fecha, 'strftime') else str(fecha)))

        tabla.setFixedHeight(110 + filas*20)
        layout.addWidget(tabla)

        layout.addSpacing(4)
        boton = QPushButton("➕ Agregar Cliente")
        boton.setStyleSheet(
            """
            background-color: #F3F4F6;
            color: #1e40ff;
            border-radius: 9px;
            padding: 7px 18px;
            font-weight: 600;
        """
        )
        boton.setFixedWidth(160)
        layout.addWidget(boton, alignment=Qt.AlignmentFlag.AlignLeft)

class ComisionWidget(CardWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        lbl = QLabel("Este mes, tu comisión como\nEspecialista de Ventas ha sido:")
        lbl.setFont(QFont("Arial", 13))
        layout.addWidget(lbl)
        val = QLabel("$12,281")
        val.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        val.setStyleSheet("color: #1e40ff;")
        layout.addWidget(val)

        grafica = QLabel()
        grafica.setPixmap(
            QPixmap("proyecto/grafica_placeholder.png").scaled(200, 60, Qt.AspectRatioMode.KeepAspectRatio)
        )
        grafica.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(grafica)

class DashboardICI(QWidget):
    def __init__(self, login_widget, usuario):
        super().__init__()
        self.login_widget = login_widget  # Referencia para volver al login
        self.usuario = usuario

        self.setWindowTitle("Dashboard ICI")
        self.setStyleSheet("background: #F8F9FB;")
        self.setMinimumSize(1440, 900)

        layout_main = QHBoxLayout(self)
        layout_main.setSpacing(0)
        layout_main.setContentsMargins(0, 0, 0, 0)

        # ------ MENÚ LATERAL IZQUIERDO ------
        menu = QFrame()
        menu.setFixedWidth(200)
        menu.setStyleSheet("background-color: white; border-right: 1px solid #ccc;")
        menu_layout = QVBoxLayout(menu)
        menu_layout.setContentsMargins(0, 20, 0, 20)
        menu_layout.setSpacing(20)

        label_logo = QLabel("ICI")
        label_logo.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        label_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_usuario = QPushButton(f"👤 {self.usuario} ▾")
        btn_usuario.setStyleSheet(
            """
            QPushButton {
                border: none;
                background: transparent;
                font-size: 14px;
                padding: 10px;
                text-align: left;
            }
            QPushButton::menu-indicator {
                image: none;
            }
            """
        )
        menu_usuario = QMenu()
        menu_usuario.addAction("Perfil")
        menu_usuario.addAction("Cerrar sesión", self.logout)
        btn_usuario.setMenu(menu_usuario)

        menu_layout.addWidget(label_logo)
        menu_layout.addWidget(btn_usuario)
        menu_layout.addStretch()

        layout_main.addWidget(menu)

        # ------ PANEL CENTRAL ------
        central_panel = QWidget()
        central_layout = QVBoxLayout(central_panel)
        central_layout.setContentsMargins(40, 34, 40, 32)
        central_layout.setSpacing(18)

        # Header
        header_layout = QHBoxLayout()
        lbl_hello = QLabel(f"Hola, {self.usuario} 👋")
        lbl_hello.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        header_layout.addWidget(lbl_hello)

        header_layout.addStretch()
        search = QLineEdit()
        search.setPlaceholderText("Search")
        search.setFixedWidth(320)
        search.setStyleSheet(
            """
            background: #F3F4F6;
            border-radius: 15px;
            padding: 12px 18px;
            font-size: 16px;
            border: none;
            color: #444;
        """
        )
        header_layout.addWidget(search)
        central_layout.addLayout(header_layout)

        # Subtítulo
        lbl_welcome = QLabel("Bienvenido a tu dashboard de ventas del mes")
        lbl_welcome.setFont(QFont("Arial", 16))
        lbl_welcome.setStyleSheet("color: #111827;")
        central_layout.addWidget(lbl_welcome)
        central_layout.addSpacing(12)

        # Cards de resumen
        cards_layout = QHBoxLayout()
        cards_layout.addWidget(ClientesWidget())
        cards_layout.addSpacing(20)
        cards_layout.addWidget(CardWidget())  
        central_layout.addLayout(cards_layout)

        central_layout.addSpacing(20)
        # Widget proveedores
        central_layout.addWidget(ProveedoresWidget())

        layout_main.addWidget(central_panel, stretch=2)

        # ------ PANEL DERECHO ------
        right_panel = QWidget()
        right_panel.setFixedWidth(370)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(28, 30, 28, 28)
        right_layout.setSpacing(22)

        right_layout.addWidget(ComisionWidget())

        
        reminder = CardWidget()
        rem_layout = QVBoxLayout(reminder)
        rem_layout.setContentsMargins(20, 16, 20, 16)
        rem_title = QLabel("Este es tu usuario de uso")
        rem_title.setFont(QFont("Arial", 13))
        rem_title.setStyleSheet("color: #1e40ff;")
        rem_layout.addWidget(rem_title)
        rem_desc = QLabel("Más fácil que Salesforce")
        rem_desc.setFont(QFont("Arial", 12))
        rem_layout.addWidget(rem_desc)
        boton = QPushButton("Set as Reminder")
        boton.setStyleSheet(
            """
            background-color: #1e40ff;
            color: white;
            border-radius: 10px;
            padding: 8px 28px;
            font-weight: 600;
        """
        )
        rem_layout.addWidget(boton)
        right_layout.addWidget(reminder)

        right_layout.addStretch()
        layout_main.addWidget(right_panel)

        self.setLayout(layout_main)

    def logout(self):
        self.close()
        self.login_widget.usuario_input.clear()
        self.login_widget.contrasena_input.clear()
        self.login_widget.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec())
