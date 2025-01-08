from PyQt5 import QtCore, QtGui, QtWidgets# type: ignore
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QHeaderView# type: ignore
import sys
import os 
import yaml #type:ignore

# Cargar la configuración desde el archivo YAML
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Cargar la configuración desde el archivo YAML
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), config['base_path']))

# Ahora, unir con los paths del YAML
imagenes_front_path = os.path.join(base_path, config['imagenes_path'])
#variables imagenes
image_back = os.path.join(imagenes_front_path,"Back.png")
image_next = os.path.join(imagenes_front_path, "Next.png") 

class Ui_ventana_seleccionar(object):

    def setupUi(self, ventana_seleccionar):
        ventana_seleccionar.setObjectName("ventana_seleccionar")
        ventana_seleccionar.setFixedSize(628, 493)
        ventana_seleccionar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        ventana_seleccionar.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(ventana_seleccionar)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 70, 411, 331))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.Label_SeleccionarColumnas = QtWidgets.QLabel(self.centralwidget)
        self.Label_SeleccionarColumnas.setGeometry(QtCore.QRect(60, 30, 361, 31))
        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Label_SeleccionarColumnas.setFont(font)
        self.Label_SeleccionarColumnas.setObjectName("Label_SeleccionarColumnas")
        self.comboBox_Ingresos = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_Ingresos.setGeometry(QtCore.QRect(470, 110, 111, 21))
        self.comboBox_Ingresos.setObjectName("comboBox_Ingresos")
        self.comboBox_Egresos = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_Egresos.setGeometry(QtCore.QRect(471, 205, 111, 21))
        self.comboBox_Egresos.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comboBox_Egresos.setObjectName("comboBox_Egresos")
        self.label_Cargos = QtWidgets.QLabel(self.centralwidget)
        self.label_Cargos.setGeometry(QtCore.QRect(470, 90, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_Cargos.setFont(font)
        self.label_Cargos.setTextFormat(QtCore.Qt.AutoText)
        self.label_Cargos.setObjectName("label_Cargos")
        self.label_Abonos = QtWidgets.QLabel(self.centralwidget)
        self.label_Abonos.setGeometry(QtCore.QRect(471, 185, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_Abonos.setFont(font)
        self.label_Abonos.setObjectName("label_Abonos")
        self.btn_Next_Seleccionar = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Next_Seleccionar.setGeometry(QtCore.QRect(483, 410, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_Next_Seleccionar.setFont(font)
        self.btn_Next_Seleccionar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_Next_Seleccionar.setLayoutDirection(QtCore.Qt.RightToLeft)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_next), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_Next_Seleccionar.setIcon(icon)
        self.btn_Next_Seleccionar.setIconSize(QtCore.QSize(50, 50))
        self.btn_Next_Seleccionar.setFlat(True)
        self.btn_Next_Seleccionar.setObjectName("btn_Next_Seleccionar")
        self.btn_Regresar = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Regresar.setGeometry(QtCore.QRect(5, 410, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_Regresar.setFont(font)
        self.btn_Regresar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_Regresar.setLayoutDirection(QtCore.Qt.LeftToRight)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(image_back), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_Regresar.setIcon(icon1)
        self.btn_Regresar.setIconSize(QtCore.QSize(50, 50))
        self.btn_Regresar.setFlat(True)
        self.btn_Regresar.setObjectName("btn_Regresar")
        ventana_seleccionar.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ventana_seleccionar)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 628, 21))
        self.menubar.setObjectName("menubar")
        ventana_seleccionar.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ventana_seleccionar)
        self.statusbar.setObjectName("statusbar")
        ventana_seleccionar.setStatusBar(self.statusbar)

        self.retranslateUi(ventana_seleccionar)
        QtCore.QMetaObject.connectSlotsByName(ventana_seleccionar)

    def retranslateUi(self, ventana_seleccionar):
        _translate = QtCore.QCoreApplication.translate
        ventana_seleccionar.setWindowTitle(_translate("ventana_seleccionar", "MainWindow"))
        self.Label_SeleccionarColumnas.setText(_translate("ventana_seleccionar", "Selecciona las columnas que corresponden"))
        self.label_Cargos.setText(_translate("ventana_seleccionar", "Columna CARGOS"))
        self.label_Abonos.setText(_translate("ventana_seleccionar", "Columna Abonos"))
        self.btn_Next_Seleccionar.setText(_translate("ventana_seleccionar", "Siguiente"))
        self.btn_Regresar.setText(_translate("ventana_seleccionar", "Regresar"))

    def disable_minimize_button(self, ventana_seleccionar):
        window_flags = ventana_seleccionar.windowFlags()
        window_flags &= ~QtCore.Qt.WindowMinimizeButtonHint
        ventana_seleccionar.setWindowFlags(window_flags)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ventana_seleccionar = QtWidgets.QMainWindow()
    ui = Ui_ventana_seleccionar()
    ui.setupUi(ventana_seleccionar)
    ventana_seleccionar.show()
    sys.exit(app.exec_())
