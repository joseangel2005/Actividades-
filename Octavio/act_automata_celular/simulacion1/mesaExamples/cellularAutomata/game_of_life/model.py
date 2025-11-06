from mesa import Model
from mesa.discrete_space import OrthogonalMooreGrid
from .agent import Cell

# aqui definimos el modelo de 50*50 celdas
class ConwaysGameOfLife(Model):
    def __init__(self, width=50, height=50, initial_fraction_alive=0.2, seed=None): #aqui definimos los parametros del modelo
        super().__init__(seed=seed)
        
        self.width = width
        self.height = height
        self.current_row = 0
        
        self.grid = OrthogonalMooreGrid((width, height), capacity=1, torus=False)

        # crearemo las celulas con el siclo for para cada celda en la 
        for y in range(height): #para  "y" en el rango de la altura sera 50
            for x in range(width): # para "x" en el rango del ancho sera 50
                cell = self.grid._cells[(x, y)]
                # Solo la primera fila (y=0) se inicializa aleatoriamente
                if y == 0: # si y es igual a 0
                    init_state = Cell.ALIVE if self.random.random() < initial_fraction_alive else Cell.DEAD# se inicializa el estado de la celda como viva o muerta segun la fraccion inicial
                else:# en caso contrario
                    init_state = Cell.DEAD # las demas filas se inicializan como muertas
                
                Cell(self, cell, init_state=init_state, row=y) # creamos la celda con su estado inicial y su fila

        self.running = True

    # en este def lo que haremos es avanzar fila por fila
    def step(self):
        # Avanzar a la siguiente fila
        if self.current_row < self.height - 1:# si la fila actual es menor que la altura menos 1
            self.current_row += 1 #luego avanzamos a la siguiente fila
            
            # Obtener agentes de la fila actual
            agents_in_row = [agent for agent in self.agents if agent.row == self.current_row] # agents_in_row sera igual a una lista de agentes en la fila actual
            
            # Calcular nuevos estados
            for agent in agents_in_row:
                agent.determine_state()
            
            # Aplicar nuevos estados
            for agent in agents_in_row:
                agent.assume_state()