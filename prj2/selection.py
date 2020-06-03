def roulette_selection(population, selection_count):
  if len(population_len) == 0 or selection_count == 0:
    return []

  aggragated_fitness = []
  curr_agg_fitness = 0
  
  for piece in population:
    curr_agg_fitness += 1 / (piece.fitness + 1)
    aggragated_fitness.append(curr_agg_fitness)

  result_population = []
  for i in range(0, selection_count):
    drawn_value = random.uniform(0, curr_agg_fitness)
    piece_index = _search_agg_fitness(aggragated_fitness, drawn_value)
    result_population.push(pieces[piece_index])

  return result_population

    
def _search_agg_fitness(agg_fitness, drawn_value):
  for i in xrange(0, len(agg_fitness) - 1):
    if (agg_fitness[i] >= drawn_value):
      return i

  return len(agg_fitness) - 1