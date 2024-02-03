# Importamos el modulo para trabajar con archivos DLL con Python
import ctypes
import re
# Modulo
from os import system
import threading

# Importamos el modulo para trabajar con Python y comunicacion ethernet
from pycomm3 import LogixDriver

# Direccion IP del controlador PLC
IP = "192.168.10.1/0"

# Funcion par leer una etiqueta del PLC
def readtag (ip, tag):
    # Direccionamos el controlador con el nombre de PLC
    with LogixDriver(ip) as plc:
        # Leemos la etiqueta del PLC
        return plc.read(tag)[1]
    
# Funcion para escribir en una etiqueta del PLC
def writetag (ip, tag, value):
    # Direccionamos el controlador con el nombre de PLC
    with LogixDriver(ip) as plc:
        # Escribimos a la etiqueta del PLC
        plc.write(tag, value)

# Creamos una funcion principal
def main():
    # Variables para controlar el dispositivo de Feasa
    FeasaDLL = ctypes.WinDLL('C:\\Firmes\\feasacom64.dll')
    FeasaCom_Open = FeasaDLL['FeasaCom_Open']
    FeasaCom_Close = FeasaDLL['FeasaCom_Close']
    FeasaCom_Send = FeasaDLL['FeasaCom_Send']
    FeasaCom_EnumPorts = FeasaDLL['FeasaCom_EnumPorts']
    FeasaCom_EnumPorts.restype = ctypes.c_int

    # A buffer is needed to store the responses obtained from the LED Analyser.
	# This buffer shuld be big enought to fit all the information returned
    BUFFER_SIZE = 256
    buffer = ctypes.create_string_buffer(BUFFER_SIZE)
    # Puerto del controlador
    port = 5

    ret = 0

    # Abrimos un bucle infinito
    while True:
        # Leemos una etiqueta
        if (readtag(IP, 'ST30FeasaTriggerTest') == True):
            
            # Limpiamos la pantalla
            system("cls")

            # Abrimos el puerto
            ret = FeasaCom_Open(port, b"115200")

            # Si tenemos respuesta por el puerto
            if ret == 1:
                # Realizamos una captura con el dispositivo de Feasa
                ret = FeasaCom_Send(port, b'CAPTURE', buffer)
                # Mostramos un mensaje del estatus de la captura
                print("Captura: " + buffer.value.decode('ascii')+"\n")
                # Realizamos la consulta de los valores de candela por metro cuadrado
                ret = FeasaCom_Send(port, b'GETABSINTALL', buffer)
                # Almacenamos los datos del buffer
                alldata = buffer.value.decode('ascii')
                # Mostramos un mensaje
                print("Valores de candela")
                # Mostramos un mensaje con los valores leidos
                print(alldata)
                # Separamos los datos
                data = alldata.split('\n')
                # Almacenamos los datos en el PLC
                t1 = threading.Thread(target=writetag(IP, "ST30FeasaCMD1", data[0][3:13]), args=(1, 'thread1'))
                t2 = threading.Thread(target=writetag(IP, "ST30FeasaCMD2", data[1][3:13]), args=(1, 'thread2'))
                t3 = threading.Thread(target=writetag(IP, "ST30FeasaCMD3", data[2][3:13]), args=(1, 'thread3'))
                t4 = threading.Thread(target=writetag(IP, "ST30FeasaCMD4", data[3][3:13]), args=(1, 'thread4'))
                t5 = threading.Thread(target=writetag(IP, "ST30FeasaCMD5", data[4][3:13]), args=(1, 'thread5'))
                t6 = threading.Thread(target=writetag(IP, "ST30FeasaCMD6", data[5][3:13]), args=(1, 'thread6'))
                t7 = threading.Thread(target=writetag(IP, "ST30FeasaCMD7", data[6][3:13]), args=(1, 'thread7'))
                t8 = threading.Thread(target=writetag(IP, "ST30FeasaCMD8", data[7][3:13]), args=(1, 'thread8'))
                t9 = threading.Thread(target=writetag(IP, "ST30FeasaCMD9", data[8][3:13]), args=(1, 'thread9'))
                t10 = threading.Thread(target=writetag(IP, "ST30FeasaCMD10", data[9][3:13]), args=(1, 'thread10'))
                t1.start()
                t2.start()
                t3.start()
                t4.start()
                t5.start()
                t6.start()
                t7.start()
                t8.start()
                t9.start()
                t10.start()
                #writetag(IP, "ST30FeasaCMD2", data[1][3:13])
                #writetag(IP, "ST30FeasaCMD3", data[2][3:13])
                #writetag(IP, "ST30FeasaCMD4", data[3][3:13])
                #writetag(IP, "ST30FeasaCMD5", data[4][3:13])
                #writetag(IP, "ST30FeasaCMD6", data[5][3:13])
                #writetag(IP, "ST30FeasaCMD7", data[6][3:13])
                #writetag(IP, "ST30FeasaCMD8", data[7][3:13])
                #writetag(IP, "ST30FeasaCMD9", data[8][3:13])
                #writetag(IP, "ST30FeasaCMD10", data[9][3:13])

                # Realizamos la consulta de los valores de candela por metro cuadrado
                ret = FeasaCom_Send(port, b'GETXYALL', buffer)
                # Almacenamos los datos del buffer
                alldata = buffer.value.decode('ascii')
                # Mostramos un mensaje
                print("\nValores X Y")
                # Mostramos un mensaje con los valores leidos
                print(alldata)
                # Separamos los datos
                data = alldata.split('\n')

                writetag(IP, "ST30FeasaX1", data[0][3:9])
                writetag(IP, "ST30FeasaX2", data[1][3:9])
                writetag(IP, "ST30FeasaX3", data[2][3:9])
                writetag(IP, "ST30FeasaX4", data[3][3:9])
                writetag(IP, "ST30FeasaX5", data[4][3:9])
                writetag(IP, "ST30FeasaX6", data[5][3:9])
                writetag(IP, "ST30FeasaX7", data[6][3:9])
                writetag(IP, "ST30FeasaX8", data[7][3:9])
                writetag(IP, "ST30FeasaX9", data[8][3:9])
                writetag(IP, "ST30FeasaX10", data[9][3:9])

                writetag(IP, "ST30FeasaY1", data[0][10:16])
                writetag(IP, "ST30FeasaY2", data[1][10:16])
                writetag(IP, "ST30FeasaY3", data[2][10:16])
                writetag(IP, "ST30FeasaY4", data[3][10:16])
                writetag(IP, "ST30FeasaY5", data[4][10:16])
                writetag(IP, "ST30FeasaY6", data[5][10:16])
                writetag(IP, "ST30FeasaY7", data[6][10:16])
                writetag(IP, "ST30FeasaY8", data[7][10:16])
                writetag(IP, "ST30FeasaY9", data[8][10:16])
                writetag(IP, "ST30FeasaY10", data[9][10:16])

                # BIT para indicar que se termino el proceso
                writetag(IP, "ST30FeasaTriggerTestDone", 1)
                # Cerramos comunicacion con el puerto
                FeasaCom_Close(port)
            # En caso contrario
            else:
                # Mostramos un mensaje de error
                print("Error al conectar con el modulo de Feasa")

# Creamos un punto de acceso
if __name__ == "__main__":
    # Llamamos a la funcion principal
    main()