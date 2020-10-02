# Este archivo implementa la simulacion del algoritmo de
# recorrido en profundidad de Awerbuch
# Alumno: Sangines Martínez Luis Fernando

import sys
from timeit import default_timer #import para calcular el tiempo de ejecución del programa
from event import Event
from model import Model
from process import Process
from simulator import Simulator
from simulation import Simulation

mensajes_enviados = 0 #Variable glogal que cuenta lo smensajes enviados en total


class AlgorithmDFS(Model):
  # Esta clase desciende de la clase Model e implementa los metodos
  # "init()" y "receive()", que en la clase madre se definen como abstractos


  def init(self):
    # Aqui se definen e inicializan los atributos particulares del algoritmo
    self.father = self.id
    self.unvisited = self.neighbors
    self.banderas = [] #Lista de banderas para los vecinos
    self.vecinos = []
    m = len(self.neighbors)
    for m in self.neighbors:#Creamos otra lista para los vecinos que tiene cada nodo
        self.vecinos.append(m)

  def receive(self, event):
    # Aqui se definen las acciones concretas que deben ejecutarse cuando se
    # recibe un evento
    global mensajes_enviados
    print("T = ", self.clock, " Nodo ", self.id, " Recibo :", event.getName(), "desde", event.getSource(),"\n")
    if  event.getName() == "DESCUBRE":
            self.father = event.getSource()
            print ("\t[", self.id,"]: Mi padres es: ", self.father, "\n")
            if len(self.unvisited) > 0:#Si aun hay vecinos sin visitar, se enviara un mensaje de VISITADO
                n = len(self.vecinos)
                for n in self.vecinos:
                    if( n != event.getSource()):
                        print ("\t[", self.id,"]: Envio VISITADO a: ", n ,"\n")
                        newevent = Event("VISITADO", self.clock + 1.0, n, self.id)
                        mensajes_enviados += 1
                        self.transmit(newevent)
                        self.banderas.append([n,True])#Agregamos a los vecimos con sus respectivas banderas
            else:
                if self.father == event.getSource():#Si el mensaje que recibi en de mi padre le envio un REGRESA
                    print ("\t[", self.id,"]: No tengo vecinos que visitar \n" )
                    newevent = Event("REGRESA", self.clock +1.0 , self.father, self.id)
                    mensajes_enviados += 1
                    self.transmit(newevent)

    if  event.getName() == "VISITADO":
        self.unvisited.remove(event.getSource())#Eliminamos a los vecinos que ya visitamos
        newevent = Event("ACK", self.clock +1.0 , event.getSource(), self.id)
        mensajes_enviados += 1
        self.transmit(newevent)

    if  event.getName() == "ACK":
        pos = self.banderas.index([event.getSource(),True])
        terminados = 0
        self.banderas[pos][1]= False#Cambiamos la bandera de nuestros vecinos cundo nos hallan respondido
        n = len(self.banderas)
        for n in self.banderas:
            if n[1] == False:
                terminados = terminados + 1
        if terminados == len(self.banderas):#Una vez que todos los vecimos contesten, el programa continua
            print ("\t[", self.id,"]: Todas las banderas estan en FALSO \n")
            newevent = Event("REGRESA", self.clock +1.0 , self.id, self.id)
            mensajes_enviados += 1
            self.transmit(newevent)

    if  event.getName() == "REGRESA":
        if len(self.unvisited) > 0:#Mientras halla vecinos son visitar, se les envia DESCUBRE
            to_visit = self.unvisited[0]
            newevent = Event("DESCUBRE", self.clock + 1.0, to_visit, self.id)
            print ("\t[", self.id,"]: Envio descubre a: ", to_visit," \n")
            mensajes_enviados += 1
            self.transmit(newevent)
            self.unvisited = self.unvisited[1:len(self.unvisited)]
        else:
            if self.father != self.id: #Enviamos REGRESA hasta encontar a la RAIZ del arbol
                newevent = Event("REGRESA", self.clock + 1.0, self.father, self.id)
                mensajes_enviados += 1
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
inicio = default_timer()
seed = Event("DESCUBRE", 0.0, 1, 1)
mensajes_enviados += 1
experiment.init(seed)
experiment.run()
fin = default_timer()
print ("\tTiempo del programa = " ,fin - inicio)
print ("\tMensajes enviados en total = ", mensajes_enviados,"\n")
