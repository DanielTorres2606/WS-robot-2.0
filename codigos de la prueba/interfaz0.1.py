from tkinter import*
from tkinter import ttk
import tkinter as tk
import time
import B2_camara
import B1
import B2_sensores

#Raiz

raiz= Tk()
raiz.title("Control Robot")
raiz.config(bg="white")
raiz.resizable(0,0)

##raiz.iconbitmap("descarga.ico")

#Frame

frameWS=Frame()
frameWS.pack()
frameWS.config(bg="white")
frameWS.config(width="600", height="2000")
#frameWS.config(cursor="pirate")


def botinit():
    
    cuadroE=Label(frameWS, text = 'Ejecutando programa...', bg="white", fg="black")
    cuadroE.grid(row=5, column=1, sticky="w",  padx=10, pady=10)
    
    i = float(cuadroTiempo.get())
    
    if lista.get() == 'B1.1 Front High':
        # X,Y,Z = B1.pruebamovimiento(1,i)
        # cuadroX = Label(frameWS, text=str(X), bg="white", fg="black")
        # cuadroX.grid(row=3, column=4, sticky="w",  padx=10, pady=10)
        # cuadroY=Label(frameWS, text=str(Y), bg="white", fg="black")
        # cuadroY.grid(row=4, column=4, sticky="w",  padx=10, pady=10)
        # cuadroZ=Label(frameWS, text=str(Z), bg="white", fg="black")
        # cuadroZ.grid(row=5, column=4, sticky="w",  padx=10, pady=10)
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
    
    if lista.get() == 'B3.1 obj 30cm US':
        X,Y,Z,US1,US2,SRP,Piso = B2_sensores.pruebamovimiento(8,i)
        cuadroX = Label(frameWS, text=str(X), bg="white", fg="black")
        cuadroX.grid(row=3, column=4, sticky="w",  padx=10, pady=10)
        cuadroY=Label(frameWS, text=str(Y), bg="white", fg="black")
        cuadroY.grid(row=4, column=4, sticky="w",  padx=10, pady=10)
        cuadroZ=Label(frameWS, text=str(Z), bg="white", fg="black")
        cuadroZ.grid(row=5, column=4, sticky="w",  padx=10, pady=10)
    
    if lista.get() == 'B3.2 obj 30cm SHARP':
        X,Y,Z,US1,US2,SRP,Piso = B2_sensores.pruebamovimiento(9,i)
        cuadroX = Label(frameWS, text=str(X), bg="white", fg="black")
        cuadroX.grid(row=3, column=4, sticky="w",  padx=10, pady=10)
        cuadroY=Label(frameWS, text=str(Y), bg="white", fg="black")
        cuadroY.grid(row=4, column=4, sticky="w",  padx=10, pady=10)
        cuadroZ=Label(frameWS, text=str(Z), bg="white", fg="black")
        cuadroZ.grid(row=5, column=4, sticky="w",  padx=10, pady=10)
    
    if lista.get() == 'B3.3 stop line':
        X,Y,Z,US1,US2,SRP,Piso = B2_sensores.pruebamovimiento(10,i)
        cuadroX = Label(frameWS, text=str(X), bg="white", fg="black")
        cuadroX.grid(row=3, column=4, sticky="w",  padx=10, pady=10)
        cuadroY=Label(frameWS, text=str(Y), bg="white", fg="black")
        cuadroY.grid(row=4, column=4, sticky="w",  padx=10, pady=10)
        cuadroZ=Label(frameWS, text=str(Z), bg="white", fg="black")
        cuadroZ.grid(row=5, column=4, sticky="w",  padx=10, pady=10)
    
    if lista.get() == 'B2.4,5,6,7 Color Camara':
        B2_camara.color(cuadroTiempo.get())
        outCamara = B2_camara.color(cuadroTiempo.get())
        #print (outCamara)
        camaraCuadro=Label(frameWS, text = outCamara, bg="white", fg="black")
        camaraCuadro.grid(row=1, column=4, sticky="w",  padx=10, pady=10)
        
        
    if lista.get() == 'B2.8,9 QR Camara':
        outCamara = B2_camara.qr(cuadroTiempo.get())
        print (outCamara)
        camaraCuadro=Label(frameWS, text = outCamara, bg="white", fg="black")
        camaraCuadro.grid(row=1, column=4, sticky="w",  padx=10, pady=10)


#Titulo interfaz

tituloLabel=Label(frameWS, text="WS Colombia, Robotica movil", font=("Small Fonts",15), fg="black", bg="white")
tituloLabel.grid(row=0, column=0, padx=0, pady=0, columnspan=6)



#Entradas y Salidas

cuadroTiempo=Entry(frameWS)
cuadroTiempo.grid(row=1, column=1, sticky="w",  padx=10, pady=10)
tiempoLabel=Label(frameWS, text="Tiempo", bg="white", fg="black")
tiempoLabel.grid(row=1, column=0, sticky="w", padx=10, pady=10)


listaPrueba=Label(frameWS, text="Prueba", bg="white", fg="black")
listaPrueba.grid(row=2, column=0, sticky="w", padx=10, pady=10)
lista = ttk.Combobox(frameWS)
lista.grid(row=2, column=1, sticky="w", padx=10, pady=10)
lista['values']=('B1.1 Front High','B1.2 Back Low','B1.3 Diagonal','B1.4 F1M','B1.5 B1M','B1.6 Giro Derecha','B1.7 Giro izquierda','B2.1 obj led US','B2.2 obj led Sharp', 'B2.3 led line',
                 'B2.4,5,6,7 Color Camara', 'B2.8,9 QR Camara','B3.1 obj 30cm US', 'B3.2 obj 30cm SHARP', 'B3.3 stop line', 'B3.4 esquinas', 'C prueba final')

botonInicio=Button(frameWS, command = botinit,text="Inicio", width=10)
botonInicio.grid(row=1, column=2, sticky="w", padx=10, pady=10)

botonParada=Button(frameWS ,text="Parada", width=10)
botonParada.grid(row=2, column=2, sticky="w", padx=10, pady=10)


camara= Label(frameWS, text="Camara", bg="white", fg="black")
camara.grid(row=1, column=3, sticky="w", padx=10, pady=10)


velocidad= Label(frameWS, text="Velocidad", bg="white", fg="black")
velocidad.grid(row=2, column=3, sticky="w", padx=10, pady=10)



x= Label(frameWS, text="X", bg="white", fg="black")
x.grid(row=3, column=3, sticky="w", padx=10, pady=10)


y= Label(frameWS, text="Y", bg="white", fg="black")
y.grid(row=4, column=3, sticky="w", padx=10, pady=10)


z= Label(frameWS, text="Z", bg="white", fg="black")
z.grid(row=5, column=3, sticky="w", padx=10, pady=10)



bateria= Label(frameWS, text="Bateria", bg="white", fg="black")
bateria.grid(row=4, column=0, sticky="w", padx=10, pady=10)
cuadroB=Entry(frameWS)
cuadroB.grid(row=4, column=1, sticky="w",  padx=10, pady=10)

estado= Label(frameWS, text= 'Estado:', bg="white", fg="black")
estado.grid(row=5, column=0, sticky="w", padx=10, pady=10)


raiz.mainloop()
