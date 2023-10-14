#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
////////////////////////////////////////////////////////////////////////////////////
//   AUTOR:   ANDRÉS R. PHILIPPS BENÍTEZ                     Octubre/2021
////////////////////////////////////////////////////////////////////////////////////
//   PROGRAMA:   DOMINGO DE PASCUA                  VERSIÓN:              
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
  
def domingoPascua(año):
    if (año <= 0):
        print(f"¡¡En el año {año} no existía la Pascua!!")
    else:
        a = año%19
        b,c = divmod(año, 100)
        d,e = divmod(b, 4)
        f,f_ = divmod((b+8), 25)
        g,g_ = divmod((b+f+1), 3)
        h = (19*a+b-d-g+15)%30
        i,j = divmod(c, 4)
        k = (32+2*e+2*i-h-j)%7
        m,m_ = divmod((a+11*h+22*k), 451)
        n,p = divmod((h+k-7*m+114), 31)

        if (año <= 2021):
            print(f"El domingo de pascua del año {año} fue el {(p+1)} de {selectorMes(n)}")
        elif (año > 2021):
            print(f"El domingo de pascua del año {año} será el {(p+1)} de {selectorMes(n)}")
        else: pass
    print()
    return

def selectorMes(mes_):
    selector = {
        1 : "enero",
        2 : "febrero",
        3 : "marzo",
        4 : "abril",
        5 : "mayo",
        6 : "junio",
        7 : "julio",
        8 : "agosto",
        9 : "septiembre",
        10 : "octubre",
        11 : "noviembre",
        12 : "diciembre",
    }
    func = selector.get(mes_, lambda: "Texto inválido")
    return func


#////////////////////////////////////////////////////////////////////////////////////
# PROGRAMA PRINCIPAL
#////////////////////////////////////////////////////////////////////////////////////
try:  
    print("""
    --- DOMINGO DE PASCUA ---
    """)             
    while True:      #iniciamos un loop infinito
        año = int(input("Digame una año: "))
        domingoPascua(año)       

except KeyboardInterrupt:         #Si el usuario pulsa CONTROL+C entonces...
    print("El usuario ha pulsado Ctrl+C...")
except:
    print("error inesperado")
finally:
    """
    CERRAMOS RECURSOS ABIERTOS
    """

