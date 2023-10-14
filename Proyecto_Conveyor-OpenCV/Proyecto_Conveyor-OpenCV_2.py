import coClases
from time import sleep
from random import randint
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

recofdrew = coClases.reconocimientoFacialDrew()
noderdrew = coClases.nodeRedDrew()
rfiddrew = coClases.lectorRfidDrew()
ordgpiodrew = coClases.ordenGpioDrew()
ordmicdrew = coClases.ordenMicroDrew()
finpdrew = coClases.finalizarProgramaDrew()


ordgpiodrew.inicializarGpios()
ordmicdrew.stopListen(iniciar=True)
valid = False
count_ord = 0
noderdrew.accesoRfid(flag=False, nombre_='')
noderdrew.enviarOrden(orden="ESPERANDO")
print("LIBRERIAS IMPORTADAS.\n")
ordgpiodrew.puntoOrigenConveyor()


while True: 
    try:
        noderdrew.medirDistancia() #OK
        valid = rfiddrew.validRFID(valid) #OK A VECES
        if (valid == True):
            print("\n       Por favor, diga 'Iniciar' para ejecutar programa.\n")
            while (str(ordmicdrew.get_orden()) != "Iniciar"):
                noderdrew.medirDistancia()
                salir, nombre  = recofdrew.reconocerCaras(fin=False)
                if (salir == True): break 
                else: pass

            if (str(ordmicdrew.get_orden()) == "Iniciar"):
                noderdrew.enviarOrden(orden="INICIAR")
                ordgpiodrew.inicarConveyor()
                if (str(ordmicdrew.get_orden()) == "Parar"):
                    noderdrew.enviarOrden(orden="PARAR")
                    ordgpiodrew.pararConveyor()
                elif (str(ordmicdrew.get_orden()) == "Finalizar"):
                    noderdrew.enviarOrden(orden="FINALIZAR")
                    print("\nFINALIZANDO PROGRAMA..")
                    ordgpiodrew.puntoOrigenConveyor()
                    finpdrew.finalizar()
                    sleep(0.6)
                    break
            elif salir == True: break
            else: pass
        else: pass
    except KeyboardInterrupt:    #Si el usuario pulsa "Ctr+C"..
        print("\nSYS!: SALIENDO POR TECLADO..")
        ordmicdrew.stopListen(iniciar=False)
        break   #Termina el programa
    except:
        print("\nSYS!: ERROR..")
        #Retardo de 3 segundos por si un error hace entrar en bucle al programa
        sleep(3.237)
        break
    finally:
        pass

GPIO.cleanup()
recofdrew.reconocerCaras(fin=True)
ordmicdrew.stopListen(iniciar=False)
