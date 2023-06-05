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
    
        # Crear el nodo inicial con la misma permutacion inicial que el hillClimbing
        actual = Node(problem.init, problem.obj_val(problem.init))
        mejor = actual
        #Cantidad de reseteos aleatorios 
        resets=10

        while True :
            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual.state) 

            # Buscar las acciones que generan el mayor incremento de valor objetivo
            max_acts = [act for act, val in diff.items() if val == max(diff.values())]

            # Elegir una accion aleatoria
            act = choice(max_acts)

            # Retornar si estamos en un optimo local
            if diff[act] <= 0 :
                #Si el optimo local es mejor que el optimo global se reemplaza
                if actual.value > mejor.value:
                    self.tour = actual.state
                    self.value = actual.value
                    mejor = actual
                #print(f"Mejor local de la iteracion {resets} es {actual.value}")
                #print(f"El mejor global a la iteriacion {resets} es {self.value}")                             
                #Si no es mejor se prodece a reiniciar el HillClimbing con una permutacion inicial aleatoria
                problem.random_reset()
                actual = Node(problem.init, problem.obj_val(problem.init))
                resets-=1
                continue


            # Sino, moverse a un nodo con el estado sucesor
            actual = Node(problem.result(actual.state, act), actual.value + diff[act])
            self.niters += 1
            
            #Cuando llegue al ultimo reset se detiene el reloj y se hace el return
            if resets==0:
                end = time()
                self.time = end - start
                #print(f"Ejecucion HillClimbing con Reset exitosa")
                return





class Tabu(LocalSearch):
    """Algoritmo de busqueda de optimo con lista Tabu."""

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con busqueda tabu.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()
        # Crear el nodo inicial
        actual = Node(problem.init, problem.obj_val(problem.init))
        mejor = actual
        # Lista tabú para almacenar acciones
        tabu = []  
        # Contador de iteraciones sin mejoras
        iteraciones_corte = 0  
        # Cantidad de elementos de la lista Tabu
        tabu_memoria = 20

        while iteraciones_corte < 500 :
            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual.state)

            # Buscar las acciones que generan el mayor incremento de valor objetivo que no esten en la lista tabu
            acciones_posibles = [act for act, val in diff.items() if act not in tabu]

            # Elegir una accion aleatoria si hay elecciones posibles
            if not acciones_posibles:
                break
            act = max(acciones_posibles, key=diff.get)

            # Moverse a un nodo con el estado sucesor
            actual = Node(problem.result(actual.state, act),
                        actual.value + diff[act])

            # Actualizar la lista tabú
            tabu.append(act)
            #print(f"En la iteracion {self.niters} se agrega al tabu {act}")
            #Control de cantidad de elementos de la lista Tabu
            if len(tabu) > tabu_memoria:
                #print(f"En la iteracion {self.niters} se quito de la lita {tabu[0]}")
                tabu = tabu[1:]  # Eliminar la acción más antigua de la lista tabú
                

            # Actualizar la mejor solución encontrada
            if actual.value > mejor.value:
                mejor = actual
            iteraciones_corte+=1
            self.niters += 1
            

        # Guardar los valores del mejor resultado obtenido luego de que se cumpla condicon de corte
        
        if iteraciones_corte == 500:
            self.tour = mejor.state
            self.value = mejor.value
            end = time()
            self.time = end - start
            #print(f"Ejecucion Busqueda Tabu exitosa")
            return
