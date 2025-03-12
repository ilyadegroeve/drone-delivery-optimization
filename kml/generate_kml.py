from hospital_coordinates.real_coordinates import get_real_coordinates

def generate_kml(coordinates):
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
    file_path = "locations.kml"
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(kml_content)
        print(f"KML file '{file_path}' has been successfully generated.")
    except Exception as e:
        print(f"Error writing KML file: {e}")

# generate_kml(locations)

generate_kml(get_real_coordinates())
