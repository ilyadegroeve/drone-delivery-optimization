import itertools
import matplotlib.pyplot as plt
from geopy.distance import geodesic

# Hospital coordinates
real_coordinates = {
    "VUB": (50.8222329, 4.3969074),
    "Edith Cavell": (50.8139343, 4.3578839),
    "Cliniques de l'Europe de Bruxelles, Sainte Elisabeth": (50.8050334, 4.3686235),
    "Epsylon ASBL - Clinique Fond'Roy": (50.7861456, 4.3666663),
    "Hôpital d’Etterbeek-Ixelles": (50.8252055, 4.3787444),
    "Clinique Saint-Jean": (50.8543172, 4.3603786),
    "Hôpitaux iris Ziekenhuizen": (50.8334341, 4.3559617),
}

# Function to calculate path distance
def calculate_path_distance(path):
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += geodesic(real_coordinates[path[i]], real_coordinates[path[i + 1]]).km
    return total_distance

# Generate all permutations starting and ending at VUB
hospitals = list(real_coordinates.keys())
hospitals.remove("VUB")
all_paths = [("VUB",) + perm + ("VUB",) for perm in itertools.permutations(hospitals)]

# Calculate distances for all paths
path_distances = [(path, calculate_path_distance(path)) for path in all_paths]

# Get the 5 shortest paths
shortest_paths = sorted(path_distances, key=lambda x: x[1])[:5]

# Plot the paths
plt.figure(figsize=(15, 10))
for i, (path, distance) in enumerate(shortest_paths):
    lats, lons = zip(*[real_coordinates[loc] for loc in path])
    plt.subplot(2, 3, i + 1)
    plt.plot(lons, lats, marker='o')
    for j, loc in enumerate(path):
        plt.text(lons[j], lats[j], loc, fontsize=9, ha='right')
    plt.title(f"Path {i + 1}: {distance:.2f} km")
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

plt.tight_layout()
plt.show()

shortest_paths
