#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
////////////////////////////////////////////////////////////////////
//   AUTOR: Andrés R. Philipps Benítez              Diciembre/2021
////////////////////////////////////////////////////////////////////
//   
//   PROGRAMA:   vpclases                VERSIÓN: 1.0      
//   DISPOSITIVO: Broadcom BCM2837B0, Cortex-A53 (ARMv8) 64-bit SoC                              
//   S.O.: BULLSEYE (64 BITS) 				Versión Python:   3.7.3                             
//   TARJETA DE APLICACIÓN: Raspberry Pi 4 B                    
////////////////////////////////////////////////////////////////////
        Explicación del programa:
    El objetivo de este programa es ser importado en el 
programa principal "Proyecto_Voz-Pandas.py" ya que aquí vienen
implementadas todas las clases y funciones necesaria para su 
funcionamiento.

Es necesario poner;
import vpclases

Y que ambos archivos estén en la misma carpeta.
////////////////////////////////////////////////////////////////////
"""
#/////////////////////////////////////////////////////////////////////
# IMPORTAR LIBRERÍAS E INSTANCIAR CLASES
#/////////////////////////////////////////////////////////////////////

#Librerías del sistema operativo y para sacar el tiempo
import os, time

#Librería para la base de datos
import pandas as pd
import matplotlib.pyplot as plt

#Librería para convertir de texto a voz
from gtts import gTTS

#Librería para el reconocimiento de voz
import speech_recognition as sr

#Librerías para generar valores y nombres aleatorios
from random import choice
from random import randint

#Librerías para enviar por correo archivos adjuntos
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

#/////////////////////////////////////////////////////////////////////
# FUNCIONES
#/////////////////////////////////////////////////////////////////////

#Creo una variable con la ruta actual del proyecto
ruta_proyecto = "/home/pi/_myDrew_/Proyecto_Voz-Pandas/"

#=======================================================

#Clase encargada de la base de datos
class baseDatosDrew():
    """"Esta clase se encargará de crear tablas, y modificarlas"""
    def __init__(self) -> None:
        pass

    #Función que necesita los parámetros de tabla, nombre, edad, altura, peso y genero
    #para crear la tabla
    def crearDataFrame(self, tabla:str,nombre, edad, altura, peso, genero ):
        print(f"CREADA LA TABLA: {tabla}")
        tabla = {'NOMBRE':[nombre], 'EDAD':[edad], 'ALTURA':[altura], 'PESO':[peso], 'GENERO':[genero]}
        df = pd.DataFrame(tabla)
        print(df)
        return df

    #Función que necesita los parámetros df y tabla, para
    #graficar
    def graficarDataFrame(self, df, tabla):
        print("Almacenado y graficando tablas...")
        print(df)

        #Almaceno la tabla creada en formato .csv
        df.to_csv(f"{ruta_proyecto}{tabla}.csv")
    
        #Almaceno la tabla creada en formato .xlsx
        df.to_excel(f"{ruta_proyecto}{tabla}.xlsx")
        
        #Genero una gráfica tipo Pie de la columna GENERO
        #y la guardo en formato .jpg
        df.value_counts("GENERO").plot.pie(autopct='%1.1f%%')
        plt.savefig(f"{ruta_proyecto}{tabla}_grafica_GENERO.jpg", bbox_inches='tight')

        #Genero una gráfica tipo Line de las columnas ALTURA Y PESO,
        #y la guardo en formato .jpg
        df.sort_values("PESO").plot.line(y="ALTURA", x="PESO")
        plt.savefig(f"{ruta_proyecto}{tabla}_grafica_ALTURA-PESO.jpg", bbox_inches='tight')
        
        #Muestro por pantalla ambas gráficas
        plt.show()
        
#=======================================================

#Clase encargada de convertir textos a voz
class vozDrew():
    
    def __init__(self) -> None:
        pass
    
    #Función de acceso rápido para acortar las líneas, necesita los 
    #parámetros de texto que es lo que va reproducir la voz, y archi 
    #que es el nombre temporal del archivo.mp3
    def voz(self, texto, archi):
        x(f"{texto}", lang="es-ES").save(f'{archi}.mp3')
        os.system(f'mpg123 -q {archi}.mp3')

    def intro(self):
        vd = vozDrew()
        vd.voz("""HOLA BUENOS DÍAS, EN ESTE PROYECTO VAMOS A CREAR UNA BASE DE DATOS,
        PARA ELLO NECESITARÉ LOS SIGUIENTES DATOS.
        NOMBRE, EDAD, ALTURA, PESO Y GÉNERO""","intro")
        
        vd.voz("""SI QUIERE QUE SIGAMOS CON EL PROCESO, DIGA "INICIAR".
        SI QUIERE DESCANSAR DIGA "PARAR".""","espera")

    def cancelar(self):
        vd = vozDrew()
        vd.voz("""CANCELANDO EL PROCESO.""","cancel")

    def orden(self, estado:bool):
        vd = vozDrew()
        if estado is True:
            vd.voz("""INICIANDO...""","iniciando")
        if estado is False:
            vd.voz("""ESPERARÉ HASTA QUE DIGAS INICIAR...""","parando")

    def preguntaSeguir(self):
        vd = vozDrew()
        vd.voz("""¿DESEAS FINALIZAR O AÑADIR MAS PERSONAS?. 
        LE RECUERDO QUE SOY CAPAZ DE GENERAR DIEZ IDENTIDADES MÁS DE FORMA ALEATORIA.
        SI DESEA FINALIZAR, DIGA FINALIZAR.
        SI DESEA AÑADIR PERSONALMENTE MAS IDENTIDADES, DIGA AÑADIR
        SI DESEA QUE GENERE DIEZ IDENTIDADES MÁS, DIGA ALEATORIO""","pregunta")

    def preguntaCorta(self):
        vd = vozDrew()
        vd.voz("""DIGA FINALIZAR, AÑADIR O ALEATORIO.""","pregunta_corta")

    def despedida(self, tabla):
        vd = vozDrew()
        vd.voz(f"""HASTA AQUÍ LA CREACIÓN DE LA BASE DE DATOS LLAMADA{tabla}.
        ESPERO QUE LA EXPERIENCIA HAYA SIDO DE BUEN AGRADO ""","despedida")

    def paradaForzada(self):
        vd = vozDrew()
        vd.voz("""LO SIENTO, HAS DICHO PARAR EN UN MOMENTO QUE NO DEBÍAS
        ASÍ QUE DARÉ POR FINALIZADO EL PROGRAMA PERO NO GUARDARÉ LA TABLA QUE ESTABAS CREANDO.
        CUANDO TENGAS GANAS DE CUMPLIR CON LAS REGLAS, VUELVE A INICIAR.""","paradaforzada")

#=======================================================

#Instancio la clase de reconocimiento
r = sr.Recognizer()

#Clase para el reconocimiento de voz
class microDrew():
    def __init__(self) -> None:
        pass
    
    #Función de acceso rápido para el reconocimiento de voz,
    #no necesita ningún parámetro
    def preguntar(self):
        #with...as.. : Es una estructura útil puesto que abre una ventana
        #temporal de los recursos a usar y después los cierra
        with sr.Microphone() as source:
            #Primero escucha
            audio = r.listen(source)
            #Convierte en texto lo reconocido en idioma Español
            text = r.recognize_google(audio, language='es-ES')
        return text

#=======================================================

#Variables necesarias para generar identidades aleatorias
random_genero = ["Hombre", "Mujer"]
random_nombre = ["Carlos", "Alejandro", "Estefanía", 
    "Lucía", "Ramón", "Carla", "Eva", "Yolanda", "Alfredo",
    "Juan", "Luis"]
random_apellido = ["Lumier", "Romero", "González", 
    "Martínez", "Cardones", "Lorenzo", "García", "Remedios", 
    "del Valle", "Quiroga", "López"]

#Clase encargada de recoger o generar los parámetros para la tabla
class paramDrew():
    def __init__(self) -> None:
        pass
    
    #Primero recoge cómo se llamará la tabla
    def nombreTabla(self):
        md = microDrew() 
        vd = vozDrew()
        
        vd.voz("¿CÓMO SE LLAMARÁ LA TABLA?","TABLA")
        tabla = md.preguntar().title()
        print(f"Tabla: {tabla}")
        return tabla

    #Recoge los parámetros de nombre, edad, altura, peso y genero
    def parametros(self):
        md = microDrew()
        vd = vozDrew()

        vd.voz("DIGA UN NOMBRE Y APELLIDO","NOMBRE")
        nombre = md.preguntar().title()  #Pone en mayuscula la primera letra de cada palabra
        print(f"Nombre: {nombre}")

        vd.voz("DIGA UNA EDAD","EDAD")
        edad = int(md.preguntar())
        print(f"Edad: {edad}")

        vd.voz("DIGA LA ALTURA EN METROS","ALTURA")
        altura = float(md.preguntar())/100  #Divide entre 100 para pasarlo a metros
        print(f"Altura: {altura}")

        vd.voz("DIGA EL PESO EN KILOGRAMOS","PESO")
        peso = int(md.preguntar())
        print(f"Peso: {peso}")
        
        vd.voz("ES HOMBRE O MUJER?","GENERO")
        genero = md.preguntar().capitalize()    #Pone en mayúscula únicamente la primera letra
        #Estructura para verificar que se dice Hombre o Mujer
        while True:
            if (genero == "Hombre" or genero == "Mujer"):
                break
            else: 
                vd.voz("ES HOMBRE O MUJER?","GENERO")
                genero = md.preguntar().capitalize()
                pass
        print(f"Genero: {genero}")

        #finalmente devuelve todos los parámetros que ha ido recogiendo
        return nombre, edad, altura, peso, genero

    #Función que genera identidades aleatorias
    def randomParam(self, num, df):
        #Genera num identidades
        for i in range(num):
            #Elije un nombre aleatorio
            name = choice(random_nombre)
            #Elije un apellido aleatorio
            apellido = choice(random_apellido)
            #Los eliminia de la lista principal para evitar
            #que se repita
            random_nombre.remove(name)
            random_apellido.remove(apellido)
            #Los suma de tal manera que; "Nombre Apellido"
            nombre = name +" "+ apellido
            #Para esa identidad genera una edad aleatoria entre 18 y 34 años
            edad = randint(18,34)

            #Estrucura para verificar si la identidad creada es Hombre o Mujer
            #Y dependiendo de su genero, generar un peso y una altura aleatoria
            gen_1 = name.endswith("a")
            gen_2 = name.endswith("ía")
            if (gen_1==True or gen_2==True):
                genero = "Mujer"
                peso = randint(49,72)
                altura = randint(152,176)/100
            else: 
                genero = "Hombre"
                peso = randint(65,98)
                altura = randint(163,194)/100

            #Añadir todos los parámetro de la identidad generada a la tabla
            df = df.append({'NOMBRE':nombre,'EDAD':edad,'ALTURA':altura,'PESO':peso,'GENERO':genero}, ignore_index=True)
        return df

#=======================================================

#Clase encargada de enviar emails
class emailDrew():
    
    def __init__(self) -> None:
        pass

    def enviarAdjuntosEmail(self, tabla):
        #Ponemos los archivos que vamos a adjuntar en función del nombre de la tabla
        files = [f'{tabla}.csv', f'{tabla}.xlsx', f'{tabla}_grafica_ALTURA-PESO.jpg', f'{tabla}_grafica_GENERO.jpg']

        remitente = 'electronpb.ar@gmail.com'
        destinatarios = ['andresphibe@outlook.es', 'jlval@cifpn1.es']
        asunto = '[RPI] Archivo CSV'
        cuerpo = f'''Buenas,

        - Envío este correo desde la Raspberry Pi-  

Además, te adjunto la tabla "{tabla}" del proyecto que te acabo de pasar, en formato ".csv" y ".xlsx".
Este último para que puedas abrirlo con el Excel.
Por último, te adjunto también la gráfica tipo "Pie" de los géneros y la gráfica tipo "Line" de la relación altura-peso.

Un saludo...    < Andrés R. Philipps Benítez >
        
Este mensaje ha sido enviado a las {time.strftime("%H:%M:%S")} del {time.strftime("%d/%m/%y")}.'''
        # Creamos el objeto mensaje
        mensaje = MIMEMultipart()
        
        # Establecemos los atributos del mensaje
        mensaje['From'] = remitente
        mensaje['To'] = ", ".join(destinatarios)
        mensaje['Subject'] = asunto
        
        # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
        mensaje.attach(MIMEText(cuerpo, 'plain'))
        
        #Usamos un for para adjuntar cada uno de los archivos de la lista files
        for f in files:
            # Creamos un objeto MIME base
            part = MIMEBase('application', 'octet-stream')
            # Y le cargamos el archivo adjunto en la ruta correspondiente
            part.set_payload(open(f"{ruta_proyecto}{f}", "rb").read())
            # Codificamos el objeto en BASE64
            encoders.encode_base64(part)
            # Agregamos una cabecera al objeto
            part.add_header('Content-Disposition', "attachment; filename= {0}".format(os.path.basename(f)))
            # Y finalmente lo agregamos al mensaje el adjunto
            mensaje.attach(part)

        # Creamos la conexión con el servidor
        sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)
        
        # Ciframos la conexión
        sesion_smtp.starttls()

        # Iniciamos sesión en el servidor
        sesion_smtp.login('electronpb.ar@gmail.com','Log_x081')

        # Convertimos el objeto mensaje a texto
        texto = mensaje.as_string()

        # Enviamos el mensaje
        sesion_smtp.sendmail(remitente, destinatarios, texto)

        # Cerramos la conexión
        sesion_smtp.quit()

#=======================================================
