from paho.mqtt import publish

print("")
temp = float(input("Por favor, escriba una temperatura en grados Cº, separando la parte decimal de la entera con un punto: "))
disp = input("Por favor, escriba el nombre del dispositivo medido: ").capitalize().replace(" ","_")
    
temp=str(round(temp,2))
mensaje = temp+"+"+disp


print("¡Gracias!")
publish.single(topic="ds18b20", payload=mensaje, hostname="127.0.0.1")
