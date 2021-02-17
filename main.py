import random
import math
import numpy as np

SIZE_INDIVIDUO = 6
SIZE_POPULACAO = 50
TAXA_MUTACAO = 0.1

class Individuo():
    def __init__(self, size):
        self.size = size
        self.parametros = []
        self.fitness = None
        for _ in range(size):
            self.parametros.append(random.random())

    def mutacao(self, taxa):
        n_cromossomos_mutados = int(self.size * taxa)
        for _ in range(n_cromossomos_mutados):
            i = random.randint(0,self.size-1)
            self.parametros[i] = random.random()
    
    def calc_fitness(self):
        self.fitness = func_obj(self.parametros)

    def get_fitness(self):
        self.calc_fitness()
        return self.fitness

class Populacao():
    def __init__(self, arg):
        self.individuos = []
        if(type(arg)==Populacao):
            self.gerar_nova_populacao(arg)
        else:
            for _ in range(arg):
                self.individuos.append(Individuo(SIZE_INDIVIDUO))
    
    def gerar_nova_populacao(self, pop):
        pop.sort_by_fitness()
        for i in pop.individuos:
            print(i.parametros, i.fitness)


    def sort_by_fitness(self):
        self.individuos = sorted(self.individuos,key = lambda individuo : individuo.get_fitness())

def func_obj(x):

	n = float(len(x))
	f_exp = -0.2 * math.sqrt(1/n * sum(np.power(x, 2)))

	t = 0
	for i in range(0, len(x)):
		t += np.cos(2 * math.pi * x[i])

	s_exp = 1.0/n * t
	f = -20 * math.exp(f_exp) - math.exp(s_exp) + 20 + math.exp(1)
    
	return f

def main():
    pop = Populacao(SIZE_POPULACAO)
    for i in pop.individuos:
        pass
        print(i.parametros,i.get_fitness())
    print('\n\n')
    pop = Populacao(pop)

if __name__=="__main__":
    main()