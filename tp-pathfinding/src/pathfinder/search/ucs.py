from ..models.grid import Grid
from ..models.frontier import StackFrontier, PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node

############################################################################################################
# Nos falto la verificacion de la frontera, si ya estuvo pero ahora tiene menor costo puede volver a ingresar
############################################################################################################

class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Uniform Cost Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)

        # Initialize the explored dictionary to be empty and 
        explored = {} 

        # Diccionario que guarda los estado ya agregados a la frontera
        seen = {}
        
        # Add the node to the explored dictionary
        explored[node.state] = True
        seen[node.state] = True

        frontier = PriorityQueueFrontier()
        frontier.add(node)

        # ¿Por que el counter?
        counter = 0
        max_counter = 20000

        while counter < max_counter:
          if frontier.is_empty():
            return NoSolution(explored)
            break
          # Supongo que se comporta como un DFS por como van quedando acomodado en la frontera cuando los agregamos
          # A la hora de hacer el pop se ve que vamos sacando de los que tienen menor costo de camino los ultimos
          # que ingresaron.
          node = frontier.pop()
          explored[node.state] = True
          if node.state == grid.end:
            return Solution(node, explored)
            break

          neighbours = grid.get_neighbours(node.state)
          for direction in neighbours.keys():
            new_state = neighbours[direction]
            if not seen.get(new_state, False):
              new_node = Node('', new_state, node.cost + grid.get_cost(new_state))
              new_node.parent = node
              new_node.action = direction
              frontier.add(new_node, priority=grid.get_cost(new_state))
              seen[new_node.state] = True
              
          counter = counter + 1
        return NoSolution(explored)
