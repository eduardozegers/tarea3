# -*- coding: utf-8 -*-
import web
import os
import re
from datetime import *
from web import form
from funciones import *

# Varaibles globales
global cancionesTodas,archivoCanciones,archivoPlaylist,nombre,slogan,porPagina

# Condiciones iniciales
cancionesTodas=[]
archivoCanciones="lista_de_canciones.txt"
archivoPlaylist="listas_de_reproducciones.txt"
nombre = "Pypotify"
slogan = "Bienvenido al sistema de gestión de canciones Pypotify.\n\
            Está es su página principal, donde podrá ingresar al menu de opciones para implementar sus funciones en el sistema."
porPagina = 5000

# Configuración de debug
web.config.debug = False

# Direcciones utilizadas
urls = (
  '/', 'index',
  '/canciones/','canciones',
  '/cancionNueva/','cancionNueva',
  '/buscar/','buscar',
  '/borrarCancion/','borrarCancion',
  '/verListas/','verListas',
  '/borrarListas/','borrarListas'
)

# Pubicacion del sitio template
render = web.template.render('templates/')

# Página de inicio
class index:
    def GET(self):
        return str(render.header("index"))+str(render.home(nombre,slogan,web.archnom))+str(render.footer())

# Página de canciones
class canciones:
    def GET(self):
        cancionesTodas = obtener_canciones(archivoCanciones)

        parametros = web.input()
        pagina = parametros.pagina if hasattr(parametros, 'pagina') else 1
        seudoFinal = (int(pagina) - 1) * porPagina
        paginas = len(cancionesTodas) / porPagina
        return str(render.header("canciones"))+str(render.canciones(data = {"cancionesTodas":cancionesTodas},paginas=int(paginas),paginaActual=int(pagina),final=int(seudoFinal),totalPaginas=int(porPagina)))+str(render.footer())

# Página para agregar una nueva canción
class cancionNueva:
    def GET(self):
        data = {"cancion":"","artista":""}
        return str(render.header("cancionNueva"))+str(render.agregarCancion(None,data))+str(render.footer())
    def POST(self):
        post_input = dict(web.input(_nethod='post'))
        del post_input["_nethod"]
        if post_input["cancion"]=="" and post_input["artista"]=="":
            return str(render.header("cancionNueva"))+str(render.agregarCancion("error",post_input))+str(render.footer())
        else:
            agregar_cancion(post_input)
            return str(render.header("cancionNueva"))+str(render.postAgregarCancion())+str(render.footer())

# Página para para buscar y luego crear una lista de canciones
class buscar:
    def GET(self):
        return str(render.header("lista"))+str(render.buscar(None))+str(render.footer())
    def POST(self):
        post_input = dict(web.input(_nethod='post'))
        del post_input["_nethod"]
        if "palabraClave" in post_input:
            cancionesTodas = obtener_canciones(archivoCanciones)
            cancionesEncontradas=filtro_busqueda(post_input["palabraClave"],cancionesTodas)
            if post_input["palabraClave"]=="":
                return str(render.header("lista"))+str(render.buscar(error="error1"))+str(render.footer())
            elif len(cancionesEncontradas)==0:
                return str(render.header("lista"))+str(render.buscar(error="error2"))+str(render.footer())
            else:
                return str(render.header("lista"))+str(render.postBuscar(cancionesEncontradas))+str(render.footer())
        else:
            crear_Playlist(post_input)
            return str(render.header("lista"))+str(render.finBuscar())+str(render.footer())

# Página para borrar canciones del archivo
class borrarCancion:
    def GET(self):
        return str(render.header("borrarCancion"))+str(render.borrarCancion(None))+str(render.footer())
    def POST(self):
        post_input = dict(web.input(_nethod='post'))
        del post_input["_nethod"]
        if "cancionesABorrar" in post_input:
            cancionesTodas = obtener_canciones(archivoCanciones)
            cancionesEncontradas=filtro_busqueda(post_input["cancionesABorrar"],cancionesTodas)
            if post_input["cancionesABorrar"]=="":
                return str(render.header("borrarCancion"))+str(render.borrarCancion(error="error1"))+str(render.footer())
            elif len(cancionesEncontradas)==0:
                return str(render.header("borrarCancion"))+str(render.borrarCancion(error="error2"))+str(render.footer())
            else:
                return str(render.header("borrarCancion"))+str(render.postBorrarCancion(cancionesEncontradas))+str(render.footer())
        else:
            eliminar_canciones(post_input)
            return str(render.header("borrarCancion"))+str(render.finBorrarCancion())+str(render.footer())

# Página para ver todas las listas existentes
class verListas:
    def GET(self):
        data=obtener_Playlist(archivoPlaylist)
        return str(render.header("verLista"))+str(render.verListas(data))+str(render.footer())

# Página para borrar listas
class borrarListas:
    def GET(self):
        data=obtener_Playlist(archivoPlaylist)
        return str(render.header("borrarListas"))+str(render.borrarListas(error=None,data=data))+str(render.footer())
    def POST(self):
        post_input = dict(web.input(_nethod='post'))
        data=obtener_Playlist(archivoPlaylist)
        del post_input["_nethod"]
        if len(post_input)==0:
            return str(render.header("borrarListas"))+str(render.borrarListas("error",data))+str(render.footer())
        else:
            borrar_Playlist(post_input,archivoPlaylist)
            return str(render.header("borrarListas"))+str(render.postBorrarListas())+str(render.footer())

# Página para páginas no encontrada (sutil esto)
def notfound():
    return web.notfound(str(render.header("index"))+str(render.notfound())+str(render.footer()))

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.notfound = notfound
    web.archnom=""
    app.run()
    #if web.archnom=="":
    #  return str(render.header("index"))+str(render.noingresado())+str(render.footer())