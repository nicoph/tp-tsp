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
#     """Algoritmo de búsqueda tabú."""

#     def solve(self, problem: OptProblem):
#         """Resuelve un problema de optimización con búsqueda tabú.

#         Argumentos:
#         ==========
#         problem: OptProblem
#             un problema de optimización
#         """
#         # Inicio del reloj
#         start = time()

#         # Crear el nodo inicial con permutación inicial aleatoria
#         actual = Node(problem.init, problem.obj_val(problem.init))
#         mejor = actual
#         tabu = []  # Lista tabú de estados visitados

#         while True:
#             # Determinar las acciones que se pueden aplicar
#             # y las diferencias en valor objetivo que resultan
#             diff = problem.val_diff(actual.state)

#             # Excluir acciones tabú
#             #possible_acts = {act: val for act, val in diff.items() if act not in tabu}
#             max_acts = [act for act, val in diff.items() if (val == max(diff.values()) and act not in tabu)]
#             print(tabu)
            

#             # Verificar si no hay acciones posibles
#             if not max_acts:
#                 print("falta")
#                 break
#             act = choice(max_acts)
#             # Buscar la acción que genere el mayor incremento de valor objetivo

#             # Retornar si estamos en un óptimo local
#             if diff[act] <= 0:
#                 print("lkasdf")
#                 self.tour = actual.state
#                 self.value = actual.value
#                 end = time()
#                 self.time = end - start 
                
#                 if actual.value > mejor.value:                    
#                     mejor = actual
                    
#                 actual = Node(problem.result(actual.state, act), actual.value + diff[act])
                
#                 continue

#             # Moverse a un nodo con el estado sucesor
#             tabu.append(act)  # Agregar el estado actual a la lista tabú
#             tabu = tabu[-20:]  # Limitar la longitud de la lista tabú
#             actual = Node(problem.result(actual.state, act), actual.value + diff[act])
#             self.niters += 1

#             # Si no hay cambios en el mejor valor durante cierto número de iteraciones, terminar
#             if self.niters > 500:
#                 if actual.value <= mejor.value:
#                     break
#             #print(len(tabu))

#         self.tour = mejor.state  # Guardar la mejor solución encontrada
#         self.value = mejor.value

# class Tabu(LocalSearch):
#     """Algoritmo de búsqueda tabú."""

#     def solve(self, problem: OptProblem):
#         """Resuelve un problema de optimización con búsqueda tabú.

#         Argumentos:
#         ==========
#         problem: OptProblem
#             un problema de optimización
#         """
#         # Inicio del reloj
#         start = time()

#         # Crear el nodo inicial con permutación inicial aleatoria
#         actual = Node(problem.init, problem.obj_val(problem.init))
#         mejor = actual
#         tabu = [actual.state]  # Lista tabú de estados visitados

#         while True:
#             # Determinar las acciones que se pueden aplicar
#             # y las diferencias en valor objetivo que resultan
#             diff = problem.val_diff(actual.state)

#             # Excluir acciones tabú
#             possible_acts = {act: val for act, val in diff.items() if act not in tabu}

#             # Verificar si no hay acciones posibles
#             if not possible_acts:
#                 break

#             # Buscar la acción que genere el mayor incremento de valor objetivo
#             max_act = max(possible_acts, key=possible_acts.get)

#             # Retornar si estamos en un óptimo local
#             if possible_acts[max_act] <= 0:
#                 self.tour = actual.state
#                 self.value = actual.value
#                 end = time()
#                 self.time = end - start
#                 if actual.value > mejor.value:                    
#                     mejor = actual
#                 actual = Node(problem.result(actual.state, max_act), actual.value + possible_acts[max_act])
#                 tabu.append(actual.state)  # Agregar el estado actual a la lista tabú
#                 tabu = tabu[-10:]  # Limitar la longitud de la lista tabú
#                 continue
            
#             # Moverse a un nodo con el estado sucesor
#             actual = Node(problem.result(actual.state, max_act), actual.value + possible_acts[max_act])
#             self.niters += 1

#             # Si no hay cambios en el mejor valor durante cierto número de iteraciones, terminar
#             if self.niters < 100:
#                 if actual.value <= mejor.value:
#                     break

#         self.tour = mejor.state  # Guardar la mejor solución encontrada
#         self.value = mejor.value

class Tabu(LocalSearch):
    """Clase que representa un algoritmo de Tabu Search.

    En cada iteración se mueve al estado sucesor con mejor valor objetivo, evitando movimientos tabúes.
    El criterio de parada es alcanzar un óptimo local o un número máximo de iteraciones.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimización con Tabu Search.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimización
        tabu_list_size: int
            tamaño de la lista tabú
        num_iterations: int
            número máximo de iteraciones
        """
        # Inicio del reloj
        start = time()

        # Crear el nodo inicial
        actual = Node(problem.init, problem.obj_val(problem.init))

        # Inicializar lista tabú
        tabu_list = []
        num_iterations=100
        tabu_list_size=50

        for _ in range(num_iterations):
            print(tabu_list)
            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual.state)

            todos_caminos=[diff.keys()]
            
            # Buscar las acciones que generan el mayor incremento de valor obj
            # pero no están en la lista tabú

            max_acts = [act for act in diff.items() if act not in todos_sin_tabu ]
            todos_sin_tabu=[x for x in todos_caminos if x not in tabu_list]

            # Elegir una acción aleatoria de las permitidas
            vecino = choice(max_acts)       
            
            

            # Retornar si estamos en un óptimo local
            if diff[vecino] <= 0:

                self.tour = actual.state
                self.value = actual.value
                end = time()
                self.time = end - start
                

            # Sino, moverse a un nodo con el estado sucesor
            

            # Actualizar el nodo actual con el estado sucesor
            actual = Node(problem.result(actual.state, vecino), actual.value + diff[vecino])
            self.niters += 1

            # Agregar la acción a la lista tabú
            
            tabu_list.append(vecino)

            # Verificar el tamaño de la lista tabú y eliminar el elemento más antiguo si es necesario
            if len(tabu_list) >= tabu_list_size:
                tabu_list.pop(0)

        # Fin del algoritmo
        # Devolver el resultado actual (mejor solución encontrada)
        self.tour = actual.state
        self.value = actual.value
        end = time()
        self.time = end - start
