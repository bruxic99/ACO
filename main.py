from ACO import Aco
import os
import json

All_test = {}


def save_to_file():
    with open("./results/result.json", "w", encoding='utf-8') as outputfile:
        json.dump(All_test, outputfile, ensure_ascii=False, indent=4)


def start():
    instances = []
    for root, dirs, files in os.walk("./instances/"):
        for filename in files:
            instances.append(filename)

    Iterations = [5]
    Alpha = [1.0]
    Beta = [5.0]
    number_of_ants = [1]
    Evaporation = [0.5]
    Pheromone = [2.0]
    for instance in instances:
        Dict = {}
        for i in range(len(Iterations)):
            aco = Aco(Alpha[i], Beta[i], number_of_ants[i], Evaporation[i], Pheromone[i], Iterations[i], instance)
            Dict = aco.solve()
        All_test.update({int(instance.split(".")[0]): Dict})


if __name__ == '__main__':
    start()
    save_to_file()
