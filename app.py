#Librerias
import time
from machine import Pin, SoftI2C
import network
import socket
import utime
import ssd1306
import claseRGB
import speedtest
import datetime

#Configuración inicial de WiFi
ssid = 'Harry Mancera'  #Nombre de la Red
password = '80352754*' #Contraseña de la red
wlan = network.WLAN(network.STA_IF)
#------------------------------------------------
wlan.active(True) #Activa el Wifi
wlan.connect(ssid, password) #Hace la conexión
#------------------------------------------------
#Configuración Pantalla OLED
# ESP32 Pin assignment
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
#------------------------------------------------
#Configuración del LED RGB
rgb = claseRGB.LedRGB(2,4,15)
#------------------------------------------------
#Ciclo que valide en 5 segundos que se establezca la conexión
for i in range(5):
    print(".")
    utime.sleep(1)
#------------------------------------------------
#Condición encargada de notificar si la conexión es Exitosa o no
if wlan.isconnected() == True:#Conexión Exitosa
    rgb.verde() #En caso de ser exitosa enciende el led RGB verde
    utime.sleep(1)
    rgb.apagado()
    print(wlan.ifconfig()) #Muestra la IP y otros datos del Wi-Fi
    oled.text('Conexion OK', 10, 32) #Muestra mensaje en pantalla oled
    oled.show()
else: #Conexión no Exitosa
    ledRGBRojo.on() #En caso de no ser exitosa enciende el led RGB Rojo
    utime.sleep(1)
    ledRGBRojo.off()
    print(wlan.ifconfig())
    oled.text('Conexion No/OK', 10, 32)#Muestra mensaje en pantalla oled
    oled.show()
#------------------------------------------------

#------------------------------------------------
    #Obteniendo datos de subida y bajada de internet     
s = speedtest.Speedtest()
while True:
   time = datetime.datetime.now().strftime("%H:%M:%S")
   downspeed = round((round(s.download()) / 1048576), 2) #Despues de tener los datos de subida/bajada se convierte a megabits por segundo (Mb/s)
   upspeed = round((round(s.upload()) / 1048576), 2) 
   print(f"time: {time}, downspeed: {downspeed} Mb/s, upspeed: {upspeed} Mb/s")
#------------------------------------------------
    
#Salidas
led = Pin(12, Pin.OUT)

#Pagina web
def web_page():  
    html = """
<html>
<head>
<title>Web Server 2021</title>
</head>            
<body>
<a href="/enciende" >ON</a>
<a href="/apaga" >OFF</a>                                
</body>            
</html>  """
    return html

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind(('', 80))
tcp_socket.listen(3)

while True:
    conn, addr = tcp_socket.accept()
    print('Nueva conexion desde:  %s' % str(addr))
    request = conn.recv(1024)
    print('Solicitud = %s' % str(request))
    request = str(request)
    if request.find('/enciende') != -1:
        print('Enciende')
        led.value(1)
    if request.find('/apaga') != -1:
        print('Apaga')
        led.value(0)

    
    #Mostrar Página
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
                   
