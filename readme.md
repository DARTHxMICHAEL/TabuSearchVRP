# Vehicle Routing Problem (VRP) – Tabu Search (Python)

This is a simple implementation of **Vehicle Routing Problem (VRP)** using a **Tabu Search**.  
The main objective is to optimize the assignment of cities to a fleet of vehicles in order to minimize the **total travel distance**.

Source: [DARTHxMICHAEL/TabuSearchVRP](https://github.com/DARTHxMICHAEL/TabuSearchVRP)

## Instalation and use

Dependencies:
```bash
pip install matplotlib
```

Example usage:
```
vrp = VRP(cities, n_cars=5, capacity=1000)
sol, cost = vrp.tabu_search()

print("Best solution:")
for i, route in enumerate(sol):
    print(f"Car {i+1}: {route}")

print("Total distance:", cost)
```

## Code explanation

- Cities are provided as (name, distance_from_root) tuples.

- The first city is assumed to be the root depot.

- Route cost is simplified as a round-trip distance ```cost = distance * 2```

- A random initial assignment distributes cities across the vehicles.

- Tabu Search improves the solution by swapping clients between vehicles.

- Results include: ``` Printed route solution, Total distance A bar chart showing distance per car ```

## How Tabu Search works

Tabu Search is a metaheuristic optimization method that explores different solutions while avoiding cycling back to already-tested configurations.
In the context of this VRP:

- The algorithm starts with a random initial assignment of clients to vehicles.

- At each iteration, it generates a neighborhood of new solutions by swapping clients between two vehicle routes.

- Every swap represents a move. Moves that were recently used are placed on a tabu list, preventing the algorithm from immediately undoing them.

- The search selects the best non-tabu neighbor, even if it does not immediately improve the global solution.

- Over time, tabu restrictions expire, allowing the search to revisit older moves while still exploring new combinations.

- This mechanism helps escape local minima and leads to better overall routing configurations.

Tabu Search therefore provides a balance between exploration (trying new route combinations) and memory-based control (avoiding unproductive oscillations), making it well-suited for combinatorial optimization tasks like VRP.
