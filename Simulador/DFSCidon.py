# Este archivo implementa la simulacion del algoritmo de
# recorrido en profundidad de Cidon
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
    self.estado = "no_visitado"
    self.edo_vecinos = []
    m = len(self.neighbors)
    for m in self.neighbors: #Llenamos la lista con sus vecimos cado uno con su variable de estado
        self.edo_vecinos.append([m,"no_visitado"])

  def explore(self):
    global mensajes_enviados
    n = len(self.edo_vecinos)
    cont = 0
    for n in self.edo_vecinos:
        if n[1] == "no_visitado": #Buscamos al primer vecino que no hemos visitado
            cont = cont + 1
            print ("\t[", self.id,"]: Envio descubre a : ", n[0],"\n")
            newevent = Event("DESCUBRE", self.clock +1.0 , n[0], self.id)
            mensajes_enviados += 1
            self.transmit(newevent)
            n[1] = "hijo"
            break
    if cont == 0: #Si ya no hay vecinos que visitar pero alguno de ellos es nuestro padre le enviamos un descubre
        for n in self.edo_vecinos:
            if n[1] == "Padre":
                newevent = Event("DESCUBRE", self.clock +1.0 , n[0], self.id)
                mensajes_enviados += 1
                self.transmit(newevent)
                print ("\t[", self.id,"]: Envio descubre a mi padre:", n[0], "\n")



  def receive(self, event):
    # Aqui se definen las acciones concretas que deben ejecutarse cuando se
    # recibe un evento
    global mensajes_enviados
    print("T = ", self.clock, " Nodo ", self.id, " Recibo :", event.getName(), "desde", event.getSource(),"\n")
    if  event.getName() == "INICIA":
        if self.estado == "no_visitado":
            self.estado = "visitado"
            self.explore()
            n = len(self.edo_vecinos)
            for n in self.edo_vecinos: #Le enviamos un mensaje a todos nuestro vecinos que esten o no visitados
                if n[1] == "no_visitado" or n[1] == "visitado":
                    print ("\t[", self.id,"]: Envio visitado a : ", n[0], "\n")
                    newevent = Event("VISITADO", self.clock +1.0 , n[0], self.id)
                    mensajes_enviados += 1
                    self.transmit(newevent)

    if event.getName() == "VISITADO":
        pos = self.neighbors.index(event.getSource())
        if self.edo_vecinos[pos][1] == "no_visitado" :
            self.edo_vecinos[pos][1] = "visitado"
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
                if n[1] == "no_visitado" or n[1] == "visitado": #Le enviamos un mensaje a todos nuestro vecinos que esten o no visitados
                    print ("\t[", self.id ,"]: Envio visitado a : ", n[0], "\n")
                    newevent = Event("VISITADO", self.clock +1.0 , n[0], self.id)
                    mensajes_enviados += 1
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
    print ("Por favor proporcione el nombre de la grafica de comunicaciones")
    raise SystemExit(1)

experiment = Simulation(sys.argv[1], 100)

# asocia un pareja proceso/modelo con cada nodo de la grafica
for i in range(1,len(experiment.graph)+1):
    m = AlgorithmDFS()
    experiment.setModel(m, i)

# inserta un evento semilla en la agenda y arranca
inicio = default_timer()
seed = Event("INICIA", 0.0, 1, 1)
mensajes_enviados += 1
experiment.init(seed)
experiment.run()
fin = default_timer()
print ("\tTiempo del programa = " ,fin - inicio)
print ("\tMensajes enviados en total = ", mensajes_enviados,"\n")
