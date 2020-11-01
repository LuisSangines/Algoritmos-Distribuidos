# Este archivo contiene la implementacion de la clase Event (11.11.10)
""" Un objeto de la clase Event encapsula la informacion que se intercambia
entre las entidades activas de un sistema distribuido """

# ----------------------------------------------------------------------------------------
class Event:                   # Descendiente de la clase "object" (default)
    """ Atributos: "name", "time", "target" y "source",
    contiene tambien un constructor y los metodos que devuelven cada
    uno de los atributos individuales """

    def __init__(self, name, time, target, source, distancia = 0, ronda = 0 , busqueda = 0 , resultado = 0, camino = 0,caminata = 0):
        """ Construye una instancia con los atributos inicializados """
        self.name   = name
        self.time   = time
        self.target = target
        self.source = source
        self.distancia = distancia
        self.ronda = ronda
        self.busqueda = busqueda
        self.resultado = resultado
        self.camino = camino
        self.caminata = caminata


    def getName(self):
        """ Devuelve el nombre del evento """
        return (self.name)

    def getTime(self):
        """ Devuelve el tiempo en el que debe ocurrir el evento """
        return (self.time)

    def getTarget(self):
        """ Devuelve la identidad del proceso al que va dirigido """
        return (self.target)

    def getSource(self):
        """ Devuelve la identidad del proceso que origina el evento """
        return (self.source)

    def getDistance(self):
        """ Devuelve la distancia recorrida desde el evento origen """
        return (self.distancia)

    def getRound(self):
        """ Devuelve la ronda """
        return (self.ronda)

    def getSearch(self):
        """ Devuelve la el valor que estamos buscando """
        return (self.busqueda)

    def getResult(self):
        """ Devuelve la lista con los nodos que contienen la variable a buscar """
        return (self.resultado)

    def getCamino(self):
        """ Devuelve la lista con los nodos que ya fueron visitados """
        return (self.camino)

    def getCaminata(self):
        """ Devuelve el número de caminatas """
        return (self.caminata)
