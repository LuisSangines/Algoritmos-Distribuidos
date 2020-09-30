# 
# Implementación del Algoritmo para exclusión mutua en un anillos
#
# Elaboro: Sangines Mártinez Luis Fernando
#

import sys
from event import Event
from model import Model
from process import Process
from simulator import Simulator
from simulation import Simulation

class Algorithm(Model):
  # Esta clase desciende de la clase Model e implementa los metodos 
  # "init()" y "receive()", que en la clase madre se definen como abstractos
  
  def init(self):
    # Aqui se definen e inicializan los atributos particulares del algoritmo

    self.sucesor = self.neighbors[0]
    self.token = False # Falso: no requieren usar la sección critica   

  def receive(self, event):

    # Se inicia el evento
    if event.getName() == "INICIA":
        print( "[", self.id, "]: recibi INICIA en t=", self.clock,"\n")
        self.transmit(Event("TOKEN", self.clock + 1.0, 1, 1))
        #Caso de prueba 1: Las solicitudes se piden en nodos en los cuales aun no ha llegado el token
        #self.transmit(Event("SOLICITUD", self.clock + 1.0, 6, 6))
        #self.transmit(Event("SOLICITUD", self.clock + 1.0, 2, 2))
        #self.transmit(Event("SOLICITUD", self.clock + 5.0, 3, 3))

        #Caso de prueba 2: 2 solicitudes donde se piden despues de haber resivido un token en un nodo
        # y la otra solicitud cuando aun no ha llegado un token
        self.transmit(Event("SOLICITUD", self.clock + 2.0, 1, 1))
        self.transmit(Event("SOLICITUD", self.clock + 5.0, 2, 2))
        self.transmit(Event("SOLICITUD", self.clock + 14.0, 3, 3))

    #Se empieza a rotar el token
    if  event.getName() == "TOKEN":
        
        if self.token == False: #Mientras nadie solicite usar la sección critica se sigue rotanto el token
            print("[", self.id, "]: Token en el nodo ", self.id ,"en el tiempo t=", self.clock, "\n" )
            self.transmit(Event("TOKEN", self.clock + 1.0, self.sucesor, self.id))
        else:
            #El token esta en el nodo y previamente se solicito el uso de la sección critica
            print("[", self.id, "]: Hay una solicitud") 
            print("[", self.id, "]: Token disponible para uso de sección critica", self.token)  
            self.transmit(Event("OK", self.clock , self.id, self.id)) 

    #Se solicita uso de la sección critica
    if event.getName() == "SOLICITUD":
        print("[", self.id, "]: Solicitud de sección critica en el nodo"
        , self.id, "en el tiempo t=", self.clock, "\n")
        self.token = True  #True: en espera del token

    #Uso de la sección critica
    if event.getName() == "OK":
        print("[", self.id, "]: En uso de la sección critica en el tiempo t=", self.clock)
        #Se suma 2 unidades de tiempo cuando ya se termina de usar la sección critica
        # Para simular el tiempo de uso 
        self.transmit(Event("LIBERA", self.clock + 2, self.id, self.id)) 
        
    #El nodo termina de usar la sección critica
    if event.getName() == "LIBERA":
        #Se vuelve a poner en rotación el token
        print("[", self.id, "]: Se termino de usar la sección critica en el tiempo t=", self.clock, "\n")
        self.token = False
        self.transmit(Event("TOKEN", self.clock + 1.0, self.sucesor, self.id))


# ----------------------------------------------------------------------------------------
# "main()"
# ----------------------------------------------------------------------------------------
# construye una instancia de la clase Simulation recibiendo como parametros el nombre del 
# archivo que codifica la lista de adyacencias de la grafica y el tiempo max. de simulacion

if len(sys.argv) != 2:
    print ("Por favor proporcione el nombre de la grafica de comunicaciones")
    print ("Ejemplo ==>python ejercicio-2.py anillo7.txt")
    raise SystemExit(1)

experiment = Simulation(sys.argv[1], 21)  

# asocia un pareja proceso/modelo con cada nodo de la grafica
for i in range(1,len(experiment.graph)+1):
    m = Algorithm()
    experiment.setModel(m, i)

# inserta un evento semilla en la agenda y arranca

seed = Event("INICIA", 0.0, 1, 1)
experiment.init(seed)
experiment.run()
