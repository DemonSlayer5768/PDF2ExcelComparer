from PyQt5 import QtCore, QtGui, QtWidgets#type: ignore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHeaderView#type: ignore
from PyQt5.QtGui import QColor#type: ignore
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
image_Excel = os.path.join(imagenes_front_path, 'excel.png')
image_home = os.path.join(imagenes_front_path, 'home.png')

class CustomTableWidget(QtWidgets.QTableWidget):

    def __init__(self, *args, **kwargs):
        super(CustomTableWidget, self).__init__(*args, **kwargs)
        self.setColumnCount(9)
        self.setRowCount(2)
        self.setSpan(0, 0, 1, 4) 
        self.setSpan(0, 5, 1, 4)

        # self.setHorizontalHeaderLabels(["", "", "", "", "", "", "", ""])
        self.setHorizontalHeaderLabels([])
        item_0_0 = QtWidgets.QTableWidgetItem("ESTADO DE CUENTA")
        item_0_0.setTextAlignment(QtCore.Qt.AlignCenter)
        item_0_0.setBackground(QColor(253,253,150))
        self.setItem(0, 0, item_0_0)
        
        item_0_3 = QtWidgets.QTableWidgetItem("AUXILIAR CONTPAQ")
        item_0_3.setTextAlignment(QtCore.Qt.AlignCenter)
        item_0_3.setBackground(QColor(253,253,150))
        self.setItem(0, 5, item_0_3)
        
        self.setItem(1, 0, QtWidgets.QTableWidgetItem("Cargos"))
        self.setItem(1, 1, QtWidgets.QTableWidgetItem("Resultado Cargos"))
        self.setItem(1, 2, QtWidgets.QTableWidgetItem("Abonos"))
        self.setItem(1, 3, QtWidgets.QTableWidgetItem("Resultado Abonos"))
        self.setItem(1, 4, QtWidgets.QTableWidgetItem(" "))
        self.setItem(1, 5, QtWidgets.QTableWidgetItem("Cargos"))
        self.setItem(1, 6, QtWidgets.QTableWidgetItem("Resultado Cargos"))
        self.setItem(1, 7, QtWidgets.QTableWidgetItem("Abonos"))
        self.setItem(1, 8, QtWidgets.QTableWidgetItem("Resultado Abonos"))



        

class Ui_ventana_Resultado(object):

    def setupUi(self, frmResultado):
        frmResultado.setObjectName("ventana_Resultado")
        frmResultado.setFixedSize(890, 560)
        self.centralwidget = QtWidgets.QWidget(frmResultado)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 6, 901, 41))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("QLabel {\n"
"    qproperty-alignment: \'AlignCenter\';\n"
"}")
        self.label.setObjectName("label")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(280, 487, 291, 61))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.btn_exportExcel = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_exportExcel.setFont(font)
        self.btn_exportExcel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_Excel), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_exportExcel.setIcon(icon)
        self.btn_exportExcel.setIconSize(QtCore.QSize(31, 31))
        self.btn_exportExcel.setDefault(False)
        self.btn_exportExcel.setFlat(False)
        self.btn_exportExcel.setObjectName("btn_exportExcel")
        self.verticalLayout_3.addWidget(self.btn_exportExcel)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(691, 488, 181, 61))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_Inicio = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_Inicio.setFont(font)
        self.btn_Inicio.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_Inicio.setLayoutDirection(QtCore.Qt.RightToLeft)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(image_home), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_Inicio.setIcon(icon1)
        self.btn_Inicio.setIconSize(QtCore.QSize(50, 50))
        self.btn_Inicio.setDefault(False)
        self.btn_Inicio.setFlat(True)
        # self.btn_Inicio.setEnabled(False) 
        self.btn_Inicio.setObjectName("btn_Inicio")
        self.verticalLayout.addWidget(self.btn_Inicio)
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(10, 490, 181, 61))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btn_regresar = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_regresar.setFont(font)
        self.btn_regresar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_regresar.setLayoutDirection(QtCore.Qt.LeftToRight)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(image_back), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_regresar.setIcon(icon2)
        self.btn_regresar.setIconSize(QtCore.QSize(50, 50))
        self.btn_regresar.setDefault(False)
        self.btn_regresar.setFlat(True)
        self.btn_regresar.setObjectName("btn_regresar")
        self.verticalLayout_2.addWidget(self.btn_regresar)

        self.tableWidget_Excel = CustomTableWidget(self.centralwidget)
        self.tableWidget_Excel.setGeometry(QtCore.QRect(21, 60, 861, 431))
        # Ajustar el tamaño de las secciones de la tabla
        self.tableWidget_Excel.horizontalHeader().setVisible(False)
        self.tableWidget_Excel.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_Excel.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        

        frmResultado.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(frmResultado)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 898, 21))
        self.menubar.setObjectName("menubar")
        frmResultado.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(frmResultado)
        self.statusbar.setObjectName("statusbar")
        frmResultado.setStatusBar(self.statusbar)

        self.retranslateUi(frmResultado)
        QtCore.QMetaObject.connectSlotsByName(frmResultado)

    def retranslateUi(self, frmResultado):
        _translate = QtCore.QCoreApplication.translate
        frmResultado.setWindowTitle(_translate("frmResultado", "MainWindow"))
        self.label.setText(_translate("frmResultado", "<html><head/><body><p>Resultados de la conciliación bancaria</p></body></html>"))
        self.btn_exportExcel.setText(_translate("frmResultado", "Guardar en EXCEL"))
        self.btn_Inicio.setText(_translate("frmResultado", "Inicio"))
        self.btn_regresar.setText(_translate("frmResultado", "Regresar"))


    def disable_minimize_button(self, frmResultado):
        window_flags = frmResultado.windowFlags()
        window_flags &= ~QtCore.Qt.WindowMinimizeButtonHint
        frmResultado.setWindowFlags(window_flags)
        
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    frmResultado = QtWidgets.QMainWindow()
    ui = Ui_ventana_Resultado()
    ui.setupUi(frmResultado)
    frmResultado.show()
    sys.exit(app.exec_())




