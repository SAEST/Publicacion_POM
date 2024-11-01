import requests
import zipfile
import os
import pytest
import allure
from shutil import rmtree

url = 'https://prep2024.ine.mx/publicacion/nacional/assets/20240603_2005_PREP.zip'
nombre_archivo = '20240603_2005_PREP.zip'
zip_pres = '20240603_2005_PREP_PRES.zip'
csv_pres = ["PRES_2024.csv", "PRES_CANDIDATURAS_2024.csv"]

directorio_destino = './data/bd'  # Carpeta en donde se descarga el zip principal
directorio_unzip = './data/bd/unzip' # Carpeta en donde se extraen los archivos del zip principal
directorio_pres = './data/bd/pres-csv'  # Carpeta donde se van a extraer los archivos para presidente
#directorio_destino = '../data'  # Carpeta donde se van a extraer los archivos en Windows
ruta_completa = os.path.join(directorio_destino, nombre_archivo)

# Crear la carpeta de destino si no existe
if not os.path.exists(directorio_destino):
    os.makedirs(directorio_destino)

# Realizar la petición GET al servidor
respuesta = requests.get(url)

# Verificar si la descarga fue exitosa (código 200)
if respuesta.status_code == 200:
    # Guardar el contenido descargado en un archivo local
    with open(ruta_completa, 'wb') as archivo:
        archivo.write(respuesta.content)
    print(f'Descarga exitosa: {ruta_completa}')
else:
    print(f'Error al descargar: {respuesta.status_code}')
    
# archivo_zip1 = os.path.join(f"{directorio_destino}/20240603_2005_PREP.zip")  # Nombre del archivo ZIP a descomprimir
archivo_zip1 = ruta_completa  # Nombre del archivo ZIP a descomprimir
# Descomprimir el archivo ZIP
with zipfile.ZipFile(archivo_zip1, 'r') as zip_ref:
    zip_ref.extractall(directorio_unzip)

print(f'Archivo ZIP "{archivo_zip1}" descomprimido exitosamente en "{directorio_unzip}"')

@pytest.fixture
def path_destino():
    return directorio_unzip #Jenkins
    #return "../data" #Windows

# @pytest.mark.parametrize("archivo_zip, archivos_esperados", [("20240603_2005_PREP_PRES.zip", ["PRES_2024.csv", "PRES_CANDIDATURAS_2024.csv"]),])

@pytest.mark.parametrize("archivo_zip, archivos_esperados", [(zip_pres, csv_pres),])
@allure.feature('Descarga de CSV Presidencia')  
@allure.story('Descompresion de CSV')  
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_descomprimir_archivo(archivo_zip, archivos_esperados, path_destino):
    """
    Prueba la descompresión de un archivo ZIP y la existencia de archivos CSV.

    Args:
        archivo_zip: Nombre del archivo ZIP a descomprimir.
        archivos_esperados: Lista de nombres de archivos CSV esperados tras la descompresión.
        directorio_destino: Directorio donde se descomprimirá el archivo.
    """
    app_version = os.getenv('APP_VERSION', '1.0.0')
    archivo_zip_path = os.path.join(directorio_unzip, archivo_zip)

    with allure.step("Descomprimiendo archivo ZIP"):
        with zipfile.ZipFile(archivo_zip_path, 'r') as zip_ref:
            zip_ref.extractall(directorio_pres)  # Descomprimir directamente en la raíz
            print(f'Archivo ZIP "{archivo_zip_path}" descomprimido exitosamente en "{directorio_pres}"')

    # Verificar y adjuntar los archivos descomprimidos
    for archivo in archivos_esperados:
        ruta_completa = os.path.join(directorio_pres, archivo)
        if os.path.exists(ruta_completa):
            allure.attach.file(ruta_completa, name=f"Archivo CSV: {archivo}", attachment_type=allure.attachment_type.CSV)
            print(f'Archivo CSV: "{archivo}" guardado exitosamente en "{directorio_pres}"')
        else:
            pytest.fail(f"El archivo CSV {archivo} no se encontró en el directorio de destino.")
            print(f'Archivo ZIP "{archivo}" no se encontró en el directorio "{ruta_completa}"')
    
    clean_path()
    
    # Adjuntar la información de éxito general
    allure.attach(f"El archivo ZIP {archivo_zip} se descomprimió exitosamente en {directorio_unzip}", 
                  name="Resultado de descompresión", attachment_type=allure.attachment_type.TEXT)
    allure.attach(app_version, name="Versión de la aplicación", attachment_type=allure.attachment_type.TEXT)

def clean_path():
    with allure.step("Limpiando archivos no usados"):
        #borrar zip que no se usan
        rmtree(directorio_unzip)

        #borrar archivo zip principal
        os.remove(ruta_completa)

        allure.attach(f"Los directorios {directorio_unzip} y archivos {nombre_archivo} creados se liberaron exitosamente ", 
                  name="Limpiando proyecto", attachment_type=allure.attachment_type.TEXT)