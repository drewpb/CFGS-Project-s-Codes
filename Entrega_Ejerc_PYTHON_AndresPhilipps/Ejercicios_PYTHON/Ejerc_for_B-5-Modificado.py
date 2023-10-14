#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
////////////////////////////////////////////////////////////////////////////////////
//   AUTOR:   ANDRÉS R. PHILIPPS BENÍTEZ                     Octubre/2021
////////////////////////////////////////////////////////////////////////////////////
//   PROGRAMA:      DIBUJAR RECTANGULOS                 VERSIÓN:              
//   Versión Python:   3.10                             
//                
////////////////////////////////////////////////////////////////////////////////////
                     Explicación del programa
////////////////////////////////////////////////////////////////////////////////////
"""
#////////////////////////////////////////////////////////////////////////////////////
# IMPORTAR LIBRERÍAS E INSTANCIAR CLASES
#////////////////////////////////////////////////////////////////////////////////////

#////////////////////////////////////////////////////////////////////////////////////
# VARIABLES GLOBALES
#////////////////////////////////////////////////////////////////////////////////////

#////////////////////////////////////////////////////////////////////////////////////
# CONFIGURACIÓN PUERTOS GPIO Y RECURSOS A UTILIZAR
#////////////////////////////////////////////////////////////////////////////////////

#////////////////////////////////////////////////////////////////////////////////////
# FUNCIONES
#////////////////////////////////////////////////////////////////////////////////////

def dibujar_rectangulo(ancho, alto, horz, vert, borde, relleno):
    for i in range(vert):
        print(f"{borde*(ancho*horz - (horz-1))}")
        for j in range(alto-2):
            print(f"{borde + (relleno*(ancho-2) + borde)*horz}")
    print(f"{borde*(ancho*horz - (horz-1))}")

#////////////////////////////////////////////////////////////////////////////////////
# PROGRAMA PRINCIPAL
#////////////////////////////////////////////////////////////////////////////////////
try:       
    print("""
    --- DIBUJANDO RECTÁNGULOS ---
    """)
    while True:
        alto = int(input("Escriba el número de altura individual: "))
        ancho = int(input("Escriba el número de ancho individual: "))
        vert = int(input("Números de rectángulos en el eje vertical: "))
        horz = int(input("Números de rectángulos en el eje horizontal: "))
        borde = " " + input("Escriba el caracter del borde: ") + " "
        relleno = " " + input("Escriba el caracter del relleno: ") + " "
        if (ancho<1 or alto<1 or vert<1 or horz<1):
            print("""
            !!SÓLO NÚMEROS POSITIVOS¡¡
            """)
        elif (len(borde)==3 and len(relleno)==3):       #VERIFICA QUE ESCRIBAS UN SOLO CARACTER
            dibujar_rectangulo(ancho, alto, horz, vert, borde, relleno)
        else:        #SI NO, TE ECHA LA BRONCA
            print("""
            !!TIENES QUE PONER UN CARACTER¡¡
            """)
        print()
        

except KeyboardInterrupt:         #Si el usuario pulsa CONTROL+C entonces...
    print("El usuario ha pulsado Ctrl+C...")
except:
    print("error inesperado")
finally:
    """
    CERRAMOS RECURSOS ABIERTOS
    """

