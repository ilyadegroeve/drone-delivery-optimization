import math
import matplotlib.pyplot as plt

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

def calculate_distance(coord1, coord2):
    """Calculate the Haversine distance between two GPS coordinates."""
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  
    return c * r

flight_route = ['VUB', 'Hôpital Etterbeek-Ixelles', 'Clinique Saint-Jean', 'Hôpitaux iris Ziekenhuizen', 'Edith Cavell', "Cliniques de l'Europe", 'Epsylon ASBL', 'VUB']
# (vaccine current dictionary omitted for brevity)

def total_current(path, initial_vaccines_amount=200, flight_velocity=7):  # flight_velocity in km/h
    amount_of_vaccines = initial_vaccines_amount
    list_of_vaccine_amounts = []
    list_of_current = []
    list_of_distances = []
    list_of_flight_times = []
    list_of_ah = []
    total_ah = 0

    for i in range(len(path) - 1):
        if i > 0:
            amount_of_vaccines -= vaccines_hospitals[path[i]]
        list_of_vaccine_amounts.append(amount_of_vaccines)

        distance = calculate_distance(real_coordinates[path[i]], real_coordinates[path[i+1]])
        list_of_distances.append(round(distance, 2))
        flight_time = distance / flight_velocity  
        list_of_flight_times.append(round(flight_time,2))

        current = vaccines_current.get(amount_of_vaccines, 0)
        list_of_current.append(round(current,2))

        ah = current * flight_time
        list_of_ah.append(round(ah,2))
        total_ah += ah
        total_ah = round(total_ah,2)

    total_wh = round(total_ah * 14.8)
    return total_wh

def inital_vaccines_route(route):
    total_vaccines = sum(vaccines_hospitals[loc] for loc in route if loc in vaccines_hospitals)
    return total_vaccines

l1 =  ['VUB', 'Hôpital Etterbeek-Ixelles', 'Hôpitaux iris Ziekenhuizen', 'Clinique Saint-Jean', 'VUB']
l2 =  ['VUB', 'Edith Cavell', "Cliniques de l'Europe", 'Epsylon ASBL', 'VUB']

def total_current_with_subroutes(list_of_subroutes):
    tot1_wh = 0
    for subroute in list_of_subroutes:
        tot1_wh += total_current(subroute, inital_vaccines_route(subroute))
    print(f"{len(list_of_subroutes)} subroutes total consumption: {tot1_wh} Wh")
    return tot1_wh

# --- New Code: Plotting the routes and vaccines amounts ---

def compute_vaccines_along_route(route):
    """
    Compute the remaining vaccines at each node.
    Starts with the initial vaccines (sum of all hospital vaccines along the route)
    and subtracts each hospital's vaccines upon arrival (skipping the start).
    """
    remaining = inital_vaccines_route(route)
    amounts = [remaining]
    for node in route[1:]:
        remaining -= vaccines_hospitals.get(node, 0)
        amounts.append(remaining)
    return amounts

def plot_route(route, color, label):
    """Plot a single route with node annotations for vaccine amounts."""
    coords = [real_coordinates[node] for node in route]
    # Use longitude for x-axis and latitude for y-axis
    lats = [coord[0] for coord in coords]
    lons = [coord[1] for coord in coords]
    vaccines_along = compute_vaccines_along_route(route)
    
    plt.plot(lons, lats, marker='o', color=color, label=label)
    for i, node in enumerate(route):
        plt.annotate(f"{node}\n{vaccines_along[i]} vax", 
                     (lons[i], lats[i]), 
                     textcoords="offset points", xytext=(5,5),
                     fontsize=8, color=color)

def plot_all_routes(routes):
    plt.figure(figsize=(8,6))
    colors = ['blue', 'red']
    for idx, route in enumerate(routes):
        plot_route(route, colors[idx % len(colors)], f"Route {idx+1}")
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Vaccine Delivery Routes')
    plt.legend()
    plt.grid(True)
    plt.show()

# Final routes as provided
final_routes = [
    ['VUB', 'Hôpital Etterbeek-Ixelles', 'Hôpitaux iris Ziekenhuizen', 'Clinique Saint-Jean', 'VUB'],
    ['VUB', 'Edith Cavell', "Cliniques de l'Europe", 'Epsylon ASBL', 'VUB']
]

# Plot the routes
plot_all_routes(final_routes)
