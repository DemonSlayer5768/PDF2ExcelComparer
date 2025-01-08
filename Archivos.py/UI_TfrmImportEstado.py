from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidgetItem, QTableWidget, QAction, QHeaderView#type: ignore
from PyQt5.QtGui import QKeySequence#type: ignore
from PyQt5.QtCore import Qt#type: ignore
from PyQt5.QtGui import QColor#type: ignore
from PyQt5 import QtCore, QtGui, QtWidgets #type: ignore
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

class Ui_ventana_Importar_Estado(object):

    def setupUi(self, frmEstado):
        frmEstado.setObjectName("ventana_Importar_Estado")
        frmEstado.setFixedSize(653, 550)
        
        # Solo creamos centralwidget una vez
        self.centralwidget = QtWidgets.QWidget(frmEstado)
        self.centralwidget.setObjectName("centralwidget")

        self.groupBox_Cargos = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Cargos.setGeometry(QtCore.QRect(15, 35, 171, 381))
        self.groupBox_Cargos.setObjectName("groupBox_Cargos")

        self.tableWidget_Cargos = QtWidgets.QTableWidget(self.groupBox_Cargos)
        self.tableWidget_Cargos.setGeometry(QtCore.QRect(10, 20, 151, 351))
        self.tableWidget_Cargos.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableWidget_Cargos.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_Cargos.setObjectName("tableWidget_Cargos")
        self.tableWidget_Cargos.setColumnCount(1)
        self.tableWidget_Cargos.setRowCount(0)
        self.tableWidget_Cargos.setHorizontalHeaderLabels(["columna_1"])


        self.groupBox_Abonos = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Abonos.setGeometry(QtCore.QRect(199, 35, 171, 381))
        self.groupBox_Abonos.setObjectName("groupBox_Abonos")

        self.tableWidget_Abonos = QtWidgets.QTableWidget(self.groupBox_Abonos)
        self.tableWidget_Abonos.setGeometry(QtCore.QRect(10, 20, 151, 351))
        self.tableWidget_Abonos.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableWidget_Abonos.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_Abonos.setObjectName("tableWidget_Abonos")
        self.tableWidget_Abonos.setColumnCount(1)
        self.tableWidget_Abonos.setRowCount(0)
        self.tableWidget_Abonos.setHorizontalHeaderLabels(["columna_2"])

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 470, 171, 61))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_regresar = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_regresar.setFont(font)
        self.btn_regresar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_regresar.setLayoutDirection(QtCore.Qt.LeftToRight)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_back), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_regresar.setIcon(icon)
        self.btn_regresar.setIconSize(QtCore.QSize(50, 50))
        self.btn_regresar.setDefault(False)
        self.btn_regresar.setFlat(True)
        self.btn_regresar.setObjectName("btn_regresar")
        self.verticalLayout.addWidget(self.btn_regresar)

        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(449, 470, 181, 61))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btn_Next_Auxiliar = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_Next_Auxiliar.setFont(font)
        self.btn_Next_Auxiliar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_Next_Auxiliar.setLayoutDirection(QtCore.Qt.RightToLeft)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(image_next), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_Next_Auxiliar.setIcon(icon1)
        self.btn_Next_Auxiliar.setIconSize(QtCore.QSize(50, 50))
        self.btn_Next_Auxiliar.setDefault(False)
        self.btn_Next_Auxiliar.setFlat(True)
        self.btn_Next_Auxiliar.setObjectName("btn_Next_Auxiliar")
        self.verticalLayout_2.addWidget(self.btn_Next_Auxiliar)
        frmEstado.setCentralWidget(self.centralwidget)

        self.label_ImportarAux = QtWidgets.QLabel(self.centralwidget)
        self.label_ImportarAux.setGeometry(QtCore.QRect(0, 6, 641, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_ImportarAux.setFont(font)
        self.label_ImportarAux.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_ImportarAux.setStyleSheet("QLabel {\n"
"    qproperty-alignment: \'AlignCenter\';\n"
"}")

        self.label_ImportarAux.setObjectName("label_ImportarAux")
        self.btn_pasteCargos = QtWidgets.QPushButton(self.centralwidget)
        self.btn_pasteCargos.setGeometry(QtCore.QRect(13, 419, 171, 41))
        self.btn_pasteCargos.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_pasteCargos.setObjectName("btn_pasteCargos")
        # self.btn_pasteCargos.clicked.connect(self.paste_from_clipboard_Cargos)

        self.btn_pasteAbonos = QtWidgets.QPushButton(self.centralwidget)
        self.btn_pasteAbonos.setGeometry(QtCore.QRect(201, 419, 171, 41))
        self.btn_pasteAbonos.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_pasteAbonos.setObjectName("btn_pasteAbonos")
        # self.btn_pasteAbonos.clicked.connect(self.paste_from_clipboard_Abonos)

        self.label_Instrucciones = QtWidgets.QLabel(self.centralwidget)
        self.label_Instrucciones.setGeometry(QtCore.QRect(444, 30, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Source Code Pro")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_Instrucciones.setFont(font)
        self.label_Instrucciones.setObjectName("label_Instrucciones")

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(380, 70, 251, 341))
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        frmEstado.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(frmEstado)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 646, 21))
        self.menubar.setObjectName("menubar")
        frmEstado.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(frmEstado)
        self.statusbar.setObjectName("statusbar")
        frmEstado.setStatusBar(self.statusbar)

        self.retranslateUi(frmEstado)
        QtCore.QMetaObject.connectSlotsByName(frmEstado)

    def retranslateUi(self, ventana_Importar_Estado):
        _translate = QtCore.QCoreApplication.translate
        ventana_Importar_Estado.setWindowTitle(_translate("ventana_Importar_Estado", "MainWindow"))
        self.btn_regresar.setText(_translate("ventana_Importar_Estado", "Regresar"))
        self.btn_Next_Auxiliar.setText(_translate("ventana_Importar_Estado", "Siguiente "))
        self.groupBox_Cargos.setTitle(_translate("ventana_Importar_Estado", "Cargos"))
        self.groupBox_Abonos.setTitle(_translate("ventana_Importar_Estado", "Abonos"))
        self.label_ImportarAux.setText(_translate("ventana_Importar_Estado", "IMPORTAR DATOS DEL ESTADO"))
        self.btn_pasteCargos.setText(_translate("ventana_Importar_Estado", "PEGAR Cargos"))
        self.btn_pasteAbonos.setText(_translate("ventana_Importar_Estado", "PEGAR Abonos"))
        self.label_Instrucciones.setText(_translate("ventana_Importar_Estado", "Instrucciónes"))
        self.textEdit.setHtml(_translate("ventana_Importar_Estado", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">1.- </span><span style=\" font-size:10pt;\">Visualiza la tabla de cargos y abonos en tu documento auxiliar</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">2.</span><span style=\" font-size:10pt;\">-selecciona una columna y haz click derecho con el mouse, luego elige la opción &quot;copiar&quot;</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">3.-</span><span style=\" font-size:10pt;\"> vuelve a la ventana &quot;IMPORTAR VALORES DE AUXILIAR&quot;</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">4.-</span><span style=\" font-size:10pt;\"> Visualiza el boton &quot;PEGAR&quot; de la columna que copiaste </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">5.-</span><span style=\" font-size:10pt;\"> Presiona el boton &quot;PEGAR&quot; y vuelve a hacer el mismo proceso con la tabla faltante</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">6.-</span><span style=\" font-size:10pt;\"> Visualiza el resultado en las columnas de la ventana &quot;IMPORTAR VALORES DE AUXILIAR &quot;</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))

        

    def disable_minimize_button(self, ventana_Importar_Auxiliar):
        window_flags = ventana_Importar_Auxiliar.windowFlags()
        window_flags &= ~QtCore.Qt.WindowMinimizeButtonHint
        ventana_Importar_Auxiliar.setWindowFlags(window_flags)
 
 

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    frmImportarEstado = QtWidgets.QMainWindow()
    ui = Ui_ventana_Importar_Estado()
    ui.setupUi(frmImportarEstado)
    frmImportarEstado.show()
    sys.exit(app.exec_())