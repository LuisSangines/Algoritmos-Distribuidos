# 
# Implementa la simulacion Cliente-Servidor
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

    #Dejamos al servidor abierto para que pueda resivir solicitudes
    if self.id == 1 :
        self.rol = "Servidor"
        self.libre= True # True = libre , False=ocupado 
        print("[", self.id, "]", "Soy ", self.rol, "\n¿El servidor esta libre? : " , self.libre, "\n")
    else:
        self.rol = "Cliente"
        self.sucesor = self.neighbors[0]
        print("[", self.id, "]", "Soy ", self.rol, "\n" )


  def receive(self, event):

    # Se inicia el evento
    if event.getName() == "INICIA":
        print( "[", self.id, "]: recibi INICIA en t=", self.clock,"\n")
        self.transmit(Event("SOLICITUD", self.clock + 3.0, 1, 3))
        self.transmit(Event("SOLICITUD", self.clock + 6.0, 1, 6))
        self.transmit(Event("SOLICITUD", self.clock + 7.0, 1, 2))

    #Se resiven las solcitudes mandadas
    if  event.getName() == "SOLICITUD":
        print("[", self.id, "]: Recibi una solicitud en t=", self.clock, 
        "de parte del cliente :", event.getSource(), "\n" )
        if self.libre == True :
            self.libre = False
            self.transmit(Event("OK", self.clock + 1.0, event.getSource(), self.id))
        else:
            print("Servidor ocupado, entra a la cola el cliente :", event.getSource(),"\n")  
            newevent=Event("SOLICITUD", self.clock + 3.0, 1, event.getSource())
            self.transmit(newevent)
            
                
    #Se confirma al cliente para que pueda ocupar el servidor        
    if  event.getName() == "OK":
        print("[", self.id, "]: Recicbi un OK de ", event.getSource(),"en t=", self.clock,"\n")
        self.transmit(Event("LIBERA", self.clock + 1.0, self.sucesor, self.id))

    #Al recibir "LIBERA" del cliente, el servidor pasa a estar libre para resivir otro cliente   
    if  event.getName() == "LIBERA":        
        print("[", self.id, "]: Se libera el servidor t=", self.clock, "\n")
        self.libre = True



# ----------------------------------------------------------------------------------------
# "main()"
# ----------------------------------------------------------------------------------------
# construye una instancia de la clase Simulation recibiendo como parametros el nombre del 
# archivo que codifica la lista de adyacencias de la grafica y el tiempo max. de simulacion

if len(sys.argv) != 2:
    print ("Por favor proporcione el nombre de la grafica de comunicaciones")
    print ("Ejemplo ==>python ejercicio-1.py estrella.txt")
    raise SystemExit(1)

experiment = Simulation(sys.argv[1], 20)  

# asocia un pareja proceso/modelo con cada nodo de la grafica
for i in range(1,len(experiment.graph)+1):
    m = Algorithm()
    experiment.setModel(m, i)

# inserta un evento semilla en la agenda y arranca

seed = Event("INICIA", 0.0, 1, 1)
experiment.init(seed)
experiment.run()


