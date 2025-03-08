# Coordinates for the locations
coordinates_data = {
    "VUB": (50.9407045, 4.2108946),
    "Edith Cavell": (50.9406812, 4.2104519),
    "Cliniques de l'Europe": (50.9405649, 4.2105543),
    "Epsylon ASBL": (50.9403610, 4.2105000),
    "Hôpital Etterbeek-Ixelles": (50.9407687, 4.2107004),
    "Clinique Saint-Jean": (50.9411201, 4.2105495),
    "Hôpitaux iris Ziekenhuizen": (50.9408986, 4.2104647),
}

# Create the KML content
kml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
'''

# Add placemarks for each location
for name, (lat, lon) in coordinates.items():
    kml_content += f'''
    <Placemark>
      <name>{name}</name>
      <Point>
        <coordinates>{lon},{lat},0</coordinates>
      </Point>
    </Placemark>
'''

# Close the KML document
kml_content += '''
  </Document>
</kml>
'''

# Write the KML content to a file