# Vehicle Routing Problem – Tabu Search (Python) - ENGLISH

This is a simple **Vehicle Routing Problem (VRP)** implementation using a **Tabu Search**.  
The main objective is to to minimalize the **total travel distance**.

Source: [DARTHxMICHAEL/TabuSearchVRP](https://github.com/DARTHxMICHAEL/TabuSearchVRP)

## Instalation and use

Dependencies:
```bash
pip install matplotlib
```

Example usage:
```
vrp = VRP(cities, n_cars=5, capacity=1000, tabu_tenure=10, iterations=100, seed=123)

sol, cost = vrp.tabu_search()
print("Best total cost:", cost)

visualize_solution(vrp, sol)
```

## Code explanation

- We use seed param in order to make the algorithm fully deterministic. 

- Cities are provided as (city_name, demand, Y coordinate, X coordinate) list.

- The first city with 0 demand is assumed to be depot (Kraków in this case).

- Route cost (distance) is calculated using euclidean distance formula.

- Each iteration tries to improve the initial/previous solution by memorizing the previous best results and paths.

- Graphical visualization includes path visualization and combined distance per all cars.

## How Tabu Search in VRP works

Tabu Search is a metaheuristic optimization method that explores different solutions while avoiding cycling back to recently visited configurations.

- The algorithm starts with a deterministic initial assignment of clients to vehicles.

- At each iteration, it generates a neighborhood of solutions by relocating a single client between two vehicle routes.

- Each relocation is treated as a move. Recently used moves are stored in a tabu list, making them temporarily forbidden.

- Among all non-tabu neighbors, the algorithm selects the one with the lowest total fleet distance, even if it does not improve the current global best.

- Over time, tabu restrictions expire, allowing previously forbidden moves to become available again.

- This mechanism enables the algorithm to escape local minima and continue exploring better route configurations.

## Limitations of this algorithm

- Our algorithm does not take the consideration of other factors such as travel time, fuel cost and more real life scenario aspects. 

- Distances between cities are calculated based on their coordinates, which is certainlly not exact measure of distance between them.

- The final distance is a summary since earth is an ellipsoid (distance in kilometers for one degree of longitude/latitude varies).

Prepared by Michał Kulikowski and Ania Walaszek.



<br/>

# Vehicle Routing Problem – Tabu Search (Python) - POLISH

Jest to prosta implementacja **Vehicle Routing Problem (Problemu Marszrutyzacji)** z wykorzystaniem przeszukiwania Tabu.
Głównym celem algorytmu jest minimalizacja sumy odległości pokonanej przez wszystkie samochody. Wprowadzenie danych jako parametry i 
zmiennej ziarna (uzależniającej wszelkie zmianne losowe) umożliwia odtworzenie tego algorytmu w różnych scenariuszach 
oraz porównywanie uzyskanych rezultatów.


Źródło: [DARTHxMICHAEL/TabuSearchVRP](https://github.com/DARTHxMICHAEL/TabuSearchVRP)

## Instalacja i użycie

Zależności:
```bash
pip install matplotlib
```

Przykładowe użycie:
```
vrp = VRP(cities, n_cars=5, capacity=1000, tabu_tenure=10, iterations=100, seed=123)

sol, cost = vrp.tabu_search()
print("Best total cost:", cost)

visualize_solution(vrp, sol)
```

## Charakterystyka kodu

- Używamy parametru ziarna (seed) w celu stworzenia powtarzalnego środowiska testowego.

- Lista miast dostarczona jest jako (city_name, demand, Y coordinate, X coordinate).

- Pierwsze miasto z zerowym zapotrzebowaniem traktowane jest jako magazyn (tutaj Kraków).

- Odległości między miastami liczone są jako najkrótsza odległość między punktami (metryka euklidesowa).

- Celem kolejnych iteracji jest poprawa wyniku wcześniejszych iteracji/kombinacji początkowej, co umożliwia zapamiętywanie parametrów takich 
jak dotychczasowy najlepszy wynik czy informacje o dotychczas użytych trasach.

- Graficzna wizualizacja przedstawiająca scieżki przebyte przez samochody i sumaryczny wynik.

## Jak działa algorytm poszukiwania tabu w VRP

- Poszukiwanie Tabu to metaheurystyczny algorytm przeszukujący przestrzeń potencjalnych rozwiązań zapamiętujący dotychczasowe konfiguracje.

- Poszukiwania zaczynamy od losowej konfiguracji powiązania klientów z samochodami.

- Każda kolejna iteracja generuje listę sąsiedztwa dotychczasowych rozwiązań poprzez zamianę klienta/ów miedzy samochodami.

- Każda relokacja jest traktowana jako jeden ruch. Lista ostatnich ruchów jest przechowywana w liście tabu, która tymczasowo uniemożwlia ich ponowne użycie.

- Spośród wszystkich dostępnych ruchów algorytm wybiera te z najniższą sumą dystansu floty, bez wględu na to czy poprawia to wynik globalny czy nie.

- Z czasem lista zabronionych ruchów ulega redukcji co pozwala na testowanie nowych konfiguracji.

- Dzięki temu prostemu mechanizmowi unikamy ryzyk związanych w utknięciem w minimum lokalnym.


## Ograniczenia naszego algorytmu

- Nasz algorytm nie uwzględnia czynników takich jak czas podróży, koszty paliwa czy inne aspekty prawdziwej prodróży.

- Dystans między miastami jest liczony jako linia prosta na podstawie ich współrzędnych, co nie musi być jednoznaczne z długością trasy między nimi.

- Ostateczny dystans jest przybliżeniem ponieważ ziemia jest elipsoidą (przelicznik dla 1 stopnia długości/szerokości ulega zmianie w zależności od lokalizacji)

Przygotowanie Michał Kulikowski i Ania Walaszek.
