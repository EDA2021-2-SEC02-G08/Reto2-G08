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


# Funciones auxiliares


def artworkInfo(artworks):
    i = 1
    while i <= 3:
        artwork = lt.getElement(artworks, i)
        print('Object ID: ' + artwork['ObjectID'] +
              '.Titulo: ' + artwork['Title'] +
              '. Fecha: ' + artwork['Date'] +
              '. Fecha de adquisicion: ' + artwork['DateAcquired'] +
              '. Medio: ' + artwork['Medium'] +
              '. Dimensiones: ' + artwork['Dimensions'])
        i += 1

    i = -2
    while i <= 0:
        artwork = lt.getElement(artworks, i)
        print('Object ID: ' + artwork['ObjectID'] +
              '.Titulo: ' + artwork['Title'] +
              '. Fecha: ' + artwork['Date'] +
              '. Fecha de adquisicion ' + artwork['DateAcquired'] +
              '. Medio: ' + artwork['Medium'] +
              '. Dimensiones: ' + artwork['Dimensions'])
        i += 1


def countPurchase(artworks):
    count = 0
    for artwork in lt.iterator(artworks):
        if 'purchase' in artwork['CreditLine'].lower():
            count += 1

    return count


def countArtists(artworks):
    auxiliar = {}
    count = 0
    for artwork in lt.iterator(artworks):
        artists_id = artwork['ConstituentID'].replace('[', '').replace(']', '')

        if ',' in artists_id:
            lista = artists_id.split(', ')
            for artist in lista:
                veces = auxiliar.get(artist, 0)
                if veces == 0:
                    auxiliar[artist] = 1
                    count += 1
        else:
            veces = auxiliar.get(artists_id, 0)
            if veces == 0:
                auxiliar[artists_id] = 1
                count += 1

    return count


# Funciones imprimir

def printArtistInfo (artist):
    name = artist['DisplayName']
    YOB = artist['BeginDate']
    YOD = artist['EndDate']
    nationality = artist['Nationality']
    gender = artist['Gender']
    print('Nombre: ' + name + '. Año de nacimiento: ' + YOB 
           + '. Año de fallecimiento: ' + YOD + '. Nacionalidad: ' + nationality
           + '. Género: ' + gender)


def printArtistsInRange(result):
    size = lt.size(result)
    print ('\nHay ' + str(size) + ' artistas nacidos en este rango de tiempo.')
    if size <= 6:
        print('Los artistas encontrados fueron:')
        for artist in lt.iterator(result):
            printArtistInfo(artist)
    else:
        print('Los primeros y últimos tres artistas encontrados fueron:')
        first = lt.subList(result, 1, 3)
        last = lt.subList(result, size-3, 3)
        for artist in lt.iterator(first):
            printArtistInfo(artist)

        for artist in lt.iterator(last):
            printArtistInfo(artist)


def printDateAcquired(result):
    size = lt.size(result)
    print('\nEl MoMA adquirió ' + str(size) + ' obras en este rango de tiempo')
    purchase = str(countPurchase(result))
    artists = str(countArtists(result))
    print('Con ' + artists + ' artistas distintos y ' +
          purchase + ' de estas obras compradas.')
    print('\nLas primeras y últimas obras de arte son:')
    artworkInfo(result)


def printNationality(result):
    top10 = result[0]
    top1 = result[1]
    print('\nEl TOP 10 de nacionalidad en el MoMA es:')

    for top in top10:
        print(top)

    print('\nEl TOP de nacionalidad en el MoMA es: ' + str(top10[0][0]) +
          ' con ' + str(top10[0][1]) + ' obras de arte.')
    print('\nLos primeros y ultimo tres en la lista de obras ' +
          str(top10[0][0]) + ' son:\n')
    artworkInfo(top1)


def printDepartment(result, search):
    artworks = result[2]
    size = lt.size(artworks)
    print('\nEl MoMA va a transportar ' + str(size) +
          ' objetos del departamento de ' + str(search))
    print('Peso estimado (kg): ' + str(result[1]))
    print('El costo estimado de transporte (USD): ' + str(result[0]))


def printArtworkInfo(artwork):
    print('Título: ' + artwork['Title'] + ' Fecha: ' + artwork['Date'] +
                ' Medio: ' + artwork['Medium'] +
                ' Dimensiones: ' + artwork['Dimensions'])


def printArtworkInfoWithDate(artwork):
    print('Título: ' + artwork['Title'] + ' Fecha: ' + artwork['Date'] + 
                ' Fecha de adquisición: ' + artwork['DateAcquired'] +
                ' Medio: ' + artwork['Medium'] +
                ' Dimensiones: ' + artwork['Dimensions'])


def printArtworkInfoWithCost(artwork):
    print('Título: ' + artwork['Title'] + ' Fecha: ' + artwork['Date'] +
                ' Medio: ' + artwork['Medium'] +
                ' Dimensiones: ' + artwork['Dimensions'] + ' Costo (USD): ' +
                str(artwork['TransCost (USD)']))


def printTechniques(result):
    size = lt.size(result)
    if size < 6:
        print('Las obras con esta técnica son:')
        for artwork in lt.iterator(result):
            printArtworkInfo(artwork)
    else:
        first = lt.subList(result, 1, 3)
        last = lt.subList(result, size-3, 3)
        for artwork in lt.iterator(first):
            printArtworkInfo(artwork)

        for artwork in lt.iterator(last):
            printArtworkInfo(artwork)

# Menu


def printMenu():
    print("\nBienvenido")
    print('0- Cargar Datos')
    print("1- Consultar los artistas segun su año de nacimiento")
    print("2- Consultar las obras segun su fecha de adquisicion")
    print("3- Consultar las obras de un artista por tecnica")
    print("4- Consultar las obras por la nacionalidad de sus artistas")
    print("5- Consultar el costo de transportar las obras")
    print("0- Salir")


catalog = None


"""
Menu principal
"""
while True:
    printMenu()
    inputs = int(input('Seleccione una opción para continuar\n'))

    if inputs == 0:
        print("Cargando información de los archivos ....")
        start_time = time.perf_counter()
        catalog = initCatalog()
        loadData(catalog)
        controller.sortBeginDate(catalog)
        controller.sortDateAcquired(catalog)
        stop_time = time.perf_counter()
        delta_time = (stop_time - start_time) * 1000
        print(delta_time)
        print('Artistas cargados: ' + str(lt.size(catalog['artists'])))
        print('Obras cargadas: ' + str(lt.size(catalog['artworks'])))

    elif inputs == 1:
        inicio = int(input('Ingrese el año inicial: '))
        fin = int(input('Ingrese el año final: '))
        result = controller.getArtistsInRange(catalog, inicio, fin)
        printArtistsInRange(result)

    elif inputs == 2:
        inicio = str(input('Ingrese la fecha inicial (AAAA-MM-DD): '))
        fin = str(input('Ingrese la fecha final (AAAA-MM-DD): '))
        result = controller.getDateAcquired(catalog, inicio, fin)
        printDateAcquired(result)

    elif inputs == 3:
        artistname = str(input('Introduzca el nombre del artista a examinar: '))
        num, num_techs, top_medium, artworks, n_top = controller.getMedia(catalog, artistname)
        print('\n' + artistname + 'tiene ' + str(num) +
              ' piezas a su nombre en el museo.')
        print('Hay un total de ' + str(num_techs) + ' técnicas a su nombre.')
        print('La técnica más utilizada por este/esta artista es ' + top_medium
              + ' con un total de ' + str(n_top) + ' obras con esta técnica.')
        printTechniques(artworks)

    elif inputs == 4:
        result = controller.getTopNactionalities(catalog)
        printNationality(result)

    elif inputs == 5:
        search = str(input('Ingrese el departamento del MoMA: '))
        result = controller.getCost(catalog, search)
        printDepartment(result, search)

        artworks = result[2]
        sorted = controller.sortExpensive(artworks)
        mostExpensive = lt.subList(sorted, 1, 5)
        sorted = controller.sortOldest(artworks)
        oldest = lt.subList(sorted, 1, 5)
        print('\nLos 5 objetos más costosos de transportar son:')
        for artwork in lt.iterator(mostExpensive):
            printArtworkInfoWithCost(artwork)

        print('\nLos 5 objetos más antiguos a transportar son:')
        for artwork in lt.iterator(oldest):
            printArtworkInfoWithCost(artwork)



    else:
        sys.exit(0)

sys.exit(0)
