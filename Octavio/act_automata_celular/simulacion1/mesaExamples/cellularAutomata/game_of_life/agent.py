from mesa.discrete_space import FixedAgent
# usaremos la regla 90 para el Triángulo de Sierpinski que de hecho se parece un poco a la trifuerza de Zelda


class Cell(FixedAgent):
    # Definición de estados
    DEAD = 0 # Celda muerta
    ALIVE = 1 # Celda viva
    
    # definimos la regla 90 en un diccionario
    RULE_90 = {
        (1, 1, 1): 0,
        (1, 1, 0): 1,
        (1, 0, 1): 0,
        (1, 0, 0): 1,
        (0, 1, 1): 1,
        (0, 1, 0): 0,
        (0, 0, 1): 1,
        (0, 0, 0): 0,
    }
    #aqui  representa una sola celda VIVA o MUERTA en la simulacion 
    def __init__(self, model, cell, init_state=DEAD, row=0):
        super().__init__(model)
        self.cell = cell
        self.pos = cell.coordinate
        self.state = init_state
        self._next_state = None
        self.row = row

    @property
    def x(self):
        return self.cell.coordinate[0]

    @property
    def y(self):
        return self.cell.coordinate[1]

    @property
    def is_alive(self):
        return self.state == self.ALIVE

    """
    Para esta parte hasta la línea donde dice "Hasta aqui",
    el código lo que hace es

    La función get_upper_neighbors busca los vecinos superiores de una celda en una cuadrícula, 
    obteniendo sus las coordenadas en x, y y checando si está en la primera fila por lo que si es así, 
    devuelve nos dara tres None porque no deberia existir vecinos arriba. en dado caso intenta obtener las celdas de hasta arriba a la izquierda, 
    central y derecha usando las coordenadas, y si esas celdas existen y contienen agentes, extrae el primero de cada una

    """

    # Obtener vecinos 
    def get_upper_neighbors(self):
        x, y = self.x, self.y # Coordenadas de la celda actual
        
        # Para la primera fila
        if y == 0:
            return None, None, None # No hay vecinos superiores
        
        # Inicializar vecinos como None
        upper_left = None
        upper_center = None
        upper_right = None
        
        # Para la obtencion de los vecinos superiores
        if x > 0:
            cell_left = self.model.grid._cells.get((x - 1, y - 1)) # Celda izquierda
            if cell_left and cell_left.agents: # Si ya existe o hay un agente en esa celda
                upper_left = list(cell_left.agents)[0]# POara tener un agente de esa celda
        
        # Celda central 
        cell_center = self.model.grid._cells.get((x, y - 1)) # Celda central 
        if cell_center and cell_center.agents: # Lo mismo que en la linea  57 checamos si existe o hay un agente
            upper_center = list(cell_center.agents)[0]
        
        # Celda derecha 
        if x < self.model.width - 1: # Si no es la ultima columna 
            cell_right = self.model.grid._cells.get((x + 1, y - 1)) # Celda derecha
            if cell_right and cell_right.agents: # Lo mismo que en la linea  57 checamos si existe o hay un agente
                upper_right = list(cell_right.agents)[0]
        
        return upper_left, upper_center, upper_right # Devolver los vecinos superiores
    
    # Hasta aqui 

    # aqui empieza la logica 
    def determine_state(self):# hacemos un def  para determinar el estado
        left, center, right = self.get_upper_neighbors() # obtner los vecions de arriba
        
        # con este if si no hay vecinos arriba para revisar si hay que cambiar el estado o no
        if center is None:
            self._next_state = self.state
            return
        
        # Aqui lo que haremos es revisar los estados de los vecinos
        left_state = left.state if left else self.DEAD # Si no hay vecino en la izquirda, considerar como muerto
        center_state = center.state # Estado del vecino central
        right_state = right.state if right else self.DEAD # Si no hay vecino en la derecha, considerar como muerto
        
        config = (left_state, center_state, right_state) # la configuracion actual de los vecinos
        self._next_state = self.RULE_90.get(config, self.DEAD) 

    def assume_state(self):
        if self._next_state is not None:
            self.state = self._next_state

    """
    Dentro del programa  implementa la regla 90 en done el automata generapatrones fractales similiares a los triangulos
    de Sierpinski, dentro de la clase el constructor inicia la celda con su posición "self.pos" y su estado inicial vivo o muerto,
    con la funcion get_upper_neighbors() logramos obtner los estados de los vecinos de arriba izquierda, central y derecha,
    buscando las coordenadas de las matriculas y guardadno los estados de los vecinos, despues en determine_state() la celda
    agarra esos estados para calcular el siguiente estado usando el diccionario de rule 90, el cual tiene las reglaas
    para tener  en cuenta el nuevo estado  basado en la configuracion de los vecionos para finalizar  ssume_state() actualiza 
    el estado de la celda al siguiente estado calculado.
    """