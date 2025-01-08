from PyQt5 import QtCore, QtGui, QtWidgets#type: ignore
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QHeaderView, QApplication#type: ignore
import pandas as pd #type: ignore
import re
import math
import sys
from openpyxl import Workbook #type: ignore
import os
from UI_TfrmSeleccionar import Ui_ventana_seleccionar

class Seleccionar(QtWidgets.QMainWindow):

    def __init__(self,  file_path = None, datosCargos = None, datosAbonos = None, datosCargosAux = None, datosAbonosAux = None):
        super().__init__()
        # Inicialización de variables

        self.datosAbonos = []
        self.datosCargos = []
        self.file_path = file_path
        self.datosCargosAux = datosCargosAux
        self.datosAbonosAux = datosAbonosAux
        self.datosCargosExtra = datosCargos
        self.datosAbonosExtra = datosAbonos
        self.df = None

        # print(f"\t Comprobar datos del init form seleccionar \n datosAbonos {self.datosAbonosExtra} \n datosCargos{self.datosCargosExtra} \n datosAbonosAux {self.datosAbonosAux} \n datosCargosAux{self.datosCargosAux} \n file {self.file_path}")
        
        
        self.ui = Ui_ventana_seleccionar() 
        self.ui.setupUi(self)


        # self.file_path = r'C:\\Users\\AUXPRO~1\\AppData\\Local\\Temp\\ESTADO DE CUENTA.xlsx'
 


        # Cargar el contenido del archivo Excel en el tableWidget
        if self.file_path:
            self.load_excel_file(self.file_path)

        # Conexiones de señal
        self.ui.comboBox_Ingresos.currentIndexChanged.connect(self.update_data_variables)
        self.ui.comboBox_Egresos.currentIndexChanged.connect(self.update_data_variables)
        self.ui.btn_Next_Seleccionar.clicked.connect(self.open_new_form)
        self.ui.btn_Regresar.clicked.connect(self.back_form)

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
        self.update_data_variables() 
        from TfrmImportAuxiliar import ImportAuxiliar
        # Instanciar y mostrar la nueva ventana
        # print(f"\tform seleccionar manda  \n datosAbonos: {self.datosAbonos}\n datosCargos: {self.datosCargos}")

        self.ventana_importar = ImportAuxiliar(self.datosAbonos, self.datosCargos, self.file_path)
        self.ventana_importar.show()
        # Ocultar la ventana actual
        self.hide()



    def df_filter(self):
        # Definir el regex para filtrar valores monetarios en formato string
        regex = re.compile(r'^\d{1,3}(?:,\d{3})*(?:\.\d{2})?$')

        # Filtrar columnas que contienen valores monetarios
        filtered_columns = [
            column for column in self.df.columns
            if any(
                isinstance(valor, str) and regex.match(valor) or
                isinstance(valor, (int, float)) and not math.isnan(valor)
                for valor in self.df[column]
            )
        ]

        # Filtrar filas que contienen al menos un valor monetario en las columnas filtradas
        filtered_df = self.df[filtered_columns].apply(
            lambda row: any(
                isinstance(valor, str) and regex.match(valor) or
                isinstance(valor, (int, float)) and not math.isnan(valor)
                for valor in row
            ), axis=1
        )

        # Retornar el DataFrame filtrado y las columnas filtradas
        return self.df.loc[filtered_df, filtered_columns], filtered_columns

    def load_excel_file(self, file_path):
        try:
            # Intentar cargar el archivo Excel
            self.df = pd.read_excel(file_path)

            if self.df is not None:
                # Filtrar el DataFrame
                filtered_df, filtered_columns = self.df_filter()

                # Configurar el número de columnas y filas en el tableWidget basado en el DataFrame filtrado
                self.ui.tableWidget.setColumnCount(len(filtered_columns))
                self.ui.tableWidget.setRowCount(len(filtered_df.index))
                self.ui.tableWidget.setHorizontalHeaderLabels(filtered_columns)

                # Poblar el tableWidget con los datos del DataFrame filtrado
                for row_idx, row_data in filtered_df.iterrows():
                    for col_idx, column in enumerate(filtered_columns):
                        value = row_data[column]
                        item = QTableWidgetItem(str(value))
                        if pd.isna(value):  # Verificar si el valor es NaN
                            item = QTableWidgetItem("")
                            item.setBackground(QtGui.QColor('pink'))  # Establecer el color de fondo para valores NaN
                        self.ui.tableWidget.setItem(row_idx, col_idx, item)

                # Actualizar los comboboxes con las columnas filtradas
                self.update_comboboxes(filtered_columns)

        except Exception as e:
            # Manejo de errores al cargar el archivo
            print(f"Error al cargar el archivo: {e}")  



    def update_comboboxes(self, columns):
        self.ui.comboBox_Ingresos.clear()
        self.ui.comboBox_Egresos.clear()
        self.ui.comboBox_Ingresos.addItems(columns)
        self.ui.comboBox_Egresos.addItems(columns)

        if len(columns) > 0:
            self.ui.comboBox_Ingresos.setCurrentIndex(0)  # Primer valor
            self.ui.comboBox_Egresos.setCurrentIndex(len(columns) - 1)  # Último valor

    def filtrar_monedas(self, lista):
        
        # Expresión regular para encontrar números con o sin decimales y coma como separador de miles.
        regex = re.compile(r'^\d{1,3}(?:,\d{3})*(?:\.\d{2})?$')

        # Filtrar valores que son numéricos y no NaN.
        return [valor for valor in lista if (isinstance(valor, str) and regex.match(valor)) or (isinstance(valor, (int, float)) and not math.isnan(valor))]

    def update_data_variables(self):

        if self.df is not None:
            # Obtener la columna seleccionada en el comboBox_Ingresos
            column_cargos = self.ui.comboBox_Ingresos.currentText()
            if column_cargos in self.df.columns:
                self.datosCargos = self.df[column_cargos].tolist()
                self.datosCargos = self.filtrar_monedas(self.datosCargos)  # Aplicar filtro

            # Obtener la columna seleccionada en el comboBox_Egresos
            column_abonos = self.ui.comboBox_Egresos.currentText()
            if column_abonos in self.df.columns:
                self.datosAbonos = self.df[column_abonos].tolist ()
                self.datosAbonos = self.filtrar_monedas(self.datosAbonos)  # Aplicar filtro

            # print(f"datosCargos: {self.datosCargos}")  # Debugging print
            # print(f"datosAbonos: {self.datosAbonos}")  # Debugging print
    
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventama_seleccionar = Seleccionar()
    ventama_seleccionar.show()
    sys.exit(app.exec())





