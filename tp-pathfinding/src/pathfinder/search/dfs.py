from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Depth First Search

        Args:
            grid (Grid): Grid of points
            
        Returns:
            Solution: Solution found
        """
         # Inicializamos la raiz con el estado inicial, y el costo = 0
        node = Node("", grid.start, 0)
        
        # Inicializamos un diccionario con los estados expandidos
        explored = {} 

        # Inicializamos la frontera y agregamos el estado inicial para luego expandirlo
        frontier = StackFrontier()
        frontier.add(node)
        
        while True:

            #  Si la frontera esta vacia no hay solucion
            if frontier.is_empty():
                return NoSolution(explored)

            # Removemos el ultimo elemento en ser agregado a la frontera
            node = frontier.remove()                       
            
            # Consultamos el test objetivo
            if node.state == grid.end:
                return Solution(node, explored)
            

            
            # Agregamos el estado al diccionario con los estados alcanzados
            explored[node.state] = True

            # Obtenemos todos los estados hijos del estado que sacamos de la frontera
            neighbours = grid.get_neighbours(node.state)

            # Vamos a ir agregando uno a uno los hijos del estado en el que estamos a la frontera en  
            # caso de que aun no hayan sido explorados
            for accion, estado in neighbours.items():
                nuevo_estado = estado
                nuevo_nodo = Node("", nuevo_estado, node.cost + grid.get_cost(nuevo_estado), node, accion)                
                if nuevo_nodo.state not in explored.keys():
                    frontier.add(nuevo_nodo)
    
