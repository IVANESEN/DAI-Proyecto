import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QFrame, QLineEdit, QTableWidget, QTableWidgetItem, QSpacerItem, QSizePolicy,
    QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QFont, QColor, QPixmap
from PyQt6.QtCore import Qt

class CardWidget(QFrame):
    """Card visual idéntica a Figma, con sombra y borde redondeado."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            background: #FFF;
            border-radius: 18px;
        """)
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
        boton.setStyleSheet("""
            background-color: #1e40ff;
            color: white;
            border-radius: 10px;
            padding: 7px 18px;
            font-weight: 600;
        """)
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

        tabla = QTableWidget(3, 2)
        tabla.setHorizontalHeaderLabels(["Nombre del Cliente", "Fecha de Registro"])
        tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        tabla.verticalHeader().setVisible(False)
        tabla.horizontalHeader().setStretchLastSection(True)
        tabla.setShowGrid(False)
        tabla.setStyleSheet("""
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
        """)
        tabla.setItem(0, 0, QTableWidgetItem("Cliente 1"))
        tabla.setItem(0, 1, QTableWidgetItem("04/07/2025"))
        tabla.setItem(1, 0, QTableWidgetItem("Cliente 2"))
        tabla.setItem(1, 1, QTableWidgetItem("05/07/2025"))
        tabla.setItem(2, 0, QTableWidgetItem("Cliente 3"))
        tabla.setItem(2, 1, QTableWidgetItem("06/07/2025"))
        tabla.setFixedHeight(110)
        layout.addWidget(tabla)

        layout.addSpacing(4)
        boton = QPushButton("➕ Agregar Cliente")
        boton.setStyleSheet("""
            background-color: #F3F4F6;
            color: #1e40ff;
            border-radius: 9px;
            padding: 7px 18px;
            font-weight: 600;
        """)
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
        grafica.setPixmap(QPixmap("proyecto/grafica_placeholder.png").scaled(200,60,Qt.AspectRatioMode.KeepAspectRatio))
        grafica.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(grafica)

class DashboardICI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard ICI")
        self.setStyleSheet("background: #F8F9FB;")
        self.setMinimumSize(1440, 900)

        layout_main = QHBoxLayout(self)
        layout_main.setSpacing(0)
        layout_main.setContentsMargins(0,0,0,0)

        # ------ MENÚ LATERAL IZQUIERDO ------
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("""
            background: #FFF;
            border-right: 1px solid #E5E7EB;
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        sidebar_layout.setContentsMargins(28, 30, 20, 18)

        logo = QLabel("ICI")
        logo.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(logo)
        sidebar_layout.addSpacing(30)

        lbl_general = QLabel("Vista general")
        lbl_general.setFont(QFont("Arial", 13))
        lbl_general.setStyleSheet("color: #1e40ff; font-weight: bold;")
        sidebar_layout.addWidget(lbl_general)
        sidebar_layout.addSpacing(8)
        lbl_user = QLabel("Mi usuario")
        lbl_user.setFont(QFont("Arial", 13))
        lbl_user.setStyleSheet("color: #111827;")
        sidebar_layout.addWidget(lbl_user)
        sidebar_layout.addSpacing(30)

        sidebar_layout.addStretch()

        legal = QLabel("Esta aplicación informática\nfue construida por Kocters, S.A. de C.V.")
        legal.setStyleSheet("color: #A5A5A5; font-size: 11px;")
        sidebar_layout.addWidget(legal)
        sidebar_layout.addSpacing(16)

        logout = QLabel("Logout")
        logout.setStyleSheet("color: #6b7280; font-size: 13px;")
        sidebar_layout.addWidget(logout)

        layout_main.addWidget(sidebar)

        # ------ PANEL CENTRAL ------
        central_panel = QWidget()
        central_layout = QVBoxLayout(central_panel)
        central_layout.setContentsMargins(40, 34, 40, 32)
        central_layout.setSpacing(18)

        # Header
        header_layout = QHBoxLayout()
        lbl_hello = QLabel("Hola, Alvín 👋")
        lbl_hello.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        header_layout.addWidget(lbl_hello)

        header_layout.addStretch()
        search = QLineEdit()
        search.setPlaceholderText("Search")
        search.setFixedWidth(320)
        search.setStyleSheet("""
            background: #F3F4F6;
            border-radius: 15px;
            padding: 12px 18px;
            font-size: 16px;
            border: none;
            color: #444;
        """)
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
        cards_layout.addWidget(CardWidget())  # Placeholder para otras cards o gráficos
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

        # Ejemplo de otro card: recordatorio
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
        boton.setStyleSheet("""
            background-color: #1e40ff;
            color: white;
            border-radius: 10px;
            padding: 8px 28px;
            font-weight: 600;
        """)
        rem_layout.addWidget(boton)
        right_layout.addWidget(reminder)

        right_layout.addStretch()
        layout_main.addWidget(right_panel)

        self.setLayout(layout_main)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardICI()
    window.show()
    sys.exit(app.exec())
