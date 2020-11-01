# Este archivo implementa la simulacion del algoritmo de
# Difución epidémica
# con una cantidad de 4 rondas
# Alumno: Sangines Martínez Luis Fernando

import sys
from timeit import default_timer #import para calcular el tiempo de ejecución del programa
from event import Event
from model import Model
from process import Process
from simulator import Simulator
from simulation import Simulation

import random # números random

mensajes_enviados = 0 #Variable glogal que cuenta los mensajes enviados en total

class AlgorithmDFS(Model):
      # Esta clase desciende de la clase Model e implementa los metodos
      # "init()" y "receive()", que en la clase madre se definen como abstractos


    def init(self):
        # Aqui se definen e inicializan los atributos particulares del algoritmo
        self.vecinos = self.neighbors
        self.contenido = []
        i = 0
        while (i < 10):
            self.contenido.append(random.randint(0,10))
            i += 1

    def busca_contenido(self,busqueda,resultado):
        m = len(self.contenido)
        for m in self.contenido:
            if m == busqueda:
                if self.id in resultado:
                    break
                else:
                    resultado.append(self.id)
                    print ("[", self.id,"]: Yo tengo el valor buscado: ", busqueda,"\n")
                    break
        return resultado

    def hijo_aleatorio(self, camino): #Se busca un hijo aleatorio que no halla sido visitado
        numero_hijos = len(self.neighbors)
        if numero_hijos != 1:
            hijo_seleccionado = -1
            while hijo_seleccionado == -1:
                hijo_alea = random.randint(0,len(self.neighbors)-1)
                if self.neighbors[hijo_alea] in camino:
                    hijo_seleccionado = -1
                else:
                    hijo_seleccionado = self.neighbors[hijo_alea]
            #print("Hijo ", hijo_seleccionado)
            #print("Valor ",hijo_alea)
        else:
            hijo_seleccionado = "null" #Se regresa null si el hijo ya no tiene hijos
        return hijo_seleccionado


    def receive(self, event):
        # Aqui se definen las acciones concretas que deben ejecutarse cuando se
        # recibe un evento
        global mensajes_enviados
        print("T = ", self.clock, " Nodo ", self.id, " Recibo :", event.getName(), "desde", event.getSource(),"\n")
        camino = event.getCamino()
        if  event.getName() == "BAJADA":
            if event.getDistance() < pow( 2, event.getRound()): #Verificamos que aun no se halla sobrepasado la distancia dada
                i = pow( 2, event.getRound()) - event.getDistance()
                tiempo = self.clock
                distancia = event.getDistance()
                camino.append(self.id)
                for j in range(i):
                    hijo_selc = self.hijo_aleatorio(event.getCamino())
                    if hijo_selc != "null": #Se verifica que el nodo tenga hijos
                        aux = self.busca_contenido(event.getSearch(), event.getResult()) # Se busca si el nodo contiene el valor buscado
                        tiempo = tiempo + 1
                        distancia = distancia + 1
                        print("\t\t\t Tiempo: ", tiempo , " Nodo : ",hijo_selc , "\n")
                        newevent = Event("BAJADA", tiempo , hijo_selc, self.id, distancia, event.getRound(), event.getSearch(), aux,camino)
                        mensajes_enviados += 1
                        self.transmit(newevent)
                    else: #Si el nodo no tiene hijos enviamos un mensaje de SUBIDA de acuerdo a nuestra lista del camino recorrido
                        print("[",self.id,"]: NO tengo vecinos a quien visitar el camino de regreso es: " , camino ,"\n" )
                        regreso = camino[-1]
                        camino.remove(regreso)
                        newevent = Event("SUBIDA", self.clock +1.0 , regreso, self.id, event.getDistance(), event.getRound(),event.getSearch(), event.getResult(),camino)
                        mensajes_enviados += 1
                        self.transmit(newevent)
            else:
                if event.getDistance() == pow( 2, event.getRound()):
                    print("[",self.id,"]: Se recorrio la longitud deseada, el camino de regreso es: " , camino, "\n")
                    regreso = camino[-1]
                    camino.remove(regreso)
                    newevent = Event("SUBIDA", self.clock +1.0 , regreso, self.id, event.getDistance(), event.getRound(),event.getSearch(), event.getResult(), camino)
                    mensajes_enviados += 1
                    self.transmit(newevent)

        if event.getName() == "SUBIDA":
            if len(camino) != 0:
                regreso = camino[-1]
                camino.remove(regreso)
                newevent = Event("SUBIDA", self.clock +1.0 , regreso, self.id, event.getDistance(), event.getRound(), event.getSearch(), event.getResult(), camino)
                mensajes_enviados += 1
                self.transmit(newevent)
            else:
                if event.getTarget() == 1:
                    print ("[", self.id,"]: Los nodos que tinene a: ", event.getSearch(), "dentro de su contenido son:  ",event.getResult(),"\n")


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
camino = []
resultado2 = []
camino2 = []
inicio = default_timer()
#Mandamos 2 caminos aleatorios
# Messaje , reloj, target, source, distancia, ronda , busqueda, resultado, camino recorrido
seed = Event("BAJADA", 0.0, 1, 1, 0, 2, 7, resultado,camino) #Solo recorre una distancia de 4 y no recorre todo el grafo
experiment.init(seed)
#seed = Event("BAJADA", 0.0, 1, 1, 0, 2, 7, resultado2,camino2, 2)
#experiment.init(seed)
experiment.run()
fin = default_timer()
print ("\tTiempo del programa = " ,fin - inicio)
print ("\tMensajes enviados en total = ", mensajes_enviados,"\n")
