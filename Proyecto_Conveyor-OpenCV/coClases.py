# -*- coding: utf-8 -*-

from cv2 import imshow, resize, rectangle, putText, VideoCapture, FONT_HERSHEY_COMPLEX, waitKey, destroyAllWindows
from face_recognition import face_locations, face_encodings, compare_faces, load_image_file

from paho.mqtt import publish

from gpiozero import LED, DistanceSensor
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

from time import sleep, strftime

import speech_recognition as sr

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
#======== OPENCV Y RECONOCIMIENTO FACIAL ============================

#Iniciar la webcam:
webcam = VideoCapture(2)
# NOTA: Si no funciona puedes cambiar el índice '0' por otro, o cambiarlo por la dirección de tu webcam.
a = 1
#Cargar una fuente de texto:
font = FONT_HERSHEY_COMPLEX

# Identificar rostros es un proceso costoso. Para poder hacerlo en tiempo real sin que haya retardo
# vamos a reducir el tamaño de la imagen de la webcam. Esta variable 'reduccion' indica cuanto se va a reducir:
reduccion = 6 #Con un 5, la imagen se reducirá a 1/5 del tamaño original
 
#Definir un array con los encodings y nuestro nombre:
encodings_conocidos = []
nombres_conocidos = ["Tifonte Smith", "Ana Eustaquia", "Hilarino Blacky",
 "Humildad Gil" , "Uldarico Soto", "Simplicia White"]
for i in range(6):
    exec ("person_%s_encodings = face_encodings(load_image_file('%s_caras/cara_%s.jpg'))[0]" % (i, ruta_archivos_proyecto, i))
    exec ("encodings_conocidos.append(person_%s_encodings)" % (i))
  
class reconocimientoFacialDrew():
    
    def __init__(self) -> None:
        pass
 
    #Recordamos al usuario cuál es la tecla para salir:
    print("\nRecordatorio: pulsa 'ESC' para cerrar.\n")
 
    def reconocerCaras(self, fin:bool):
        fp = finalizarProgramaDrew()
        nd = nodeRedDrew()
        #Definimos algunos arrays y variables:
        loc_rostros = [] #Localizacion de los rostros en la imagen
        encodings_rostros = [] #Encodings de los rostros
        nombres_rostros = [] #Nombre de la persona de cada rostro
        nombre = "" #Variable para almacenar el nombre
    
        #Capturamos una imagen con la webcam:
        valid, img = webcam.read()

        #Si la imagen es válida (es decir, si se ha capturado correctamente), continuamos:
        if valid:
    
            #La imagen está en el espacio de color BGR, habitual de OpenCV. Hay que convertirla a RGB:
            img_rgb = img[:, :, ::-1]
    
            #Reducimos el tamaño de la imagen para que sea más rápida de procesar:
            img_rgb = resize(img_rgb, (0, 0), fx=1.0/reduccion, fy=1.0/reduccion)
    
            #Localizamos cada rostro de la imagen y extraemos sus encodings:
            loc_rostros = face_locations(img_rgb)
            encodings_rostros = face_encodings(img_rgb, loc_rostros)
    
            #Recorremos el array de encodings que hemos encontrado:
            for encoding in encodings_rostros:
    
                #Buscamos si hay alguna coincidencia con algún encoding conocido:
                coincidencias = compare_faces(encodings_conocidos, encoding)
    
                #El array 'coincidencias' es ahora un array de booleanos. Si contiene algun 'True', es que ha habido alguna coincidencia:
                if True in coincidencias:
                    nombre = nombres_conocidos[coincidencias.index(True)]
                    fp.setName(nombre)
                    nd.enviarNombre(nombre=nombre)

                #Si no hay ningún 'True' en el array 'coincidencias', no se ha podido identificar el rostro:
                else:
                    nombre = "NO IDENTIFICADO"
                    nd.enviarNombre(nombre="NO IDENTIFICADO")
    
                #Añadir el nombre de la persona identificada en el array de nombres:
                nombres_rostros.append(nombre)
    
            #Dibujamos un recuadro rojo alrededor de los rostros desconocidos, y uno verde alrededor de los conocidos:
            for (top, right, bottom, left), nombre in zip(loc_rostros, nombres_rostros):
                
                #Deshacemos la reducción de tamaño para tener las coordenadas de la imagen original:
                top = top*reduccion
                right = right*reduccion
                bottom = bottom*reduccion
                left = left*reduccion
    
                #Cambiar de color según si se ha identificado el rostro:
                if nombre != "NO IDENTIFICADO":
                    color = (0,255,0)
                else:
                    color = (0,0,255)
    
                #Dibujar un rectángulo alrededor de cada rostro identificado, y escribir el nombre:
                rectangle(img, (left, top), (right, bottom), color, 2)
                rectangle(img, (left, bottom - 40), (right, bottom), color, -1)
                putText(img, nombre, (left, bottom - 6), font, 0.8, (0,0,0), 1)
    
            #Mostrar el resultado en una ventana:
            imshow('Output', img)
    
            #Salir con 'ESC'
            k = waitKey(5) & 0xFF
            if k == 27:
                destroyAllWindows()
                salir = True
            else: salir = False
        
        if (fin == True):
            webcam.release()

        return salir, nombre


#====================================================================
#======== NodeRED Y MosQuiTTo =======================================

sensor = DistanceSensor(echo=12, trigger=16)

class nodeRedDrew():
    def __init__(self) -> None:
        pass

    def enviarNombre(self, nombre:str):
        publish.single(topic="reconocimiento", payload=nombre, hostname="127.0.0.1")

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

    def validRFID(self, valid:bool):
        print("\nVALIDANDO..\n")
        nd = nodeRedDrew()
        fp = finalizarProgramaDrew()
        global count_validRFID
        try:
            if (count_validRFID == 0 or (count_validRFID % 3 == 0)):
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
            elif(valid == True): 
                print(f"VECES QUE HAS PARADO EL SISTEMA: {count_validRFID} ")
                print(f"TE QUEDAN {3-(count_validRFID % 3)} PARADAS PARA NUEVA VALIDACIÓN RFID")
                valid = True
        finally:
            count_validRFID += 1
            
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

    def inicarConveyor(self):
        rf = reconocimientoFacialDrew()
        og = ordenGpioDrew()
        nd = nodeRedDrew()
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
        while(orden != "Parar"):
            if orden == "Finalizar": break
            else: pass
            rf.reconocerCaras(fin=False)
            nd.medirDistancia()
            

    def pararConveyor(self):
        og = ordenGpioDrew()
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
lista_conocidos = []
distancia_conocidos = []
resumen_conocidos = []
hora_conocido = []
acceso_persona = []
hora_persona = []
resumen_persona = []
class finalizarProgramaDrew():
    def __init__(self):
        pass

    def setName(self, nombre):
        if not nombre in lista_conocidos:
            lista_conocidos.append(nombre)
            distancia_conocidos.append(round(sensor.distance*100,2))
            hora_conocido.append(strftime("%H:%M:%S"))

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
        for l in lista_conocidos:
            n_cara = nombres_conocidos.index(l)
            dist = distancia_conocidos[lista_conocidos.index(l)]
            hora = hora_conocido[lista_conocidos.index(l)]
            resumen_conocidos.append(f"""\n     Reconocimiento Nº{coinc} :
        - Nombre de la persona:                     {l}
        - Distancia a la que fue reconocida:        {dist} cm
        - Hora a la que fue reconocida :            {hora}
        - La imagen adjuntada correspondiente:  cara_{n_cara}.jpg\n""")
            coinc +=1

        print("\n PREPARANDO EL ENVIO DE CORREO..")
        fp.enviarAdjuntosEmail()
        sleep(0.618)
        print("\n       PROGRAMA FINALIZADO \n")


        #Clase encargada de enviar emails
    def enviarAdjuntosEmail(self):
        #Ponemos los archivos que vamos a adjuntar en función del nombre de la tabla
        files = []
        for l in lista_conocidos:
            n_cara = nombres_conocidos.index(l)
            files.append(f"cara_{n_cara}.jpg")
        remitente = 'electronpb.ar@gmail.com'
        destinatarios = ['andresphibe@outlook.es' , 'jlval@cifpn1.es']
        asunto = '[RPI] Informe OpenCV'
        cuerpo = f'''Buenas,

        - Enviado desde la Raspberry Pi -  

    En este correo te envío un informe del proyecto OpenCV-Conveyor.
    Para ello te adjunto las imagenes correspondientes a las personas que han sido identificada a lo largo
    del programa. Además, dejaré constancia de otros datos referentes al reconocimiento como el nombre de la persona,
    la distancia a la fue reconocida, la hora, y el nombre de la imagen adjuntada correspondiente a dicha persona.

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
            part.set_payload(open(f"{ruta_archivos_proyecto}_caras/{f}", "rb").read())
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
        sesion_smtp.login('user@gmail.com','passwd')

        # Convertimos el objeto mensaje a texto
        texto = mensaje.as_string()

        # Enviamos el mensaje
        sesion_smtp.sendmail(remitente, destinatarios, texto)
        print("\n ENVIANDO EMAIL.. \n")
        # Cerramos la conexión
        sesion_smtp.quit()

#=======================================================

    