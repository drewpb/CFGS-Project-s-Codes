#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
////////////////////////////////////////////////////////////////////////////////////
//   AUTOR:   ANDRÉS R. PHILIPPS BENÍTEZ                     Octubre/2021
////////////////////////////////////////////////////////////////////////////////////
//   PROGRAMA:                          VERSIÓN:              
//   Versión Python:   3.5.3                             
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

def switch_dia(i1):
    selector = {
        0: "domingo",
        1: "lunes",
        2: "martes",
        3: "miércoles",
        4: "jueves",
        5: "viernes",
        6: "sábado"
    }
    i_final = selector.get(i1)
    return i_final

def calculadora(dia, mes, año):
    a = round((14-mes)/12)
    b = round(año-a)
    c = round(mes+((12*a)-2))
    d = b/4
    e = b/100
    f = b/400
    g = round((31*c)/12)
    h = round(dia+b+d-(e+f+g))
    i = round(h % 7)

    """print(f"a: {a}")
    print(f"c: {c}")
    print(f"g: {g}")
    print(f"h: {h}")
    print(f"i: {i}")"""

    return i

#////////////////////////////////////////////////////////////////////////////////////
# PROGRAMA PRINCIPAL
#////////////////////////////////////////////////////////////////////////////////////
try:                 
    print("""
    --- CÁLCULO DEL DÍA DE LA SEMANA ---
    """)
    while True:
        dia = int(input("Escriba el número de día (1-31): "))
        mes = int(input("Escriba el número de mes (1-12): "))
        año = int(input("Escriba el número de año (a partir de 1583): "))
        if (dia>31 or dia<1 or mes<1 or mes>12):    #VERIFICACIÓN DIA Y MES CORRECTOS
            print("""
            HA INTRODUCIDO DIA O MES FUERA DE SU RANGO:
                DIA -> 1 AL 31
                MES -> 1 AL 12 
            """)
        elif (año<1583):    #VERIFICACIÓN AÑO CORRECTO
            print("""
            ¡¡¡EL AÑO DEBE SER MAYOR DE 1583!!!
            """)
        else:
            print(f"""
            El día {dia} del mes {mes} de {año} cae un {switch_dia(calculadora(dia, mes, año))}.
            """)

except KeyboardInterrupt:         #Si el usuario pulsa CONTROL+C entonces...
    print("El usuario ha pulsado Ctrl+C...")
except:
    print("error inesperado")
finally:
    """
    CERRAMOS RECURSOS ABIERTOS
    """

