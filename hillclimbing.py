import time
from enum import Enum
from aima.search import *
from aima.utils import *
from aima.search import Problem

class PosType(Enum):
    '''
    Enumerado com caracteres possiveis para representação do lobirinto
    '''
    FREE = ' '
    COIN = '.'
    B_COIN = 'o'
    WALL = '|'
    GHOST = 'G'
    PACMAN = 'P'
    GOAL = 'X'
    PATH = '+'

    @staticmethod
    def valid_inits():
        '''
        Retorna todos os enumerados validos que podem estar contidos em arquivo txt
        '''
        return [ptype for ptype in PosType if ptype not in [PosType.PATH]]

    @staticmethod
    def valid_pacman_positions():
        '''
        Retorna os enumerados onde o pacman pode se movimentar
        '''
        return [PosType.FREE, PosType.COIN, PosType.B_COIN, PosType.GOAL, PosType.PACMAN]

class Maze:
    '''
    Classe para ler arquivos txt representativos dos labirintos e comportamento dos elementos ao interagir
    com o pacman

    :self.w: largura do mapa
    :self.h: altura do mapa
    :self.initial_state: estado inicial (x, y)
    :self.goal_states: lista de estados objetivos [(x, y)]
    :self.free_cost: custo de uma célula livre
    :self.coin_cost: custo moeda simples
    :self.bcoin_cost: custo de uma moeda grande
    '''

    def __init__(self, filepath, free_cost=10, coin_cost=2, bcoin_cost=1):
        # Classe construtora para um maze - ler arquivo e guarda em uma lista de strings
        # Faz algumas checagens para prevenir formatos errados
        file = open(filepath, "r")
        self._maze = file.read().splitlines()
        file.close()
        self.w = len(self._maze[0])
        self.h = len(self._maze)
        self.initial_state = None
        self.goal_states = []
        self.free_cost = free_cost
        self.coin_cost = coin_cost
        self.bcoin_cost = bcoin_cost

        for y in range(self.h):
            if len(self._maze[y]) is not self.w:
                raise ValueError('Invalid map dimensions')
            else:
                # Percorre linhas obtidas pelo arquivo procurando por seugestao de posicao inicial do
                # pacman e os objetivos (se houverem), há uma simples checagem de formato invalido de mapa
                for x in range(self.w):
                    pos = (x, y)
                    if self.get(pos) is PosType.PACMAN:
                        if self.initial_state is None:
                            self.initial_state = pos
                        else:
                            raise ValueError('Multiple pacmans position')
                    elif self.get(pos) is PosType.GOAL:
                        self.goal_states.append(pos)
                    elif self.get(pos) not in PosType.valid_inits():
                        raise ValueError('Invalid char {}'.format(self._maze[y][x]))

                # Remove objetivos e pacman do mapa
                self._maze[y] = self._maze[y].replace(PosType.PACMAN.value, ' ').replace(PosType.GOAL.value, ' ')

    def get(self, pos):
        # definimos _maze[y][x]
        return PosType(self._maze[pos[1]][pos[0]])

    def get_cost(self, pos):
        # retorna o custo de acordo com a posicao
        ptype = self.get(pos)
        if ptype == PosType.COIN:
            return self.coin_cost
        elif ptype == PosType.B_COIN:
            return self.bcoin_cost
        else:
            return self.free_cost

    def possible_positions(self, pos):
        '''
        Retorna possiveis posicoes que o pacman consegue chegar a partir de pos
        :pos: posição do pacman (x, y)
        return lista de posicoes (x, y)
        '''
        x, y = pos[0], pos[1]
        possible_positions = []
        for step in [(0, -1), (1, 0), (0, 1), (-1, 0)]:  # up, right, down, left
            # soma os steps com x, e y, tomando cuidados com os limites transversais do mapa
            newX = self.w - 1 if x + step[0] < 0 else (x + step[0]) % self.w
            newY = self.h - 1 if y + step[1] < 0 else (y + step[1]) % self.h
            pos = (newX, newY)
            if self.get(pos) in PosType.valid_pacman_positions():
                possible_positions.append(pos)

        return possible_positions

    def __str__(self):
        string = ''
        for line in self._maze:
            string = string + line + '\n'
        return string

    @staticmethod
    def _print(maze):
        for line in maze:
            print(''.join(line))
        print('\n')

    def _copy_maze_list(self):
        maze = list()
        for line in self._maze:
            maze.append(list(line))
        return maze

    def print_solution(self, solution):
        '''
        Printa solucao
        :solution: lista de posicoes que levam a solucao [(x, y) ...]
        '''
        maze = self._copy_maze_list()
        for state in solution:
            maze[state[1]][state[0]] = PosType.PATH.value
        self._print(maze)

    def print_map(self):
        '''
        Printa mapa com posicao inical e objetivo
        '''
        maze = self._copy_maze_list()
        maze[self.initial_state[1]][self.initial_state[0]] = PosType.PACMAN.value
        for goal in self.goal_states:
            maze[goal[1]][goal[0]] = PosType.GOAL.value
        self._print(maze)

class MazePacmanProblem(Problem):
    '''
    Define o conjunto de ações, resultados, custo, e teste objetivo para o problema
    '''

    def __init__(self, maze):
        '''
        Instancia um objeto problema
        :initial: estado inicial do pacman - posicao por uma tupla (x, y)
        :goal: estado final, obejtivo do pacman - posição por uma tupla (x, y) ou lista de tuplas
        '''
        Problem.__init__(self, maze.initial_state, maze.goal_states)
        self.maze = maze

    def actions(self, state):
        return self.maze.possible_positions(state)

    def result(self, state, action):
        return action

    def goal_test(self, state):
        if isinstance(self.goal, list):
            return state in self.goal
        else:
            return state == self.goal

    def path_cost(self, cost_so_far, stateA, action, stateB):
        # custo do caminho é incrementado com o custo da proxima célula
        return cost_so_far + self.maze.get_cost(action)
    
    def value(self, state):
        [xGoal, yGoal] = self.goal[0]
        [xState, yState] = state

        value = abs(xGoal - xState) + abs(yGoal - yState)

        return value

class Statistics:
    '''
    Classe para auxiliar/organizar as metragens de estatisticas dos algoritmos
    :self.iterations: numero de iteracoes
    :self.expanded: numero de nos expandidos pelo algoritmo
    :self.memory: pico de memoria (numero maximo de estados salvos ao mesmo tempo)
    :self.time: tempo em ms
    :self.path_cost: custo total da solução
    '''

    def __init__(self, iterations=0, expanded=1, memory=1):
        self.iterations = iterations
        self.expanded = expanded
        self.memory = memory
        self.time = None
        self.path_cost = None
        self._start_time = time.time()

    def update_iterations(self, increment):
        self.iterations = self.iterations + increment

    def update_expanded(self, increment):
        self.expanded = self.expanded + increment

    def update_memory(self, new_memory):
        if new_memory > self.memory:
            self.memory = new_memory

    def finish(self, path_cost):
        '''
        Finaliza o timer (aberto no construtor) e salva custo da solucao
        '''
        self.path_cost = path_cost
        self.time = time.time() - self._start_time

    def __str__(self):
        sb = []
        for key in self.__dict__:
            sb.append("{key}='{value}'".format(key=key, value=self.__dict__[key]))

        return ', '.join(sb)

    def __repr__(self):
        return self.__str__()

def hill_climbing(problem):
    statistics = Statistics()
    current = Node(problem.initial)
    while True:
        #statistics.update_memory(len(frontier))
        statistics.update_iterations(1)
        neighbors = current.expand(problem)
        if not neighbors:
            break
        neighbor = argmin_random_tie(neighbors, key=lambda node: problem.value(node.state))
        if problem.value(neighbor.state) > problem.value(current.state):
            break
        current = neighbor
        statistics.update_expanded(1)
        print(current)
    statistics.finish(1)   
    return statistics, current

maze = Maze("mazes/maze_himclimbing.txt")
problem = MazePacmanProblem(maze)
print(maze)
statistics, node = hill_climbing(problem)
print(statistics)