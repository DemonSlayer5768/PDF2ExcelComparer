	PDF2ExcelComparer

Descripción

PDF2ExcelComparer es una herramienta que te permite comparar datos extraídos de un archivo PDF con un archivo auxiliar en Excel.
Utiliza diversas bibliotecas de Python para extraer, procesar y visualizar datos, con una interfaz gráfica de usuario (GUI) diseñada con PyQt5.

	Requisitos Previos

      Python: Version 3.11.9

	Configuración de Paths

El archivo config.yaml contiene todas las rutas utilizadas en el proyecto, 
incluyendo las rutas a las bibliotecas externas necesarias y los recursos de la interfaz gráfica. 
Puedes modificar estas rutas según sea necesario.

	Paths Utilizados:

    asposecells: Biblioteca para manipular archivos de Excel.
    poppler-24.02.0: Utilizado para la conversión de PDFs.
    Tesseract-OCR: Utilizado para el reconocimiento óptico de caracteres (OCR) en las imágenes.

	Carpeta de Imágenes

La carpeta ImagenesFront contiene todos los iconos e imágenes (.jpg) utilizados en la interfaz gráfica.
 Asegúrate de agregar todas las imágenes requeridas en esta carpeta.

Herramientas de Diseño de la Interfaz
Para diseñar la interfaz gráfica, es necesario instalar las herramientas de PyQt5.

		bash
	pip install Pyqt5-tools

Una vez instaladas, puedes encontrar la herramienta QTDesigner en la siguiente ruta: Python\Lib\site-packages\PyQt5_tools

	Instalación de Librerías

Debes instalar las siguientes bibliotecas para ejecutar correctamente el programa.
Aquí están los comandos para instalar cada una desde la terminal:

	bash
	pip install matplotlib pillow pandas pytesseract PyPDF2 pdf2image PyQt5 PyMuPDF openpyxl pyyaml XlsxWriter

Detalle de las Librerías

matplotlib: Para la visualización de gráficos.

bash

pip install matplotlib

Pillow (PIL): Para la manipulación de imágenes.

bash

pip install pillow

pandas: Para el manejo y análisis de datos.

bash

pip install pandas

pytesseract: Para realizar OCR en las imágenes.

bash

pip install pytesseract

PyPDF2: Para la manipulación y lectura de archivos PDF.

bash

pip install PyPDF2

pdf2image: Para convertir PDFs en imágenes.

bash

pip install pdf2image

PyQt5: Para construir la interfaz gráfica del programa.

bash

pip install PyQt5

PyMuPDF (fitz): Para la lectura avanzada de archivos PDF.

bash

pip install PyMuPDF

openpyxl: Para manipular archivos Excel.

bash

pip install openpyxl

pyyaml: Para trabajar con archivos YAML.

bash

pip install pyyaml

XlsxWriter: Para escribir en archivos Excel.

bash

    pip install XlsxWriter

Ejecución del Programa

Para iniciar el programa, simplemente ejecuta el siguiente comando en la terminal, reemplazando (nombre del archivo) por el nombre del archivo Python principal:

bash

python (nombre del archivo)

