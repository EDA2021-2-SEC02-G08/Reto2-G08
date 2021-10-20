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
from itertools import islice
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
               'dateAcquired': None,
               'ID-Media': None,
               'nationality': None,
               'ArtistNames': None}

    catalog['artists'] = lt.newList('ARRAY_LIST')
    catalog['artworks'] = lt.newList('SINGLE_LINKED')

    """
    A continuacion se crean indices por diferentes criterios
    para llegar a la informacion consultada.
    Estos indices no replican informacion, solo la referencian.
    """

    """
    Indice para almacenar las obras por fecha de adquisición.
    Factor de carga = N / M
    0.75 = 425 / 570,
    donde 350 es el total de fechas de adquisición en el csv large.
    """
    catalog['dateAcquired'] = mp.newMap(570,
                                        maptype='CHAINING',
                                        loadfactor=0.75)

    """
    Indice para almacenar las técnicas por ConstituentID.
    Factor de carga = N / M
    0.75 = 16000 / 22000,
    donde 16000 es el total de artistas en el csv large.
    """
    catalog['ID-Media'] = mp.newMap(22000,
                                     maptype='CHAINING',
                                     loadfactor=0.75)

    """
    Indice para almacenar la nacionalidad por ID.
    """
    catalog['constituentID'] = mp.newMap(22000,
                                         maptype='CHAINING',
                                         loadfactor=0.75)

    
    """
    Índice para almacenar el nombre de un artista y su ID.
    """
    catalog['ArtistNames'] = mp.newMap(22000,
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
    artists_id = artwork['ConstituentID'].replace('[', '').replace(']', '')
    artists_id = artists_id.split(', ')

    for id in artists_id:
        addIDMedia(catalog, id, artwork)
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


def addName(catalog, artist):
    names = catalog['ArtistNames']
    name = artist['DisplayName']
    name_exists = mp.contains(names, name)

    if name_exists:
        pass
    else:
        mp.put(names, name, artist['ConstituentID'])


def addDateAcquired(catalog, artwork):
    """
    Esta función crea la siguiente estructura de datos:
    {'key': dateAcquired, 'value': [artworks]}
    """
    dateAcquired = artwork['DateAcquired']

    if dateAcquired != '':
        exist_date = mp.contains(catalog['dateAcquired'], dateAcquired)
        arrayList = lt.newList('ARRAY_LIST')

        if exist_date:
            pass
        else:
            mp.put(catalog['dateAcquired'], dateAcquired, arrayList)

        pair = mp.get(catalog['dateAcquired'], dateAcquired)
        arrayList = me.getValue(pair)
        lt.addLast(arrayList, artwork)


def addIDMedia(catalog, id, artwork):
    """
    Esta función crea la siguiente estructura de datos
    por id_artist en catalog['medium']:
    {'key': id, 'value': {'key': 'medium', 'value':[artworks]}}
    """
    ids = catalog['IDMedia']
    exist_id = mp.contains(ids, id)

    if exist_id:
        pass
    else:
        map = mp.newMap(70,
                    maptype='CHAINING',
                    loadfactor=0.75)
        mp.put(ids, id, map)

    key = mp.get(ids, id)
    map = me.getValue(key)
    medium = artwork['Medium']
    exist_medium = mp.contains(map, medium)

    if exist_medium:
        pass
    else:
        arrayList = lt.newList('ARRAY_LIST')
        mp.put(map, medium, arrayList)

    medium = mp.get(map, medium)
    artworks = me.getValue(medium)
    lt.addLast(artworks, artwork)


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


def take(n, iterable):
    "Return first n items of the iterable as a list"

    return list(islice(iterable, n))


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

def YearBinarySearch(catalog, element):
    """
    Retorna la posición de un elemento en una lista organizada.
    Esta función encuentra el año de nacimiento del artista.
    En caso de no existir, retorna la última posición encontrada.
    """
    low = 0
    high = lt.size(catalog) - 1
    mid = 0

    while low <= high:
        mid = (high + low) // 2
        cmp = lt.getElement(catalog, mid)
        if int(cmp['BeginDate']) < element:
            low = mid + 1
        elif int(cmp['BeginDate']) > element:
            high = mid - 1
        else:
            return mid

    return mid

# Funciones de consulta

def getArtistsInRange(catalog, inicio, fin):
    """
    Retorna un arrayList con los artistas
    en un rango de tiempo.
    """
    artists = catalog['artists']
    pos_inicio = YearBinarySearch(artists, inicio)
    pos_fin = YearBinarySearch(artists, fin)
    n = pos_fin-pos_inicio
    sublist = lt.subList(artists, pos_inicio, n)

    return sublist

def getDateAcquired(catalog, inicio, fin):
    """
    Retorna un arrayList con las obras de arte
    en un rango de fechas de adquisición.
    """
    arrayList = mp.keySet(catalog['dateAcquired'])
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


def getTopNactionalities(catalog):
    """
    Retorna el TOP 10 de nacionalidades por obras.
    Retorna un arrayList con todas las obras de la
    nacionalidad más recurrente en el MoMA.
    """
    auxiliar = {}
    nationalities = mp.keySet(catalog['nationality'])

    for nationality in lt.iterator(nationalities):
        if nationality != 'Nationality unknown':
            if nationality != '':
                pair = mp.get(catalog['nationality'], nationality)
                value = me.getValue(pair)
                auxiliar[nationality] = lt.size(value)

    auxiliar_sorted = dict(sorted(auxiliar.items(), key=lambda item: item[1],
                           reverse=True))
    top10 = take(10, auxiliar_sorted.items())
    top1 = take(1, auxiliar_sorted.items())
    pair = mp.get(catalog['nationality'], top1[0][0])
    arrayList = me.getValue(pair)

    return top10, arrayList


def getArtistID (catalog, artistname):
    names = catalog['ArtistNames']
    exists = mp.contains(names, artistname)
    if exists:
        pair = mp.get(names, artistname)
        id = me.getValue(pair)
        return int(id)
    return None


def getMedia(catalog, artist):
    IDs = catalog['IDMedia']
    id = getArtistID(catalog, artist)
    if id is not None:
        pair = mp.get(IDs, id)
        media_map = me.getValue(pair)
        media = mp.keySet(media_map)
        N_media = lt.size(media)
        N_artworks = 0
        top_artworks = None
        top_medium = None
        N_top = 0
        for medium in lt.iterator(media):
            pair = mp.get(media_map, medium)
            artworks = me.getValue(pair)
            N = lt.size(artworks)
            N_artworks += N
            if N > N_top:
                top_medium = medium
                N_top = N
                top_artworks = artworks

        return N_artworks, N_media, top_medium, top_artworks, N_top

    return None

# Funciones de comparación


def cmpDateAcquired(date1, date2):
    return date.fromisoformat(date1) < date.fromisoformat(date2)

def cmpBeginDate(artist1, artist2):
    """
    Retorna True si el 'BeginDate' de artist1
    es menor que el de artist2.
    """
    return int(artist1['BeginDate']) < int(artist2['BeginDate'])


# Funciones de ordenamiento


def sortDateAcquired(arrayList):
    mg.sort(arrayList, cmpDateAcquired)

def sortBeginDate(catalog):
    mg.sort(catalog['artists'], cmpBeginDate)
