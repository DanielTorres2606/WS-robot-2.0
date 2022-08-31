from pyArduino import *
import matplotlib.pyplot as plt
import numpy as np
paradas = False
Bateria = 0
def pruebamovimiento (prueba=0, tf = 1.5, Q = 0):
        print("INFO: POSICIONAMIENTO ACTIVO")
        global paradas
        global Bateria
	######## TIEMPO	#########
        #tf = 1.5
        ts = 0.1
        t = np.arange (0, tf + ts, ts)

        N = len(t)

        ####### CONDICIONES INICIALES ####### 
        ## ASIGNAMOS MEMORIA

        hx = np.zeros (N + 1)
        hy = np.zeros (N + 1)
        phi = np.zeros (N + 1)

        hx[0] = 0
        hy[0] = 0 
        phi[0] = 0*(np.pi/180)

        ######## VELOCIDADES DE REFERENCIAS #########

        if (prueba == 1):   # avanza a maxima velocidad hacia adelante
                ufRef =  10.0 * np.ones (N) 	# Velocidad lineal en metros / segundo [m/s] eje x * 1.25
                ulRef =  0.0 * np.ones (N) 	# Velocidad lineal en metros / segundo [m/s] eje y
                wRef =   0.0 * np.ones (N)  	# Velocidad lineal en radianes / segundo [rad/s]
        elif (prueba == 2): # avanza a baja velocidad hacia atras
                ufRef = -5.0 *  np.ones (N) 	# Velocidad lineal en metros / segundo [m/s] eje x * 1.25
                ulRef =  0.0 *  np.ones (N) 	# Velocidad lineal en metros / segundo [m/s] eje y
                wRef =   0.0 *  np.ones (N)  	# Velocidad lineal en radianes / segundo [rad/s]
        elif (prueba == 3): # se mueve en diagonal
                ufRef =  10.0 *  np.ones (N) 	# Velocidad lineal en metros / segundo [m/s] eje x * 1.25
                ulRef =  10.0 *  np.ones (N) 	# Velocidad lineal en metros / segundo [m/s] eje y
                wRef =   0.0 *  np.ones (N)  	# Velocidad lineal en radianes / segundo [rad/s]
        elif (prueba == 4): # avanza 1m adelante
                ufRef =  10.0 *  np.ones (N) 	# Velocidad lineal en metros / segundo [m/s] eje x * 1.25
                ulRef =  0.0 *  np.ones (N) 	# Velocidad lineal en metros / segundo [m/s] eje y
                wRef =   0.0 *  np.ones (N)  	# Velocidad lineal en radianes / segundo [rad/s]
        elif (prueba == 5): # avanza 1m atras
                ufRef =  -7.0 *  np.ones (N) 	# Velocidad lineal en metros / segundo [m/s] eje x * 1.25
                ulRef =  0.0 *  np.ones (N) 	# Velocidad lineal en metros / segundo [m/s] eje y
                wRef =   0.0 *  np.ones (N)  	# Velocidad lineal en radianes / segundo [rad/s]
        elif (prueba == 6): #gira en sentido horario
                ufRef =  0.0 *  np.ones (N) 	# Velocidad lineal en metros / segundo [m/s] eje x * 1.25
                ulRef =  0.0 *  np.ones (N) 	# Velocidad lineal en metros / segundo [m/s] eje y
                wRef =   -20.0 *  np.ones (N)  	# Velocidad lineal en radianes / segundo [rad/s]
        elif (prueba == 7): # gira en sentido antihorario
                ufRef =  0.0  * np.ones (N) 	# Velocidad lineal en metros / segundo [m/s] eje x * 1.25
                ulRef =  0.0  * np.ones (N) 	# Velocidad lineal en metros / segundo [m/s] eje y
                wRef =   20.0 * np.ones (N)  	# Velocidad lineal en radianes / segundo [rad/s]
        else:
                ufRef =  0.0 * np.ones (N) 	# Velocidad lineal en metros / segundo [m/s] eje x * 1.25
                ulRef =  0.0 * np.ones (N) 	# Velocidad lineal en metros / segundo [m/s] eje y
                wRef =   0.0 * np.ones (N)  	# Velocidad lineal en radianes / segundo [rad/s]
                

        ################ COMUNICACION SERIAL ############
        port = '/dev/ttyACM0'
        baudRate = 9600
        arduino = serialArduino(port, baudRate,8)
        arduino.readSerialStart()

        ######## VELOCIDADES MEDIDAS #########

        ufMeas = 0.0 * np.ones (N)
        ulMeas = 0.0 * np.ones (N)
        wMeas = 0.0 * np.ones (N)

        Bateria = 0.0
        US1 = 0.0
        US2 = 0.0
        Sharp = 0.0
        Piso = 0


        ####### BUCLE DESIMULACION #####
        time.sleep(2)
        for k in range (N):
                
                if paradas==True:
                        print("INFO: PRUEBAS DE MOVIMIENTO ABORTADO")
                        break
                        
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
                
                #X[k]    = arduino.rawData[0]
                #Y[k]    = arduino.rawData[1]
                #PHI[k]  = arduino.rawData[2]

                phi [k+1] = phi[k] + ts * wMeas[k]

                hxp = ufMeas[k] * np.cos(phi[k+1]) - ulMeas[k] * np.sin(phi[k+1])
                hyp = ufMeas[k] * np.cos(phi[k+1]) + ulMeas[k] * np.sin(phi[k+1])	

                hx[k+1] = hx[k] + hxp
                hy[k+1] = hy[k] + hyp
                
                elapsed_time = time.time() - start_time
                time.sleep (ts-elapsed_time) #espera a terminar el tiempo de muestreo
                

        #################### COMUNICACION SERIAL ############
        arduino.sendData([0,0,0]) # Detiene el robot
        if paradas==False:
                print("INFO: PRUEBAS DE MOVIMIENTO FINALIZADO")
        arduino.close() #cierra el puerto serial
