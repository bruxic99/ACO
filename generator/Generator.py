from random import randint
import pathlib


class Generator:
    graph = []
    min_degree = 0
    max_degree = 0
    min_weight = 0
    max_weight = 0
    Filename = ""
    number_of_vertexes = 0

    def __init__(self, min_d, max_d, min_w, max_w, nov, filename):
        self.min_degree = min_d
        self.max_degree = max_d
        self.min_weight = min_w
        self.max_weight = max_w
        self.number_of_vertexes = nov
        self.Filename = filename

    def generate(self):
        vertex_degree = [[0, randint(self.min_degree, self.max_degree)] for x in range(self.number_of_vertexes)]
        for i in range(self.number_of_vertexes):
            actual_degree = vertex_degree[i][1] - vertex_degree[i][0]
            if actual_degree >= 1:
                neighbours = [self.check_if_the_same(randint(0, (self.number_of_vertexes-1)), i) for x in range(actual_degree-1)]
                for neighbour in neighbours:
                    vertex_degree[i][0] += 1
                    vertex_degree[neighbour][0] += 1
                    self.graph.append([i, neighbour, randint(self.min_weight, self.max_weight)])
            else:
                continue
        for i in range(self.number_of_vertexes):
            count = 0
            for j in self.graph:
                if i == j[0] or i == j[1]:
                    count += 1
            if count == 0:
                self.graph.append([i, randint(0, (self.number_of_vertexes-1)), randint(self.min_weight, self.max_weight)])

        self.graph = sorted(self.graph, key=lambda x: x[0])
        self.save()

    def check_if_the_same(self, number, actual):
        if actual == number:
            return self.check_if_the_same(randint(0, (self.number_of_vertexes-1)), actual)
        else:
            return number

    def save(self):
        path = str(pathlib.Path().absolute()).split("\\")
        path_to_save = "\\".join(path[0:len(path)-1])
        with open(f"{path_to_save}/instances/{self.Filename}", "w") as f:
            for item in self.graph:
                f.write(f"{item[0]} {item[1]} {item[2]}\n")


if __name__ == "__main__":
    graphs = [[30, [2, 6], [1, 100]],
              [35, [1, 5], [1, 100]],
              [40, [3, 6], [1, 100]],
              [45, [2, 4], [90, 100]]]
    for graph in graphs:
        generator = Generator(graph[1][0], graph[1][1], graph[2][0], graph[2][1], graph[0], f"{graph[0]}.txt")
        generator.generate()