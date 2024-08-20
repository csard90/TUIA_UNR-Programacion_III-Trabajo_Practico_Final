from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Breadth First Search

        Args:
            grid (Grid): Grid of points
            
        Returns:
            Solution: Solution found
        """
        # Inicializamos la raiz con el estado inicial, y el costo = 0
        node = Node("", grid.start, 0)
        
        # Inicializamos un diccionario con los estados alcanzados
        explored = {} 
        
        # Agregamos la raiz al diccionario con los estados alcanzados
        explored[node.state] = True
        
        if node.state == grid.end:
            return Solution(node, explored)

        # Inicializamos la frontera y agregamos el estado inicial para luego expandirlo
        frontier = QueueFrontier()
        frontier.add(node)
        
        while True:

            #  Si la frontera esta vacia no hay solucion
            if frontier.is_empty():
                return NoSolution(explored)

            # Removemos el primero elemento en ser agregado a la frontera
            node = frontier.remove()           

            # Obtenemos todos los estados hijos del estado que sacamos de la frontera
            neighbours = grid.get_neighbours(node.state)

            # Vamos a ir evaluando uno a uno los hijos del estado en el que estamos para ver
            # si son el estado objetivo y sino agregarlos a la frontera si es que aun no los alcanzamos
            for accion, estado in neighbours.items():
                nuevo_estado = estado
                nuevo_nodo = Node("", nuevo_estado, node.cost + grid.get_cost(nuevo_estado), node, accion)
                # Chequeamos aca cada uno de los hijos que generamos para evitar expandir nodos de mas
                if nuevo_nodo.state == grid.end: # Test objetivo
                    return Solution(nuevo_nodo, explored)
                if nuevo_nodo.state not in explored.keys():
                    explored[nuevo_nodo.state] = True
                    frontier.add(nuevo_nodo)
