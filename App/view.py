"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """


import time as time
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
assert cf

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def initCatalog():
    """
    Inicializa el catalogo de libros
    """
    return controller.initCatalog()


def loadData(catalog):
    """
    Carga los libros en la estructura de datos
    """
    controller.loadData(catalog)


def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Obtener las obras más antiguas de un medio o técnica")


catalog = None


"""
Menu principal
"""
while True:
    printMenu()
    inputs = int(input('Seleccione una opción para continuar\n'))

    if inputs == 1:
        print("Cargando información de los archivos ....")
        start_time = time.perf_counter()
        catalog = initCatalog()
        loadData(catalog)
        stop_time = time.perf_counter()
        delta_time = (stop_time - start_time) * 10000
        print(delta_time)
        print('Artistas cargados: ' + str(lt.size(catalog['artists'])))
        print('Obras cargadas: ' + str(lt.size(catalog['artworks'])))
        result = controller.getDateAcquired(catalog, '1993-01-01', '2000-01-01')
        print(result)
    elif inputs == 2:
        medium = str(input('Ingrese la técnica a examinar: '))
        N = int(input('Ingrese el número de obras a retornar: '))
        artworks = controller.getOldestInMedium(catalog, N, medium)
        for artwork in lt.iterator(artworks):
            print('Nombre de la obra: ' + str(artwork['Title']) +
                  '\tFecha de la obra: ' + str(artwork['Date']))
    else:
        sys.exit(0)

sys.exit(0)
