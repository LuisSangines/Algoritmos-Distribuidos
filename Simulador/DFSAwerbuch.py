# Este archivo implementa la simulacion del algoritmo de 
# recorrido en profundidad de Cheung 

import sys
from event import Event
from model import Model
from process import Process
from simulator import Simulator
from simulation import Simulation

class AlgorithmDFS(Model):
  # Esta clase desciende de la clase Model e implementa los metodos 
  # "init()" y "receive()", que en la clase madre se definen como abstractos
  
  def init(self):
    # Aqui se definen e inicializan los atributos particulares del algoritmo
    self.father = self.id
    self.unvisited = self.neighbors  
    self.banderas = []
    self.vecinos = []
    m = len(self.neighbors)
    for m in self.neighbors:
        self.vecinos.append(m)
    
  def receive(self, event):
    # Aqui se definen las acciones concretas que deben ejecutarse cuando se
    # recibe un evento
    print("T = ", self.clock, " Nodo ", self.id, " Recibo :", event.getName(), "desde", event.getSource(),"\n")
    if  event.getName() == "DESCUBRE":
            self.father = event.getSource()
            print ("[", self.id,"]: Mi padres es: ", self.father, "\n")
            
            if len(self.unvisited) > 0:
                n = len(self.vecinos)
                for n in self.vecinos:
                    if( n != event.getSource()):
                        print ("[", self.id,"]: Envio VISITADO a: ", n ,"\n")
                        newevent = Event("VISITADO", self.clock + 1.0, n, self.id)
                        self.transmit(newevent)
                        self.banderas.append([n,True])
            else:
                if self.father == event.getSource():
                    print ("[", self.id,"]: No tengo vecinos que visitar \n" ) 
                    newevent = Event("REGRESA", self.clock +1.0 , self.father, self.id)
                    self.transmit(newevent)
    
    if  event.getName() == "VISITADO":
        self.unvisited.remove(event.getSource())
        newevent = Event("ACK", self.clock +1.0 , event.getSource(), self.id)
        self.transmit(newevent)

    if  event.getName() == "ACK": 
        pos = self.banderas.index([event.getSource(),True])
        terminados = 0
        self.banderas[pos][1]= False
        print ("[", event.getSource(),"]: Mi bandera cambio a :", self.banderas[pos][1] ,"\n")
        n = len(self.banderas)
        for n in self.banderas:
            
            if n[1] == False:
                terminados = terminados + 1
        if terminados == len(self.banderas):
            print ("[", self.id,"]: Todas las banderas estan en FALSO \n")  
            newevent = Event("REGRESA", self.clock +1.0 , self.id, self.id)
            self.transmit(newevent)         
            
    if  event.getName() == "REGRESA":     
        if len(self.unvisited) > 0:
            to_visit = self.unvisited[0]
            newevent = Event("DESCUBRE", self.clock + 1.0, to_visit, self.id)
            self.transmit(newevent) 
            self.unvisited = self.unvisited[1:len(self.unvisited)] 
        else:
            if self.father != self.id:    
                newevent = Event("REGRESA", self.clock + 1.0, self.father, self.id)
                self.transmit(newevent)
	  

# ----------------------------------------------------------------------------------------
# "main()"
# ----------------------------------------------------------------------------------------
# construye una instancia de la clase Simulation recibiendo como parametros el nombre del 
# archivo que codifica la lista de adyacencias de la grafica y el tiempo max. de simulacion

if len(sys.argv) != 2:
    print("Please supply a file name")
    raise SystemExit(1)

experiment = Simulation(sys.argv[1], 100)  

# asocia un pareja proceso/modelo con cada nodo de la grafica
for i in range(1,len(experiment.graph)+1):
    m = AlgorithmDFS()
    experiment.setModel(m, i)

# inserta un evento semilla en la agenda y arranca

seed = Event("DESCUBRE", 0.0, 1, 1)
experiment.init(seed)
experiment.run()
