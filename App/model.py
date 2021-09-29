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
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf


# Construccion de modelos


def newCatalog():
    """
    Inicializa el catálogo de libros.
    Retorna el catalogo inicializado.
    """

    catalog = {'artists': None,
               'artworks': None,
               'id_medium': None,
               'medium': None}

    catalog['artists'] = lt.newList('SINGLE_LINKED')
    catalog['artworks'] = lt.newList('SINGLE_LINKED')

    """
    A continuacion se crean indices por diferentes criterios
    para llegar a la informacion consultada.
    Estos indices no replican informacion, solo la referencian.
    """

    """
    Indice para almacenar las técnicas por id_artist.
    """
    catalog['id_medium'] = mp.newMap(2000,
                                     maptype='CHAINING',
                                     loadfactor=3)

    """
    Indice para almacenar las obras por técnica.
    """
    catalog['medium'] = mp.newMap(2000,
                                  maptype='CHAINING',
                                  loadfactor=3)

    return catalog


# Funciones para agregar informacion al catalogo


def addArtist(catalog, artist):
    lt.addLast(catalog['artists'], artist)


def addArtwork(catalog, artwork):
    lt.addLast(catalog['artworks'], artwork)
    addMedium(catalog, artwork)
    artists_id = artwork['ConstituentID'].replace('[', '').replace(']', '')
    artists_id = artists_id.split(', ')

    for id in artists_id:
        addIdMedium(catalog, id, artwork)


def addIdMedium(catalog, id, artwork):
    """
    Esta función crea la siguiente estructura de datos
    por id_artist en catalog['medium]:
    {'key': id, 'value': {'key': 'medium', 'value':[artworks]}}
    """
    exist_id = mp.contains(catalog['id_medium'], id)
    map = mp.newMap(3,
                    maptype='CHAINING',
                    loadfactor=3)
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


def addMedium(catalog, artwork):
    """
    Esta función crea la siguiente estructura de datos:
    {'key': 'medium', 'value':[artworks]}
    """
    medium = artwork['Medium']
    exist_medium = mp.contains(catalog['medium'], medium)
    arrayList = lt.newList('ARRAY_LIST')

    if exist_medium:
        pass
    else:
        mp.put(catalog['medium'], medium, arrayList)

    pair = mp.get(catalog['medium'], medium)
    arrayList = me.getValue(pair)
    lt.addLast(arrayList, artwork)


# Funciones para creacion de datos

# Funciones de consulta

# Funciones de comparación


def compareMedium(medium, entry):
    pass


# Funciones de ordenamiento
