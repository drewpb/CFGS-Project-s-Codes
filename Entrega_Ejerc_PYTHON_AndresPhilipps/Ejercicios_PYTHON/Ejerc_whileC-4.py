#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
////////////////////////////////////////////////////////////////////////////////////
//   AUTOR:   ANDRÉS R. PHILIPPS BENÍTEZ                     Octubre/2021
////////////////////////////////////////////////////////////////////////////////////
//   PROGRAMA:     OPERACIONES(4)                  VERSIÓN:              
//   Versión Python:   3.10                             
//                
////////////////////////////////////////////////////////////////////////////////////
                     Explicación del programa
////////////////////////////////////////////////////////////////////////////////////
"""
#////////////////////////////////////////////////////////////////////////////////////
# IMPORTAR LIBRERÍAS E INSTANCIAR CLASES
#////////////////////////////////////////////////////////////////////////////////////

from random import randint
from time import time

#////////////////////////////////////////////////////////////////////////////////////
# VARIABLES GLOBALES
#////////////////////////////////////////////////////////////////////////////////////

#////////////////////////////////////////////////////////////////////////////////////
# CONFIGURACIÓN PUERTOS GPIO Y RECURSOS A UTILIZAR
#////////////////////////////////////////////////////////////////////////////////////

#////////////////////////////////////////////////////////////////////////////////////
# FUNCIONES
#////////////////////////////////////////////////////////////////////////////////////

#////////////////////////////////////////////////////////////////////////////////////
# PROGRAMA PRINCIPAL
#////////////////////////////////////////////////////////////////////////////////////
try:                
    print("""
    --- OPERACIONES(4) ---
    """) 
    while True:      #iniciamos un loop infinito
        cuestiones_cont = 0
        intentos_cont = 0
        cuestiones = int(input("¿Con cuántas operaciones correctas se acaba el programa?: "))
        tiempo = time()
        while ((cuestiones>0) and (cuestiones!=cuestiones_cont)):
            print()
            num1 = randint(1,100)
            num2 = randint(1,100)
            resultado = int(input(f"{num1} + {num2} = "))
            resultado_pro = num2+num1
            if (resultado != resultado_pro):
                intentos_cont+=1
                pass
            else:
                tiempo_total = time()-tiempo
                intentos_cont+=1
                cuestiones_cont+=1
                print("     ¡¡¡RESPUESTA CORRECTA!!!")
        print(f"""
            ¡¡ENHORABUENA!!

Has tardado {round(tiempo_total, 2)} segundos en acertar {cuestiones_cont} operación(es)
    y sólo te ha costado {intentos_cont} intento(s).
        """)

except KeyboardInterrupt:         #Si el usuario pulsa CONTROL+C entonces...
    print("El usuario ha pulsado Ctrl+C...")
except:
    print("error inesperado")
finally:
    """
    CERRAMOS RECURSOS ABIERTOS
    """

