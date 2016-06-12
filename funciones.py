# Integrantes:
# 18000123-0 Perico Los Palotes
# 18000456-7 Fulanita de Tal
# 18000890-k Federico Santa Maria

# -*- coding: utf-8 -*-
from random import *

archivoCanciones = 'lista_de_canciones.txt'
archivoPlaylist  = 'listas_de_reproducciones.txt'

def obtener_canciones(archivo):
	#Leer el archivo
	fp 			= open(archivo, 'r')
	canciones 	= []
	for linea in fp:
		canciones.append(linea.strip().split('<SEP>'))
	#Ordenarlas por nombre de artista
	ordenadas 	= []
	for cancion in canciones:
		ordenadas.append([cancion[2], cancion[0], cancion[1], cancion[3]])
	ordenadas.sort()
	#Filtrar las palabras
	ordenadas 	= filtro_palabras_largas(ordenadas, 40)
	#Unirlas en string nuevamente
	canciones 	= []
	for cancion in ordenadas:
		canciones.append('<SEP>'.join([cancion[1], cancion[2], cancion[0], cancion[3]]))
	#Cerrar el archivo
	fp.close()
	#Retornar la lista ordenada y filtrada
	return canciones

def filtro_busqueda(palabrasClaves,todasCanciones):
	return []

def filtro_palabras_largas(todasCanciones,maximo):
	filtradas = []
	for cancion in todasCanciones:
		if len(cancion[0]) < 40 and len(cancion[-1]) < 40:
			filtradas.append(cancion)
	return filtradas

def generar_codigo(inicio,intermedio):
	return ""

def agregar_cancion(datos):
	return None

def eliminar_canciones(diccionarioCanciones):
	return None

def crear_Playlist(diccionarioCanciones):
	return None


def obtener_Playlist(archivo):
	return {}

def borrar_Playlist(diccionarioPlaylist,archivo):
	return None
