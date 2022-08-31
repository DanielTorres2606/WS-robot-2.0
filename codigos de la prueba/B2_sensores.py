from pyArduino import *
import matplotlib.pyplot as plt
import numpy as np

paradas = False
Bateria = 0

def posicionamiento (prueba=0, tf = 1.5):
        print("INFO: POSICIONAMIENTO ACTIVO")
        global paradas
        global Bateria

        ######## TIEMPO	#########

        #tf = 1.5
        ts = 0.1
        t = np.arange (0, tf + ts, ts)

        N = len(t)
        Vf = 0

        ####### CONDICIONES INICIALES ####### 
        ## ASIGNAMOS MEMORIA

        hx = np.zeros (N + 1)
        hy = np.zeros (N + 1)
        phi = np.zeros (N + 1)

        hx[0] = 0
        hy[0] = 0 
        phi[0] = 0*(np.pi/180)

        ######## VELOCIDADES DE REFERENCIAS #########

        if (prueba == 8):   # avanza hacia adelante y se detiene a 14cm de la pared
                ufRef =  Vf * np.ones (N) 	# Velocidad lineal en metros / segundo [m/s] eje x * 1.25
                ulRef =  0.0 * np.ones (N) 	# Velocidad lineal en metros / segundo [m/s] eje y
                wRef =   0.0 * np.ones (N)  	# Velocidad lineal en radianes / segundo [rad/s]

        elif (prueba == 9): # avanza hacia atras y se detiene a 14cm de la pared
                ufRef =  Vf *  np.ones (N) 	# Velocidad lineal en metros / segundo [m/s] eje x * 1.25
                ulRef =  0.0 *  np.ones (N) 	# Velocidad lineal en metros / segundo [m/s] eje y
                wRef =   0.0 *  np.ones (N)  	# Velocidad lineal en radianes / segundo [rad/s]

        elif (prueba == 10): # avanza hacia adelante y para al leer una linea
                ufRef =  Vf *  np.ones (N) 	# Velocidad lineal en metros / segundo [m/s] eje x * 1.25
                ulRef =  0.0 *  np.ones (N) 	# Velocidad lineal en metros / segundo [m/s] eje y
                wRef =   0.0 *  np.ones (N)  	# Velocidad lineal en radianes / segundo [rad/s]

        else:
                ufRef =  0.0 * 1.25 * np.ones (N) 	# Velocidad lineal en metros / segundo [m/s] eje x * 1.25
                ulRef =  0.0 * 1.25 * np.ones (N) 	# Velocidad lineal en metros / segundo [m/s] eje y
                wRef =   0.0 * 1.25 * np.ones (N)  	# Velocidad lineal en radianes / segundo [rad/s]
                

        ################ COMUNICACION SERIAL ############
        port = '/dev/ttyACM0'
        baudRate = 9600
        arduino = serialArduino(port, baudRate,8)
        arduino.readSerialStart()

        ######## VELOCIDADES MEDIDAS #########

        ufMeas = 0.0 * np.ones (N)
        ulMeas = 0.0 * np.ones (N)
        wMeas = 0.0 * np.ones (N)

        ####### SENSORES ######

        US1 = 0.0
        US2 = 0.0
        Sharp = 0.0
        Piso = 0
        Bateria = 0.0

        prevError = 0
        sumaError = 0
        ####### BUCLE DESIMULACION #####
        time.sleep(2)
        for k in range (N):
                start_time = time.time() # MIDE EL TIEMPO ACTUAL

                arduino.sendData ([ufRef[k],ulRef[k],wRef[k]])

                ufMeas[k] = arduino.rawData[0]
                ulMeas[k] = arduino.rawData[1]
                wMeas[k] = arduino.rawData[2]
                US1 = arduino.rawData[3]
                US2 = arduino.rawData[4]
                Sharp = arduino.rawData[5]
                Piso = arduino.rawData[6]
                Bateria = arduino.rawData[7]

                #print ('ultrasonido 1: ' + str(US1))
                #print ('ultrasonido 2: ' + str(US2))
                #print ('Sharp:  ' + str(Sharp))
                #print ('Piso:  ' + str(Piso))
                
                if (prueba == 8):
                        error = 30 - US1
                        if (US1 > 31):
                                Vf =+ (error * 0.2) + (prevError * 0.3)+(sumaError* 0.1)
                                Vf = max(min(-3, Vf,),-5)
                                
                        elif (US1 < 29):
                                Vf =+ (error * 1) + (prevError * 0.55)+(sumaError* 0.1125)
                                Vf = max(min(3, Vf,),5)
                
                        else:
                                Vf = 0
                                

                        #print(Vf)
                
                        prevError = error
                        #sumaError =+ error
                
                if (prueba==9):
                        
                        error = 30 - Sharp
                        if (Sharp < 29):
                                Vf =+ (error * 1) + (prevError * 0.55)+(sumaError* 0.1)
                                Vf = max(min(-3.2, Vf,),-5)
                
                        elif (Sharp > 31):
                                #Vf = error * 0.8 #KP
                                Vf =+ (error * 0.2) + (prevError * 0.25)+(sumaError* 0.1125)
                                Vf = max(min(3, Vf,),5)

                        else:
                                Vf = 0
                #Vf = max(min(5, Vf,),-8)

                        print(Vf)
                        prevError = error
                if (prueba == 10):
                        if (Piso == 1):
                                Vf = -15
                                arduino.sendData([Vf,0,0]) # Detiene e l robot	
                                #print(Vf)
                                break
                
                
                ufRef = Vf * np.ones (N) 	# Velocidad lineal en metros / segundo [m/s] eje x * 1.25

                phi [k+1] = phi[k] + ts * wMeas[k]
                
                hxp = ufMeas[k] * np.cos(phi[k+1]) - ulMeas[k] * np.sin(phi[k+1])
                hyp = ufMeas[k] * np.cos(phi[k+1]) + ulMeas[k] * np.sin(phi[k+1])
                
                hx[k+1] = hx[k] + hxp
                hy[k+1] = hy[k] + hyp
                
                #return hx[k+1], hy[k+1], phi [k+1], US1, US2, Sharp, Piso
                
                elapsed_time = time.time() - start_time
                time.sleep (ts-elapsed_time) #espera a terminar el tiempo de muestreo
                
                if paradas==True:
                        print("INFO: POSICIONAMIENTO ABORTADO")
                        break

        #################### COMUNICACION SERIAL ############
        arduino.sendData([0,0,0]) # Detiene el robot
        if paradas==False:
                print("INFO: POSICIONAMIENTO FINALIZADO")
        arduino.close() #cierra el puerto serial

FUS1 = 0
FUS2 = 0
FSharp = 0
FPiso = 0
	
def sensor(prueba=0, tf = 30):
        print("INFO: SENSORES ACTIVO")

        #tf = 60
        ts = 0.1
        t = np.arange (0, tf + ts, ts)

        N = len(t)

        US1 = 0.0
        US2 = 0.0
        Sharp = 0.0
        Piso = 0

        ######## VELOCIDADES MEDIDAS #########

        ufMeas = 0.0 * np.ones (N)
        ulMeas = 0.0 * np.ones (N)
        wMeas = 0.0 * np.ones (N)

        ################ COMUNICACION SERIAL ############
        port = '/dev/ttyACM0'
        baudRate = 9600
        arduino = serialArduino(port, baudRate,8)
        arduino.readSerialStart()

        #######BUCLE#####
        #for k in range (N):
        global Bateria
        global paradas
        while paradas == False:
                start_time = time.time() # MIDE EL TIEMPO ACTUAL

                ufMeas = arduino.rawData[0]
                ulMeas = arduino.rawData[1]
                wMeas = arduino.rawData[2]
                US1 = arduino.rawData[3]
                US2 = arduino.rawData[4]
                Sharp = arduino.rawData[5]
                Piso = arduino.rawData[6]
                Bateria = arduino.rawData[7]
                
                
                global FUS1
                global FUS2
                global FSharp
                global FPiso
                
                #print ('ultrasonido 1: ' + str(US1))
                #print ('ultrasonido 2: ' + str(US2))
                # print ('Sharp:  ' + str(Sharp))
                #print ('Piso:  ' + str(Piso))
                
                if (prueba == 1):
                        if (US1 > 29):
                                FUS1 = 1
                        else: FUS1 = 0
                
                # if (prueba == X):
                        # if (US2 > 29):
                                # FUS2 = 1
                        # else: FUS2 = 0
                        
                if (prueba == 2):
                        if (Sharp > 29):
                                FSharp = 1
                        else: FSharp = 0
                
                if (prueba == 3):
                        if (Piso == 1):
                                FPiso = 1
                        else: FPiso = 0
                if paradas == True:
                        print("INFO: SENSORES ABORTADO")
                        break
                        
                elapsed_time = time.time() - start_time
                time.sleep (ts-elapsed_time) #espera a terminar el tiempo de muestreo
        if paradas==False:
                print("INFO: PRUEBAS DE MOVIMIENTO FINALIZADO")
        arduino.sendData([0,0,0]) # Detiene el robot
        arduino.close() #cierra el puerto serial
		
#sensor()
