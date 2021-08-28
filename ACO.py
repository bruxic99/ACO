from random import randint
import time


class Aco:
    best_solution = []
    best_score = 0
    graph = []
    Solution = []
    pheromone_matrix = []
    probabilities = []
    counter_edges = []
    Solution_score = 0
    alpha = 1.0
    beta = 5.0
    number_of_ants = 5
    number_of_vertexes = 0
    evaporation = 0.5
    pheromone = 2.0
    iterations = 0
    Dictionary = {}

    '''
        Konstruktor klasy Aco
    '''

    def __init__(self, Alpha, Beta, Number_of_Ants, Evaporation, Pheromone, iterations, filename):
        self.graph = []
        self.load_from_file(filename)
        self.alpha = Alpha
        self.beta = Beta
        self.number_of_ants = Number_of_Ants
        self.evaporation = Evaporation
        self.iterations = iterations
        self.pheromone = Pheromone

    '''
        Glowna funkcja w ktorej startuje algorytm
    '''

    def solve(self):
        self.Dictionary = {}
        self.spread_pheromone()
        for iteration in range(self.iterations):
            self.counter_edges = [0 for x in range(len(self.graph))]
            self.best_score = 0
            self.best_solution = []
            start = time.time()
            for ant in range(self.number_of_ants):
                vertexes = []
                self.Solution = []
                self.Solution_score = 0
                vertex = randint(0, (self.number_of_vertexes - 1))
                while True:
                    if vertex not in vertexes:
                        vertexes.append(vertex)
                    edge = self.select_next_vertex(vertex)
                    self.add_solution(edge)
                    vertex = self.update_vertex(edge, vertex)
                    if len(vertexes) == self.number_of_vertexes:
                        break
                self.update_result()
            self.pheromone_evaporation()
            self.Dictionary[iteration] = {"Solution_score": self.best_score, "Alpha": self.alpha, "Beta": self.beta,
                                          "Evaporation": self.evaporation, "Pheromone": self.pheromone,
                                          "Time": time.time() - start}
        return self.Dictionary

    '''
        Wybranie nastepnego wierzcholka
    '''

    def select_next_vertex(self, current_index):
        neighbours = self.get_neighbours(current_index)
        if self.check_visited(neighbours):
            possible = self.get_possible(neighbours)
            self.get_probability(possible)
            drawn = randint(0, 99) / 100
            total = 0.0
            for i in range(len(possible)):
                total += self.probabilities[i]
                if total >= drawn:
                    return possible[i]
        else:
            if len(neighbours) == 1:
                return neighbours[0]
            else:
                return neighbours[randint(0, (len(neighbours) - 1))]

    '''
        Uaktualnienie najlepszego wyniku
    '''

    def update_result(self):
        if len(self.best_solution) == 0:
            self.best_score = self.Solution_score
            self.best_solution = self.Solution
        if self.Solution_score < self.best_score:
            self.best_score = self.Solution_score
            self.best_solution = self.Solution

    '''
        Uaktualnienie zmiany wierzcholka
    '''

    def update_vertex(self, index, current):
        if self.graph[index][0] == current:
            return self.graph[index][1]
        else:
            return self.graph[index][0]

    '''
        Wczytanie grafu z pliku
    '''

    def load_from_file(self, filename):
        f = open(f"./instances/{filename}", "r")
        for line in f:
            self.graph.append([int(x) for x in line.split()])
        self.number_of_vertexes = int(filename.split(".")[0])
        f.close()

    '''
        Wyszukanie sasiadow aktualnego wierzcholka
    '''

    def get_neighbours(self, current):
        neighbours = []
        for i in range(len(self.graph)):
            if self.graph[i][1] == current or self.graph[i][0] == current:
                neighbours.append(i)
        return neighbours

    '''
        Obliczenie prawdopodbienstwa dla kazdego z sasiadow na podstawie wzoru
    '''

    def get_probability(self, neighbours):
        pheromone = 0.0
        numerators = []
        self.probabilities = []
        for neighbour in neighbours:
            x = (self.pheromone_matrix[neighbour] ** self.alpha) * \
                (1.0 / self.graph[neighbour][2] ** self.beta)
            pheromone += x
            numerators.append(x)
        for numerator in numerators:
            self.probabilities.append(numerator / pheromone)

    '''
        Sprawdzenie czy sasiedzi aktualnego wierzcholka byli juz odwiedzani
    '''

    def check_visited(self, neighbours):
        for neighbour in neighbours:
            if neighbour not in self.Solution:
                return True
        return False

    '''
        Rozlozenie feromonu (poczatkowa wartosc)
    '''

    def spread_pheromone(self):
        self.pheromone_matrix = [self.pheromone for x in range(len(self.graph))]

    '''
        Wyparowanie feromonu oraz uaktualnienie feromonu na krawedziach
    '''

    def pheromone_evaporation(self):
        for i in range(len(self.pheromone_matrix)):
            self.pheromone_matrix[i] *= self.evaporation
        for edge in self.Solution:
            self.pheromone_matrix[edge] += self.pheromone * 5

    '''
        Wyszukanie i zwrocenie krawedzi ktore nie byly wykorzystane
    '''

    def get_possible(self, neighbours):
        possible = []
        for neighbour in neighbours:
            if neighbour not in self.Solution:
                possible.append(neighbour)
        return possible

    '''
        Dodanie ideksu krawedzi do rozwiazania, zwiekszona ilosc przejscia o 1 oraz podliczenie wyniku podanego w problemie
    '''

    def add_solution(self, index):
        self.Solution.append(index)
        self.counter_edges[index] += 1
        self.Solution_score += self.graph[index][2] * self.counter_edges[index]
