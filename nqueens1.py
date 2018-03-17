import numpy as np
import random


class Solver_8_queens:

    board_width = 8
    cross_prob = 0.4
    mut_prob = 0.2
    pop_size = 101

    FitValue = np.zeros((pop_size, 1), dtype=np.int)  # для хранения значений Fitnesses для всей популяции
    population = np.zeros((pop_size, board_width), dtype=np.int)

    def __init__(self, pop_size=80, cross_prob=0.25, mut_prob=0.9):
        self.pop_size = pop_size
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob

    def solve(self, min_fitnes=0.07, max_epochs=50000):
        iter = 0
        self.generate_population()

        viner,  ibest = self.CalculateFitnesses()
        while viner < 0 and iter < max_epochs and float(self.FitValue[ibest])/28 > min_fitnes:
            iter = iter + 1
            self.SortIndivids()
            self.Crossing()
            self.Mutation()
            viner, ibest = self.CalculateFitnesses()

        return self.FitValue[ibest],  iter, self.Visual(self.population[ibest])

    def generate_population(self): #Генерация исходной популяции
        for hromosom in self.population:
            for position in range(len(hromosom)):
                hromosom[position] = random.randrange(0, self.board_width-1, 1)

    def CalculateFitnesses(self):
        BestFit = 2 * self.board_width
        winner = -1
        ibest = 0
        for i in range(self.pop_size):
            Fit_V = self.Fitness(self.population[i])
            self.FitValue[i] = Fit_V
            if Fit_V < BestFit:
                BestFit = Fit_V
                ibest = i
            if BestFit == 0:
                winner = i
                ibest = i
                break
        return winner, ibest

    def Fitness(self, gen):
        Fit = 0
        for igen in range(0, self.board_width - 1, 1):
            for jgen in range(igen + 1, self.board_width, 1):
                if gen[igen] == gen[jgen] or abs(gen[igen] - gen[jgen]) == abs(igen - jgen) or abs(
                        gen[igen] + gen[jgen]) == abs(igen + jgen):
                    Fit = Fit + 1

        return Fit

    def SortIndivids(self):
        for i in range(self.pop_size - 1):
            for j in range(i + 1, self.pop_size):
                if self.FitValue[i] > self.FitValue[j]:
                    a = self.population[j].copy()
                    self.population[j] = self.population[i]
                    self.population[i] = a

                    b = self.FitValue[j].copy()
                    self.FitValue[j] = self.FitValue[i]
                    self.FitValue[i] = b

    def Crossing(self):
        ngood = self.pop_size // 2
        nthebest = self.pop_size // 4

        for igood in range(ngood):
            ithebest = random.randrange(0, 32767, 1) % (nthebest + 1)
            while igood == ithebest:
                ithebest = random.randrange(0, 32767, 1) % (nthebest + 1)
                break

            if ithebest == nthebest:
                ithebest = self.pop_size // 2 + random.randrange(0, 32767, 1) % (self.pop_size // 2)

            parent1 = self.population[igood]
            parent2 = self.population[ithebest]
            parent1, parent2 = self.DoCross(parent1, parent2)

            self.population[2 * igood] = parent1
            self.population[2 * igood + 1] = parent2

    def DoCross(self, parent1, parent2):
        breakpoint = random.randrange(0, self.board_width-1, 1)
        child1=np.zeros(self.board_width, dtype=np.uint8)
        child2 = np.zeros(self.board_width, dtype=np.uint8)

        for i in range(breakpoint):
            child1[i] = parent1[i]
            child2[i] = parent2[i]

        for i in range(breakpoint+1, self.board_width):
            child1[i] = parent2[i]
            child2[i] = parent1[i]
        return child1, child2

    def Mutation(self):
        for i in range(int(self.mut_prob * self.pop_size)):
            n = random.randrange(0, self.pop_size, 1)
            k = random.randrange(0, self.board_width-1, 1)
            self.population[n, k] = random.randrange(0, self.board_width-1, 1)

    def Visual(self, gen):
        visualization = np.zeros((self.board_width, self.board_width), dtype=np.dtype)
        for j in range(self.board_width):
            for i in range(self.board_width):
                if gen[j] == i:
                    visualization[i, j] ='Q'
                else:
                    visualization[i, j] ='+'
        return visualization







