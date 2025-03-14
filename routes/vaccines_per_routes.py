vaccines_hospitals = {
    "Hôpital Etterbeek-Ixelles": 30,
    "Clinique Saint-Jean": 20,
    "Cliniques de l'Europe": 50,
    "Edith Cavell": 40,
    "Hôpitaux iris Ziekenhuizen": 40,
    "Epsylon ASBL": 20,
    "VUB": 0,
}

locations = ['VUB', 'Hôpital Etterbeek-Ixelles', 'Hôpitaux iris Ziekenhuizen', 
             'Clinique Saint-Jean', 'VUB']

# Calculate total vaccines needed
total_vaccines = sum(vaccines_hospitals[loc] for loc in locations if loc in vaccines_hospitals)

print("Total vaccines needed:", total_vaccines)

# make a function out of this

def inital_vaccines_route(route):
    total_vaccines = sum(vaccines_hospitals[loc] for loc in route if loc in vaccines_hospitals)
    return total_vaccines

inital_vaccines_route(locations)