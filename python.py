import random
import math
from typing import List, Tuple
import matplotlib.pyplot as plt

class VRP:
	"""
	Simple Vehicle Routing Problem (VRP) solver using Tabu Search.
	"""

	def __init__(self, cities: List[Tuple[str, float]], n_cars=5, capacity=1000, tabu_tenure=10, iterations=200, seed=42):
		"""
		Initialize the VRP model.


		Args:
		cities (List[Tuple[str, float]]): List of (city_name, distance) pairs. First city is the root.
		n_cars (int): Number of available vehicles.
		capacity (int): Capacity per vehicle (simplified as client count capacity).
		tabu_tenure (int): Number of iterations a move stays tabu.
		iterations (int): Number of tabu search iterations.
		seed (int): Random seed for deterministic behavior.
		"""

		self.cities = cities
		self.n_cars = n_cars
		self.capacity = capacity
		self.tabu_tenure = tabu_tenure
		self.iterations = iterations
		self.seed = seed

		random.seed(self.seed)

		self.root = cities[0]
		self.client_distances = [dist for _, dist in cities[1:]]

		# trivial demand: each client demands "distance" units or 1 unit? (use 1)
		self.demands = [1 for _ in cities[1:]]

	def total_distance(self, solution):
		"""
		Compute the total cost of all routes.

		Args:
		solution: A list of routes where each route is a list of distances.

		Returns:
		float: Total distance of the solution.
		"""

		return sum(sum(route) for route in solution)

	def create_initial_solution(self):
		"""
		Build a random feasible initial solution by assigning clients to cars.

		Returns:
		List[List[float]]: Initial set of routes.
		"""

		# randomly assign each client to a car if capacity allows
		routes = [[] for _ in range(self.n_cars)]
		capacities = [self.capacity] * self.n_cars

		for dist in self.client_distances:
			assigned = False
			while not assigned:
				car = random.randint(0, self.n_cars - 1)
				if capacities[car] >= 1:
					routes[car].append(dist * 2)  # go-and-return cost
					capacities[car] -= 1
					assigned = True
		return routes

	def tabu_search(self):
		"""
		Run the tabu search optimization process.

		Returns:
		Tuple[solution, cost]: Best found solution and its total cost.
		"""

		current_solution = self.create_initial_solution()
		best_solution = current_solution
		best_cost = self.total_distance(best_solution)

		tabu_list = {}

		for it in range(self.iterations):
			neighborhood = []

			# generate neighbors by swapping clients between cars
			for i in range(self.n_cars):
				for j in range(self.n_cars):
					if i != j and current_solution[i] and current_solution[j] is not None:
						for a in range(len(current_solution[i])):
							for b in range(len(current_solution[j])):
								new_solution = [route[:] for route in current_solution]
								new_solution[i][a], new_solution[j][b] = new_solution[j][b], new_solution[i][a]

								move = (i, j, a, b)
								if move not in tabu_list:
									neighborhood.append((new_solution, move))

			if not neighborhood:
				break

			best_neighbor = None
			best_neighbor_cost = float('inf')
			best_move = None

			for solution, move in neighborhood:
				cost = self.total_distance(solution)
				if cost < best_neighbor_cost:
					best_neighbor = solution
					best_neighbor_cost = cost
					best_move = move

			current_solution = best_neighbor
			tabu_list[best_move] = self.tabu_tenure

			# decrease tabu tenure
			for k in list(tabu_list.keys()):
				tabu_list[k] -= 1
				if tabu_list[k] <= 0:
					del tabu_list[k]

			if best_neighbor_cost < best_cost:
				best_solution = best_neighbor
				best_cost = best_neighbor_cost

		return best_solution, best_cost

cities = [
	("Krakow", 0),
	("Bialystok", 500),
	("Bielsko-Biala", 50),
	("Chrzanow", 400),
	("Gdansk", 200),
	("Gdynia", 100),
	("Gliwice", 40),
	("Gromnik", 200),
	("Katowice", 300),
	("Kielce", 30),
	("Krosno", 60),
	("Krynica", 50),
	("Lublin", 60),
	("Lodz", 160),
	("Malbork", 100),
	("NowyTarg", 120),
	("Olsztyn", 300),
	("Poznan", 100),
	("Pulawy", 200),
	("Radom", 100),
	("Rzeszow", 60),
	("Sandomierz", 200),
	("Szczecin", 150),
	("Szczucin", 60),
	("SzklarskaPoreba", 50),
	("Tarnow", 70),
	("Warszawa", 200),
	("Wieliczka", 90),
	("Wroclaw", 40),
	("Zakopane", 200),
	("Zamosc", 300)
]

vrp = VRP(cities, n_cars=5, capacity=1000, seed=123)
sol, cost = vrp.tabu_search()

print("Best solution:")
for i, route in enumerate(sol):
	print(f"Car {i+1}: {route}")

print("Total distance:", cost)

car_distances = [sum(route) for route in sol]

plt.figure(figsize=(8,4))
plt.bar(range(1, len(car_distances)+1), car_distances)
plt.xlabel("Car Number")
plt.ylabel("Distance [km]")
plt.title("Distance per car")
plt.tight_layout()
plt.show()