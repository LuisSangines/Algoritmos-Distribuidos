# Este archivo implementa la simulacion del algoritmo de
# recorrido en profundidad de Cheung
# Alumno: Sangines Martínez Luis Fernando

import sys
from timeit import default_timer #import para calcular el tiempo de ejecución del programa
from event import Event
from model import Model
from process import Process
from simulator import Simulator
from simulation import Simulation

mensajes_enviados = 0 #Variable glogal que cuenta los mensajes enviados en total

class AlgorithmDFS(Model):
  # Esta clase desciende de la clase Model e implementa los metodos
  # "init()" y "receive()", que en la clase madre se definen como abstractos


  def init(self):
    # Aqui se definen e inicializan los atributos particulares del algoritmo
    self.father = self.id
    self.visited = False
    self.unvisited = self.neighbors

  def go_explore_more(self):
    global mensajes_enviados
    if len(self.unvisited) > 0:
        to_visit = self.unvisited[0]
        self.unvisited = self.unvisited[1:len(self.unvisited)]
        newevent = Event("DESCUBRE", self.clock + 1.0, to_visit, self.id)
        mensajes_enviados += 1
        self.transmit(newevent)
    elif self.father != self.id:
        newevent = Event("REGRESA", self.clock + 1.0, self.father, self.id)
        mensajes_enviados += 1
        self.transmit(newevent)
        print (self.id,"termino")
    else:
        print (self.id,"termino")


  def receive(self, event):
    # Aqui se definen las acciones concretas que deben ejecutarse cuando se
    # recibe un evento
    global mensajes_enviados
    print("T = ", self.clock, " Nodo ", self.id, " Recibo :", event.getName(), "desde", event.getSource())
    if  event.getName() == "DESCUBRE":
        if  event.getSource() != self.id:
            self.unvisited.remove(event.getSource())

        if self.visited == True:
            print ("soy ", self.id, " ya estoy visitado, envio rechazo a ", event.getSource())
            newevent = Event("RECHAZO", self.clock + 1.0, event.getSource(), self.id)
            mensajes_enviados += 1
            self.transmit(newevent)
        else:
            self.visited = True
            self.father = event.getSource()
            print ("Soy ", self.id, " y mi padre es ", self.father)
            self.go_explore_more()
        if self.father == self.id:
            print ("Soy ", self.id, "y soy RAIZ" )


    elif  event.getName() == "REGRESA" or event.getName() == "RECHAZO":
        self.go_explore_more()


# ----------------------------------------------------------------------------------------
# "main()"
# ----------------------------------------------------------------------------------------
# construye una instancia de la clase Simulation recibiendo como parametros el nombre del
# archivo que codifica la lista de adyacencias de la grafica y el tiempo max. de simulacion

if len(sys.argv) != 2:
    print ("Por favor proporcione el nombre de la grafica de comunicaciones")
    raise SystemExit(1)

experiment = Simulation(sys.argv[1], 100)

# asocia un pareja proceso/modelo con cada nodo de la grafica
for i in range(1,len(experiment.graph)+1):
    m = AlgorithmDFS()
    experiment.setModel(m, i)

# inserta un evento semilla en la agenda y arranca
inicio = default_timer()
seed = Event("DESCUBRE", 0.0, 1, 1)
mensajes_enviados += 1
experiment.init(seed)
experiment.run()
fin = default_timer()
print ("\nTiempo del programa" ,fin - inicio)
print ("Mensajes enviados en total: ", mensajes_enviados,"\n")
