# Drone Delivery Optimization for Vaccine Distribution

## Overview

This repository contains code for optimizing drone delivery routes for vaccine distribution to hospitals in the Brussels area. It addresses the challenge of minimizing energy consumption (Wh) during deliveries, considering factors like distance, vaccine payload, and drone battery consumption model. The project explores both direct routes and sub-route strategies to enhance delivery efficiency.

## Project Structure

The repository is organized as follows:

-   **`resources_used.py`**: Defines hospital locations (coordinates and vaccine needs), drone battery consumption model, and functions to calculate distances and energy consumption.
-   **`bruteforce_subroutes.py`**: Implements a brute-force approach to find the optimal sub-routes for vaccine delivery to minimize energy consumption.
-   **`plotting/`**: Contains scripts for visualizing delivery routes on a map.
    -   **`plot_paths.py`**: Generates plots of vaccine distribution routes, highlighting hospital locations, delivery paths, and vaccine amounts.
-   **`routes/`**: Stores optimal route information.
    -   **`route1.txt`**: Contains information about the shortest route without subroutes, and the best subroutes.
-   **`hospital_coordinates/`**: Contains different sets of coordinates for the hospitals.
    -   **`field_coordinates.py`**: Defines a set of hospital coordinates, likely for testing or simulation purposes.

## Key Components

### 1. Data Definition (`resources_used.py`)

-   **`vaccines_hospitals`**: A dictionary mapping hospital names to the number of vaccines they require.
    ```python
    vaccines_hospitals = {
        "Hôpital Etterbeek-Ixelles": 30,
        "Clinique Saint-Jean": 20,
        "Cliniques de l'Europe": 50,
        "Edith Cavell": 40,
        "Hôpitaux iris Ziekenhuizen": 40,
        "Epsylon ASBL": 20,
        "VUB": 0,  # Assuming VUB is the depot
    }
    ```
-   **`real_coordinates`**: A dictionary containing the GPS coordinates (latitude, longitude) of each hospital and the depot (VUB).
    ```python
    real_coordinates = {
        "VUB": (50.8222329, 4.3969074),
        "Edith Cavell": (50.8139343, 4.3578839),
        # ... other hospitals
    }
    ```
-   **`vaccines_current`**: A dictionary mapping the amount of vaccines to the current. This is used in calculations to estimate energy consumption.
    ```python
    vaccines_current = {0: 15.23, 1: 15.29, 2: 15.34, ..., 200: 28.48}
    ```
-   **`calculate_distance(coord1, coord2)`**: Function to calculate the Haversine distance (in km) between two GPS coordinates.
-   **`total_current(path, initial_vaccines_amount, flight_velocity)`**: Function to calculate the total energy consumption (Wh) for a given delivery route. It considers the number of vaccines, distance, flight velocity, and a predefined battery consumption model. The default `flight_velocity` is 7 km/h.
-   **`inital_vaccines_route(route)`**: Function to calculate the total vaccines needed for a route.
-   **`total_current_with_subroutes(list_of_subroutes)`**: Calculates the total energy consumption for a list of sub-routes.

### 2. Route Optimization (`bruteforce_subroutes.py`)

-   **Brute-Force Approach**: The script uses a brute-force algorithm to explore all possible combinations of sub-routes to find the one with the minimum energy consumption.
-   **Partitioning**: The `get_all_partitions` function generates all possible ways to divide the hospitals into different delivery groups (partitions).
-   **Sub-route Creation**: The `create_subroutes` function constructs actual delivery routes by adding the depot ("VUB") as the starting and ending point for each sub-route.
-   **Optimization**:  The `optimize_route` function iterates through all permutations of hospitals and partitions, calculates the total energy consumption for each combination using `total_current_with_subroutes`, and identifies the optimal sub-routes with the lowest energy consumption.

### 3. Visualization (`plotting/plot_paths.py`)

-   **Route Plotting**: The `plot_paths.py` script uses `matplotlib` to visualize the delivery routes on a map.
-   **Annotations**: Arrows indicate the direction of travel, and vaccine amounts are displayed along each path segment.
-   The script can plot a single route, or multiple subroutes, as shown in the file.

### 4. Alternate Hospital Coordinates (`hospital_coordinates/field_coordinates.py`)

-   **`field_coordinates`**: This file defines an alternative set of coordinates for the hospitals. These coordinates might represent a simplified or simulated environment, potentially used for initial testing or faster prototyping. These coordinates don't seem like real coordinates.

## Usage

1.  **Install Dependencies:**

    ```bash
    pip install matplotlib
    ```

2.  **Run Route Optimization:**

    ```bash
    python bruteforce_subroutes.py
    ```

    This script will output the best sub-routes found and their corresponding total energy consumption.  Note that due to the nature of the brute-force approach, this script may take a significant amount of time to run, especially as the number of hospitals increases.

3.  **Visualize Routes:**

    Modify the `plotting/plot_paths.py` script to reflect the desired routes.  Then, run the script:

    ```bash
    cd plotting
    python plot_paths.py
    ```

    This will generate a `vaccine_distribution_map.png` or `vaccine_distribution_map_two_paths.png` file showing the delivery routes.

## Example

The `resources_used.py` file contains an example usage:

```python
print(total_current(['VUB', 'Edith Cavell', "Cliniques de l'Europe", 'Epsylon ASBL', 'VUB'],110))
```

This calculates the total energy consumption for the route: VUB -> Edith Cavell -> Cliniques de l'Europe -> Epsylon ASBL -> VUB, starting with 110 vaccines.

## Configuration

-   **Hospital Locations and Vaccine Needs:**  Modify the `vaccines_hospitals` and `real_coordinates` dictionaries in `resources_used.py` to reflect the specific scenario.
-   **Drone Parameters:**  Adjust the `flight_velocity` parameter in the `total_current` function in `resources_used.py` to match the drone's specifications. Also, ensure the `vaccines_current` dictionary accurately represents the drone's battery consumption profile.
-   **Coordinate system:** Choose which coordinate system to use in the relevant files.

## Future Enhancements

-   **Implement more efficient optimization algorithms**: Replace the brute-force approach with more scalable algorithms like genetic algorithms, simulated annealing, or constraint programming.
-   **Consider additional constraints**: Incorporate real-world constraints such as drone battery capacity, time windows for deliveries, weather conditions, and traffic congestion.
-   **Dynamic Routing**: Implement a dynamic routing system that can adapt to changing conditions in real-time.
-   **GUI**: Develop a graphical user interface (GUI) for easy route planning and visualization.
-   **3D Visualization**: Visualize the routes in 3D for a more realistic representation.

## Notes
The `routes/route1.txt` file provides an example of a shortest route without subroutes, and an example with 2 subroutes.
```
shortest route without subroutes:
['VUB', 'Hôpital Etterbeek-Ixelles', 'Clinique Saint-Jean', 'Hôpitaux iris Ziekenhuizen', 'Edith Cavell', "Cliniques de l'Europe", 'Epsylon ASBL', 'VUB']

shortest route with 2 subroutes:

Best subroutes: [['VUB', 'Hôpital Etterbeek-Ixelles', 'Hôpitaux iris Ziekenhuizen', 'Clinique Saint-Jean', 'VUB'], ['VUB', 'Edith Cavell', "Cliniques de l'Europe", 'Epsylon ASBL', 'VUB']]
```

## License

[Choose an appropriate license, e.g., MIT License]
