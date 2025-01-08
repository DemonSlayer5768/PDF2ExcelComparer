import matplotlib.pyplot as plt # type: ignore
from matplotlib.patches import Rectangle # type: ignore
from matplotlib.widgets import RectangleSelector # type: ignore
from PIL import Image # type: ignore
import pandas as pd # type: ignore
import pytesseract # type: ignore
import os
from PyPDF2 import PdfFileReader # type: ignore
from pdf2image import convert_from_path # type: ignore
from PyQt5 import QtCore, QtGui, QtWidgets# type: ignore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QGraphicsScene, QGraphicsPixmapItem, QGraphicsRectItem, QFileDialog # type: ignore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget # type: ignore
from PyQt5.QtGui import QPixmap, QPen # type: ignore
from PyQt5.QtCore import Qt # type: ignore
import fitz  # type: ignore
import shutil
import tempfile
import sys
from openpyxl import Workbook# type: ignore
import yaml# type: ignore
from UI_TfrmPrincipal import Ui_frmPrincipal


# Cargar la configuración desde el archivo YAML
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Cargar la configuración desde el archivo YAML
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), config['base_path']))

# Ahora, unir con los paths del YAML
tesseract_path = os.path.join(base_path, config['tesseract_path'])
tessdata_path = os.path.join(base_path, config['tessdata_path'])
poppler_path = os.path.join(base_path, config['poppler_path'])
        
# Configurar Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = tesseract_path
os.environ['TESSDATA_PREFIX'] = tessdata_path


class Principal(QtWidgets.QMainWindow):
    # Agrega el método para abrir la ventana Seleccionar
    def __init__(self, datosCargos =None ,datosAbonos = None, datosAbonosAux = None, datosCargosAux = None, file_path = None):
        super().__init__()

        self.datosCargosAux = datosCargosAux
        self.datosAbonosAux = datosAbonosAux
        self.datosCargos = datosCargos
        self.datosAbonos = datosAbonos
        self.file_pathExtra = file_path


        #interfaz
        self.ui = Ui_frmPrincipal()
        self.ui.setupUi(self)

        # print(f"\t Comprobar datos form principal \n datosAbonos {self.datosAbonos} \n datosCargos{self.datosCargos} \n datosAbonosAux {self.datosAbonosAux} \n datosCargosAux{self.datosCargosAux} \n file {self.file_pathExtra}")

        #conexiones 
        self.ui.btn_Import_PDF.clicked.connect(self.import_file)
        self.ui.btn_SavePages.clicked.connect(self.save_pages)
        self.ui.btnCreateExcel.clicked.connect(self.createExcel)
        self.ui.btn_der.clicked.connect(self.on_btn_der)
        self.ui.btn_Izq.clicked.connect(self.on_btn_izq)
        self.ui.btn_Next.clicked.connect(self.nextWindow)
        self.ui.btn_Import_Excel.clicked.connect(self.window_aux_estado)
        
        
        # componentes extras
        self.scene = QGraphicsScene()
        self.ui.Regions_View.setScene(self.scene)
        self.comboselection = self.create_excel_from_template_SoloUnaHoja   # Establecer la opción predeterminada
        
        # Variables para almacenar información del PDF
        self.pdf_path = ""
        self.doc = None
        self.current_page = 0
        self.temp_images = None
        

    def disable_minimize_button(self, frmPrincipal):
        window_flags = frmPrincipal.windowFlags()
        window_flags &= ~QtCore.Qt.WindowMinimizeButtonHint
        frmPrincipal.setWindowFlags(window_flags)

    def window_aux_estado(self):
        from TfrmImportEstado import ImportEstado
        
        self.ventana_Estado = ImportEstado()
        self.ventana_Estado.show()
        # Ocultar la ventana actual
        self.hide()
        
       
        
   
    def import_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_dialog = QFileDialog()
        file_dialog.setOptions(options)
        file_dialog.setNameFilter("PDF Files (*.pdf)")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        
        if file_dialog.exec_() == QFileDialog.Accepted:
            self.pdf_path = file_dialog.selectedFiles()[0]
            self.pdf_name = os.path.basename(self.pdf_path)
            # print(f"Archivo seleccionado: {self.pdf_path}")
            self.load_pdf()
            # visualizar archivo importado 
            self.ui.label_Verificado.setVisible(True)
            self.ui.label_oculto.setVisible(True)
            # mostrar labels
            self.ui.label_pageEnd.setVisible(True)
            self.ui.label_Diagonal.setVisible(True)
            self.ui.label_pageStart.setVisible(True)
            # activar botones
            self.ui.CB_PageStart.setEnabled(True)
            self.ui.CB_PageEnd.setEnabled(True)
        

            self.ui.btn_der.setEnabled(True)
            self.ui.btn_Izq.setEnabled(True)
            self.ui.btn_SavePages.setEnabled(True)


             #llamar  funcion count_pages
            self.number_pages = self.Count_Pages_PDF()      
            # print(f"Número de páginas: {self.number_pages}")
            self.ui.label_pageEnd.setText (str(self.number_pages))

            

    def load_pdf(self):
        if self.pdf_path:
            self.doc = fitz.open(self.pdf_path)
            self.show_page(self.current_page)
            self.update_comboboxes()

    def update_comboboxes(self):
        if self.doc:
            num_pages = self.doc.page_count
            pages = [str(i + 1) for i in range(num_pages)]
            
            self.ui.CB_PageStart.clear()
            self.ui.CB_PageEnd.clear()
            
            self.ui.CB_PageStart.addItems(pages)
            self.ui.CB_PageEnd.addItems(pages)
            self.ui.CB_PageStart.setCurrentIndex(0)
            self.ui.CB_PageEnd.setCurrentIndex(num_pages -1)


    def save_pages(self):
        self.ui.btn_SavePages.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        pages = self.get_pages_from_input()
        if not pages:
            QMessageBox.warning(None, "Error", "Please enter valid page numbers.")
            return

        if self.temp_images is None:
            self.temp_images = []

        self.temp_images = self.convert_pdfs_to_images(self.pdf_path, pages)
        self.regions = []

        if self.temp_images:
            for image_path in self.temp_images:
                selected_regions = self.select_and_draw_regions([image_path])
                self.regions.append({
                    'image_path': image_path,
                    'regions': selected_regions[0]['regions']
                })
            
            self.current_image_index = 0
            self.scene.clear()
            self.show_image_with_regions()
            #mostrar btn create_excel
            self.ui.comboBox.setEnabled(True)
            self.ui.btnCreateExcel.setEnabled(True)
            self.ui.btn_Next.setEnabled(True)
            self.ui.btn_SavePages.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))


    def get_pages_from_input(self):
        try:
            start_page = int(self.ui.CB_PageStart.currentText()) - 1
            end_page = int(self.ui.CB_PageEnd.currentText()) - 1
            if start_page > end_page or start_page < 0 or end_page >= self.doc.page_count:
                return None
            return range(start_page +1 , end_page + 2)
        except ValueError:
            return None
            

    def show_page(self, page_num):
        if self.doc:
            page = self.doc.load_page(page_num)  # Cargar la página específica del PDF
            pixmap = QPixmap.fromImage(QtGui.QImage.fromData(page.get_pixmap().tobytes()))
            self.scene.clear()
            self.scene.addPixmap(pixmap)
            self.ui.Regions_View.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
            self.current_page = page_num
            self.update_page_label()  # Actualizar el número de página


    # funciones de botones
    def on_btn_izq(self):
        if self.temp_images:
            self.show_previous_image()
        else:
            self.show_previous_page()

    def on_btn_der(self):
        if self.temp_images:
            self.show_next_image()
        else:
            self.show_next_page()

    def show_next_page(self):
        if self.current_page < self.doc.page_count - 1:
            self.current_page += 1
            self.show_page(self.current_page)

    def show_previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page(self.current_page)

    # funcion contar paginas el pdf
    def  Count_Pages_PDF(self):
        document = fitz.open(self.pdf_path)
        number_pages = document.page_count
        document.close()
        return number_pages
    # pagina actual del pdf         
    def update_page_label(self):
        if self.doc:
            self.ui.label_pageStart.setText(str(self.current_page + 1))

    
    def convert_pdfs_to_images(self, file, pages):
        try:
            images = convert_from_path(file, poppler_path=poppler_path)
            temp_images = []
            for page_number in pages:
                if 1 <= page_number <= len(images):
                    temp_image = images[page_number - 1]
                    temp_image_path = os.path.join(tempfile.gettempdir(), f'temp_image_{page_number}.png')
                    temp_image.save(temp_image_path)
                    temp_images.append(temp_image_path)
                else:
                    print(f'The PDF {file} does not have page {page_number}')
            return temp_images
        except Exception as e:
            print(f"Error converting PDF file {file}: {e}")
            return []

        # Función para gestionar la selección de regiones
    def onselect(self, eclick, erelease, regions, rect_patches, ax):
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        if x1 != x2 and y1 != y2:  # Verifica que las coordenadas no sean iguales
            # Añadir la nueva región
            new_region = {'coords': (x1, y1, x2, y2)}
            regions.append(new_region)
            
            # Dibujar el nuevo rectángulo
            rect = Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=2, edgecolor='green', facecolor='none')
            ax.add_patch(rect)
            rect_patches.append(rect)
            plt.draw()

    # Función para eliminar la región previa con clic derecho
    def on_click(self, event, regions, rect_patches):
        if event.button == 3 and regions:  # Botón derecho del ratón
            regions.pop()
            rect_patches.pop().remove()
            plt.draw()

    # Función principal para seleccionar y dibujar regiones en imágenes
    def select_and_draw_regions(self, image_paths):
        all_regions = []

        for image_path in image_paths:
            try:
                image = Image.open(image_path)
                # Desactivar la barra de herramientas
                plt.rcParams['toolbar'] = 'None'
            except FileNotFoundError:
                print(f"Error: No se encontró el archivo en la ruta especificada: {image_path}")
                continue

            regions = []
            rect_patches = []

            fig, ax = plt.subplots()
            ax.imshow(image)
            # print(f"Haz clic y arrastra para seleccionar las regiones de interés en {image_path}.")
            # print("Cierra la ventana de la imagen cuando hayas terminado.")

            # Maximizar la ventana
            figManager = plt.get_current_fig_manager()
            figManager.window.showMaximized()
             

            # Crear el RectangleSelector
            toggle_selector = RectangleSelector(
                ax, 
                lambda eclick, erelease: self.onselect(eclick, erelease, regions, rect_patches, ax), 
                interactive=True,
            )

            def toggle_selector_func(event):
                if event.key in ['Q', 'q'] and toggle_selector.active:
                    toggle_selector.set_active(False)
                elif event.key in ['A', 'a'] and not toggle_selector.active:
                    toggle_selector.set_active(True)

            plt.connect('key_press_event', toggle_selector_func)
            fig.canvas.mpl_connect('button_press_event', lambda event: self.on_click(event, regions, rect_patches))

            plt.show()

            all_regions.append({'image_path': image_path, 'regions': regions})

        return all_regions
    
    # mostrar imagenes en el pdf 
    def show_image_with_regions(self):

        
        if not self.temp_images or not self.regions:
            # print("No images or regions to show.")
            return
        
        image_path = self.regions[self.current_image_index]['image_path']
        regions_for_image = self.regions[self.current_image_index]['regions']

        if not os.path.exists(image_path):
            # print(f"Image path does not exist: {image_path}")
            return

        try:
            self.ui.Regions_View.setScene(None)
            self.scene.clear()
            scene = QtWidgets.QGraphicsScene()
            pixmap = QtGui.QPixmap(image_path)
            pixmap_item = QtWidgets.QGraphicsPixmapItem(pixmap)
            scene.addItem(pixmap_item)

            # Get the dimensions of the QGraphicsView
            view_width = self.ui.Regions_View.viewport().width()
            view_height = self.ui.Regions_View.viewport().height()

            # Scale the pixmap to fit the view
            pixmap_item.setTransformationMode(QtCore.Qt.SmoothTransformation)
            scaled_pixmap = pixmap.scaled(view_width, view_height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            pixmap_item.setPixmap(scaled_pixmap)

            # Calculate scale factors
            scale_x = scaled_pixmap.width() / pixmap.width()
            scale_y = scaled_pixmap.height() / pixmap.height()

            for region in regions_for_image:
                x1, y1, x2, y2 = region['coords']
                rect_item = QtWidgets.QGraphicsRectItem(x1 * scale_x, y1 * scale_y, (x2 - x1) * scale_x, (y2 - y1) * scale_y)
                rect_item.setPen(QtGui.QPen(QtCore.Qt.green, 2))
                scene.addItem(rect_item)

            # self.Regions_View.clear(scene)
            self.ui.Regions_View.setScene(scene)
            self.ui.Regions_View.fitInView(pixmap_item, QtCore.Qt.KeepAspectRatio)  # Fit the pixmap in the view



            # mostrar pagina en el label diagonal
              # mostrar labels
            self.ui.label_pageEnd.setVisible(False)
            self.ui.label_Diagonal.setVisible(True)
            self.update_page_label_diagonal()
            # self.label_Diagonal
            self.ui.label_pageStart.setVisible(False)
            
        except Exception as e:
            print(f"Error displaying image with regions: {e}")


    def update_page_label_diagonal(self):
        if self.temp_images:
            # Extraer el número de página del nombre del archivo
            image_path = self.regions[self.current_image_index]['image_path']
            page_number = os.path.splitext(os.path.basename(image_path))[0].split('_')[-1]  # Suponiendo que el nombre del archivo incluye el número de página
            self.ui.label_Diagonal.setText(f"{page_number}")
            
            # Ajustar el ancho del label
            label_width = 40  # Establecer el ancho deseado
            label_height = self.ui.label_Diagonal.height()  # Mantener la altura actual
            self.ui.label_Diagonal.resize(label_width, label_height)
            # print(page_number)

        
    def show_next_image(self):
        # if self.current_image_index < len(self.temp_images) - 1:
        if self.current_image_index < len(self.temp_images) - 1:
            self.current_image_index += 1
            self.show_image_with_regions()

    def show_previous_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.show_image_with_regions()


    # Función que extrae el texto de una región específica de una imagen
    def extract_text_from_region(self, image_path, region):
        try:
            image = Image.open(image_path)
            cropped_image = image.crop(region)
            text = pytesseract.image_to_string(cropped_image, lang='spa')
            # print(text)
            return text.strip().split('\n')  # Devolver una lista de líneas de texto
        except Exception as e:
            print(f"Error extrayendo texto de la región {region} en {image_path}: {e}")
            return []

    def combo_activated(self, index):
        if index == 0:
            self.comboselection = self.create_excel_from_template_SoloUnaHoja
            self.ui.btn_Next.setEnabled(True)

        elif index == 1:
            self.comboselection = self.create_excel_from_template_Multiples
            self.ui.btn_Next.setEnabled(False)

        else:
            QtWidgets.QMessageBox.warning(None, "Error", "Ingrese una Opción Válida")
        



    def open_new_form(self, file_path):
        from TfrmSeleccionar import Seleccionar
        if file_path:
        # Instanciar y mostrar la nueva ventana
            self.ventana_Estado = Seleccionar(file_path)
            self.ventana_Estado.show()
            
            # Ocultar la ventana actual
            self.hide()
    

    def nextWindow(self):

        if hasattr(self, 'comboselection'):
            temp_dir = tempfile.gettempdir()
            file_name = self.pdf_name.replace('.pdf', '.xlsx')
            file_path = os.path.join(temp_dir, file_name)

            QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

            try:
                self.comboselection(self.temp_images, self.regions, file_path)

                 # Cargar el archivo Excel para limpiar los NaN
                df = pd.read_excel(file_path)
                df = df.dropna(how='all')  # Eliminar filas que tienen todos los valores NaN
                # Eliminar columnas que tienen todos los valores NaN
                df = df.dropna(axis=1, how='all')

                # Guardar el DataFrame limpio en el mismo archivo
                df.to_excel(file_path, index=False)

                # QtWidgets.QMessageBox.information(None, "Guardado Exitoso", f"El archivo se ha guardado en {file_path}")

                # Llama a open_seleccionar_window pasando el file_path
                self.open_new_form(file_path)
                return file_name
            except Exception as e:
                # QtWidgets.QMessageBox.critical(None, "Error", f"No se pudo guardar el archivo: {str(e)}")
                return None
            finally:
                QtWidgets.QApplication.restoreOverrideCursor()
        else:
            QtWidgets.QMessageBox.warning(None, "Error", "Por favor, selecciona una opción válida antes de continuar.")
            return None



# hasta aqui 
    def createExcel(self):
        if hasattr(self, 'comboselection'):
            options = QtWidgets.QFileDialog.Options()
            file_name = self.pdf_name.replace('.pdf', '.xlsx')
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Guardar archivo Excel", file_name, "Archivos Excel (*.xlsx)", options=options)

            if file_path:
                if not file_path.endswith('.xlsx'):
                    file_path += '.xlsx'

                # Cambiar a cursor de espera
                QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

                # Ejecutar el método de creación del Excel
                self.comboselection(self.temp_images, self.regions, file_path)

                # Volver al cursor normal
                QtWidgets.QApplication.restoreOverrideCursor()
            else:
                QtWidgets.QMessageBox.warning(None, "Cancelado", "Guardado de archivo cancelado.")
        else:
            QtWidgets.QMessageBox.warning(None, "Error", "Por favor, selecciona una opción válida antes de continuar.")



    # funcion crear excel con solo una hoja
    def create_excel_from_template_SoloUnaHoja(self, temp_images, regions, xlsx_file_path):
        try:
            with pd.ExcelWriter(xlsx_file_path, engine='xlsxwriter') as writer:
                combined_data = []  # Lista para almacenar todos los datos combinados
                for image_data in regions:
                    image_path = image_data['image_path']
                    regions_for_image = image_data['regions']
                    columns_data = []

                    for region in regions_for_image:
                        lines_of_text = self.extract_text_from_region(image_path, region['coords'])
                        columns_data.append(lines_of_text)  # Agregar las líneas de texto a la lista de columnas

                    if not columns_data:  # Verificar si columns_data está vacío
                        print(f"No se encontraron datos en las regiones de {image_path}")
                        continue

                    # Crear un DataFrame donde cada columna corresponde a una región y cada fila a una línea de texto
                    max_lines = max(len(col) for col in columns_data)
                    data = {}
                    for i, col in enumerate(columns_data):
                        col_name = f'Columna_{i+1}'
                        data[col_name] = col + [''] * (max_lines - len(col))  # Completar con cadenas vacías

                    df = pd.DataFrame(data)
                    combined_data.append(df)
                    combined_data.append(pd.DataFrame([['']] * max_lines))  # Agregar filas vacías como separador

                # Concatenar todos los DataFrames
                if combined_data:
                    final_df = pd.concat(combined_data, ignore_index=True)
                    # Eliminar filas completamente vacías
                    final_df_sin_filas_vacias = final_df.dropna(how='all')

                    # Escribir todo en una sola hoja de Excel
                    final_df_sin_filas_vacias.to_excel(writer, sheet_name='Datos', index=False)

            # print("Archivo guardado")
            if self.nextWindow:
                self.delete_temp_images()
            else:
                QtWidgets.QMessageBox.warning(None, "Archivo Guardado", f'Archivo Guardado en {xlsx_file_path}')
                self.delete_temp_images()
                
        except Exception as e:
            self.ui.btnCreateExcel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            print(f"Error guardando el texto en el archivo Excel: {e}")

            
    # Función para organizar el texto extraído en un archivo Excel con hojas separadas
    def create_excel_from_template_Multiples(self, temp_images, regions, xlsx_file_path):
        try:
            QtWidgets.QApplication.processEvents()  # Para actualizar inmediatamente el cursor

            with pd.ExcelWriter(xlsx_file_path, engine='xlsxwriter') as writer:
                for image_data in regions:
                    image_path = image_data['image_path']
                    regions_for_image = image_data['regions']
                    columns_data = []
                    
                    for region in regions_for_image:
                        lines_of_text = self.extract_text_from_region(image_path, region['coords'])
                        columns_data.append(lines_of_text)  # Agregar las líneas de texto a la lista de columnas
                    
                    if not columns_data:  # Verificar si columns_data está vacío
                        print(f"No se encontraron datos en las regiones de {image_path}")
                        continue
                    
                    # Crear un DataFrame donde cada columna corresponde a una región y cada fila a una línea de texto
                    max_lines = max(len(col) for col in columns_data)
                    data = {}
                    for i, col in enumerate(columns_data):
                        col_name = f'Columna_{i+1}'
                        data[col_name] = col + [''] * (max_lines - len(col))  # Completar con cadenas vacías
                    
                    df = pd.DataFrame(data)
                    df_sin_filas_vacias = df.dropna(how='all')
                    # Nombre de la hoja de Excel basado en el nombre de la imagen
                    sheet_name = os.path.splitext(os.path.basename(image_path))[0]
                    df_sin_filas_vacias.to_excel(writer, sheet_name=sheet_name, index=False)

            # print("Archivo guardado")
            QtWidgets.QMessageBox.warning(None, "Archivo Guardado", f'Archivo Guardado en {xlsx_file_path}')
            self.delete_temp_images()
        except Exception as e:
            print(f"Error guardando el texto en el archivo Excel: {e}")
            
    # def closeEvent(self, frmPrincipal):
    #         self.delete_temp_images()
    #         frmPrincipal.accept()  # Acepta el evento para cerrar la ventana
            
    #Funcion para eliminar las imagenes temp generadas 
    def delete_temp_images(self):
        if self.temp_images:
            for image_path in self.temp_images:
                try:
                    os.remove(image_path)
                    # print(f"Deleted temporary image: {image_path}")
                except Exception as e:
                    print(f"Error deleting temporary image {image_path}: {e}")

    # def open_new_form(self):
    #     self.new_form = Ui_ventana_seleccionar()
    #     self.new_form.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Principal()
    window.show()
    sys.exit(app.exec())




# ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛
# ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛
# ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛
# ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🟨🟨🟨⬛⬛⬛
# ⬜⬜⬜⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🟨🟨🟨🟨⬛⬛⬜
# ⬜⬜⬜⬛⬛⬛🟧🟧🟧⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🟨🟨🟨🟨🟧⬛⬛⬜
# ⬜⬜⬜⬜⬜⬛⬛🟫🟨🟨🟨🟨🟧⬛⬛⬛⬛⬜⬛⬛⬛⬛⬛⬛⬛⬜⬛⬛🟨🟨🟨🟨🟧🟧⬛⬜⬜
# ⬜⬜⬜⬜⬜⬜⬛⬛🟫🟧🟨🟨🟨🟨🟨🟨🟧⬛🟨🟨🟨🟨🟨🟨🟨⬛🟧🟨🟨🟨🟨🟧🟧⬛⬜⬜⬜
# ⬜⬜⬜⬜⬜⬜⬜⬛⬛🟧🟧🟧🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟧🟧🟧⬛⬜⬜⬜⬜
# ⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛🟧🟧🟧🟧🟧🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟧⬛🟧⬛⬜⬜⬜⬜⬜
# ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛🟧⬛🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟧⬛⬜⬜⬜⬜⬜⬜
# ⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛⬜⬜⬜⬜⬜⬜
# ⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🟨🟨🟨⬛⬛🟨🟨🟨🟨🟨🟨🟨🟨⬛⬛🟨🟨⬛⬜⬜⬜⬜⬜⬜
# ⬛🟧⬛⬜⬜⬜⬜⬜⬜⬜⬜⬛🟧🟨🟨⬛⬛⬜⬛🟨🟨🟨🟨🟨🟨⬛⬛⬜⬛🟨🟧⬛⬜⬜⬜⬜⬜
# ⬛🟨🟧⬛⬜⬜⬜⬜⬜⬜⬜⬛🟨🟨🟨⬛⬛⬛⬛🟨🟨🟨🟨🟨🟨⬛⬛⬛⬛🟨🟨⬛⬜⬜⬜⬜⬜
# ⬛🟨🟨🟧⬛⬜⬜⬜⬜⬜⬜⬛🟨🟨🟨🟨⬛⬛🟨🟨🟨🟨🟨🟨🟨🟨⬛⬛🟨🟨🟨⬛⬜⬜⬜⬜⬜
# ⬛🟨🟨🟨🟧⬛⬜⬜⬜⬜⬛🟨🟨🟥🟥🟨🟨🟨🟨🟨🟨⬛⬛🟨🟨🟨🟨🟨🟨🟥🟥🟨⬛⬜⬜⬜⬜
# ⬛🟨🟨🟨🟨🟧⬛⬜⬜⬜⬛🟨🟥🟥🟥🟥🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟥🟥🟥🟥⬛⬜⬜⬜⬜
# ⬛🟨🟨🟨🟨🟨🟧⬛⬜⬜⬛🟨🟥🟥🟥🟥🟨🟨⬛🟨🟨⬛⬛🟨🟨⬛🟨🟨🟥🟥🟥🟥⬛⬜⬜⬜⬜
# ⬛🟨🟨🟨🟨🟨🟨🟧⬛⬜⬛🟨🟨🟥🟥🟨🟨🟨🟨⬛⬛🟨🟨⬛⬛🟨🟨🟨🟨🟥🟥🟨⬛⬜⬜⬜⬜
# ⬛🟨🟨🟨🟨🟨🟨🟨🟧⬛⬛⬛🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛⬜⬜⬜⬜⬜
# ⬛🟨🟨🟨🟨🟨🟨🟨🟨🟧⬛⬛🟧🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟧⬛⬜⬜⬜⬜⬜
# ⬜⬛🟨🟨🟨🟨🟨🟨🟨🟨⬛⬜⬛🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛⬜⬜⬜⬜⬜⬜
# ⬜⬜⬛🟨🟨🟨🟨🟨🟨⬛⬜⬛🟧🟨🟨🟨🟨🟨🟨🟨🟧🟧🟧🟧🟨🟨🟨🟨🟨🟨🟧⬛⬜⬜⬜⬜⬜
# ⬜⬜⬜⬛🟨🟨🟨🟨⬛⬜⬜⬛⬛🟨🟨🟨🟨🟨🟨🟨🟨🟧🟧🟨🟨🟨🟨🟨🟨🟨🟨⬛⬜⬜⬜⬜⬜
# ⬜⬜⬛🟨🟨🟨🟨⬛⬜⬜⬜⬛🟨🟨🟨🟨🟨🟨⬛🟨🟨🟨🟨🟨🟨⬛🟨🟨🟨🟨🟨⬛⬜⬜⬜⬜⬜
# ⬜⬜⬛🟨🟨🟨🟨🟨⬛⬜⬛🟨🟨🟨⬛🟨🟨🟨⬛🟨🟨🟨🟨🟨🟨⬛🟨🟨🟨⬛🟨⬛⬜⬜⬜⬜⬜
# ⬜⬜⬜⬛🟨🟨🟨🟨🟨⬛⬛🟨🟨🟨⬛🟨🟨🟨🟨⬛🟨🟨🟨🟨⬛🟨🟨🟨🟨⬛🟨🟨⬛⬜⬜⬜⬜
# ⬜⬜⬜⬜⬛🟨🟨🟧🟧🟫⬛🟨🟨🟨🟧⬛🟨🟨🟨⬛🟨🟨🟨🟨⬛🟨🟨🟨⬛🟧🟨🟨⬛⬜⬜⬜⬜
# ⬜⬜⬜⬜⬜⬛🟧🟧🟧⬛⬛🟨🟨🟨🟧⬛🟨🟨🟨⬛🟨🟨🟨🟨⬛🟨🟨🟨⬛🟧🟨🟨⬛⬜⬜⬜⬜
# ⬜⬜⬜⬜⬜⬜⬛🟧🟫🟫⬛🟨🟨🟨🟨🟧⬛🟨🟨⬛🟨🟨🟨🟨⬛🟨🟨⬛🟧🟨🟨🟨⬛⬜⬜⬜⬜
# ⬜⬜⬜⬜⬜⬛🟫🟫🟫🟫⬛🟨🟨🟨🟨🟨🟧⬛⬛🟨🟨🟨🟨🟨🟨⬛⬛🟧🟨🟨🟨🟨⬛⬜⬜⬜⬜
# ⬜⬜⬜⬜⬜⬜⬛🟫🟫🟫⬛🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛⬜⬜⬜⬜
# ⬜⬜⬜⬜⬜⬜⬜⬛⬛🟫⬛🟧🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛⬜⬜⬜⬜
# ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛⬜⬜⬜⬜⬜
# ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🟧🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛⬜⬜⬜⬜⬜
# ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🟨🟨🟨🟨🟨🟨🟧🟧🟧🟧🟧🟨🟨🟨🟨🟨🟨⬛⬜⬜⬜⬜⬜⬜
# ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🟧🟨🟧🟧⬛⬛⬛⬛⬛⬛⬛🟧🟧🟨🟧⬛⬜⬜⬜⬜⬜⬜⬜
# ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🟨🟨🟨⬛⬛⬛⬜⬜⬜⬜⬜⬜⬛⬛🟨🟨🟨⬛⬜⬜⬜⬜⬜⬜
# ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜