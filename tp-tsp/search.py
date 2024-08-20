"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo, y los empates se resuelvan de forma aleatoria.
Ya viene implementado.

* HillClimbingReset: algoritmo de ascension de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de busqueda tabu.
No viene implementado, se debe completar.
"""


from __future__ import annotations
from problem import OptProblem
from node import Node
from random import choice
from time import time

class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)


class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Crear el nodo inicial
        actual = Node(problem.init, problem.obj_val(problem.init)) # problem.init crea el estado inicial, obj_val devuelve el valor del estado

        while True:

            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual.state) # Diferencia entre sucesor y el estado actual

            # Buscar las acciones que generan el  mayor incremento de valor obj
            max_acts = [act for act, val in diff.items() if val ==
                        max(diff.values())]

            # Elegir una accion aleatoria
            act = choice(max_acts)

            # Retornar si estamos en un optimo local
            if diff[act] <= 0: # Si todas las diferencias son negativas, es decir, el sucesor es mas grande que todos los potenciales

                self.tour = actual.state
                self.value = actual.value
                end = time()
                self.time = end-start
                return

            # Sino, moverse a un nodo con el estado sucesor
            else:

                actual = Node(problem.result(actual.state, act),
                              actual.value + diff[act])
                self.niters += 1

# Definimos una clase para la lista tabú
class TabuList():
  def __init__(self, size: int) -> None:
    self.list = [] # Lista donde guardamos las acciones prohibidas
    self.size = size

class HillClimbingReset(LocalSearch):    
    """Clase que representa un algoritmo de ascension de colinas con reinicio aleatorio.

        Realiza una serie de busquedas de ascension de colinas desde un estado inicial generado
        aleatoriamente, hasta encontrar su estado objetivo.
        Esto le agrega completitud con cierta probabilidad.
        """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas con reinicio aleatorio.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """

        # Inicio del reloj
        start = time()        

        # Con 20 iteraciones se alarga bastante el tiempo pero casi siempre encuentra lo que parece ser la 
        # solucion optima
        for i in range(0,20):
            
            problem.random_reset()
            actual = Node(problem.init, problem.obj_val(problem.init))

            while True:

                # Determinar las acciones que se pueden aplicar
                # y las diferencias en valor objetivo que resultan
                diff = problem.val_diff(actual.state)

                # Buscar las acciones que generan el  mayor incremento de valor obj
                max_acts = [act for act, val in diff.items() if val ==
                            max(diff.values())]


                # Elegir una accion aleatoria
                act = choice(max_acts)

                # Retornar si estamos en un optimo local
                # Nos va a dar positivo solo si hay una mejora en el valor objetivo del estado sucesor
                if diff[act] <= 0:
                    # Si no hay mejora en el valor objetivo
                    # Y es la primera vuelta seteamos como mejor candidato al estado actual y su valor objetivo
                    if i == 0:
                        self.tour = actual.state
                        self.value = actual.value
                    # Si no es la primera vuelta solo seteamos como mejor candidato al estado actual si su valor
                    # objetivo es mejor que el del anterior mejor candidato
                    elif actual.value > self.value:
                        self.tour = actual.state
                        self.value = actual.value
                    # Rompemos el bucle while para terminar con esta iteracion de ascension de colinas y comenzar una nueva.
                    break
                    
                # En el caso de que haya mejoras en el valor objetivo nos vemos al estado sucesor.
                else:

                    actual = Node(problem.result(actual.state, act),
                                actual.value + diff[act])
                    self.niters += 1
                    
        end = time()  
        self.time = end-start    
        return

  # Agregar una acción a la lista tabú (Decidimos mantener el largo de la lista quitando elementos de esta como criterio de parada)
def add(self, action: tuple) -> None:
    self.list.append(action)
    if len(self.list) > self.size:
      self.list.pop(0)

class Tabu(LocalSearch):
    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Creamos un nodo con el estado inicial y su valor objetivo
        actual = Node(problem.init, problem.obj_val(problem.init))

        
        tabu_size = 20

        limit_niter = 50

        # Crear lista Tabú
        tabu_list = TabuList(size = tabu_size)
        
        # Mejor estado
        global_solution = actual

        while (self.niters < limit_niter):

             # Devuelve las acciones posible a hacerle al estado actual y 
             # la diferencia de valor objetivo entre el estado sucesor y el estado actual
             # (Se busca que sea positiva eso quiere decir que el estado sucesor lo mejora)
            diff = problem.val_diff(actual.state)

            # En este primer paso se filtra las que no estan en la lista tabu y las que tienen
            # mayor valor objetivo que el mejor estado            
            diff_tabu = {act: val for act, val in diff.items() if
                        # Si la accion ni su inversa estan en la lista tabu "o"
                        ( (act not in tabu_list.list and act[::-1] not in tabu_list.list) 
                        ##################################################################################
                        # 1.¿Por que nos quedamos tanto con las acciones que ya estan en la lista tabu como con sus
                        # opuestas?
                        ##################################################################################
                        # El valor objetivo del estado sucesor es mayor al valor objetivo de la mejor 
                        # solucion encontrada hasta ahora (este es un criterio de aspiracion)
                        or problem.obj_val(problem.result(actual.state, act)) > global_solution.value) }     
                        # Con esto no hay riesgo de ciclar porque no lo habiamos encontrado anteriormente                
            
                        # No tienen que estar en la lista tabu o si van a estarlo al menos tienen que tener
                        # el estado sucesor un mejor valor objetivo que la solucion actual

            # En este segundo paso nos quedamos con las acciones que tienen mayor valor objetivo de todas las
            # anteriormente filtradas
            
            max_acts = [act for act, val in diff_tabu.items() 
                        # Elige el máximo y lo mejor es que la diferencia de positiva, eso significa que la mejora
                        if val == max(diff_tabu.values())] 
                        
            # Elegir una accion aleatoria
            act = choice(max_acts)

            # Al no estar el chequeo de abajo le estamos permitiendo pasar por estados que empeoran el valor objetivo
            # siempre vamos a intentar ir al que tiene el mayor valor objetivo pero si el mayor lo empeora nos vamos
            # a mover

            # diff.tabu[act] <= 0:
            #   --no nos movemos al estado--

            # Se agrega a la lista tabu para no repetirla
            tabu_list.add(act)
            
            # Generamos el nuevo estado con su valor objetivo
            actual = Node(problem.result(actual.state, act), actual.value + diff[act])
            

            # Si el valor del actual es mayor al del mejor estado entonces el mejor ahora es el actual
            if actual.value > global_solution.value:
              global_solution = actual
            
            # Sumamos una iteracion
            self.niters += 1

            # Y en la siguiente iteracion vamos a operar sobre el nodo que acabamos de actualizar, sea
            # que mejoro nuestra situacion o no, de ese modo tenemos posibilidades de buscar otras opciones

        # Luego de que se haya alcanzado el límite de iteraciones, devolver la mejor solución
        
        self.tour = global_solution.state
        self.value = global_solution.value
        end = time()
        self.time = end - start
        return


