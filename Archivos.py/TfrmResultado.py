from PyQt5 import QtCore, QtGui, QtWidgets#type: ignore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHeaderView#type: ignore
from PyQt5.QtGui import QColor#type: ignore
import math
import pandas as pd#type: ignore
import re
from openpyxl import Workbook #type: ignore
import os
import xlsxwriter #type: ignore
import sys
from UI_TfrmResultado import Ui_ventana_Resultado

    
class Resultado(QtWidgets.QMainWindow):
    
    def __init__(self, datosAbonos, datosCargos, datosAbonosAux, datosCargosAux, file_path):
        super().__init__()
        self.datosAbonos = datosAbonos
        self.datosCargos = datosCargos
        self.datosAbonosAux = datosAbonosAux 
        self.datosCargosAux = datosCargosAux
        self.file_Path = file_path
        
        # print(f"\t Comprobar datos del init form result \n datosAbonos {self.datosAbonos} \n datosCargos{self.datosCargos} \n datosAbonosAux {self.datosAbonosAux} \n datosCargosAux{self.datosCargosAux} \n file {self.file_Path}")
        
        self.ui = Ui_ventana_Resultado()
        self.ui.setupUi(self)

        # Conexiones de señal
        self.ui.btn_exportExcel.clicked.connect(self.save_to_excel)
        self.ui.btn_regresar.clicked.connect(self.back_form)
        self.ui.btn_Inicio.clicked.connect(self.inicio_form)
        # llamar funcion comparar al principio
        self.funcion_comparar()
    
    def back_form(self):
        from TfrmImportAuxiliar import ImportAuxiliar
        try:
            # Limpiar los valores antes de abrir la nueva ventana
            self.datosAbonos = self.datosAbonos
            self.datosCargos = self.datosCargos
            self.file_Path = None
            self.datosAbonosAux = self.datosAbonosAux
            self.datosCargosAux = self.datosCargosAux

            # print(f"se retornan valores de \n datosAbonos {self.datosAbonos} \n datosCargos {self.datosCargos}")
            # print(f"se retornan  valores de \n datosAbonosAux {self.datosAbonosAux} \n datosCargosAux {self.datosCargosAux} \n file {self.file_Path}")

            # Instanciar y mostrar la nueva ventana
            self.ventana_Auxiliar = ImportAuxiliar(self.datosAbonos, self.datosCargos, self.file_Path, self.datosAbonosAux, self.datosCargosAux)
            self.ventana_Auxiliar.show()

            # Ocultar la ventana actual
            self.hide()
        except Exception as e:
            print(f"Error al abrir la nueva ventana: {e}")

    def inicio_form(self):
        # if self.save_to_excel:
        #     self.ui.btn_Inicio.setEnabled(True)

        from TfrmPrincipal import Principal
        try:
            # Limpiar los valores antes de abrir la nueva ventana
            self.datosAbonos = None
            self.datosCargos = None
            self.datosAbonosAux = None
            self.datosCargosAux = None
            self.file_Path = None
            # Instanciar y mostrar la nueva ventana
            self.ventana_Auxiliar = Principal(self.datosAbonos, self.datosCargos, self.datosAbonosAux, self.datosCargosAux, self.file_Path)
            # print(f"se elimino \n datosAbonos {self.datosAbonos} \n datosCargos{self.datosCargos} \n datosAbonosAux {self.datosAbonosAux} \n datosCargosAux{self.datosCargosAux} \n file {self.file_Path}")
            self.ventana_Auxiliar.show()

            # Ocultar la ventana actual
            self.hide()
        except Exception as e:
            print(f"Error al abrir la nueva ventana: {e}")


    def funcion_comparar(self):
     
        # Eliminar valores vacíos y NaN de las listas
        self.datosCargos = self.clean_data(self.datosCargos)
        self.datosAbonos = self.clean_data(self.datosAbonos)
        self.datosCargosAux = self.clean_data(self.datosCargosAux)
        self.datosAbonosAux = self.clean_data(self.datosAbonosAux)


        # Eliminar filas existentes antes de agregar nuevas filas
        self.ui.tableWidget_Excel.setRowCount(2)

        # Determinar el número máximo de filas necesarias
        max_rows = max(len(self.datosCargos), len(self.datosAbonos), len(self.datosCargosAux), len(self.datosAbonosAux))

        # Ajustar el número de filas en la tabla
        self.ui.tableWidget_Excel.setRowCount(max_rows + 2)
        
            # Pegar datos en las columnas correspondientes
        for i, value in enumerate(self.datosCargos):
            item = QtWidgets.QTableWidgetItem(str(value))
            self.ui.tableWidget_Excel.setItem(i + 2, 0, item)
            status_item = QtWidgets.QTableWidgetItem("Existe" if value in self.datosCargosAux else "Falta")
            if value in self.datosCargosAux:
                status_item.setBackground(QColor(119,221,119))
            else:
                status_item.setBackground(QColor('pink'))
            self.ui.tableWidget_Excel.setItem(i + 2, 1, status_item)

        for i, value in enumerate(self.datosAbonos):
            item = QtWidgets.QTableWidgetItem(str(value))
            self.ui.tableWidget_Excel.setItem(i + 2, 2, item)
            status_item = QtWidgets.QTableWidgetItem("Existe" if value in self.datosAbonosAux else "Falta")
            if value in self.datosAbonosAux:
                status_item.setBackground(QColor(119,221,119))
            else:
                status_item.setBackground(QColor("pink"))
            self.ui.tableWidget_Excel.setItem(i + 2, 3, status_item)

        for i, value in enumerate(self.datosCargosAux):
            item = QtWidgets.QTableWidgetItem(str(value))
            self.ui.tableWidget_Excel.setItem(i + 2, 5, item)
            status_item = QtWidgets.QTableWidgetItem("Existe" if value in self.datosCargos else "Falta")
            if value in self.datosCargos:
                status_item.setBackground(QColor(119,221,119))
            else:
                status_item.setBackground(QColor('pink'))
            self.ui.tableWidget_Excel.setItem(i + 2, 6, status_item)

        for i, value in enumerate(self.datosAbonosAux):
            item = QtWidgets.QTableWidgetItem(str(value))
            self.ui.tableWidget_Excel.setItem(i + 2, 7, item)
            status_item = QtWidgets.QTableWidgetItem("Existe" if value in self.datosAbonos else "Falta")
            if value in self.datosAbonos:
                status_item.setBackground(QColor(119,221,119))
            else:
                status_item.setBackground(QColor('pink'))
            self.ui.tableWidget_Excel.setItem(i + 2, 8, status_item)




    # Función para eliminar valores vacíos y NaN
    def clean_data(self,data):
        return [value for value in data if value and not (isinstance(value, float) and math.isnan(value))]

    # # ordenar lista

    def ordenar_valores(self, valores, valores_aux):
        # Ordenar valores colocando los existentes en valores_aux al principio
        return sorted(valores, key=lambda x: (x not in valores_aux, x))


    # Guardar archivo excel
    def save_to_excel(self):
        # Obtener la ruta del escritorio
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        # downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")

        options = QtWidgets.QFileDialog.Options()

        # Verificar si file_path está definido
        if not hasattr(self,'file_path' ) or self.file_path is None:
            file_name = 'conciliacion bancaria.xlsx'
        else:
            file_name = self.file_path.replace('.pdf', '.xlsx')

            
        # Crear una instancia de QFileDialog
        dialog = QtWidgets.QFileDialog()
        dialog.setWindowTitle("Guardar archivo Excel")
        dialog.setNameFilter("Archivos Excel (*.xlsx)")
        dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        dialog.setOptions(options)
        
        # Establecer el directorio inicial
        dialog.setDirectory(desktop_path)
        # dialog.setDirectory(downloads_path)

        
        # Establecer el nombre del archivo por defecto
        print(self.file_Path)
        print(file_name)
        dialog.selectFile(file_name)
        
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            file_path = dialog.selectedFiles()[0]
            file_pathAux = self.file_Path

            if not file_path.endswith('.xlsx'):
                file_path += '.xlsx'

            # Cambiar a cursor de espera
            QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

            try:
                # Ejecutar el método de creación del Excel
                self.save_table_to_excel(file_path)
                QtWidgets.QMessageBox.information(None, "Archivo Guardado", f'Archivo Guardado en {file_path}')
                
                # Intentar eliminar el archivo auxiliar
                try:
                    os.remove(file_pathAux)
                    # print(f"elimine el archivo{file_pathAux}")
                except Exception as e:
                    print(f"Error al eliminar el archivo {file_pathAux}: {e}")
            finally:
                # Volver al cursor normal
                QtWidgets.QApplication.restoreOverrideCursor()
                # self.centralwidget.parent().close()

        else:
            QtWidgets.QMessageBox.warning(None, "Cancelado", "Guardado de archivo cancelado.")

    # Crear formato para crear el archivo de excel
    def save_table_to_excel(self, path):
        column_headers = []

        for j in range(self.ui.tableWidget_Excel.columnCount()):
            column_headers.append(self.tableWidget_Excel.horizontalHeaderItem(j).text() if self.ui.tableWidget_Excel.horizontalHeaderItem(j) else f'Column {j}')

        df = pd.DataFrame(columns=column_headers)

        for i in range(self.ui.tableWidget_Excel.rowCount()):
            for j in range(self.ui.tableWidget_Excel.columnCount()):
                item_text = self.ui.tableWidget_Excel.item(i, j).text() if self.ui.tableWidget_Excel.item(i, j) else ''
                df.at[i, column_headers[j]] = item_text

        # Convertir columnas a valores de moneda
        for col in ['Column 0', 'Column 2', 'Column 5', 'Column 7']:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: float(x.replace('$', '').replace(',', '')) if isinstance(x, str) and x.replace('$', '').replace(',', '').replace('.', '').isdigit() else x)

        # Guardar el DataFrame en un archivo Excel con formato
        with pd.ExcelWriter(path, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Hoja de Calculo', header=False)
            workbook = writer.book
            worksheet = writer.sheets['Hoja de Calculo']

            # Formatos para el excel
            money_format = workbook.add_format({'num_format': '$#,##0.00'})

            names_tablet_format = workbook.add_format({
                                'align': 'center',
                                'valign': 'vcenter',
                                'bg_color': '#FDFD96'
                            })
            

            # Aplicar formato de moneda a las columnas especificadas
            col_map = {
                'Column 0': 'A',
                'Column 2': 'C',
                'Column 5': 'F',
                'Column 7': 'H'
            }

            for col_name, col_letter in col_map.items():
                if col_name in df.columns:
                    col_idx = df.columns.get_loc(col_name)
                    worksheet.set_column(col_idx, col_idx, None, money_format)

            # Obtener el número de filas y columnas
            row_count = self.ui.tableWidget_Excel.rowCount()
            column_count = self.ui.tableWidget_Excel.columnCount()

            # Recorrer cada celda en el QTableWidget 
            for row in range(row_count):
                for col in range(column_count):
                    item = self.ui.tableWidget_Excel.item(row, col)
                    if item:
                        text = item.text()
                        background_color = item.background().color()
                        bg_color_hex = background_color.name()

                        if bg_color_hex == '#000000':
                            cell_format = workbook.add_format({
                                'align': 'center',
                                'valign': 'vcenter',
                                # 'bg_color': 'white',
                            })
                        else:
                            cell_format = workbook.add_format({
                                'align': 'center',
                                'valign': 'vcenter',
                                'bg_color': bg_color_hex,
                            })

                        worksheet.write(row, col, text, cell_format)  


            # Ajuste automático de ancho de columnas
            for i, column in enumerate(df.columns):
                max_len = max(df[column].astype(str).map(len).max(), len(column))
                worksheet.set_column(i, i, max_len + 2)  # Agregar un poco de margen

            # Aplicar formato de moneda a las celdas específicas
            for col_name, col_letter in col_map.items():
                if col_name in df.columns:
                    col_idx = df.columns.get_loc(col_name)
                    for row in range(row_count):
                        value = df.iloc[row, col_idx]
                        if isinstance(value, (int, float)):
                            worksheet.write_number(row , col_idx, value, money_format)


            # Combinar celdas (setSpan equivalente)
            worksheet.merge_range(0, 0, 0, 3, self.ui.tableWidget_Excel.item(0, 0).text() if self.ui.tableWidget_Excel.item(0, 0) else '',names_tablet_format)
            worksheet.merge_range(0, 5, 0, 8, self.ui.tableWidget_Excel.item(0, 5).text() if self.ui.tableWidget_Excel.item(0, 5) else '',names_tablet_format)
            
                
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Resultado()
    window.show()
    sys.exit(app.exec())


    

