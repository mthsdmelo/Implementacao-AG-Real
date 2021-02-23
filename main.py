import random
import math
import numpy as np
import argparse

parametros_execucao = {
    'tamanho_individuo' : 10,
    'tamanho_populacao' : 50,
    'taxa_mutacao' : 0.01,
    'taxa_cruzamento' : 1,
    'numero_geracoes' : 100,
    'elitismo' : True
}

class Individuo():
    def __init__(self, *args):
        self.size = 0
        self.parametros = []
        if len(args) >= 1:
            size = args[0]
            self.size = size
            for _ in range(size):
                self.parametros.append(random.random())

    def mutacao(self):
        taxa = parametros_execucao.get('taxa_mutacao')
        n_cromossomos_mutados = int(round(self.size * taxa))
        for _ in range(n_cromossomos_mutados):
            i = random.randint(0,self.size-1)
            self.parametros[i] = random.random()

    def get_fitness(self):
        return func_obj(self.parametros)

    def add_parametro(self, x):
        self.size += 1
        self.parametros.append(x)

    def get(self):
        return self.parametros

class Populacao():
    def __init__(self, *args):
        self.individuos = []
        if len(args) >= 1:
            tamanho_populacao = args[0]
            for _ in range(tamanho_populacao):
                self.individuos.append(Individuo(parametros_execucao.get('tamanho_individuo')))
    
    def add_individuo(self, individuo):
        self.individuos.append(individuo)

    def seleciona_pais(self):
        fitness_inverso = []
        for i in range(len(self.individuos)):
            fitness_inverso.append(1/self.individuos[i].get_fitness())
        
        total = sum(fitness_inverso)

        roleta = []
        for i in range(len(self.individuos)):
            roleta.append(fitness_inverso[i]/total)

        tamanho_pop = parametros_execucao.get('tamanho_populacao')
        pais = []
        for i in range(tamanho_pop):
            r = random.random()
            soma = 0
            for item in roleta:
                soma += item
                if soma >= r:
                    pais.append(roleta.index(item))
                    break
        
        selecionados = []
        for i in range(int(tamanho_pop/2)):
            selecionados.append((pais[i*2],pais[i*2+1]))

        return selecionados

    def cruzamento(self, pais):
        pai1 = pais[0]
        pai2 = pais[1]
        X = self.individuos[pai1]
        Y = self.individuos[pai2]

        if X.get_fitness() > Y.get_fitness():
            aux = X
            X = Y
            Y = aux

        d = []
        for a,b in zip(X.get(), Y.get()):
            d.append(abs(a-b))

        filho1 = Individuo()
        filho2 = Individuo()

        alfa = 0.75
        beta = 0.25

        for i in range(X.size):
            if X.get()[i] <= Y.get()[i]:
                filho1.add_parametro(random.uniform(X.get()[i]-alfa*d[i], Y.get()[i]+beta*d[i]))
                filho2.add_parametro(random.uniform(X.get()[i]-alfa*d[i], Y.get()[i]+beta*d[i]))
            else:
                filho1.add_parametro(random.uniform(Y.get()[i]-beta*d[i], X.get()[i]+alfa*d[i]))
                filho2.add_parametro(random.uniform(Y.get()[i]-beta*d[i], X.get()[i]+alfa*d[i]))

        return filho1, filho2

    def get_proxima_geracao(self):
        pais = self.seleciona_pais()
        
        nova_pop = Populacao()

        for casal in pais:
            filho1, filho2 = self.cruzamento(casal)
            filho1.mutacao()
            filho2.mutacao()
            nova_pop.add_individuo(filho1)
            nova_pop.add_individuo(filho2)

        if parametros_execucao.get('elitismo') :
            melhor = self.melhor_individuo()
            pos = random.randint(0, parametros_execucao.get('tamanho_populacao')-1)
            nova_pop.individuos[pos] = melhor

        return nova_pop


    def get(self):
        return self.individuos

    def media_fitness(self):
        media = 0
        for ind in self.individuos:
            media += ind.get_fitness()

        media /= parametros_execucao.get('tamanho_populacao')

        return media

    def melhor_individuo(self):
        melhor = (None, 999999999)
        for ind in self.individuos:
            fit = ind.get_fitness()
            if  fit < melhor[1]:
                melhor = (ind, fit)

        return melhor[0]

def func_obj(x):

	n = float(len(x))
	f_exp = -0.2 * math.sqrt(1/n * sum(np.power(x, 2)))

	t = 0
	for i in range(0, len(x)):
		t += np.cos(2 * math.pi * x[i])

	s_exp = 1.0/n * t
	f = -20 * math.exp(f_exp) - math.exp(s_exp) + 20 + math.exp(1)
    
	return f

def ler_parametros_execucao():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tamanho_individuo', "-i")
    parser.add_argument('--tamanho_populacao', "-p")
    parser.add_argument('--taxa_mutacao', "-m")
    parser.add_argument('--taxa_cruzamento', "-c")
    parser.add_argument('--numero_geracoes', "-g")
    parser.add_argument('--elitismo', "-e")

    args = parser.parse_args()

    global parametros_execucao
    try:
        if args.tamanho_individuo:
            parametros_execucao['tamanho_individuo'] = int(args.tamanho_individuo)
        if args.tamanho_populacao:
            parametros_execucao['tamanho_populacao'] = int(args.tamanho_populacao)
        if args.taxa_mutacao:
            parametros_execucao['taxa_mutacao'] = float(args.taxa_mutacao)
        if args.taxa_cruzamento:
            parametros_execucao['taxa_cruzamento'] = float(args.taxa_cruzamento)
        if args.numero_geracoes:
            parametros_execucao['numero_geracoes'] = int(args.numero_geracoes)
        if args.elitismo:
            parametros_execucao['elitismo'] = bool(int(args.elitismo))
    except:
        print('Parametro de entrada invalido')

def main():
    ler_parametros_execucao()
    pop = Populacao(parametros_execucao.get('tamanho_populacao'))

    for _ in range(parametros_execucao.get('numero_geracoes')):
        nova_pop = pop.get_proxima_geracao()
        pop = nova_pop
        print(nova_pop.media_fitness())

    print(pop.melhor_individuo().get(), pop.media_fitness())

if __name__=="__main__":
    main()