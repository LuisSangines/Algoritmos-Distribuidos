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
    self.estado = "no_visitado"
    self.edo_vecinos = []
    m = len(self.neighbors)
    for m in self.neighbors:
        self.edo_vecinos.append([m,"no_visitado"])

  def explore(self):
    n = len(self.edo_vecinos)
    cont = 0
    for n in self.edo_vecinos:
        if n[1] == "no_visitado":
            cont = cont + 1
            print ("[", self.id,"]: Envio descubre a : ", n[0],"\n")
            newevent = Event("DESCUBRE", self.clock +1.0 , n[0], self.id)
            self.transmit(newevent)
            n[1] = "hijo"
            break
    if cont == 0:
        for n in self.edo_vecinos:        
            if n[1] == "Padre":
                newevent = Event("DESCUBRE", self.clock +1.0 , n[0], self.id)
                self.transmit(newevent)
                print ("[", self.id,"]Envio descubre a ", n[0], "\n")



  def receive(self, event):
    # Aqui se definen las acciones concretas que deben ejecutarse cuando se
    # recibe un evento
    print("T = ", self.clock, " Nodo ", self.id, " Recibo :", event.getName(), "desde", event.getSource(),"\n")
    if  event.getName() == "INICIA":
        if self.estado == "no_visitado":
            self.estado = "visitado"
            self.explore()
            n = len(self.edo_vecinos)
            for n in self.edo_vecinos:
                if n[1] == "no_visitado" or n[1] == "visitado":
                    print ("Envio visitado a : ", n[0], "\n")
                    newevent = Event("VISITADO", self.clock +1.0 , n[0], self.id)
                    self.transmit(newevent)

    if event.getName() == "VISITADO":
        pos = self.neighbors.index(event.getSource())
        if self.edo_vecinos[pos][1] == "no_visitado" :
            self.edo_vecinos[pos][1] = "visitado"
            print ("Cambie a ",event.getSource(), " en visitado\n")
        if self.edo_vecinos[pos][1] == "hijo" :
            self.edo_vecinos[pos][1] = "visitado"
            self.explore()

    if event.getName() == "DESCUBRE":
        pos = self.neighbors.index(event.getSource())
        if self.estado == "no_visitado":
            self.edo_vecinos[pos][1] = "Padre"
            self.estado = "visitado"
            self.explore()
            n = len(self.edo_vecinos)
            for n in self.edo_vecinos:
                if n[1] == "no_visitado" or n[1] == "visitado":
                    print ("[", self.id ,"]: Envio visitado a : ", n[0], "\n")
                    newevent = Event("VISITADO", self.clock +1.0 , n[0], self.id)
                    self.transmit(newevent)
        else:
            if  self.edo_vecinos[pos][1] == "no_visitado":
                self.edo_vecinos[pos][1] = "visitado"
            if  self.edo_vecinos[pos][1] == "hijo":
                self.explore()





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

seed = Event("INICIA", 0.0, 1, 1)
experiment.init(seed)
experiment.run()
