#from pyzbar import pyzbar
import pyzbar
import time # revisar para procurar no generar retrasos
import numpy as np
from cv2 import *
paradas = False

def QR_barcode(Q=False):
    global paradas
    BarcodeData = "no encontrado"
    print("INFO: QR ACTIVO")
    camara=cv2.VideoCapture(0)
    
    while True:    
        _,frame=camara.read()
        ret,raw = camara.read()
        raw = cv2.flip(raw,-1)
        
        for barcode in decode(raw):
            BarcodeData = barcode.data.decode("utf-8")
            return BarcodeData 
        if paradas:
            print("INFO: QR ABORTADO")
            break
    if paradas == False:
        print("INFO: QR APAGADO")
    cap.release()
    cv2.destroyAllWindows()


def color (entrada='None'):
    print("INFO: COLOR ACTIVO")
    global paradas
    def dibujar (mask, color):
        contornos,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #Blue, Green, Red
        for i in contornos:
            area = cv2.contourArea(i)
            if area > 10000:
                M = cv2.moments(i)
                if(M['m00']==0): M['m00'] = 1
                x = int(M['m10']/M['m00'])
                y = int(M['m01']/M['m00'])
                if color[0] == 0 and color[1] == 0 and color[2] != 0:
                        z = 'rojo'
                elif color[0] == 0 and color[1] != 0 and color[2] == 0:
                        z = 'verde'
                elif color[0] != 0 and color[1] == 0 and color[2] == 0:
                        z = 'azul'
                elif color[0] == 0 and color[1] != 0 and color[2] != 0:
                        z = 'amarillo'

                nuevoContorno = cv2.convexHull(i)
                #cv2.putText (frame, z, (x+10,y+20), FONT_HERSHEY_SIMPLEX, 1,[255,255,255], 1, cv2.LINE_AA)
                #cv2.drawContours(frame, [nuevoContorno], 0, color, 3)
                return (z)
    cap = cv2.VideoCapture(0)
    # valores de color
    amarilloBajo = np.array ([20,100,20], np.uint8)
    amarilloAlto = np.array ([32,255,255], np.uint8)

    azulBajo = np.array ([100,100,20], np.uint8)
    azulAlto = np.array ([125,255,255], np.uint8)

    rojoBajo1 = np.array ([0,100,20], np.uint8)
    rojoAlto1 = np.array ([10,255,255], np.uint8)
    rojoBajo2 = np.array ([175,100,20], np.uint8)
    rojoAlto2 = np.array ([180,255,255], np.uint8)

    verdeBajo = np.array ([36,100,20], np.uint8)
    verdeAlto = np.array ([70,255,255], np.uint8)
    
    salida = 'None'
    

    while True:
        ret, frame=cap.read()
        if ret:
            frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            ylw = cv2.inRange (frameHSV, amarilloBajo, amarilloAlto)
            blue = cv2.inRange (frameHSV, azulBajo, azulAlto)
            Red1 = cv2.inRange (frameHSV, rojoBajo1, rojoAlto1)
            Red2 = cv2.inRange (frameHSV, rojoBajo2, rojoAlto2)
            Red = cv2.add (Red1, Red2)
            Grn = cv2.inRange (frameHSV, verdeBajo, verdeAlto)


            resultado = [dibujar(ylw, (0,255,255)), dibujar(blue, (255,0,0)), dibujar(Red, (0,0,255)), dibujar(Grn, (0,255,0)) ]

            if entrada == resultado[0]:
                salida = resultado[0]
                break
                

            elif entrada == resultado[1]:
                salida = resultado[1]
                break

            elif entrada == resultado[2]:
                salida = resultado[2]
                break

            elif entrada == resultado[3]:
                salida = resultado[3]
                break

            if cv2.waitKey(1) & 0xFF == ord('s'):
                break
            
            if paradas:
                print("INFO: COLOR ABORTADO")
                break
            
            #PRUEBAS DE LECTURA
            #cv2.imshow('rojo', Red)
            #cv2.imshow('Azul', blue)
            #cv2.imshow('Verde', Grn)
            #cv2.imshow('Amarillo',ylw)
            #cv2.imshow('camara', frame)
    if paradas == False:
        print("INFO: COLOR APAGADO")
    cap.release()
    cv2.destroyAllWindows()
    return salida   
                
#color()

