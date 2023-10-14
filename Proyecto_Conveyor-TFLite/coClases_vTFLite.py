# -*- coding: utf-8 -*-

from paho.mqtt import publish

from gpiozero import LED, DistanceSensor
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

from time import sleep, strftime

import speech_recognition as sr
import cv2

#Librerías para enviar por correo archivos adjuntos
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from os import path

ruta_archivos_proyecto = "/home/pi/_myDrew_/Proyecto_Conveyor-OpenCV/archivos_necesarios/"

#/////////////////////////////////////////////////////////////////////
# CLASES Y FUNCIONES
#/////////////////////////////////////////////////////////////////////
#====================================================================
#======== NodeRED Y MosQuiTTo =======================================

sensor = DistanceSensor(echo=12, trigger=16)
dicc_objetos = {'car':'Coche', 'donut':'Donut', 'giraffe':'Jirafa', 
'scissors':'Tijeras', 'book':'Libro', 'dog':'Perro'}
list_objetos_reconocidos = []
distancia_conocidos = []
resumen_conocidos = []
hora_conocido = []


class nodeRedDrew():
    def __init__(self) -> None:
        pass

    def medirDistancia(self):
        publish.single(topic="distancia", payload=round(sensor.distance*100,2), hostname="127.0.0.1")

    def enviarOrden(self, orden):
        publish.single(topic="orden", payload=orden, hostname="127.0.0.1")

    def accesoRfid(self, flag, nombre_ ):
        if flag == True:
            publish.single(topic="rfid_flag", payload="ON", hostname="127.0.0.1")
            publish.single(topic="rfid_nombre", payload=nombre_, hostname="127.0.0.1")
        if flag == False: 
            publish.single(topic="rfid_flag", payload="OFF", hostname="127.0.0.1")
            publish.single(topic="rfid_nombre", payload="ACCESO NO PERMITIDO: ", hostname="127.0.0.1")

    def enviarCoincidencias(self, object_name, score, frame):
        if score>=85:
            for obj in dicc_objetos:
                if object_name == obj:
                    #print(dicc_objetos[obj])
                    if not dicc_objetos[obj] in list_objetos_reconocidos:
                        objRec = dicc_objetos[obj]
                        list_objetos_reconocidos.append(objRec)
                        distancia_conocidos.append(round(sensor.distance*100,2))
                        hora_conocido.append(strftime("%H:%M:%S"))  
                        cv2.imwrite(f"/home/pi/_myDrew_/Proyecto_Conveyor-TFLite/objetos_img/{objRec}.jpg", frame)
                        publish.single(topic="reconocimiento", payload=objRec, hostname="127.0.0.1")
                else: pass
                     


#====================================================================
#======== LECTOR RFID ===============================================

reader = SimpleMFRC522()
count_validRFID = 0
text_admin = "Administrador: Andrés R. Philipps Benítez"
text_user = "Usuario: Jose Luis Pérez del Val"
id_permited = {262927241975: text_user, 689386524944: text_admin}


class lectorRfidDrew():
    def __init__(self) -> None:
        GPIO.setwarnings(False)
        pass

    def validRFID(self, valid:bool, orden_ultima):
        nd = nodeRedDrew()
        fp = finalizarProgramaDrew()
        global count_validRFID
        try:
            if orden_ultima=="Iniciar": pass
            elif orden_ultima=="init": 
                print("\nVALIDANDO..\n")   
                if (count_validRFID == 0):
                    print("\n       "+'\033[1;4m'+"*** Por favor, acerque su tarjeta RFID ***\n"+ '\033[0m')
                    id, text = reader.read()
                    not_valid = 0
                    for i in id_permited:
                        if (id == i):
                            nombre_ = id_permited[i]
                            fp.setAcceso(nombre_)
                            flag = True
                            print('\x1b[38;2;33;240;60m'+f"""{"*"*60}
                ACCESO PERMITIDO:\n\n  \t\t{id_permited[i]}  \n{"*"*60}"""+'\x1b[0m')
                            valid = True
                            nd.accesoRfid(flag, nombre_)
                        else: not_valid += 1
                    if not_valid == len(id_permited.keys()):
                        print('\x1b[38;2;204;1;1m'+f"""{"*"*60}
                ACCESO DENEGADO   \n{"*"*60}"""+'\x1b[0m')
                    else: pass
            else: pass

        finally:
            pass
            
        return valid

#==============================================================================================================
#===== ORDENES CON GPIO ==================================================================================

orden=""
paro = LED(5)
marcha = LED(6)
marcha.off()
paro.off()

class ordenGpioDrew():
    def __init__(self) -> None:
        pass

    def puntosEspera(self, tm:float):
        for i in range(3):
            print(" "*42+"·")
            sleep(tm)
        print(" "*41+"___")

    def inicarConveyor(self, orden_ultima):
        og = ordenGpioDrew()
        nd = nodeRedDrew()
        if orden_ultima=="Iniciar": pass
        elif orden_ultima!="Iniciar":


            print("""
                                Iniciando el conveyor..
                - Para detener la ejecución del programa, diga 'Parar' -
                    - Para finalizar el programa, diga 'Finalizar' - 
                        """)
            og.puntosEspera(0.6)
            print("\n  ***VENTANA DE RECONOCIMIENTO - OPENCV:",'\033[1;4m'+ "¡¡AQUI NO FUNCIONA 'ESC'!!\n" + '\033[0m')
            marcha.off()
            paro.off()
            sleep(0.16)
            marcha.on()
            sleep(0.23)
            marcha.off()
            sleep(0.23)
            marcha.on()   
        nd.medirDistancia()
            

    def pararConveyor(self, orden_ultima):
        og = ordenGpioDrew()
        if orden_ultima=="Parar": pass
        elif orden_ultima!="Parar":
            print("""
                                Parando el conveyor..
                        """)
            marcha.off()
            paro.on()
            og.puntosEspera(0.2)
    
    def inicializarGpios(self):
        og = ordenGpioDrew()
        marcha.off()
        paro.off()

    def puntoOrigenConveyor(self):
        marcha.off()
        paro.off()
        sleep(0.16)
        marcha.on()
        sleep(0.16)
        marcha.off()
        sleep(0.16)
        marcha.on()  

#==============================================================================================================
#==== FUNCIONES MICRóFONO =====================================================================================

r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening


class ordenMicroDrew():
    def __init__(self) -> None:
        self.orden = ""

    # this is called from the background thread
    def callback(self, recognizer, audio):
        # received audio data, now we'll recognize it using Google Speech Recognition
        global orden
        try:
            orden = recognizer.recognize_google(audio, language='es-ES').title()
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            print(" "*50+f"---<(Has dicho '{orden}')>---")
        except sr.UnknownValueError:
            print("Google Speech Recognition no ha podido entender su orden.")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
    def get_orden(self):
        self.orden = orden
        return orden

    def stopListen(self, iniciar:bool):
        ordmicdrew = ordenMicroDrew()
        if iniciar == True:
            # start listening in the background (note that we don't have to do this inside a `with` statement)
            exec ("stop_listening = r.listen_in_background(m, ordmicdrew.callback)")
        elif iniciar == False:
            exec ("stop_listening()")

#==============================================================================================================
#==== FUNCIONES FINALLY =====================================================================================
acceso_persona = []
hora_persona = []
resumen_persona = []
class finalizarProgramaDrew():
    def __init__(self):
        pass

    def setAcceso(self, persona):
        if not persona in acceso_persona:
            acceso_persona.append(persona)
            hora_persona.append(strftime("%H:%M:%S"))

    def finalizar(self):
        fp = finalizarProgramaDrew()
        coinc = 1
        print("\n ESPERE MIENTRAS SE FINALIZA EL PROGRAMA..\n")
        for a in acceso_persona:
            hr = hora_persona[acceso_persona.index(a)]
            resumen_persona.append(f"\n\t{a} a las {hr} ")

        for o in list_objetos_reconocidos:
            dist = distancia_conocidos[list_objetos_reconocidos.index(o)]
            hora = hora_conocido[list_objetos_reconocidos.index(o)]
            resumen_conocidos.append(f"""\n     Reconocimiento Nº{coinc} :
        - Objeto:                                    {o}
        - Distancia de reconocimiento:        {dist} cm
        - Hora de reconocimiento :            {hora}
        - La imagen adjuntada correspondiente:      {o}.jpg\n""")
            coinc +=1
        print(' '.join(resumen_conocidos))
        print("\n PREPARANDO EL ENVIO DE CORREO..")
        fp.enviarAdjuntosEmail()
        sleep(0.618)
        print("\n       PROGRAMA FINALIZADO \n")


        #Clase encargada de enviar emails
    def enviarAdjuntosEmail(self):
        #Ponemos los archivos que vamos a adjuntar en función del nombre de la tabla
        files = []
        for l in list_objetos_reconocidos:
            files.append(f"{l}.jpg")
        remitente = 'electronpb.ar@gmail.com'
        destinatarios = ['andresphibe@outlook.es', 'jlval@cifpn1.es', 'victorphilipps@gmail.com'] 
        asunto = '[RPI] Informe OpenCV'

        cuerpo = f'''Buenas,

        - Enviado desde la Raspberry Pi -  

    En este correo te envío un informe del proyecto TFLite-Conveyor.
    Para ello te adjunto las imagenes correspondientes a los objetos que han sido reconocidos a lo largo
    del programa. Además, dejaré constancia de otros datos referentes al reconocimiento como el nombre,
    la distancia a la fue reconocido, la hora, y el nombre de la imagen adjuntada correspondiente a dicho objeto.

    Informe:
    {' '.join(resumen_conocidos)}

    Acceso RFID validado por:
    {' '.join(resumen_persona)}
    
Un saludo...    < Andrés R. Philipps Benítez >
        
Este mensaje ha sido enviado a las {strftime("%H:%M:%S")} del {strftime("%d/%m/%y")}.'''
        # Creamos el objeto mensaje
        mensaje = MIMEMultipart()

        # Establecemos los atributos del mensaje
        mensaje['From'] = remitente
        mensaje['To'] = ", ".join(destinatarios)
        mensaje['Subject'] = asunto
        
        # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
        mensaje.attach(MIMEText(cuerpo, 'plain'))

        #Usamos un for para adjuntar cada uno de los archivos de la lista files
        for f in files:
            # Creamos un objeto MIME base
            part = MIMEBase('application', 'octet-stream')
            # Y le cargamos el archivo adjunto en la ruta correspondiente
            part.set_payload(open(f"/home/pi/_myDrew_/Proyecto_Conveyor-TFLite/objetos_img/{f}", "rb").read())
            # Codificamos el objeto en BASE64
            encoders.encode_base64(part)
            # Agregamos una cabecera al objeto
            part.add_header('Content-Disposition', "attachment; filename= {0}".format(path.basename(f)))
            # Y finalmente lo agregamos al mensaje el adjunto
            mensaje.attach(part)

        # Creamos la conexión con el servidor
        sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)
        
        # Ciframos la conexión
        sesion_smtp.starttls()

        # Iniciamos sesión en el servidor
        sesion_smtp.login('electronpb.ar@gmail.com','Log_x081')

        # Convertimos el objeto mensaje a texto
        texto = mensaje.as_string()

        # Enviamos el mensaje
        sesion_smtp.sendmail(remitente, destinatarios, texto)
        print("\n ENVIANDO EMAIL.. \n")
        # Cerramos la conexión
        sesion_smtp.quit()

#=======================================================

    