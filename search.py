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
from problem import TSP
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
            if diff[act] <= 0:

                self.tour = actual.state
                self.value = actual.value
                end = time()
                self.time = end-start
                return

            # Sino, moverse a un nodo con el estado sucesor
            else:
                
                actual = Node(problem.result(actual.state, act), actual.value + diff[act])
                self.niters += 1



class HillClimbingReset(LocalSearch):
    """Algoritmo de ascension de colinas con reinicio aleatorio."""


    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.


        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()
    

        # Crear el nodo inicial con permutacion inicial aleatoria
        actual = Node(problem.init, problem.obj_val(problem.init))
        mejor = actual
        iteraciones=33

        while True and iteraciones != 0:
            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual.state) 


            # Buscar las acciones que generan el mayor incremento de valor objetivo
            max_acts = [act for act, val in diff.items() if val == max(diff.values())]


            # Elegir una accion aleatoria
            act = choice(max_acts)


            # Retornar si estamos en un optimo local
            if diff[act] <= 0 :
                self.tour = actual.state
                self.value = actual.value
                end = time()
                self.time = end - start
                if actual.value < mejor.value:
                    mejor = actual                
                #actual =Node(problem.result(actual.state, act), actual.value + diff[act])  # Reiniciar con permutacion inicial aleatoria
                problem.random_reset()
                actual = Node(problem.init, problem.obj_val(problem.init))
                iteraciones-=1
                continue


            # Sino, moverse a un nodo con el estado sucesor
            
            actual = Node(problem.result(actual.state, act), actual.value + diff[act])
            self.niters += 1





# class Tabu(LocalSearch):
#     """Algoritmo de busqueda tabu."""
#     def solve(self, problem: OptProblem):
#         """Resuelve un problema de optimizacion con ascension de colinas.


#         Argumentos:
#         ==========
#         problem: OptProblem
#             un problema de optimizacion
#         """
#         # Inicio del reloj
#         start = time()
    

#         # Crear el nodo inicial con permutacion inicial aleatoria
#         actual = Node(problem.init, problem.obj_val(problem.init))
#         mejor = actual
#         tabu=[]

#         while True :#no se cumpla
#             # Determinar las acciones que se pueden aplicar
#             # y las diferencias en valor objetivo que resultan
#             diff = problem.val_diff(actual.state) 


#             # Buscar las acciones que generan el mayor incremento de valor objetivo
#             max_acts = [act for act, val in diff.items() if val == max(diff.values())]


#             # Elegir una accion aleatoria
#             act = choice(max_acts)


#             # Retornar si estamos en un optimo local
#             if diff[act] <= 0 :
#                 self.tour = actual.state
#                 self.value = actual.value
#                 end = time()
#                 self.time = end - start
#                 if actual.value < mejor.value:
#                     mejor = actual
#                     tabu.append(mejor)               
#                 #actual =Node(problem.result(actual.state, act), actual.value + diff[act])  # Reiniciar con permutacion inicial aleatoria
        

#             # Sino, moverse a un nodo con el estado sucesor
#             actual = Node(problem.result(actual.state, act), actual.value + diff[act])
#             self.niters += 1
#         return

class Tabu(LocalSearch):
    """Algoritmo de búsqueda tabú."""

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimización con búsqueda tabú.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimización
        """
        # Inicio del reloj
        start = time()

        # Crear el nodo inicial con permutación inicial aleatoria
        actual = Node(problem.init, problem.obj_val(problem.init))
        mejor = actual
        tabu = []  # Lista tabú de nodos visitados

        while True:
            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual.state)

            # Excluir tabu
            possible_acts = {act: val for act, val in diff.items() if act not in tabu}

            # Verificar si no hay acciones posibles(ponemos?)
            if not possible_acts:
                break

            # Buscar la acción que genere el mayor incremento de valor objetivo
            max_act = max(possible_acts, key=possible_acts.get)

            # Retornar si estamos en un óptimo local
            if possible_acts[max_act] <= 0:
                self.tour = actual.state
                self.value = actual.value
                end = time()
                self.time = end - start
                if actual.value < mejor.value:
                    mejor = actual
                tabu.append(mejor)  # Agregar el mejor nodo a la lista tabú
                problem.random_reset()  # Reiniciar con permutación inicial aleatoria
                actual = Node(problem.init, problem.obj_val(problem.init))
                continue

            # Moverse a un nodo con el estado sucesor
            actual = Node(problem.result(actual.state, max_act), actual.value + possible_acts[max_act])
            self.niters += 1

        self.tour = mejor.state  # Guardar la mejor solución encontrada
        self.value = mejor.value