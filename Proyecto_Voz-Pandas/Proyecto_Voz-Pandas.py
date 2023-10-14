#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
////////////////////////////////////////////////////////////////////
//   AUTOR: Andrés R. Philipps Benítez              Diciembre/2021
////////////////////////////////////////////////////////////////////
//   
//   PROGRAMA:   Proyecto Voz-Pandas                VERSIÓN: 1.0      
//   DISPOSITIVO: Broadcom BCM2837B0, Cortex-A53 (ARMv8) 64-bit SoC                              
//   S.O.: BULLSEYE (64 BITS) 				Versión Python:   3.7.3                             
//   TARJETA DE APLICACIÓN: Raspberry Pi 4 B                    
////////////////////////////////////////////////////////////////////
        Explicación del programa:
    El objetivo fundamental de este programa es la creación de una
base de datos sencilla mediante la libreria "Pandas", para 
posteriormente mostrar dos gráficas.
    En este caso, la base de datos estará formada por una única tabla
cuyo nombre será el que el usuario desee. Dicha tabla tendrá los 
siguientes parámetros:
    |   NOMBRE  |   EDAD    |   ALTURA  |   PESO    |   GENERO  |

    Para ir completándola, una voz proporcionada por la librería
"gTTS" irá guiando al usuario.
    Este programa, necesita la librería "vpclases" para su  correcto
funcionamiento, puesto que en ella vienen todas las clases y funciones
definidas por el autor.

    Los materiales necesarios son:
    - Una Raspberry Pi (3b+ ó 4b)
    - Un altavoz con conector tipo Jack 3.5mm
    - Un micrófono

    A parte, de las funciones básicas requeridas en el enunciado,
se le han añadido nuevas funcionalidades:
    - Generación de diez identidades aleatorias para que la tabla
    resultante tenga una mayor riqueza de información
    - Almacenar la tabla resultante en formato .csv y .xlsx con el
    nombre que el usuario ha puesto a la tabla.
    - Alamacenar las dos gráficas resultantes en formato .jpg, 
    especificando el nombre de la tabla y el tema de la gráfica.
    - Enviar por correo electrónico un email a tantas personas como
    se desee, adjuntando los cuatro archivos almacenados anteriormente
////////////////////////////////////////////////////////////////////
"""
#/////////////////////////////////////////////////////////////////////
# IMPORTAR LIBRERÍAS E INSTANCIAR CLASES
#/////////////////////////////////////////////////////////////////////
#Importamos la librería vpclases necesaria
import vpclases
#De la libreria time importamos sleep para añadir algun retardo
from time import sleep

#Se instacian las clases propias del autor:
#Clase para crear, modificar y graficar la base de datos
bddrew = vpclases.baseDatosDrew()  
#Clase para la comunicación de salida por voz con el usuario
vdrew = vpclases.vozDrew()
#Clase para que el usuario interactúe con el sistema por el micrófono
micdrew = vpclases.microDrew()
#Clase para modificar los parámetros de la tabla y generar identidades
pardrew = vpclases.paramDrew()
#clase para enviar emails con los archivos generados al final
edrew = vpclases.emailDrew()

#/////////////////////////////////////////////////////////////////////
# VARIABLES GLOBALES
#/////////////////////////////////////////////////////////////////////

#/////////////////////////////////////////////////////////////////////
# CONFIGURACIÓN PUERTOS GPIO Y RECURSOS A UTILIZAR
#/////////////////////////////////////////////////////////////////////
tabla = ""
#/////////////////////////////////////////////////////////////////////
# FUNCIONES
#/////////////////////////////////////////////////////////////////////

    # Se ubican todas en la librería vpclases

#/////////////////////////////////////////////////////////////////////
# PROGRAMA PRINCIPAL
#/////////////////////////////////////////////////////////////////////

vdrew.intro()   #Voz comunica al usuario sobre la intro del programa
print(" DIGA: 'INICIAR' O 'PARAR'")
text = micdrew.preguntar()  #Usuario debe decir "Iniciar" o "Parar"
while True:     #Bucle infinito
    try:
        if text=="iniciar":     #Si el usuario ha dicho "iniciar"..
            print("Iniciando..")
            #Funcion orden de la clase vozDrew 
            vdrew.orden(True)   
            #Funcion nombreTabla de la clase paramDrew
            tabla = pardrew.nombreTabla()
            #Guardo en variables los parametros pedidos por la funcion parametros de la clase paramDrew
            nombre, edad, altura, peso, genero = pardrew.parametros()
            #Guardo en la variable df el DataFrame resultante de la funcion crearDataFrame de la clase baseDatosDrew
            df = bddrew.crearDataFrame(tabla, nombre, edad, altura, peso, genero)
            #Funcion preguntaSeguir de la clase vozDrew
            vdrew.preguntaSeguir()
            #El usuario tiene que elegir entre añadir, aleatorio, o finalizar
            text = micdrew.preguntar()
            while text=="añadir":    #Mientras la respuesta del usuario sea añadir..
                #Se vuelve a preguntar por los parámetros
                nombre, edad, altura, peso, genero = pardrew.parametros()
                #Y se añaden al DataFrame ya creado
                df = df.append({'NOMBRE':nombre,'EDAD':edad,'ALTURA':altura,'PESO':peso,'GENERO':genero}, ignore_index=True)
                print(df)
                #Version acortada de preguntaSeguir
                vdrew.preguntaCorta()
                #El usuario debe elegir de nuevo entre añadir, aleatorio y finalizar
                text = micdrew.preguntar()
        elif text=="aleatorio":     #Si el usuario elige "aleatorio"..
            print('Generando diez identidades aleatorias...')
            #Genero diez identidades nuevas que son guardadas en el DataFrame
            df = pardrew.randomParam(10,df)
            #Obligo al programa a finalizar
            text = "finalizar"
        elif text=="parar":     #Si el usuario dijo "parar"..
            #Si la variable tabla está vacía, quiere decir que todavía no se 
            #había creado
            if tabla=="":   
                vdrew.orden(False)
                text = micdrew.preguntar()
            #Pero si ya estaba creada, quiere decir que el usuario dijo "parar"
            #en medio de la creación de la tabla
            else:
                print("PARADA FORZADA")
                #La voz te avisa de lo sucedido
                vdrew.paradaForzada()
                #Rompe el bucle While principal y termina el programa sin guardar nada
                break
        elif text=="finalizar":     #Si el usuario dijo "finalizar"..
            print("Adios..")
            #Función graficarDataFrame de la clase baseDatosDrew
            bddrew.graficarDataFrame(df, tabla)
            #Función enviarAdjuntosEmail de la clase emailDrew
            edrew.enviarAdjuntosEmail(tabla)
            #La voz se despide
            vdrew.despedida(tabla)
            #Y termina el programa
            break
        else: pass
    except KeyboardInterrupt:    #Si el usuario pulsa "Ctr+C"..
        print("SALIENDO POR TECLADO..")
        #Termina el programa
        break
    except:
        print("ERROR")
        #Retardo de 3 segundos por si un error hace entrar en bucle al programa
        sleep(3)

        