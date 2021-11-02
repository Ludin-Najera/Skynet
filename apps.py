import json
import string
import requests 
from tinydb import TinyDB, Query
import os
import aiml


k = aiml.Kernel()

BRAIN_FILE = "brain.dump"


if os.path.exists(BRAIN_FILE):
    print("Cargando desde archivo cerebral file: " + BRAIN_FILE)
    k.loadBrain(BRAIN_FILE)
else:
    print("Parsing aiml files")
    k.bootstrap(learnFiles="std-startup.xml", commands="LOAD AIML B")
    #k.bootstrap(learnFiles="asignacion.aiml")
    #k.bootstrap(learnFiles="asignacion.aiml", commands="load aiml b")
    #k.bootstrap(learnFiles="asignacion.aiml", commands="INFORMACION")
    #k.learn("std-startup.xml")
    #k.respond("LOAD AIML B")
    #k.respond("asignacion.aiml")
    print("Cargando Skynet: " + BRAIN_FILE)
    k.saveBrain(BRAIN_FILE)


db = TinyDB('conversations.json')
Usuario = Query()

 
#Variables para el Token y la URL del chatbot
TOKEN = "2064186165:AAHWqyRrGM6uBjckK5RJy9TulQwy8CVGMhs" #Cambialo por tu token
URL = "https://api.telegram.org/bot" + TOKEN + "/"
 
 



def update(offset):
    #Llamar al metodo getUpdates del bot, utilizando un offset
    respuesta = requests.get(URL + "getUpdates" + "?offset=" + str(offset) + "&timeout=" + str(100))
 
 
    #Decodificar la respuesta recibida a formato UTF8
    mensajes_js = respuesta.content.decode("utf8")
 
    #Convertir el string de JSON a un diccionario de Python
    mensajes_diccionario = json.loads(mensajes_js)
 
    #Devolver este diccionario
    return mensajes_diccionario
 
def leer_mensaje(mensaje):
 
    #Extraer el texto, nombre de la persona e id del último mensaje recibido
    texto = mensaje["message"]["text"]
    persona = mensaje["message"]["from"]["first_name"]
    id_chat = mensaje["message"]["chat"]["id"]
 
    #Calcular el identificador unico del mensaje para calcular el offset
    id_update = mensaje["update_id"]
 
    #Devolver las dos id, el nombre y el texto del mensaje
    return id_chat, persona, texto, id_update


def enviar_mensaje(idchat, texto):
    #Llamar el metodo sendMessage del bot, passando el texto y la id del chat
    requests.get(URL + "sendMessage?text=" + texto + "&chat_id=" + str(idchat))
 
 
 
#Variable para almacenar la ID del ultimo mensaje procesado
ultima_id = 0
 
while(True):
    mensajes_diccionario = update(ultima_id)
    for i in mensajes_diccionario["result"]:
 
        #Llamar a la funcion "leer_mensaje()"
        idchat, nombre, texto, id_update = leer_mensaje(i)
 
        #Si la ID del mensaje es mayor que el ultimo, se guarda la ID + 1
        if id_update > (ultima_id-1):
            ultima_id = id_update + 1



        #Generar una respuesta a partir de la informacion del mensaje
        #if "INFORMACION" == texto:
        #res = str(k.learn)
        #res2 = str(k.bootstrap)
        #if texto in str(k.respond):

        #if str(k.respond) in texto:
        
        #if k.respond(texto) in texto:
        #if k.respond() == texto:

            texto_respuesta = k.respond(texto)
        
#        elif "Adios" in texto:
#            texto_respuesta = "Hasta pronto!"
        
        #else:
        #    texto_respuesta = "Has escrito: \"" + texto + "\""
 
        #Enviar la respuesta
        
            enviar_mensaje(idchat, texto_respuesta)
 
    #Vaciar el diccionario
    mensajes_diccionario = [] 
