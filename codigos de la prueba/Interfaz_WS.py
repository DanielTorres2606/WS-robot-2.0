from tkinter import*
from tkinter import ttk
import tkinter as tk
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
import threading
import time

#Programas
import B1
import B2_camara
from B2_sensores import FUS1, FSharp, FPiso, paradas
import B2_sensores

#Raiz

raiz= Tk()
raiz.title("Control Robot")
raiz.config(bg="white")
raiz.resizable(0,0)

#raiz.iconbitmap("descarga.ico")

#Frame

frameWS=Frame()
frameWS.pack()
frameWS.config(bg="white")
frameWS.config(width="600", height="500")
#frameWS.config(cursor="pirate")

#Titulo interfaz

tituloLabel=Label(frameWS, text="WS Colombia, Robotica movil", font=("Small Fonts",15), fg="black", bg="white")#.place(x=180, y=2)
tituloLabel.grid(row=0, column=0, padx=0, pady=0, columnspan=10)

cancelar=False

# C A M A R A

def visualizar():

    global cap
    
    if cap is not None:
        ret, frameWS = cap.read()
        if ret == True:
            frameWS = imutils.resize(frameWS, width=300)
            frameWS = cv2.cvtColor(frameWS, cv2.COLOR_BGR2RGB)

            im = Image.fromarray(frameWS)
            img = ImageTk.PhotoImage(image=im)

            video.configure(image=img)
            video.image = img
            video.after(10,visualizar)
            
        else:
            video.image = ""
            cap.realease()

def encender():
    
    global cap
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    visualizar()
    
def apagar():

    global cap
    cap.release()
      
cap = None

#LEDS

def leds(led):
    B2_sensores.sensor(led)


############################### FUNCION DE BOTONES EN INTERFAZ ####################################

################################### EJECUTOR ######################################
def proceso():
    
    global cancelar
    B1.paradas = False
    B2_sensores.paradas = False
    B2_camara.paradas = False
    cancelar = False
    
    i = float(cuadroTiempo.get())

########################### MOVIMIENTO ##############################
    
    if lista.get() == 'B1.1 Front High':
        B1.pruebamovimiento(1,i)
        
    if lista.get() == 'B1.2 Back Low':
        B1.pruebamovimiento(2,i)
        
    if lista.get() == 'B1.3 Diagonal':
        B1.pruebamovimiento(3,i)
        
    if lista.get() == 'B1.4 F1M':
        B1.pruebamovimiento(4,i)
    
    if lista.get() == 'B1.5 B1M':
        B1.pruebamovimiento(5,i)
    
    if lista.get() == 'B1.6 Giro Derecha':
        B1.pruebamovimiento(6,i)
    
    if lista.get() == 'B1.7 Giro izquierda':
        B1.pruebamovimiento(7,i)

########################### PRUEBA SENSORES ##############################

    if lista.get() == 'B2.1 obj led US':
        H2 = threading.Thread(target = leds, args = (1,),daemon = True).start()
        while True:
            if B2_sensores.FUS1 == 0:
                casillaU.config(background = "green")
            else:
                casillaU.config(background = "red")
        
            if cancelar == True:
                break
    
    if lista.get() == 'B2.2 obj led SHARP':
        H2 = threading.Thread(target = leds, args = (2,), daemon = True).start()
        while True:
            if B2_sensores.PSharp == 1:
                casillaS.config(background = "green")
            else:
                casillaS.config(background = "red")
                
            if cancelar == True:
                break
    
    if lista.get() == 'B2.3 led line':
        H2 = threading.Thread(target = leds, args = (3,),daemon = True).start()
        while True:
            if B2_sensores.FPiso == 1:
                casillaP.config(background = "green")
            else:
                casillaP.config(background = "red")
            if cancelar == True:
                break

########################### COLORES Y QR ##############################

    if lista.get() == 'B2.4 Color R Camara':
        camaraCuadro.config(text = "")
        camaraCuadro.config(bg="white")
        camaraCuadro.config(text = B2_camara.color('rojo'))
        camaraCuadro.config(bg="red")
    
    if lista.get() == 'B2.5 Color B Camara':
        camaraCuadro.config(text = "")
        camaraCuadro.config(bg="white")
        camaraCuadro.config(text = B2_camara.color('azul'))
        camaraCuadro.config(bg="blue")
        
    if lista.get() == 'B2.6 Color G Camara':
        camaraCuadro.config(text = "")
        camaraCuadro.config(bg="white")
        camaraCuadro.config(text = B2_camara.color('verde'))
        camaraCuadro.config(bg="green")
        
    if lista.get() == 'B2.7 Color Y Camara':
        camaraCuadro.config(text = "")
        camaraCuadro.config(bg="white")
        camaraCuadro.config(text = B2_camara.color('amarillo'))
        camaraCuadro.config(bg="yellow")

    if lista.get() == 'B2.8 Barcode Camara':
        camaraCuadro.config(text = B2_camara.QR_barcode())
    
    if lista.get() == 'B2.9 Qr Camara':
        camaraCuadro.config(text = B2_camara.QR_barcode())

########################### POSICIONAMIENTO ##############################

    if lista.get() == 'B3.1 obj 30cm US':
        B2_sensores.posicionamiento(8,i)

    if lista.get() == 'B3.2 obj 30cm SHARP':
        B2_sensores.posicionamiento(9,i)

    if lista.get() == 'B3.3 stop line':
        B2_sensores.posicionamiento(10,i)
        
    
    #if lista.get() == 'B3.4 esquinas':
        #for i in range(0,4):
            #B2_sensores.posicionamiento(10,i) poner delay de llegada
            #activa codigo de proximidad 30 cm
            #B2_sensores.posicionamiento(9,i)
            #hace gesto(opcional)
            #gira 90
            #B1.pruebamovimiento(7,i)
            #repite
        #gesto de fin de la operacion
        #casillaU.config(background = "green")
        #casillaS.config(background = "green")
        #casillaP.config(background = "green")
        #time.sleep(3)
        #casillaU.config(background = "red")
        #casillaS.config(background = "red")
        #casillaP.config(background = "red")
        
        #opcion 1
        #ejecuta programa de seguimiento de camino
        #gesto de fin de la operacion
            
########################### FINAL ##############################
    
    #if lista.get() == 'C prueba final':
        #lee el cliente mediante Qr o barcode (opcional)
        #for i in range(0,4):
            #B2_sensores.posicionamiento(10,i) poner delay de llegada
            #activa codigo de proximidad 30 cm
            #B2_sensores.posicionamiento(9,i)
            #hace gesto(opcional)
            #lee color
            #if #salidacolor# == #color seleccionado#:
                #casillaU.config(background = "green")
                #casillaS.config(background = "green")
                #casillaP.config(background = "green")
            #gira 90
            #B1.pruebamovimiento(7,i)
            #repite
        #gesto de fin de la operacion
        #casillaU.config(background = "green")
        #casillaS.config(background = "green")
        #casillaP.config(background = "green")
        #time.sleep(3)
        #casillaU.config(background = "red")
        #casillaS.config(background = "red")
        #casillaP.config(background = "red")
        
    if cancelar == False:
        cuadroE.config(text = 'Fin del programa...')
        time.sleep(3)
        cuadroE.config(text = '')
        camaraCuadro.config(bg="white")
        
####### CANCELAR #######
def fin():
    global cancelar
    B1.paradas = True
    B2_sensores.paradas = True
    B2_camara.paradas = True
    cancelar = True
    camaraCuadro.config(bg="white")
    camaraCuadro.config(text = '')
    cuadroE.config(text = 'Cancelando programa...')
    time.sleep(3)
    cuadroE.config(text = '')
    
    
####### BOTON INICIO #######    
def inicio():
    cuadroE.config(text = 'Ejecutando programa...')        
    H1 = threading.Thread(target = proceso)
    H1.start()
    
####### BOTON PARADA #######
    
def parada():
    H0 = threading.Thread(target = fin).start()
    
##################################### INTERFAZ ###########################################
#Tiempo
cuadroTiempo=Entry(frameWS)
cuadroTiempo.insert(0,0)
cuadroTiempo.grid(row=2, column=1, sticky="w",  padx=10, pady=10)
tiempoLabel=Label(frameWS, text="Tiempo:", bg="white", fg="black")
tiempoLabel.grid(row=2, column=0, sticky="w", padx=10, pady=10)

#Boton Inicio y Apagado
botonInicio=Button(frameWS, command = inicio, text="Inicio", width=10)
botonInicio.grid(row=2, column=2, sticky="w", padx=10, pady=10)

botonParada=Button(frameWS ,command = parada, text="Parada", width=10)
botonParada.grid(row=3, column=2, sticky="w", padx=10, pady=10)

#Pruebas a realizar 
listaPrueba=Label(frameWS, text="Prueba:", bg="white", fg="black")
listaPrueba.grid(row=1, column=0, sticky="w", padx=10, pady=10)
lista=ttk.Combobox(frameWS)
lista.grid(row=1, column=1, sticky="w", padx=10, pady=10)
lista['values']=(
    'B1.1 Front High','B1.2 Back Low','B1.3 Diagonal','B1.4 F1M',
    'B1.5 B1M','B1.6 Giro Derecha','B1.7 Giro izquierda',### PRUEBAS MOVIMIENTO
    'B2.1 obj led US','B2.2 obj led Sharp', 'B2.3 led line',### PRUEBAS SENSORES
    'B2.4 Color R Camara', 'B2.5 Color B Camara', 'B2.6 Color G Camara',
    'B2.7 Color Y Camara', 'B2.8 Barcode Camara','B2.9 QR Camara',###PRUEBAS CAMARA
    'B3.1 obj 30cm US','B3.2 obj 30cm SHARP', 'B3.3 stop line', 'B3.4 esquinas',###PRUEBA POSICIONAMIENTO
    'C prueba final')


#Parte 2 de CAMARA
camara= Label(frameWS, text="Camara:", bg="white", fg="black")
camara.grid(row=1, column=3, sticky="w", padx=10, pady=10)
camaraCuadro=Label(frameWS, text="", bg="white", fg="black")
camaraCuadro.grid(row=1, column=4, sticky="w",  padx=10, pady=10)
botCamE=Button(frameWS, text="On", command = encender)
botCamE.grid(row=7, column=0, padx=10, pady=10)
botCamA=Button(frameWS, text="Off", command = apagar)
botCamA.grid(row=8, column=0, padx=10, pady=10)
video= Label(frameWS)
video.grid(row=8, column=1,  columnspan=7)

#velocidades
velocidad= Label(frameWS, text="Velocidad:", bg="white", fg="black")
velocidad.grid(row=2, column=3, sticky="w", padx=10, pady=10)
x= Label(frameWS, text= "X", bg="white", fg="black")
x.grid(row=2, column=5, sticky="w", padx=10, pady=10)
cuadroX=Entry(frameWS)
cuadroX.grid(row=2, column=6, sticky="w",  padx=10, pady=10)
y= Label(frameWS, text="Y", bg="white", fg="black")
y.grid(row=3, column=5, sticky="w", padx=10, pady=10)
cuadroX=Entry(frameWS)
cuadroX.grid(row=3, column=6, sticky="w",  padx=10, pady=10)
z= Label(frameWS, text="Z", bg="white", fg="black")
z.grid(row=4, column=5, sticky="w", padx=10, pady=10)
cuadroX=Entry(frameWS)
cuadroX.grid(row=4, column=6, sticky="w",  padx=10, pady=10)

#Bateria
bateria= Label(frameWS, text="Bateria:", bg="white", fg="black")
bateria.grid(row=3, column=0, sticky="w", padx=10, pady=10)
cuadroB=Entry(frameWS)
cuadroB.grid(row=3, column=1, sticky="w",  padx=10, pady=10)

#Estado
estado= Label(frameWS, text="Estado:", bg="white", fg="black")
estado.grid(row=4, column=0, sticky="w", padx=10, pady=10)
cuadroE=Label(frameWS, text="", bg="white", fg="black")
cuadroE.grid(row=4, column=1, sticky="w",  padx=10, pady=10)

#Sensores
ultraS= Label(frameWS, text="Ultrasonido:", bg="white", fg="black")
ultraS.grid(row=1, column=7, sticky="w", padx=10, pady=10)
casillaU=Entry(frameWS, width=6, bg="red")                              ## led Ultra sonido
casillaU.grid(row=1, column=8, sticky="w",  padx=10, pady=10)

sharp= Label(frameWS, text="Sharp:", bg="white", fg="black")
sharp.grid(row=2, column=7, sticky="w", padx=10, pady=10)               ## Led Sharp
casillaS=Entry(frameWS, width=6, bg="red")
casillaS.grid(row=2, column=8, sticky="w",  padx=10, pady=10)

piso= Label(frameWS, text="QTI:", bg="white", fg="black")
piso.grid(row=3, column=7, sticky="w", padx=10, pady=10)                ## Led Piso
casillaP=Entry(frameWS, width=6, bg="red")
casillaP.grid(row=3, column=8, sticky="w",  padx=10, pady=10)

##    #Ensayo cambio de color (puedes eliminarlo cunado se agregue el encendido con
##    #los sensores) :3 
##    alv=Button(frameWS, text="color", width=10, command= leds)
##    alv.grid(row=7, column=8, sticky="w", padx=10, pady=10)

#Botones de colores 
bAmarillo=Button(frameWS ,text="Amarillo", width=10, bg="yellow")
bAmarillo.grid(row=6, column=1, sticky="e", padx=10, pady=10)
bAzul=Button(frameWS ,text="Azul", width=10, bg="blue")
bAzul.grid(row=6, column=2, sticky="w", padx=10, pady=10)
bVerde=Button(frameWS ,text="Verde", width=10, bg="green")
bVerde.grid(row=6, column=3, sticky="w", padx=10, pady=10)
bRojo=Button(frameWS ,text="Rojo", width=10, bg="red")
bRojo.grid(row=6, column=4, sticky="w", padx=10, pady=10)

raiz.mainloop()
