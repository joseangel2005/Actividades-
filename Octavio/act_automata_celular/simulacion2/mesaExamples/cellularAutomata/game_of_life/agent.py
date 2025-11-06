from mesa.discrete_space import FixedAgent

#Usaremos la regla 30 Caótica 

# usaremos esta clase para representar una sola celda VIVA o MUERTA en la simulacion
class Cell(FixedAgent):

    DEAD = 0 #muerta
    ALIVE = 1 #viva

    #aqui  representa una sola celda VIVA o MUERTA en la simulacion
    @property
    def x(self):
        return self.cell.coordinate[0]

    @property
    def y(self):
        return self.cell.coordinate[1]

    @property
    def is_alive(self):
        return self.state == self.ALIVE
    
    #con el constructor inicializamos la celda con su estado inicial
    def __init__(self, model, cell, init_state=DEAD): #defininmos el constructor de la clase Cell
        super().__init__(model) #llamamos al constructor de la clase padre FixedAgent
        self.cell = cell# guardamos la celda
        self.pos = cell.coordinate #guardamos la posicion de la celda
        self.state = init_state # guardamos el estado inicial de la celda
        self._next_state = None # iniciamos la variable para el siguiente estado

    def get_upper_neighbors(self):#despues en definimos la funcion para obtener los vecinos superiores
        x, y = self.x, self.y
        width, height = self.model.grid.dimensions
        
        
        left_up = ((x - 1) % width, (y + 1) % height) # coordenadas del vecino izquierdo
        center_up = (x, (y + 1) % height) # coordenadas del vecino del centro
        right_up = ((x + 1) % width, (y + 1) % height) # coordenadas del vecino derecha                 
        
    
        neighbors = []# en neighbors guardaremos los estados de los vecinos
        for coord in [left_up, center_up, right_up]: # para cada coordenada de los vecinos
            cell = self.model.grid._cells[coord] # obtenemos la celda en esa coordenada

            # si agents existe en la celda, obtenemos el estado del primer agente
            if cell.agents:
                neighbors.append(list(cell.agents)[0].state) # agregamos el estado del vecino a la lista
            else:
                neighbors.append(self.DEAD) # si no hay agente, consideramos que el vecino está muerto
        
        return tuple(neighbors)

    #empezamos a definir la funcion para determinar el siguiente estado de la celda
    def determine_state(self): # primero obtenemos los estados de los vecinos superiores
        left, center, right = self.get_upper_neighbors() # para despues aplicar la regla 30
        
        # definimos la regla 30 en un diccionario
        rule_30 = {
            (1, 1, 1): 0,
            (1, 1, 0): 1,
            (1, 0, 1): 0,
            (1, 0, 0): 1,
            (0, 1, 1): 1,
            (0, 1, 0): 0,
            (0, 0, 1): 1,
            (0, 0, 0): 0,
        }
        
        #Aqui aplicamos la regla 30 para determinar el siguiente estado de la celda
        pattern = (left, center, right) # patron es igua a a los estados de los vecinos
        self._next_state = rule_30.get(pattern, self.DEAD) #self._next_state = rule_30.get(pattern, self.DEAD) hara que si el patron no esta en la regla 30, la celda se considere muerta

    def assume_state(self):
        self.state = self._next_state

"""
La logica radica en que el codigo se basa en la regla 30 en onde el automata 
genera patrones de manera caotica, dentro de la clase el constructor inicia la
celda con su posición "self.pos" y su estado inicial vivo o muerto, con la funcion 
get_upper_neighbors() logramos obtner los estados de losvecinos de arriba izquierda,
central y derecha, buscando las coordenadas en la matricula y guardando los estados 
si existiera el caso de que en esa pocision no haya agente, se considera muerto
luegp en determine_state() la celda toma los estados con el nuevo valor calculado 
en donde se obtiene del diccionario rule_30 que contiene las reglas para determinar el
siguiente estado de la celda basado en los estados de sus vecinos superiores y para finalizar 
assume_state() actualiza el estado de la celda al siguiente estado calculado
"""