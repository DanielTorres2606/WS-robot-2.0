# from pyRobotics import *
# import matplotlib.pyplot as plt

from pyArduino import *
import matplotlib.pyplot as plt
import numpy as np
import time

#################### TIEMPO ###################

tf = 30 # tiempo de simulacion
ts = 0.1 #  tiempo de muestreo
t = np.arange(0,tf+ts,ts) # vector tiempo

N = len(t) # cantidad de muestras

###################  PARAMETROS DEL ROBOT ################### 

a = 0  # Distancia hacia el punto de control en metros [m]

################### CONDICIONES INICIALES ###################
# Asignar memoria 
x1 = np.zeros(N+1) 
y1 = np.zeros(N+1)
phi = np.zeros(N+1)

x1[0] = 0   # Posicion inicial en el eje x en metros [m]
y1[0] = 0  # Posicion inicial en el eje y en metros [m]
phi[0] = 0*(np.pi/180)  # Orientacion inicial en radianes [rad]


################### PUNTO DE CONTROL ###################


# Asignar memoria 
hx = np.zeros(N+1) 
hy = np.zeros(N+1)

hx[0] = x1[0]+a*np.cos(phi[0])  
hy[0] = y1[0]+a*np.sin(phi[0])


################### CAMINO DESEADO ####################
vMax = 8 # Velocidad maxima deseada en metros/segundo [m/s]

#Camino de 1 linea
div = 300

pxd1 = 0
pxd2 = 59.5

pyd1 = 0
pyd2 = 0

pxd = np.linspace(pxd1,pxd2,div)
pyd = np.linspace(pyd1,pyd2,div)

#Camino de 2 linea
##div = 250
##
##pointX = [0,1,2]
##pointY = [0,0.8,1.2]
##
##px = []
##py = []
##
##px.append(np.linspace(pointX[0],pointX[1],div))
##py.append(np.linspace(pointY[0],pointY[1],div))
##
##px.append(np.linspace(pointX[1],pointX[2],div))
##py.append(np.linspace(pointY[1],pointY[2],div))
##
##pxd = np.hstack(px)
##pyd = np.hstack(py)


# Camino de n lineas
# div = 300

# pointX = [0,-0.1,-20.69,  -20.7,  -20.7, -20.69,  -0.1,    0,   0]
# pointY = [0,   0,    0,  -0.1, -20.69,  -20.7,  -20.7,-20.69,-0.1]

# px = []
# py = []

# for p in range(len(pointX)-1):
     # px.append(np.linspace(pointX[p],pointX[p+1],div))
     # py.append(np.linspace(pointY[p],pointY[p+1],div))

# pxd = np.hstack(px)
# pyd = np.hstack(py)     


sizePoints = len(pxd)

beta = np.zeros(sizePoints)

for p in range(sizePoints):
     if p == 0:
          beta[p] = np.arctan2(pyd[p+1]-pyd[p],pxd[p+1]-pxd[p])
     else:
          beta[p] = np.arctan2(pyd[p]-pyd[p-1],pxd[p]-pxd[p-1])

phid = 0*(np.pi/180)*np.ones(N)
phidp = np.zeros(N)

################### VELOCIDADES DE REFERENCIA #################### 

ufRef = np.zeros(N) # Velocidad lineal en metros/segundos [m/s] eje x 
ulRef = np.zeros(N) # Velocidad lineal en metros/segundos [m/s] eje y
wRef = np.zeros(N) # Velocidad angular en radianes/segundos [rad/s]

######## VELOCIDADES MEDIDAS #########

ufMeas = np.zeros (N)
ulMeas = np.zeros (N)
wMeas = np.zeros (N)

################### ERRORES ####################
hxe = np.zeros(N) # Error en el eje x en metros [m]
hye = np.zeros(N) # Error en el eje y en metros [m]
phie = np.zeros(N) # Error de orientación en radianes [rad]


################ COMUNICACION SERIAL ############
port = '/dev/ttyACM0'
baudRate = 9600
arduino = serialArduino(port, baudRate,7)
arduino.readSerialStart()


################### BUCLE ####################  
for k in range(N):
     ################# CONTROLADOR ###############
     start_time = time.time() # MIDE EL TIEMPO ACTUAL
     
     
     # Punto mas cercano
     minimo = 1000
     for p in range(sizePoints):
          distancia = np.sqrt((pxd[p]-hx[k])**2+(pyd[p]-hy[k])**2)

          if distancia<minimo:
               minimo = distancia
               pos = p
     # Error

     hxe[k] = pxd[pos]-hx[k]
     hye[k] = pyd[pos]-hy[k]
     phie[k] = phid[k] - phi[k]

     he = np.array([[hxe[k]],[hye[k]],[phie[k]]])

     # Matriz Jacobiana
     J = np.array([[ np.cos(phi[k]), -np.sin(phi[k]), -a*np.sin(phi[k])],
                   [ np.sin(phi[k]),    np.cos(phi[k]), a*np.cos(phi[k])],
                   [ 0             ,   0              ,1                ]])

     
     # Parametros de control
     K =  10*np.array([[1, 0, 0],
                      [0, 1, 0],
                      [0, 0, 1]])

     # Velocidad deseada
     pxdp = vMax*np.cos(beta[pos])
     pydp = vMax*np.sin(beta[pos])

     pdp = np.array([[pxdp],[pydp],[phidp[k]]])

     # Ley de control
     qpRef = np.linalg.pinv(J)@(pdp+K@he)
     

     #################### APLICAR ACCIONES DE CONTROL #####################

     ufRef[k] = qpRef[0][0]
     ulRef[k] = qpRef[1][0]
     wRef[k] = qpRef[2][0]
     
     arduino.sendData ([ufRef[k],ulRef[k],wRef[k]])
     
     ufMeas[k] = arduino.rawData[0]
     ulMeas[k] = arduino.rawData[1]
     wMeas[k] = arduino.rawData[2]

    # Integral numerica
     phi[k+1] = phi[k]+ts*wRef[k]

     # Modelo cinemático
     
     x1p = ufRef[k]*np.cos(phi[k+1])-ulRef[k]*np.sin(phi[k+1])
     y1p = ufRef[k]*np.sin(phi[k+1])+ulRef[k]*np.cos(phi[k+1])
     
     # Integral numerica
     x1[k+1] = x1[k] + ts*x1p
     y1[k+1] = y1[k] + ts*y1p

     hx[k+1] = x1[k+1]+a*np.cos(phi[k+1])  
     hy[k+1] = y1[k+1]+a*np.sin(phi[k+1])
# arduino.sendData([-15,0,0])
# time.sleep(1)
arduino.sendData([0,0,0]) # Detiene el robot
arduino.close() #cierra el puerto serial


################### SIMULACION VIRTUAL #################### 
# # Cargar componentes del robot
# path = "stl"
# color = ['yellow','white']
# omni3 = robotics(path,color)

# # Configurar escena
# xmin = -2
# xmax = 2
# ymin = -2
# ymax = 2
# zmin = 0
# zmax = 2
# bounds = [xmin, xmax, ymin, ymax, zmin, zmax]
# omni3.configureScene(bounds)

# # Mostrar graficas
# omni3.plotDesiredTrajectory(pxd,pyd)
# omni3.initTrajectory(hx,hy)

# escala = 2
# omni3.initRobot(x1,y1,phi,escala)

# omni3.startSimulation(1,ts)


############################## Graficas ######################
     
# Errores
fig = plt.figure()

plt.subplot(211)
plt.plot(t,hxe,'b',linewidth = 2, label='hxe')
plt.plot(t,hye,'r',linewidth = 2,  label='hye')
plt.legend(loc='upper right')
plt.xlabel('Tiempo [s]')
plt.ylabel('Error [m]')
plt.grid()

plt.subplot(212)
plt.plot(t,phie,'g',linewidth = 2, label='phie')
plt.legend(loc='upper right')
plt.xlabel('Tiempo [s]')
plt.ylabel('Error [rad]')
plt.grid()

    
# Acciones de control
fig = plt.figure()
plt.subplot(211)
plt.plot(t,ufRef,linewidth = 2,label='Velocidad frontal [vx]')
plt.plot(t,ulRef,linewidth = 2,label='Velocidad lateral [vy]')
plt.legend(loc='upper right')
plt.xlabel('Tiempo [s]')
plt.ylabel('Velocidad [m/s]')
plt.grid()

plt.subplot(212)
plt.plot(t,wRef,linewidth = 2,label='Velocidad angular [w]')
plt.legend(loc='upper right')
plt.xlabel('Tiempo [s]')
plt.ylabel('Velocidad [rad/s]')
plt.grid()

plt.show()     

















