#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
////////////////////////////////////////////////////////////////////////////////////
//   AUTOR:   ANDRÉS R. PHILIPPS BENÍTEZ                     Octubre/2021
////////////////////////////////////////////////////////////////////////////////////
//   PROGRAMA:    SUMADOR DE PARES E IMPARES               VERSIÓN:              
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

par = []
inpar = []
suma_par = 0
suma_inpar = 0

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
    --- SUMADOR DE PARES E IMPARES ---
    """)
    while True:
        cant_num = int(input("¿Cuántos números va a escribir? "))
        if (cant_num <= 0):
            print("La cantidad de números a escribir no puede ser nula o negativa. Programa terminado")
        else:
            for i in range(cant_num):
                num = int(input("Escriba un número entero: "))
                div_num = num % 2
                if div_num == 0:
                    par += [num]
                    print(par)
                else: 
                    inpar += [num]
                    print(inpar)
            sum_par = sum(par)
            sum_inpar = sum(inpar)

        print()
        print(f"La suma de los números pares que ha escrito es {sum_par}")
        print(f"La suma de los números inpares que ha escrito es {sum_inpar}")
        print("""
        Programa terminado
        Gracias por jugar conmigo
        """)

except KeyboardInterrupt:         #Si el usuario pulsa CONTROL+C entonces...
    print("El usuario ha pulsado Ctrl+C...")
except:
    print("error inesperado")
finally:
    """
    CERRAMOS RECURSOS ABIERTOS
    """
