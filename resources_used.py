import math


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

vaccines_current = {0: 15.23, 1: 15.29, 2: 15.34, 3: 15.4, 4: 15.46, 5: 15.52, 6: 15.58, 7: 15.63, 8: 15.69, 9: 15.75, 10: 15.81, 11: 15.87, 12: 15.92, 13: 15.98, 14: 16.04, 15: 16.1, 16: 16.16, 17: 16.21, 18: 16.27, 19: 16.33, 20: 16.39, 21: 16.45, 22: 16.5, 23: 16.56, 24: 16.62, 25: 16.68, 26: 16.74, 27: 16.79, 28: 16.85, 29: 16.91, 30: 16.97, 31: 17.03, 32: 17.08, 33: 17.14, 34: 17.2, 35: 17.26, 36: 17.32, 37: 17.37, 38: 17.43, 39: 17.49, 40: 17.55, 41: 17.61, 42: 17.66, 43: 17.72, 44: 17.78, 45: 17.84, 46: 17.9, 47: 17.95, 48: 18.01, 49: 18.07, 50: 18.13, 51: 18.19, 52: 18.24, 53: 18.3, 54: 18.36, 55: 18.42, 56: 18.48, 57: 18.53, 58: 18.59, 59: 18.65, 60: 18.71, 61: 18.77, 62: 18.82, 63: 18.88, 64: 18.95, 65: 19.02, 66: 19.09, 67: 19.15, 68: 19.22, 69: 19.29, 70: 19.36, 71: 19.42, 72: 19.49, 73: 19.56, 74: 19.63, 75: 19.69, 76: 19.76, 77: 19.83, 78: 19.9, 79: 19.96, 80: 20.03, 81: 20.1, 82: 20.17, 83: 20.23, 84: 20.3, 85: 20.37, 86: 20.44, 87: 20.51, 88: 20.57, 89: 20.64, 90: 20.71, 91: 20.78, 92: 20.84, 93: 20.91, 94: 20.98, 95: 21.05, 96: 21.11, 97: 21.18, 98: 21.25, 99: 21.32, 100: 21.38, 101: 21.45, 102: 21.52, 103: 21.59, 104: 21.65, 105: 21.72, 106: 21.79, 107: 21.86, 108: 21.92, 109: 21.99, 110: 22.06, 111: 22.13, 112: 22.2, 113: 22.26, 114: 22.33, 115: 22.4, 116: 22.47, 117: 22.53, 118: 22.6, 119: 22.67, 120: 22.74, 121: 22.8, 122: 22.87, 123: 22.94, 124: 23.01, 125: 23.07, 126: 23.14, 127: 23.21, 128: 23.28, 129: 23.34, 130: 23.41, 131: 23.48, 132: 23.55, 133: 23.61, 134: 23.68, 135: 23.75, 136: 23.82, 137: 23.89, 138: 23.95, 139: 24.02, 140: 24.09, 141: 24.16, 142: 24.22, 143: 24.3, 144: 24.37, 145: 24.44, 146: 24.52, 147: 24.59, 148: 24.66, 149: 24.74, 150: 24.81, 151: 24.89, 152: 24.96, 153: 25.03, 154: 25.11, 155: 25.18, 156: 25.25, 157: 25.33, 158: 25.4, 159: 25.48, 160: 25.55, 161: 25.62, 162: 25.7, 163: 25.77, 164: 25.84, 165: 25.92, 166: 25.99, 167: 26.07, 168: 26.14, 169: 26.21, 170: 26.29, 171: 26.36, 172: 26.44, 173: 26.51, 174: 26.58, 175: 26.66, 176: 26.73, 177: 26.8, 178: 26.88, 179: 26.95, 180: 27.03, 181: 27.1, 182: 27.17, 183: 27.25, 184: 27.32, 185: 27.39, 186: 27.47, 187: 27.54, 188: 27.62, 189: 27.69, 190: 27.76, 191: 27.84, 192: 27.91, 193: 27.98, 194: 28.06, 195: 28.13, 196: 28.21, 197: 28.28, 198: 28.34, 199: 28.41, 200: 28.48}




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
    

    print("Vaccine amounts:", list_of_vaccine_amounts)
    # print("List of current:", list_of_current)
    # print("List of distances:", list_of_distances)
    # print("List of flight times (hours):", list_of_flight_times)
    # print("List of Ah:", list_of_ah)
    # print(f"Total distance: {round(sum(list_of_distances))} km")

    # print(f"Total Ah: {total_ah} Ah")
    # print(f"Total Wh: {round(total_ah * 14.8, 3)} Wh")


    return total_wh

def inital_vaccines_route(route):
    total_vaccines = sum(vaccines_hospitals[loc] for loc in route if loc in vaccines_hospitals)
    return total_vaccines


def total_current_with_subroutes(list_of_subroutes):
    tot1_wh = 0
    
    for subroute in list_of_subroutes:
        tot1_wh += total_current(subroute, inital_vaccines_route(subroute))
    print(f"{len(list_of_subroutes)} subroutes total consumption: {tot1_wh} Wh")
    return tot1_wh

print(total_current(['VUB', 'Edith Cavell', "Cliniques de l'Europe", 'Epsylon ASBL', 'VUB'],110))