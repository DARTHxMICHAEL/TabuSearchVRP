import random
import math
import matplotlib.pyplot as plt

class VRP:
	def __init__(self, cities, n_cars=5, capacity=1000, tabu_tenure=10, iterations=200, seed=42):
		"""
		Initialize the VRP model.

		cities: list of tuples (name, demand, y, x)
		n_cars: number of available vehicles
		capacity: maximum total demand per vehicle
		tabu_tenure: number of iterations a move remains tabu
		iterations: total number of tabu search iterations
		seed: random seed for deterministic behavior
		"""
		self.cities = cities
		self.n_cars = n_cars
		self.capacity = capacity
		self.tabu_tenure = tabu_tenure
		self.iterations = iterations
		self.seed = seed

		random.seed(self.seed)

		# the first city with 0 demand is threated as a depo
		self.depot = next(c for c in cities if c[1] == 0)
		# all other with positive demand is threated as a client
		self.clients = [c for c in cities if c[1] > 0]

	def distance(self, a, b):
		"""
		Distance between two cities (euclidean).
		"""
		return math.hypot(a[2] - b[2], a[3] - b[3])

	def route_cost(self, route):
		"""
		Calculate the total distance of a single vehicle route,
		(start and end at depot).
		"""
		cost = 0
		prev = self.depot
		for c in route:
			cost += self.distance(prev, c)
			prev = c
		cost += self.distance(prev, self.depot)
		return cost

	def total_cost(self, solution):
		"""
		Calculate the total distance traveled by all vehicles.
		"""
		return sum(self.route_cost(r) for r in solution)

	def route_demand(self, route):
		"""
		Calculate the total demand served by a single route.
		"""
		return sum(c[1] for c in route)

	def initial_solution(self):
		"""
		Construct a simple initial solution.
		"""
		routes = [[] for _ in range(self.n_cars)]
		loads = [0] * self.n_cars

		for client in self.clients:
			for i in range(self.n_cars):
				if loads[i] + client[1] <= self.capacity:
					routes[i].append(client)
					loads[i] += client[1]
					break

		return routes

	def tabu_search(self):
		"""
		Run the Tabu Search algorithm to minimize
		the sum of distances traveled by all vehicles.
		"""
		current = self.initial_solution()
		best = current
		best_cost = self.total_cost(best)

		tabu = {}

		for it in range(self.iterations):
			neighbors = []

			for i in range(self.n_cars):
				for j in range(self.n_cars):
					if i == j:
						continue
					for c in current[i]:
						if self.route_demand(current[j]) + c[1] <= self.capacity:
							new = [r[:] for r in current]
							new[i].remove(c)
							new[j].append(c)
							move = (c[0], i, j)
							if move not in tabu:
								neighbors.append((new, move))

			if not neighbors:
				break

			neighbors.sort(key=lambda x: self.total_cost(x[0]))
			current, move = neighbors[0]
			cost = self.total_cost(current)

			tabu[move] = self.tabu_tenure

			for m in list(tabu):
				tabu[m] -= 1
				if tabu[m] <= 0:
					del tabu[m]

			if cost < best_cost:
				best = current
				best_cost = cost

		return best, best_cost


def visualize_solution(vrp, solution):
	"""
	Create a simple path visualizations for all cars.
	"""
	depot = vrp.depot

	plt.figure(figsize=(10, 8))

	total_distance = 0
	labeled = set()  # labeled cities

	for i, route in enumerate(solution):
		if not route:
			continue

		# depot -> route -> depot
		path = [depot] + route + [depot]

		x = [c[3] for c in path]
		y = [c[2] for c in path]

		route_distance = vrp.route_cost(route)
		total_distance += route_distance

		plt.plot(
			x, y, marker='o',
			label=f'Car {i+1} (dist={route_distance:.2f})'
		)

		# cities label
		for c in route:
			if c[0] not in labeled:
				plt.text(
					c[3], c[2], c[0],
					fontsize=8,
					ha='left',
					va='bottom'
				)
				labeled.add(c[0])

	plt.scatter(depot[3], depot[2], s=180, marker='*', color='black')
	plt.text(
		depot[3], depot[2], depot[0],
		fontsize=10,
		fontweight='bold',
		ha='right',
		va='bottom'
	)

	plt.title(
		f'VRP Solution – Total distance = {total_distance:.2f} '
		f'(~{total_distance * 111:.1f} km)'
	)
	plt.xlabel('Longitude (X)')
	plt.ylabel('Latitude (Y)')
	plt.legend()
	plt.grid(True)
	plt.tight_layout()
	plt.show()

cities = [
	#(city_name, demand, Y, X)
	("Krakow", 0, 50.0647, 19.9450),
	("Bialystok", 500, 53.1325, 23.1688),
	("Bielsko-Biala", 50, 49.8224, 19.0584),
	("Chrzanow", 400, 50.1355, 19.4021),
	("Gdansk", 200, 54.3520, 18.6466),
	("Gdynia", 100, 54.5189, 18.5305),
	("Gliwice", 40, 50.2945, 18.6714),
	("Gromnik", 200, 49.8500, 21.0833),
	("Katowice", 300, 50.2649, 19.0238),
	("Kielce", 30, 50.8661, 20.6286),
	("Krosno", 60, 49.6936, 21.7707),
	("Krynica", 50, 49.4121, 20.9597),
	("Lublin", 60, 51.2465, 22.5684),
	("Lodz", 160, 51.7592, 19.4550),
	("Malbork", 100, 54.0350, 19.0267),
	("NowyTarg", 120, 49.4775, 20.0321),
	("Olsztyn", 300, 53.7784, 20.4801),
	("Poznan", 100, 52.4064, 16.9252),
	("Pulawy", 200, 51.4178, 21.9660),
	("Radom", 100, 51.4027, 21.1471),
	("Rzeszow", 60, 50.0413, 21.9990),
	("Sandomierz", 200, 50.6820, 21.7486),
	("Szczecin", 150, 53.4285, 14.5528),
	("Szczucin", 60, 50.3500, 21.1833),
	("Szklarska-Poreba", 50, 50.8280, 15.5266),
	("Tarnow", 70, 50.0138, 20.9881),
	("Warszawa", 200, 52.2297, 21.0122),
	("Wieliczka", 90, 49.9875, 20.0642),
	("Wroclaw", 40, 51.1079, 17.0385),
	("Zakopane", 200, 49.2992, 19.9496),
	("Zamosc", 300, 50.7174, 23.2523)
]

vrp = VRP(cities, n_cars=5, capacity=1000, tabu_tenure=10, iterations=100, seed=123)

sol, cost = vrp.tabu_search()
print("Best total cost:", cost)

visualize_solution(vrp, sol)

"""
results = {}

for n in range(1, 11):
	vrp = VRP(
		cities,
		n_cars=n,
		capacity=1000,
		tabu_tenure=10,
		iterations=100,
		seed=123
	)
	_, cost = vrp.tabu_search()
	results[n] = cost
	print(f"Best total cost for {n} car: {cost:.2f}")

# arrays for visualitzation
cars = list(results.keys())
costs = list(results.values())

plt.figure(figsize=(8, 5))
plt.plot(cars, costs, marker='o')
plt.xlabel("Number of Cars")
plt.ylabel("Total Distance [degrees]")
plt.title("Total Distance vs Number of Cars")
plt.grid(True)
plt.tight_layout()
plt.show()
"""