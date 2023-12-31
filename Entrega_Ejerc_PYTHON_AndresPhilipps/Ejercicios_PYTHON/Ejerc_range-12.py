#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
////////////////////////////////////////////////////////////////////////////////////
//   AUTOR:   ANDRÉS R. PHILIPPS BENÍTEZ                     Octubre/2021
////////////////////////////////////////////////////////////////////////////////////
//   PROGRAMA:      MÚLTIPLOS ENTRE VALORES         VERSIÓN:              
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

lista = 0

#////////////////////////////////////////////////////////////////////////////////////
# CONFIGURACIÓN PUERTOS GPIO Y RECURSOS A UTILIZAR
#////////////////////////////////////////////////////////////////////////////////////

#////////////////////////////////////////////////////////////////////////////////////
# FUNCIONES
#////////////////////////////////////////////////////////////////////////////////////

def multiplos(i,f,m):
    lista = list(range(i-1, f+1, m))
    cant = len(lista)
    return lista, cant
    
#////////////////////////////////////////////////////////////////////////////////////
# PROGRAMA PRINCIPAL
#////////////////////////////////////////////////////////////////////////////////////

try:    
    print("""
    --- MÚLTIPLOS ENTRE VALORES ---
    """) 
    while True:
        ini = int(input("Escriba un número entero incial (>0): "))
        fin = int(input("Escriba un número entero final (>0): "))
        mult = int(input("¿Qué múltiplo quiere?: "))
        if (ini>=fin):
            print("""
            ¡¡EL NÚMERO FINAL DEBE SER MAYOR QUE EL INICIAL!!
            """)
        elif (mult == 0):
            print("""
            ¡¡¡EL MÚLTIPLO NO DEBE SER CERO!!!
            """)
        else:
            lista, cant = multiplos(ini, fin, mult)
            print(f"""Entre {ini} y {fin} hay {cant} múltiplos de {mult}:
    {lista}
            """)
except KeyboardInterrupt:         #Si el usuario pulsa CONTROL+C entonces...
    print("El usuario ha pulsado Ctrl+C...")
except:
    print("error inesperado")
finally:
    """
    CERRAMOS RECURSOS ABIERTOS
    """

