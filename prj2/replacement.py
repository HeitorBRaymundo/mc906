def extermination(population, new_population):
    '''Selecionando metade da população original para gerar os descendentes. Funciona somente se a taxa de crossover for de 100%'''
    return new_population


def elitism(best_individual, new_population):
    new_population.insert(0, best_individual)
    return new_population


def steady_state(population, new_population, steady_rate=0.1):
    number_of_individuals_to_replace = int(len(population) * steady_rate)

    new_population = new_population[0:(len(new_population) - number_of_individuals_to_replace)]

    for i in range(number_of_individuals_to_replace):
        new_population.append(population[i])

    return new_population
