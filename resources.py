vaccines_hospitals = {
    "Hôpital Etterbeek-Ixelles": 30,
    "Clinique Saint-Jean": 20,
    "Cliniques de l'Europe": 50,
    "Edith Cavell": 40,
    "Hôpitaux iris Ziekenhuizen": 40,
    "Epsylon ASBL": 20,
}


def calculate_vaccine_weight(vaccines_amount):
    return vaccines_amount * 0.00573 # kg


def new_payload_weight(hospital_name, current_payload_weight):
    current_payload_weight -= calculate_vaccine_weight(vaccines_hospitals[hospital_name])
    return current_payload_weight
