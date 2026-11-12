
import json
import os


# ==========================================
# 1. CARGAR DATOS
# ==========================================

def cargar_datos(nombre_archivo, datos_iniciales):

    try:

        with open(nombre_archivo, "r", encoding="utf-8") as archivo:

            datos = json.load(archivo)

            print("Datos cargados correctamente desde", nombre_archivo)

            return datos

    except FileNotFoundError:

        print("El archivo no existe. Se iniciaran datos vacios.")

        return datos_iniciales

    except json.JSONDecodeError:

        print("Error: el archivo JSON esta dañado.")

        return datos_iniciales

    except OSError as error:

        print("No se pudo leer el archivo:", error)

        return datos_iniciales


# ==========================================
# 2. GUARDAR DATOS
# ==========================================

def guardar_datos(nombre_archivo, datos):

    archivo_temporal = nombre_archivo + ".tmp"

    try:

        # Primero se crea un archivo temporal
        with open(archivo_temporal, "w", encoding="utf-8") as archivo:

            json.dump(datos, archivo, indent=4, ensure_ascii=False)

        # Si se guardo correctamente, reemplaza el archivo anterior
        os.replace(archivo_temporal, nombre_archivo)

        print("Datos guardados correctamente en", nombre_archivo)

        return True

    except (OSError, TypeError, ValueError) as error:

        print("Error al guardar los datos:", error)

        return False

    finally:

        # Eliminar el temporal si quedo sin utilizar
        if os.path.exists(archivo_temporal):

            try:
                os.remove(archivo_temporal)

            except OSError:
                print("No se pudo eliminar el archivo temporal.")
