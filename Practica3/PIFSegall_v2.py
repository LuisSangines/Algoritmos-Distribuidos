# Este archivo implementa la simulacion del algoritmo de
# recorrido en profundidad de Segall separandolos en 2 mensajes uno de bajado y otro de subida
# Alumno: Sangines Martínez Luis Fernando

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
    self.visitado = False
    self.vecinos = self.neighbors
    self.ok = []
    n = len(self.neighbors)
    for n in self.neighbors:
        self.ok.append([n,False])

  def receive(self, event):
    # Aqui se definen las acciones concretas que deben ejecutarse cuando se
    # recibe un evento
    global mensajes_enviados
    print("T = ", self.clock, " Nodo ", self.id, " Recibo :", event.getName(), "desde", event.getSource(),"\n")
    if  event.getName() == "BAJADA":
            cont = 0
            if self.id != event.getSource():
                pos = self.neighbors.index(event.getSource())
                self.ok[pos][1] = True
                #print ("[", self.id,"]: Cambie la bandera de :" ,event.getSource()," a" , self.ok[pos][1] ,"\n")
            n = len(self.neighbors)
            if self.visitado == False:
                self.father = event.getSource()
                self.visitado = True
                if event.getDistance() < pow( 2, event.getRound()): #Verificamos que aun no se halla sobrepasado la distancia dada
                    for n in self.ok:
                        if n[0] != event.getSource():
                            #print ("[", self.id,"]: Envio M a :" , n[0],"\n")
                            newevent = Event("BAJADA", self.clock +1.0 , n[0], self.id, event.getDistance() + 1, event.getRound())
                            self.transmit(newevent)
                else:
                    if event.getDistance() == pow( 2, event.getRound()):
                        if self.father != self.id:
                            newevent = Event("SUBIDA", self.clock +1.0 , self.father, self.id, event.getDistance(), event.getRound())
                            self.transmit(newevent)
            for n in self.ok:
                if n[1] == True:
                    cont = cont + 1
            if cont == len(self.neighbors):
                if self.father != self.id:
                    newevent = Event("SUBIDA", self.clock +1.0 , self.father, self.id, event.getDistance(), event.getRound())
                    self.transmit(newevent)

    if event.getName() == "SUBIDA":
        if self.id != event.getSource():
            pos = self.neighbors.index(event.getSource())
            self.ok[pos][1] = True
        n = len(self.neighbors)
        cont = 0
        for n in self.ok:
            if n[1] == True:
                cont = cont + 1
        if cont == len(self.neighbors):
            if self.father != self.id:
                newevent = Event("SUBIDA", self.clock +1.0 , self.father, self.id, event.getDistance(), event.getRound())
                self.transmit(newevent)

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
#seed = Event("BAJADA", 0.0, 1, 1, 1, 1)   #Solo recorre una distancia de 2 y no recorre todo el grafo
seed = Event("BAJADA", 0.0, 1, 1, 1, 2)  #Solo recorre una distancia de 4 y no recorre todo el grafo
#seed = Event("BAJADA", 0.0, 1, 1, 1, 3)  #Solo recorre una distancia de 6 y recorre todo el grafo
experiment.init(seed)
experiment.run()
