import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from itertools import permutations
from math import radians, sin, cos, sqrt, atan2

def haversine_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a)) 
    r = 6371  # Earth radius in km
    return c * r

def optimize_vaccine_delivery(vaccines_hospitals, real_coordinates, initial_vaccines=200):
    hospitals = [h for h in vaccines_hospitals.keys() if h != "VUB"]
    all_locations = ["VUB"] + hospitals + ["VUB"]
    
    distance_matrix = {
        (loc1, loc2): haversine_distance(*real_coordinates[loc1], *real_coordinates[loc2])
        for loc1 in all_locations for loc2 in all_locations if loc1 != loc2
    }
    
    min_distance = float('inf')
    optimal_path = None
    
    for perm in permutations(hospitals):
        path = ["VUB"] + list(perm) + ["VUB"]
        total_dist = sum(distance_matrix[(path[i], path[i+1])] for i in range(len(path)-1))
        
        if total_dist < min_distance:
            min_distance = total_dist
            optimal_path = path
    
    return optimal_path, min_distance

def plot_vaccine_route(optimal_path, total_distance, real_coordinates):
    plt.figure(figsize=(10, 8))
    G = nx.DiGraph()
    
    for i in range(len(optimal_path) - 1):
        G.add_edge(optimal_path[i], optimal_path[i + 1])
    
    pos = {loc: real_coordinates[loc] for loc in optimal_path}
    
    nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightblue', edge_color='gray', font_size=10)
    plt.title(f"Vaccine Delivery Route (Total Distance: {total_distance:.2f} km, Time: {total_distance / 7:.2f} hrs)")
    plt.show()

vaccines_hospitals = {
    "Hôpital Etterbeek-Ixelles": 30,
    "Clinique Saint-Jean": 20,
    "Cliniques de l'Europe": 50,
    "Edith Cavell": 40,
    "Hôpitaux iris Ziekenhuizen": 40,
    "Epsylon ASBL": 20,
    "VUB": 0,
}

real_coordinates = {
    "VUB": (50.8222329, 4.3969074),
    "Edith Cavell": (50.8139343, 4.3578839),
    "Cliniques de l'Europe": (50.8050334, 4.3686235),
    "Epsylon ASBL": (50.7861456, 4.3666663),
    "Hôpital Etterbeek-Ixelles": (50.8252055, 4.3787444),
    "Clinique Saint-Jean": (50.8543172, 4.3603786),
    "Hôpitaux iris Ziekenhuizen": (50.8334341, 4.3559617),
}

optimal_path, total_distance = optimize_vaccine_delivery(vaccines_hospitals, real_coordinates)
plot_vaccine_route(optimal_path, total_distance, real_coordinates)
print(f"Total distance: {total_distance:.2f} km")
print(f"Total flight time at 7 km/h: {total_distance / 7:.2f} hours")
