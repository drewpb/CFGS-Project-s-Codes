#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
////////////////////////////////////////////////////////////////////////////////////
//   AUTOR:   ANDRÉS R. PHILIPPS BENÍTEZ                     Octubre/2021
////////////////////////////////////////////////////////////////////////////////////
//   PROGRAMA: ADIVINAR NÚMEROS D-2                     VERSIÓN:              
//   Versión Python:   3.10                            
//                
////////////////////////////////////////////////////////////////////////////////////
                     Enunciado

Bucle ej-while (3) - D-2

Escriba un programa para jugar a adivinar un número 
(el usuario piensa un número y el programa tiene que adivinarlo). 
El programa empieza pidiendo entre qué números está el número a 
adivinar y después intenta adivinar de qué número se trata. El 
usuario va diciendo si el número que ha dicho el programa es menor, 
mayor o igual al buscado.
////////////////////////////////////////////////////////////////////////////////////
"""
#////////////////////////////////////////////////////////////////////////////////////
# IMPORTAR LIBRERÍAS E INSTANCIAR CLASES
#////////////////////////////////////////////////////////////////////////////////////

from random import randint
from time import sleep

#////////////////////////////////////////////////////////////////////////////////////
# VARIABLES GLOBALES
#////////////////////////////////////////////////////////////////////////////////////

espera = 1.5
intentos = 0
new_max = []
new_min = []

#////////////////////////////////////////////////////////////////////////////////////
# CONFIGURACIÓN PUERTOS GPIO Y RECURSOS A UTILIZAR
#////////////////////////////////////////////////////////////////////////////////////

#////////////////////////////////////////////////////////////////////////////////////
# FUNCIONES
#////////////////////////////////////////////////////////////////////////////////////

def switchComparar(resp):
    selector = {
        "mayor" : 0,
        "menor" : 1,
        "igual" : 2
    }
    func = selector.get(resp, lambda: "Texto inválido")
    if (func==0):
        numAdivNew_ = mayor(numAdivNew)
    elif (func==1):
        numAdivNew_ = menor(numAdivNew)
    elif (func==2):
        igual(intentos)
    else:
        print("Escribir únicamente mayor, menor o igual")
    return numAdivNew_
    
def mayor(num):
    new_min.append(num)
    numAdivMy = randint((max(new_min)+1), (min(new_max)-1))
    return numAdivMy

def menor(num):
    new_max.append(num)
    numAdivMn = randint((max(new_min)+1), (min(new_max)-1))
    return numAdivMn

def igual(intentos):
    if True:
        print(f"""   
    ¡¡HE ACERTADO!!

¡¡He necesitado {intentos} intentos!!
Gracias por jugar conmigo.
    """)
    return

#////////////////////////////////////////////////////////////////////////////////////
# PROGRAMA PRINCIPAL
#////////////////////////////////////////////////////////////////////////////////////
try:
    print("""
    --- ADIVINANDO NÚMEROS ---
    """)
    mini = int(input("Valor mínimo: "))
    maxi = int(input("Valor máximo: "))
    numAdiv = randint(mini, maxi)
    if mini<maxi:
        print(f"""Le dejo {espera} segundos para que piense un número 
entero entre {mini} y {maxi} a ver si lo adivino...""")   
        sleep(espera)
        new_max.append(maxi)
        new_min.append(mini)
        numAdivNew = numAdiv
        while (new_min<new_max):
            print()
            intentos+=1
            respuesta = input(f"¿Es {numAdivNew}?: ").lower()
            numAdivNew = switchComparar(respuesta)            

    else: print("""         -- NO HA SEGUIDO LAS NORMAS, ASÍ QUE NO JUEGO CONTIGO. --
        --- VUELVA A JUGAR CUANDO ESTÉ DISPUESTO A SEGUIRLAS ---""")

except KeyboardInterrupt:         #Si el usuario pulsa CONTROL+C entonces...
    print("El usuario ha pulsado Ctrl+C...")
except:
    print("error inesperado")
finally:
    """
    CERRAMOS RECURSOS ABIERTOS
    """

