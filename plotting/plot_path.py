import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
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

def optimize_vaccine_delivery(vaccines_hospitals, real_coordinates, initial_vaccines=200):
    """
    Find the shortest path to deliver vaccines to all hospitals, starting and ending at VUB.
    Track vaccine payload throughout the journey.
    
    Args:
        vaccines_hospitals: Dictionary mapping hospital names to vaccine amounts
        real_coordinates: Dictionary mapping hospital names to (lat, lon) coordinates
        initial_vaccines: Initial vaccine payload
    
    Returns:
        optimal_path: List of hospital names in optimal order
        total_distance: Total distance traveled in km
        vaccine_amounts: List of vaccine amounts at each step
    """
    # Create a list of all hospitals (excluding VUB which is start/end)
    hospitals = [h for h in vaccines_hospitals.keys() if h != "VUB"]
    
    # Create a distance matrix
    n = len(hospitals) + 1  # +1 for VUB
    all_locations = ["VUB"] + hospitals
    distance_matrix = np.zeros((n, n))
    
    for i, loc1 in enumerate(all_locations):
        for j, loc2 in enumerate(all_locations):
            if i != j:
                lat1, lon1 = real_coordinates[loc1]
                lat2, lon2 = real_coordinates[loc2]
                distance_matrix[i, j] = haversine_distance(lat1, lon1, lat2, lon2)
    
    # Try all permutations of hospitals (excluding VUB)
    min_distance = float('inf')
    optimal_path = None
    
    for perm in permutations(hospitals):
        # Create full path starting and ending at VUB
        path = ["VUB"] + list(perm) + ["VUB"]
        
        # Calculate total distance
        total_dist = sum(distance_matrix[all_locations.index(path[i])][all_locations.index(path[i+1])] 
                         for i in range(len(path)-1))
        
        if total_dist < min_distance:
            min_distance = total_dist
            optimal_path = path
    
    # Calculate vaccine amounts throughout the journey
    vaccine_amounts = [initial_vaccines]
    current_vaccines = initial_vaccines
    
    for hospital in optimal_path[1:-1]:  # Skip VUB at start and end
        current_vaccines -= vaccines_hospitals[hospital]
        vaccine_amounts.append(current_vaccines)
    
    # Add final amount at VUB
    vaccine_amounts.append(current_vaccines)
    
    return optimal_path, min_distance, vaccine_amounts

def plot_vaccine_route(optimal_path, vaccine_amounts, real_coordinates):
    """
    Plot the optimal route on a map with vaccine amounts labeled.
    
    Args:
        optimal_path: List of hospital names in optimal order
        vaccine_amounts: List of remaining vaccine amounts after each hospital
        real_coordinates: Dictionary mapping hospital names to (lat, lon) coordinates
    """
    plt.figure(figsize=(12, 10))
    
    # Create a graph
    G = nx.DiGraph()
    
    # Add nodes
    for hospital in optimal_path:
        G.add_node(hospital, pos=real_coordinates[hospital])
    
    # Add edges
    for i in range(len(optimal_path) - 1):
        G.add_edge(optimal_path[i], optimal_path[i+1])
    
    # Get positions
    pos = nx.get_node_attributes(G, 'pos')
    
    # Draw the graph
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='skyblue')
    nx.draw_networkx_edges(G, pos, width=2, edge_color='grey', 
                          arrowstyle='->', arrowsize=20)
    
    # Add labels with vaccine amounts
    labels = {}
    for i, hospital in enumerate(optimal_path):
        labels[hospital] = f"{hospital}\nVaccines: {vaccine_amounts[i]}"
    
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_weight='bold')
    
    # Add title with total distance
    plt.title(f"Vaccine Delivery Route (Total Distance: {min_distance:.2f} km)")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# Example usage
vaccines_hospitals = {
    "Hôpital Etterbeek-Ixelles": 30,
    "Clinique Saint-Jean": 20,
    "Cliniques de l'Europe": 50,
    "Edith Cavell": 40,
    "Hôpitaux iris Ziekenhuizen": 40,
    "Epsylon ASBL": 20,
    "VUB": 0,
}

field_coordinates = {
    "VUB": (50.9407045, 4.2108946),
    "Edith Cavell": (50.9406812, 4.2104519),
    "Cliniques de l'Europe": (50.9405649, 4.2105543),
    "Epsylon ASBL": (50.9403610, 4.2105000),
    "Hôpital Etterbeek-Ixelles": (50.9407687, 4.2107004),
    "Clinique Saint-Jean": (50.9411201, 4.2105495),
    "Hôpitaux iris Ziekenhuizen": (50.9408986, 4.2104647),
}

# Find the optimal path and plot it
optimal_path, min_distance, vaccine_amounts = optimize_vaccine_delivery(vaccines_hospitals, field_coordinates)
plot_vaccine_route(optimal_path, vaccine_amounts, field_coordinates)

print(f"Optimal path: {' -> '.join(optimal_path)}")
print(f"Total distance: {min_distance:.2f} km")
print(f"Vaccine amounts at each step: {vaccine_amounts}")