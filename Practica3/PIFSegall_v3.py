# Este archivo implementa la simulacion del algoritmo de
# recorrido en profundidad de Segall buscando que nodo dentro de su busca_contenido
# contiene un número buscado por el nodo raiz
# Alumno: Sangines Martínez Luis Fernando

import sys
from event import Event
from model import Model
from process import Process
from simulator import Simulator
from simulation import Simulation

import random # números random

class AlgorithmDFS(Model):
      # Esta clase desciende de la clase Model e implementa los metodos
      # "init()" y "receive()", que en la clase madre se definen como abstractos


    def init(self):
        # Aqui se definen e inicializan los atributos particulares del algoritmo
        self.father = self.id
        self.visitado = False
        self.vecinos = self.neighbors
        self.contenido = []
        self.ok = []
        n = len(self.neighbors)
        for n in self.neighbors:
            self.ok.append([n,False])
        i = 0
        while (i < 10):
            self.contenido.append(random.randint(0,10))
            i += 1

    def busca_contenido(self, resultado,busqueda):
        m = len(self.contenido)
        for m in self.contenido:
            if m == busqueda:
                resultado.append(self.id)
                print ("[", self.id,"]: Yo tengo el valor buscado: ", busqueda,"\n")
                break
        return resultado

    def receive(self, event):
        # Aqui se definen las acciones concretas que deben ejecutarse cuando se
        # recibe un evento
        global mensajes_enviados
        print("T = ", self.clock, " Nodo ", self.id, " Recibo :", event.getName(), "desde", event.getSource(),"\n")
        if  event.getName() == "BAJADA":
                cont = 0
                aux = 0
                if self.id != event.getSource():
                    pos = self.neighbors.index(event.getSource())
                    self.ok[pos][1] = True
                    #print ("[", self.id,"]: Cambie la bandera de :" ,event.getSource()," a" , self.ok[pos][1] ,"\n")
                n = len(self.neighbors)
                if self.visitado == False:
                    self.father = event.getSource()
                    self.visitado = True
                    aux = self.busca_contenido(event.getResult(),event.getSearch()) # Se busca si el nodo contiene el valor buscado
                    if event.getDistance() < pow( 2, event.getRound()): #Verificamos que aun no se halla sobrepasado la distancia dada
                        for n in self.ok:
                            if n[0] != event.getSource():
                                #print ("[", self.id,"]: Envio M a :" , n[0],"\n")
                                newevent = Event("BAJADA", self.clock +1.0 , n[0], self.id, event.getDistance() + 1, event.getRound(), event.getSearch(), aux)
                                self.transmit(newevent)
                    else:
                        if event.getDistance() == pow( 2, event.getRound()):
                            if self.father != self.id:
                                newevent = Event("SUBIDA", self.clock +1.0 , self.father, self.id, event.getDistance(), event.getRound(),event.getSearch(), event.getResult())
                                self.transmit(newevent)
                for n in self.ok:
                    if n[1] == True:
                        cont = cont + 1
                if cont == len(self.neighbors):
                    if self.father != self.id:
                        newevent = Event("SUBIDA", self.clock +1.0 , self.father, self.id, event.getDistance(), event.getRound(), event.getSearch(), event.getResult())
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
                    newevent = Event("SUBIDA", self.clock +1.0 , self.father, self.id, event.getDistance(), event.getRound(), event.getSearch(), event.getResult())
                    self.transmit(newevent)
                else:
                    print ("[", self.id,"]: Los nodos que tinene a: ", event.getSearch(), "dentro de su contenido son:  ",event.getResult())


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
resultado = []
# Messaje , reloj, target, source, distancia, ronda , busqueda, resultado
#seed = Event("BAJADA", 0.0, 1, 1, 1, 1, 10, resultado) #Solo recorre una distancia de 2 y no recorre todo el grafo
seed = Event("BAJADA", 0.0, 1, 1, 1, 2, 10, resultado) #Solo recorre una distancia de 4 y no recorre todo el grafo
#seed = Event("BAJADA", 0.0, 1, 1, 1, 3, 10, resultado) #Solo recorre una distancia de 6 y recorre todo el grafo
experiment.init(seed)
experiment.run()
