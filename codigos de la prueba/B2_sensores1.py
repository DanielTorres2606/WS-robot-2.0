from pyArduino import *
import matplotlib.pyplot as plt
import numpy as np

def pruebamovimiento (prueba=0, tf = 60):

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
	arduino = serialArduino(port, baudRate,7)
	arduino.readSerialStart()

	######## VELOCIDADES MEDIDAS #########

	ufMeas = 0.0 * np.ones (N)
	ulMeas = 0.0 * np.ones (N)
	wMeas = 0.0 * np.ones (N)
	
	US1 = 0.0
	US2 = 0.0
	Sharp = 0.0
	Piso = 0
	
	prevError = 0.0
	sumaError = 0.0

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
	
		print ('ultrasonido 1: ' + str(US1))
		#print ('ultrasonido 2: ' + str(US2))
		#print ('Sharp:  ' + str(Sharp))
		#print ('Piso:  ' + str(Piso))
		
		if (prueba == 8):
			error = 20 - US1
			if (US1 > 21):
				Vf =+ (error * 0.2) + (prevError * 0.3)+(sumaError* 0.1)
				Vf = max(min(-3, Vf,),-5)
		
			elif (US1 < 19):
				#Vf = error * 0.8 #KP
				Vf =+ (error * 1) + (prevError * 0.55)+(sumaError* 0.1125)
				Vf = max(min(3, Vf,),5)
		
			else:
				Vf = 0
				#Vf = max(min(5, Vf,),-8)
	
			print(Vf)
		
			prevError = error
			#sumaError =+ error
		
		if (prueba==9):
			
			error = 20 - Sharp
			if (Sharp < 19):
				Vf =+ (error * 1) + (prevError * 0.55)+(sumaError* 0.1)
				Vf = max(min(-3.2, Vf,),-5)
			
			elif (Sharp > 21):
				#Vf = error * 0.8 #KP
				Vf =+ (error * 0.2) + (prevError * 0.25)+(sumaError* 0.1125)
				Vf = max(min(3, Vf,),5)

			else:
				Vf = 0
		#Vf = max(min(5, Vf,),-8)
	
			print(Vf)
			
		
		
		ufRef = Vf * np.ones (N) 	# Velocidad lineal en metros / segundo [m/s] eje x * 1.25
		
		phi [k+1] = phi[k] + ts * wMeas[k]
		
		hxp = ufMeas[k] * np.cos(phi[k+1]) - ulMeas[k] * np.sin(phi[k+1])
		hyp = ufMeas[k] * np.cos(phi[k+1]) + ulMeas[k] * np.sin(phi[k+1])
		
		hx[k+1] = hx[k] + hxp
		hy[k+1] = hy[k] + hyp
		
		elapsed_time = time.time() - start_time
		time.sleep (ts-elapsed_time) #espera a terminar el tiempo de muestreo

	#################### COMUNICACION SERIAL ############
	arduino.sendData([0,0,0]) # Detiene el robot
	arduino.close() #cierra el puerto serial
pruebamovimiento(8,60)
