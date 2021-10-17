"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from datetime import date
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as mg
assert cf


# Construccion de modelos


def newCatalog():
    """
    Inicializa el catálogo de libros.
    Retorna el catalogo inicializado.
    """

    catalog = {'artists': None,
               'artworks': None,
               'constituentID': None,
               'dateAcquired_list': None,
               'dateAcquired': None,
               'id_medium': None,
               'nationality': None}

    catalog['artists'] = lt.newList('SINGLE_LINKED')
    catalog['artworks'] = lt.newList('SINGLE_LINKED')
    catalog['dateAcquired_list'] = lt.newList('ARRAY_LIST')

    """
    A continuacion se crean indices por diferentes criterios
    para llegar a la informacion consultada.
    Estos indices no replican informacion, solo la referencian.
    """

    """
    Indice para almacenar las obras por fecha de adquisición.
    Factor de carga = N / M
    0.75 = 72000 / 96000,
    donde 72000 es el total de fechas de adquisición en el csv large.
    """
    catalog['dateAcquired'] = mp.newMap(96000,
                                        maptype='CHAINING',
                                        loadfactor=0.75)

    """
    Indice para almacenar las técnicas por id_artist.
    Factor de carga = N / M
    0.75 = 16000 / 22000,
    donde 16000 es el total de artistas en el csv large.
    """
    catalog['id_medium'] = mp.newMap(22000,
                                     maptype='CHAINING',
                                     loadfactor=0.75)

    """
    Indice para almacenar la nacionalidad por ID.
    """
    catalog['constituentID'] = mp.newMap(22000,
                                         maptype='CHAINING',
                                         loadfactor=0.75)

    """
    Indice para almacenar las obras por nacionalidad.
    Factor de carga = N / M
    0.75 = 120 / 160,
    donde 120 es el total de nacionalidades en el csv large.
    """
    catalog['nationality'] = mp.newMap(160,
                                       maptype='PROBING',
                                       loadfactor=0.75)

    return catalog


# Agregar informacion al catalogo


def addArtist(catalog, artist):
    lt.addLast(catalog['artists'], artist)
    addID(catalog, artist)


def addArtwork(catalog, artwork):
    lt.addLast(catalog['artworks'], artwork)
    addDateAcquired(catalog, artwork)
    dates(catalog, artwork)
    artists_id = artwork['ConstituentID'].replace('[', '').replace(']', '')
    artists_id = artists_id.split(', ')

    for id in artists_id:
        addIdMedium(catalog, id, artwork)
        addNationality(catalog, id, artwork)


# Funciones para agregar informacion al catalogo


def addID(catalog, artist):
    """
    Esta función crea la siguiente estructura de datos:
    {'key': 'constituentID', 'value': 'nationality'}
    """
    id = artist['ConstituentID']
    id_exists = mp.contains(catalog['constituentID'], id)

    if id_exists:
        pass
    else:
        mp.put(catalog['constituentID'], id, artist['Nationality'])


def addDateAcquired(catalog, artwork):
    """
    Esta función crea la siguiente estructura de datos:
    {'key': dateAcquired, 'value': [artworks]}
    """
    dateAcquired = artwork['DateAcquired']
    exist_date = mp.contains(catalog['dateAcquired'], dateAcquired)
    arrayList = lt.newList('ARRAY_LIST')

    if exist_date:
        pass
    else:
        mp.put(catalog['dateAcquired'], dateAcquired, arrayList)

    pair = mp.get(catalog['dateAcquired'], dateAcquired)
    arrayList = me.getValue(pair)
    lt.addLast(arrayList, artwork)


def addIdMedium(catalog, id, artwork):
    """
    Esta función crea la siguiente estructura de datos
    por id_artist en catalog['medium]:
    {'key': id, 'value': {'key': 'medium', 'value':[artworks]}}
    """
    exist_id = mp.contains(catalog['id_medium'], id)
    map = mp.newMap(20,
                    maptype='CHAINING',
                    loadfactor=0.75)
    arrayList = lt.newList('ARRAY_LIST')

    if exist_id:
        pass
    else:
        mp.put(catalog['id_medium'], id, map)

    id = mp.get(catalog['id_medium'], id)
    map = me.getValue(id)
    medium = artwork['Medium']
    exist_medium = mp.contains(map, medium)

    if exist_medium:
        pass
    else:
        mp.put(map, medium, arrayList)

    medium = mp.get(map, medium)
    arrayList = me.getValue(medium)
    lt.addLast(arrayList, artwork)


def addNationality(catalog, id, artwork):
    """
    Esta función crea la siguiente estructura de datos:
    {'key': 'nationality', 'value': [artworks]}
    """
    pair = mp.get(catalog['constituentID'], id)
    nationality = me.getValue(pair)
    nationality_exists = mp.contains(catalog['nationality'], nationality)

    if nationality_exists:
        pass
    else:
        arrayList = lt.newList('ARRAY_LIST')
        mp.put(catalog['nationality'], nationality, arrayList)

    pair = mp.get(catalog['nationality'], nationality)
    arrayList = me.getValue(pair)
    lt.addLast(arrayList, artwork)


# Funciones auxiliares


auxiliar = {}


def dates(catalog, artwork):
    """
    Crea una arrayList con todas las fechas de adqusición.
    """
    arrayList = catalog['dateAcquired_list']
    dateAcquired = artwork['DateAcquired']
    if dateAcquired != '':
        if dateAcquired in auxiliar.keys():
            pass
        else:
            lt.addLast(arrayList, dateAcquired)
            auxiliar[dateAcquired] = 0


# Funciones de busqueda


def busquedabinaria(arrayList, element):
    low = 0
    high = lt.size(arrayList) - 1
    mid = 0
    element = date.fromisoformat(element)

    while low <= high:
        mid = (high + low) // 2
        cmp = lt.getElement(arrayList, mid)
        if date.fromisoformat(cmp) < element:
            low = mid + 1
        elif date.fromisoformat(cmp) > element:
            high = mid - 1
        else:
            return mid

    return mid


# Funciones de consulta


def getDateAcquired(catalog, inicio, fin):
    arrayList = catalog['dateAcquired_list']
    sortDateAcquired(arrayList)
    pos_inicio = busquedabinaria(arrayList, inicio)
    pos_fin = busquedabinaria(arrayList, fin)
    n = pos_fin - pos_inicio
    subList = lt.subList(arrayList, pos_inicio, n)
    artworks = lt.newList('ARRAY_LIST')

    for element in lt.iterator(subList):
        pair = mp.get(catalog['dateAcquired'], element)
        value = me.getValue(pair)
        for element in lt.iterator(value):
            lt.addLast(artworks, element)

    return artworks


def getOldestInMedium(catalog, n, medium):
    media_list = catalog['medium']
    medium_exists = mp.contains(media_list, medium)
    if medium_exists:
        medium1 = mp.get(media_list, medium)
        artworks = me.getValue(medium1)
        sortArtworks(artworks)
        return lt.subList(artworks, 1, n)


# Funciones de comparación


def cmpDateAcquired(date1, date2):
    return date.fromisoformat(date1) < date.fromisoformat(date2)


def compareArtworksByAge(artwork1, artwork2):
    age1 = artwork1['Date']
    age2 = artwork2['Date']
    return int(age1) < int(age2)


# Funciones de ordenamiento


def sortDateAcquired(arrayList):
    mg.sort(arrayList, cmpDateAcquired)


def sortArtworks(artworks):
    mg.sort(artworks, compareArtworksByAge)
