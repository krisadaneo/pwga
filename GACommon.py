import random

class Gene:

	def __init__(self, allele):
		self.allele = allele
	
	def get_allele(self):
		return self.allele
	
	def set_allele(self, allele):
		return self.allele
	
	def __repr__(self):
		return str(self.allele)

class Individual:
	
	def __init__(self, chromosome, sampling=[], fitness=0.0):
		self.fitness = fitness
		self.chromosome = None
		self.sampling = sampling
		if type(chromosome) == list:
			self.init_list(chromosome)
		else:
			self.init_size(chromosome)
	
	def init_list(self, chromosome):
		self.chromosome = []
		for chr in chromosome:
			self.chromosome.append(Gene(chr))
	
	def init_size(self, chromosome):
		self.chromosome = []
		sampling_size = len(self.sampling) - 1
		for ch in range(chromosome):
			index = random.randint(0, sampling_size)
			self.chromosome.append(Gene(self.sampling[index]))
	
	def get_chromosome(self):
		return self.chromosome
	
	def get_chromosome_size(self):
		return len(self.chromosome)
	
	def set_gene(self, offset, gene):
		self.chromosome[offset] = gene
	
	def get_gene(self, offset):
		return self.chromosome[offset]
	
	def set_fitness(self, fitness):
		self.fitness = fitness
	
	def get_fitness(self):
		return self.fitness
	
	def __repr__(self):
		return self.chromosome.__str__()+" fitness:{}".format(self.fitness)

class Population:

	def __init__(self, individuals, chromosome_size, sampling=[]):
		self.individuals = None
		self.population_fitness = -1
		if type(individuals) == list:
			self.individuals = individuals
		else:
			self.init_population(individuals, chromosome_size, sampling)
	
	def init_population(self, population_size, chromosome_size, sampling):
		self.individuals = []
		for index in range(population_size):
			self.individuals.append(Individual(chromosome_size, sampling))
		
	def get_individuals(self):
		return self.individuals
	
	def get_fittest(self, offset):
		self.individuals.sort(key=lambda x: x.fitness, reverse=True)
		return self.individuals[offset]
	
	def set_population_fitness(self, fitness):
		self.population_fitness = fitness
	
	def get_population_fitness(self):
		return self.population_fitness
		
	def size(self):
		return len(self.individuals)
	
	def set_individual(self, offset, individual):
		self.individuals[offset] = individual
	
	def get_individual(self, offset):
		return self.individuals[offset]

	def shuffle(self):
		for i in range(len(self.individuals) - 1, -1, -1):
			index = random.randrange(-1, i)
			individual = self.individuals[index]
			self.individuals[index] = self.individuals[i]
			self.individuals[i] = individual
		
class GACommon:

	def __init__(self, sampling=[],
		chromosome_size=10,
		population_size=100,
		mutation_rate=0.01,
		crossover_rate=0.95,
		elitism_count=0):
		self.chromosome_size = chromosome_size
		self.population_size = population_size
		self.mutation_rate = mutation_rate
		self.crossover_rate = crossover_rate
		self.elitism_count = elitism_count
		self.sampling = sampling
	
	def initial_population(self, population, adapter=None):
		if type(population) == list:
			self.set_population(population, adapter)
		else:
			self.set_population_size(population, adapter)
	
	def set_population(self, population, adapter=None):
		if adapter == None:
			self.population = population
		else:
			adapter(self.population, population) 
		
	def set_population_size(self, population_size, adapter=None):
		self.population = []
		if adapter == None:
			adapter(self.chromosome_size, population_size, self.population)
		else:
			for index in range(population_size):
				self.population.append(Individual(self.chromosome_size, self.sampling))
	
	def calc_fitness(self, individual):
		pass
	
	def eval_population(self, population):
		pop_fitness = 0.0
		for indv in population.get_individuals():
			pop_fitness += self.calc_fitness(indv)
		population.set_population_fitness(pop_fitness)
	
	def is_termination(self, population):
		for indv in population.get_individuals():
			if indv.get_fitness() == 1:
				return True
		return False
	
	def select_parent(self, population):
		indvs = population.get_individuals()
		populationFitness = population.get_population_fitness()
		position = random.uniform(0.0, 1.0) * populationFitness
		spin = 0
		for indv in indvs:
			spin += indv.get_fitness()
			if spin >= position:
				return indv
		return indvs[-1]
	
	def crossover(self, population):
		new_population = Population(population.size(), 
			population.get_chromosome_size(), self.sampling)
		for inx in range(population.size()):
			parent1 = population.get_fittest(inx)
			if self.crossover_rate > random.uniform(0.0, 1.0) and inx > self.elitism_count:
				offspring = Individual(parent1.get_chromosome_size(), self.sampling)
				parent2 = self.select_parent(population)
				for inx2 in range(parent1.get_chromosome_size()):
					if 0.5 > random.uniform(0.0, 1.0):
						offspring.set_gene(inx2, parent1.get_gene(inx2))
					else:
						offspring.set_gene(inx2, parent2.get_gene(inx2))
				new_population.set_individual(inx, offspring)
			else:
				new_population.set_individual(inx, parent1)
		return new_population
	
	def mutation(self, population):
		new_population = Population(population.size(), 
			population.get_chromosome_size(), self.sampling)
		for indx in range(population.size()):
			indv = population.get_fittest(indx)
			for ingx in range(indv.get_chromosome_size()):
				if indx >= self.elitism_count:
					if self.mutation_rate > random.uniform(0.0, 1.0):
						mu_chk = False
						while not mu_chk:
							mu_inx = random.randint(0, len(self.sampling)-1)
							if indv.get_gene(ingx).get_allele() != self.sampling[mu_inx]:
								indv.set_gene(ingx, self.sampling[mu_inx])
								mu_chk = True
			new_population.set_individual(indx, indv)
		return new_population
	
	def execution(self):
		pass
		
def main(adap):
	sampling = ['000', '001', '002', '003']
	ins = []
	'''chromosome_size = 3'''
	chromosome_size = ['000', '001', '002', '003']
	ins.append(Individual(chromosome_size, sampling, 3.0))
	ins.append(Individual(chromosome_size, sampling, 1.0))
	ins.append(Individual(chromosome_size, sampling, 9.0))
	ins.append(Individual(chromosome_size, sampling, 2.0))
	ins.append(Individual(chromosome_size, sampling, 4.0))
	ins.append(Individual(chromosome_size, sampling, 7.0))
	ins.append(Individual(chromosome_size, sampling, 6.0))
	ins.append(Individual(chromosome_size, sampling, 8.0))
	ins.append(Individual(chromosome_size, sampling, 0.0))
	ins.append(Individual(chromosome_size, sampling, 5.0))
	pop = Population(ins, chromosome_size)
	'''print("Fit:{}".format(pop.get_fittest(0)))'''
	pop.shuffle()
	indvs = pop.get_individuals()
	for ind in indvs:
		print("indv:{}".format(ind))
	adap(903)
	

if __name__ == "__main__":
	main(adapter)