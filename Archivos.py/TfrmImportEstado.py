from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidgetItem, QTableWidget, QAction, QHeaderView #type: ignore
from PyQt5.QtGui import QKeySequence#type: ignore
from PyQt5.QtCore import Qt#type: ignore
from PyQt5.QtGui import QColor#type: ignore
from PyQt5 import QtCore, QtGui, QtWidgets#type: ignore
import pandas as pd#type: ignore
import sys
import re
import math
from UI_TfrmImportEstado import Ui_ventana_Importar_Estado

class ImportEstado(QtWidgets.QMainWindow):
    
    def __init__(self, file_path = None, datosCargos = None, datosAbonos = None, datosCargosAux = None, datosAbonosAux = None):
        super().__init__()
         # Inicialización de variables

        self.datosAbonos = []
        self.datosCargos = []
        self.file_path = file_path
        self.datosCargosAux = datosCargosAux
        self.datosAbonosAux = datosAbonosAux
        self.datosCargosExtra = datosCargos
        self.datosAbonosExtra = datosAbonos

        self.ui = Ui_ventana_Importar_Estado()
        self.ui.setupUi(self)

        #ver datos que recibe el init
        # print(f"\t Comprobar datos del init form seleccionar \n datosAbonos {self.datosAbonosExtra} \n datosCargos{self.datosCargosExtra} \n datosAbonosAux {self.datosAbonosAux} \n datosCargosAux{self.datosCargosAux} \n file {self.file_path}")

        # Conexiones de señal
        self.ui.btn_pasteAbonos.clicked.connect(self.paste_from_clipboard_Abonos)
        self.ui.btn_Next_Auxiliar.clicked.connect(self.open_new_form)
        self.ui.btn_pasteCargos.clicked.connect(self.paste_from_clipboard_Cargos)
        self.ui.btn_regresar.clicked.connect(self.back_form)

    def back_form(self):
        from TfrmPrincipal import Principal
        try:
            # Limpiar los valores antes de abrir la nueva ventana
            self.datosAbonos = None
            self.datosCargos = None
            self.file_path = None
            # print(f"se eliminan  de \n datosAbonos {self.datosAbonos} \n datosCargos {self.datosCargos} \n file {self.file_path}")
            # Instanciar y mostrar la nueva ventana
            self.ventana_Principal = Principal(self.datosAbonos, self.datosCargos, self.file_path)
            self.ventana_Principal.show()

            # Ocultar la ventana actual
            self.hide()
        except Exception as e:
            print(f"Error al abrir la nueva ventana: {e}")

    def open_new_form(self):
        from TfrmImportAuxiliar import ImportAuxiliar
        # Instanciar y mostrar la nueva ventana
        # print(f"\tform Estado manda  \n datosAbonos: {self.datosAbonos}\n datosCargos: {self.datosCargos}")

        self.ventana_importar = ImportAuxiliar(self.datosAbonos, self.datosCargos, self.file_path)
        self.ventana_importar.show()
        # Ocultar la ventana actual
        self.hide()
            
    # funcion para ocultar o mostrar las instrucciones
    def toggle_text_edit(self, checked):
        if checked:
            self.textEdit.hide()
        else:
            self.textEdit.show()

   
    # Función para pegar datos en la tabla de Cargos
    def paste_from_clipboard_Abonos(self):
        clipboard = QApplication.clipboard()
        data = clipboard.text()
        rows = data.split('\n')

         # Eliminar última fila vacía si existe
        if rows[-1] == '':
            rows.pop()  # Elimina el último elemento si es una cadena vacía

        
        # Convertir los datos a una lista usando .tolist()
        self.datosAbonos = pd.Series(rows).tolist()
        self.datosAbonos = self.filtro_num(self.datosAbonos)  # Aplicar filtro

        
        # Limpiar el QTableWidget de Cargos
        self.ui.tableWidget_Abonos.clearContents()
        
        # Ajustar el número de filas según los datos pegados
        self.ui.tableWidget_Abonos.setRowCount(len(self.datosAbonos))
        
        # Ingresar datos en el QTableWidget
        for row_index, cell_data in enumerate(self.datosAbonos):
            cell_data = cell_data.strip()
            
            # Si la celda está vacía o contiene 'nan' (como texto)
            if pd.isna(cell_data) or cell_data.lower() == 'nan' or cell_data == '':
                item = QTableWidgetItem("")
                item.setBackground(QColor('pink'))
            else:
                item = QTableWidgetItem(cell_data)
            
            self.ui.tableWidget_Abonos.setItem(row_index, 0, item)
        
        # Ajustar tamaño de las celdas al tamaño del QTableWidget
        self.ui.tableWidget_Abonos.horizontalHeader().setStretchLastSection(True)
        self.ui.tableWidget_Abonos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tableWidget_Abonos.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Devolver los datos guardados si se necesitan fuera de esta función
        # print(f"datos de abonos: \n{self.datosAbonos}")
        return self.datosAbonos



    # Función para pegar datos en la tabla de Cargos
    def paste_from_clipboard_Cargos(self):
        clipboard = QApplication.clipboard()
        data = clipboard.text()
        rows = data.split('\n')

        # Eliminar última fila vacía si existe
        if rows[-1] == '':
            rows.pop()  # Elimina el último elemento si es una cadena vacía
        
        # Convertir los datos a una lista usando .tolist()
        self.datosCargos = pd.Series(rows).tolist()
        self.datosCargos = self.filtro_num(self.datosCargos)  # Aplicar filtro
        # print(self.datosCargos)

        
        # Limpiar el QTableWidget de Cargos
        self.ui.tableWidget_Cargos.clearContents()
        
        # Ajustar el número de filas según los datos pegados
        self.ui.tableWidget_Cargos.setRowCount(len(self.datosCargos))
        
        # Ingresar datos en el QTableWidget
        for row_index, cell_data in enumerate(self.datosCargos):
            cell_data = cell_data.strip()
            
            # Si la celda está vacía o contiene 'nan' (como texto)
            if pd.isna(cell_data) or cell_data.lower() == 'nan' or cell_data == '':
                item = QTableWidgetItem("")
                item.setBackground(QColor('pink'))
            else:
                item = QTableWidgetItem(cell_data)
            
            self.ui.tableWidget_Cargos.setItem(row_index, 0, item)
        
        # Ajustar tamaño de las celdas al tamaño del QTableWidget
        self.ui.tableWidget_Cargos.horizontalHeader().setStretchLastSection(True)
        self.ui.tableWidget_Cargos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tableWidget_Cargos.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Devolver los datos guardados si se necesitan fuera de esta función
        # print(f"datos de cargos: \n{self.datosCargos}")
        return self.datosCargos
    
    def filtro_num(self, lista):
        numeros = []
        for elemento in lista:
            # Elimina el símbolo de dólar pero mantiene las comas
            clean_elemento = elemento.replace('$', '')
            if clean_elemento:  # Asegúrate de que no esté vacío
                try:
                    # Eliminamos las comas para convertir el valor a flotante
                    value_without_commas = clean_elemento.replace(',', '')
                    float(value_without_commas)
                    # Solo añadimos el elemento limpio sin el símbolo de dólar
                    numeros.append(clean_elemento)
                except ValueError:
                    # Si la conversión falla, el elemento no es un número
                    continue
        return numeros
    
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImportEstado()
    window.show()
    sys.exit(app.exec())
    