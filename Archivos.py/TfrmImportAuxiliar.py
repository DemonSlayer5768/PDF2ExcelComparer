from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidgetItem, QTableWidget, QAction, QHeaderView#type: ignore
from PyQt5.QtGui import QKeySequence#type: ignore
from PyQt5.QtCore import Qt#type: ignore
from PyQt5.QtGui import QColor#type: ignore
from PyQt5 import QtCore, QtGui, QtWidgets#type: ignore
import pandas as pd#type: ignore
import sys
import re
import math
from UI_TfmrImportAuxiliar import Ui_ventana_Importar_Auxiliar


class ImportAuxiliar(QtWidgets.QMainWindow):
    
    def __init__(self, datosAbonos, datosCargos, file_path, datosCargosAux = None, datosAbonosAux = None):
        super().__init__()

        #inicializacion de variables 
        self.datosCargosAux = []
        self.datosAbonosAux = []
        #datos del init
        self.datosAbonos = datosAbonos 
        self.datosCargos = datosCargos
        self.file_path = file_path
        self.datosAbonosAuxExtra = datosAbonosAux
        self.datosCargosAuxExtra = datosCargosAux

        # print(f"\t Comprobar datos del init form Auxiliar \n datosAbonos {self.datosAbonos} \n datosCargos{self.datosCargos} \n datosAbonosAux {self.datosAbonosAuxExtra} \n datosCargosAux{self.datosCargosAuxExtra} \n file {self.file_path}")

        
        self.ui = Ui_ventana_Importar_Auxiliar()
        self.ui.setupUi(self)

        # Conexiones de señal
        self.ui.btn_pasteAbonos.clicked.connect(self.paste_from_clipboard_Abonos)
        self.ui.btn_Next_Auxiliar.clicked.connect(self.open_new_form)
        self.ui.btn_pasteCargos.clicked.connect(self.paste_from_clipboard_Cargos)
        self.ui.btn_regresar.clicked.connect(self.verificar)

    def verificar(self):
        if self.file_path is  None:
            self.back_form_Estado()
        else:
            self.back_form()

    def back_form(self):
        from TfrmSeleccionar import Seleccionar
        try:
            # Limpiar los valores antes de abrir la nueva ventana
            self.datosAbonos = self.datosAbonos
            self.datosCargos = self.datosCargos
            self.file_path = self.file_path
            self.datosAbonosAux = None
            self.datosCargosAux = None
            # Instanciar y mostrar la nueva ventana
            self.ventana_Seleccionar = Seleccionar(self.datosAbonos, self.datosCargos, self.file_path, self.datosAbonosAux, self.datosCargosAux)
            #retorna e elimina
            # print(f"se eliminan valores de \n datosAbonosAux {self.datosAbonosAux} \n datosCargosAux {self.datosCargosAux}")
            # print(f"se retorna valores de \n datosAbonos {self.datosAbonos} \n datosCargos {self.datosCargos} \n file {self.file_path}")
            self.ventana_Seleccionar.show()

            # Ocultar la ventana actual
            self.hide()
        except Exception as e:
            print(f"Error al abrir la nueva ventana: {e}")

    def back_form_Estado(self):
        from TfrmImportEstado import ImportEstado
        try:
            # Limpiar los valores antes de abrir la nueva ventana
            self.datosAbonos = self.datosAbonos
            self.datosCargos = self.datosCargos
            self.file_path = self.file_path
            self.datosAbonosAux = None
            self.datosCargosAux = None
            # Instanciar y mostrar la nueva ventana
            self.ventana_Estado = ImportEstado(self.datosAbonos, self.datosCargos, self.file_path, self.datosAbonosAux, self.datosCargosAux)
            #retorna e elimina
            # print(f"se eliminan valores de \n datosAbonosAux {self.datosAbonosAux} \n datosCargosAux {self.datosCargosAux}")
            # print(f"se retorna valores de \n datosAbonos {self.datosAbonos} \n datosCargos {self.datosCargos} \n file {self.file_path}")
            self.ventana_Estado.show()

            # Ocultar la ventana actual
            self.hide()
        except Exception as e:
            print(f"Error al abrir la nueva ventana: {e}")

    def open_new_form(self):
        from TfrmResultado import Resultado
        try:
            # Instanciar y mostrar la nueva ventana
            self.ventana_Resultado = Resultado(self.datosAbonos, self.datosCargos, self.datosAbonosAux, self.datosCargosAux, self.file_path)
            self.ventana_Resultado.show()

            # Ocultar la ventana actual
            self.hide()
        except Exception as e:
            print(f"Error al abrir la nueva ventana: {e}")
    
    # Función para pegar datos en la tabla de Cargos
    def paste_from_clipboard_Abonos(self):
        clipboard = QApplication.clipboard()
        data = clipboard.text()
        rows = data.split('\n')

         # Eliminar última fila vacía si existe
        if rows[-1] == '':
            rows.pop()  # Elimina el último elemento si es una cadena vacía

        
        # Convertir los datos a una lista usando .tolist()
        self.datosAbonosAux = pd.Series(rows).tolist()
        self.datosAbonosAux = self.filtro_num(self.datosAbonosAux)  # Aplicar filtro

        
        # Limpiar el QTableWidget de Cargos
        self.ui.tableWidget_Abonos.clearContents()
        
        # Ajustar el número de filas según los datos pegados
        self.ui.tableWidget_Abonos.setRowCount(len(self.datosAbonosAux))
        
        # Ingresar datos en el QTableWidget
        for row_index, cell_data in enumerate(self.datosAbonosAux):
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
        # print(f"datos de abonos: \n{self.datosAbonosAux}")
        return self.datosAbonosAux



    # Función para pegar datos en la tabla de Cargos
    def paste_from_clipboard_Cargos(self):
        clipboard = QApplication.clipboard()
        data = clipboard.text()
        rows = data.split('\n')

        # Eliminar última fila vacía si existe
        if rows[-1] == '':
            rows.pop()  # Elimina el último elemento si es una cadena vacía
        
        # Convertir los datos a una lista usando .tolist()
        self.datosCargosAux = pd.Series(rows).tolist()
        self.datosCargosAux = self.filtro_num(self.datosCargosAux)  # Aplicar filtro

        
        # Limpiar el QTableWidget de Cargos
        self.ui.tableWidget_Cargos.clearContents()
        
        # Ajustar el número de filas según los datos pegados
        self.ui.tableWidget_Cargos.setRowCount(len(self.datosCargosAux))
        
        # Ingresar datos en el QTableWidget
        for row_index, cell_data in enumerate(self.datosCargosAux):
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
        # print(f"datos de cargos: \n{self.datosCargosAux}")
        return self.datosCargosAux
    

    # elimina el signo de dolar y valores string
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
    window = ImportAuxiliar()
    window.show()
    sys.exit(app.exec())


