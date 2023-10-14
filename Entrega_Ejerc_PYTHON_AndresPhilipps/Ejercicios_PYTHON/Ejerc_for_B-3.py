#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
////////////////////////////////////////////////////////////////////////////////////
//   AUTOR:   ANDRÉS R. PHILIPPS BENÍTEZ                     Octubre/2021
////////////////////////////////////////////////////////////////////////////////////
//   PROGRAMA:     CÁLCULO ESTIMADO                  VERSIÓN:              
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

#////////////////////////////////////////////////////////////////////////////////////
# VARIABLES GLOBALES
#////////////////////////////////////////////////////////////////////////////////////

#////////////////////////////////////////////////////////////////////////////////////
# CONFIGURACIÓN PUERTOS GPIO Y RECURSOS A UTILIZAR
#////////////////////////////////////////////////////////////////////////////////////

#////////////////////////////////////////////////////////////////////////////////////
# FUNCIONES
#////////////////////////////////////////////////////////////////////////////////////

def preguntas(preg):
    nota = 0.0
    for i in range(preg):
        num1 = randint(2,99)
        num2 = randint(2,99)
        verif = num1*num2
        resp = int(input(f"¿Cuánto es {num1} x {num2}? >> "))
        if (verif == resp):
            print("""           ¡¡¡RESPUESTA CORRECTA!!!
            """)
            nota += 10.0
        elif (verif < resp):
            diferencia = ((abs(verif-resp)/((verif+resp)/2))*100)
            print(f"""¡ERRASTE CON UNA DIFERENCIA DEL {round(diferencia, 2)}% POR ENCIMA!
            LA RESPUESTA CORRECTA ERA - {verif} -
            """)
            if (diferencia>=100):
                nota += 0
            else:
                nota = (100-diferencia)/10 + nota
        else:
            diferencia = ((abs(verif-resp)/((verif+resp)/2))*100)
            print(f"""¡ERRASTE CON UNA DIFERENCIA DEL {round(diferencia, 2)}% POR DEBAJO! 
            LA RESPUESTA CORRECTA ERA - {verif} -
            """)
            if (diferencia>=100):
                nota += 0
            else:
                nota = (100-diferencia)/10 + nota
    nota_fin = nota/(preg)
    print(f"LE CORRESPONDE UNA NOTA DE {round(nota_fin, 2)} SOBRE 10")

#////////////////////////////////////////////////////////////////////////////////////
# PROGRAMA PRINCIPAL
#////////////////////////////////////////////////////////////////////////////////////
try:         
    print("""
    --- CÁLCULO ESTIMADO ---
    """)
    while True:
        preg = int(input("""
    ¿Cuántas multiplicaciones quiere que le pregunte?: """))
        preguntas(preg)

except KeyboardInterrupt:         #Si el usuario pulsa CONTROL+C entonces...
    print("El usuario ha pulsado Ctrl+C...")
except:
    print("error inesperado")
finally:
    """
    CERRAMOS RECURSOS ABIERTOS
    """

