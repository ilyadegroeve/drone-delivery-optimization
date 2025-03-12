import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations
from math import radians, sin, cos, sqrt, atan2

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    r = 6371  # Radius of earth in kilometers
    
    return c * r

def calculate_distance_matrix(coordinates):
    """Create a distance matrix between all locations using Haversine distance"""
    locations = list(coordinates.keys())
    n = len(locations)
    distance_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if i != j:
                lat1, lon1 = coordinates[locations[i]]
                lat2, lon2 = coordinates[locations[j]]
                distance_matrix[i, j] = haversine_distance(lat1, lon1, lat2, lon2)
    
    return distance_matrix, locations

def find_shortest_path(distance_matrix, locations, start_location="VUB"):
    """Find the shortest path that visits all locations and returns to the start"""
    n = len(locations)
    start_idx = locations.index(start_location)
    
    # We need to consider all possible permutations of locations excluding the start
    other_locations_idx = [i for i in range(n) if i != start_idx]
    
    min_distance = float('inf')
    best_path_indices = []
    
    for perm in permutations(other_locations_idx):
        # Complete path: start -> perm -> start
        path_indices = [start_idx] + list(perm) + [start_idx]
        
        # Calculate total distance for this path
        distance = sum(distance_matrix[path_indices[i], path_indices[i+1]] 
                        for i in range(len(path_indices)-1))
        
        if distance < min_distance:
            min_distance = distance
            best_path_indices = path_indices
    
    # Convert indices back to location names
    best_path = [locations[i] for i in best_path_indices]
    
    return best_path, min_distance

def plot_path(coordinates, path):
    """Plot the locations and the path between them on a map"""
    plt.figure(figsize=(10, 8))
    
    # Extract coordinates for plotting
    lats = [coordinates[loc][0] for loc in coordinates]
    lons = [coordinates[loc][1] for loc in coordinates]
    
    # Plot all locations
    plt.scatter(lons, lats, c='blue', marker='o', s=100, zorder=2)
    
    # Plot the path
    path_lats = [coordinates[loc][0] for loc in path]
    path_lons = [coordinates[loc][1] for loc in path]
    plt.plot(path_lons, path_lats, 'r-', linewidth=2, zorder=1)
    
    # Add labels for each location
    for loc, lat, lon in zip(coordinates.keys(), lats, lons):
        plt.text(lon, lat, loc, fontsize=9, ha='right', va='bottom')
    
    # Highlight starting/ending point
    plt.scatter(coordinates[path[0]][1], coordinates[path[0]][0], 
                c='green', marker='*', s=200, zorder=3)
    
    plt.title("Shortest Path Between Locations")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)
    plt.tight_layout()
    
    return plt

# Main execution
def main():
    real_coordinates = {
        "VUB": (50.8222329, 4.3969074),
        "Edith Cavell": (50.8139343, 4.3578839),
        "Cliniques de l'Europe de Bruxelles, Sainte Elisabeth": (50.8050334, 4.3686235),
        "Epsylon ASBL - Clinique Fond'Roy": (50.7861456, 4.3666663),
        "Hôpital d'Etterbeek-Ixelles": (50.8252055, 4.3787444),
        "Clinique Saint-Jean": (50.8543172, 4.3603786),
        "Hôpitaux iris Ziekenhuizen": (50.8334341, 4.3559617),
    }
    
    # Calculate distance matrix
    distance_matrix, locations = calculate_distance_matrix(real_coordinates)
    
    # Find the shortest path
    best_path, total_distance = find_shortest_path(distance_matrix, locations, "VUB")
    
    # Print results
    print("Shortest Path:")
    for i, loc in enumerate(best_path):
        if i < len(best_path) - 1:
            print(f"{loc} →", end=" ")
        else:
            print(loc)
    
    print(f"\nTotal Distance: {total_distance:.2f} km")
    
    # Plot the path
    plt = plot_path(real_coordinates, best_path)
    plt.show()

if __name__ == "__main__":
    main()
