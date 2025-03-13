import itertools
import math
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt

def calculate_distance(coord1, coord2):
    """Calculate the Haversine distance between two GPS coordinates."""
    # Convert latitude and longitude from degrees to radians
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

def find_shortest_path_with_recharge(coordinates, min_stops_before_recharge, restricted_before_recharge=None):
    """
    Find the shortest path visiting all hospitals with one recharge stop at VUB.
    The path must start at VUB, visit at least min_stops_before_recharge hospitals,
    return to VUB for recharging, visit remaining hospitals, and end at VUB.
    
    Args:
        coordinates: Dictionary of location names and their GPS coordinates
        min_stops_before_recharge: Minimum number of hospitals to visit before recharging
        restricted_before_recharge: List of hospitals that cannot be visited immediately before recharging
    """
    # If restricted_before_recharge is None, initialize as empty list
    if restricted_before_recharge is None:
        restricted_before_recharge = []
    
    # Extract all locations except VUB
    other_locations = [loc for loc in coordinates.keys() if loc != "VUB"]
    min_distance = float('inf')
    best_path = []
    
    # Try all possible ways to split the locations (with minimum stops constraint)
    for split_point in range(min_stops_before_recharge, len(other_locations)):
        # Try all possible permutations of the locations
        for perm in itertools.permutations(other_locations):
            # Skip if the last hospital before recharging is restricted
            if perm[split_point-1] in restricted_before_recharge:
                continue
                
            # Split the permutation at the current split point
            first_part = perm[:split_point]
            second_part = perm[split_point:]
            
            # Complete path: VUB -> first_part -> VUB (recharge) -> second_part -> VUB
            path = ["VUB"] + list(first_part) + ["VUB"] + list(second_part) + ["VUB"]
            
            # Calculate total distance for this path
            total_distance = 0
            for i in range(len(path) - 1):
                total_distance += calculate_distance(
                    coordinates[path[i]], 
                    coordinates[path[i + 1]]
                )
            
            # Update if this path is shorter
            if total_distance < min_distance:
                min_distance = total_distance
                best_path = path
    
    return best_path, min_distance

def plot_path_on_map(coordinates, path):
    """
    Plot the shortest path on a map with numbered subpaths and highlighting the recharge stop.
    
    Args:
        coordinates: Dictionary of location names and their GPS coordinates (lat, lon)
        path: List of location names representing the shortest path
    """
    # Create a figure with a map projection
    plt.figure(figsize=(12, 10))
    
    # Use OpenStreetMap for the background
    osm_tiles = cimgt.OSM()
    ax = plt.axes(projection=osm_tiles.crs)
    
    # Determine map boundaries
    lats = [coord[0] for coord in coordinates.values()]
    lons = [coord[1] for coord in coordinates.values()]
    min_lat, max_lat = min(lats) - 0.01, max(lats) + 0.01
    min_lon, max_lon = min(lons) - 0.01, max(lons) + 0.01
    ax.set_extent([min_lon, max_lon, min_lat, max_lat], crs=ccrs.Geodetic())
    
    # Add the map tiles to the plot
    ax.add_image(osm_tiles, 14)  # Zoom level 14
    
    # Find the recharge stop index (the second occurrence of VUB)
    recharge_index = path[1:].index("VUB") + 1
    
    # Plot each location
    for name, (lat, lon) in coordinates.items():
        marker = 'o'
        color = 'blue'
        markersize = 10
        
        if name == "VUB":
            marker = '*'
            color = 'red'
            markersize = 15
            
        ax.plot(lon, lat, marker=marker, color=color, markersize=markersize, 
                transform=ccrs.Geodetic())
        
        if name == "VUB":
            # Add a label for VUB with special indication for start/recharge/end
            occurrences = [i for i, x in enumerate(path) if x == "VUB"]
            label = "VUB (Start/Recharge/End)"
        else:
            label = name
            
        ax.text(lon, lat, label, fontsize=9, transform=ccrs.Geodetic(),
                bbox=dict(facecolor='white', alpha=0.7))
    
    # Plot the path with numbered subpaths
    for i in range(len(path) - 1):
        # Get coordinates for the current segment
        start_name = path[i]
        end_name = path[i + 1]
        start_coords = coordinates[start_name]
        end_coords = coordinates[end_name]
        
        # Use different line styles for before/after recharge
        if i < recharge_index:
            linestyle = '-'  # Solid line before recharge
            color = 'green'
        elif i == recharge_index:
            linestyle = '--'  # Dashed line for the recharge segment
            color = 'orange'
        else:
            linestyle = '-.'  # Dash-dot line after recharge
            color = 'purple'
        
        # Draw line segment between points
        ax.plot([start_coords[1], end_coords[1]], 
                [start_coords[0], end_coords[0]],
                color=color, linewidth=2, linestyle=linestyle, transform=ccrs.Geodetic())
        
        # Calculate midpoint for placing the segment number
        mid_lon = (start_coords[1] + end_coords[1]) / 2
        mid_lat = (start_coords[0] + end_coords[0]) / 2
        
        # Add a number label for the segment
        ax.text(mid_lon, mid_lat, str(i+1), fontsize=12, fontweight='bold',
                bbox=dict(facecolor='yellow', alpha=0.7),
                transform=ccrs.Geodetic(), ha='center', va='center')
    
    # Create a legend for the line styles
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='green', lw=2, linestyle='-', label='Before Recharge'),
        Line2D([0], [0], color='orange', lw=2, linestyle='--', label='Recharge Trip'),
        Line2D([0], [0], color='purple', lw=2, linestyle='-.', label='After Recharge')
    ]
    ax.legend(handles=legend_elements, loc='lower left')
    
    # Title and additional information
    recharge_segment = recharge_index + 1
    plt.title(f"Shortest Path Between Hospitals with Recharge at VUB (Segment {recharge_segment})")
    plt.tight_layout()
    
    return plt

def generate_text_report(coordinates, path):
    """Generate a detailed text report of the path."""
    # Find the recharge point
    recharge_index = path[1:].index("VUB") + 1
    
    report = "Shortest Path With Recharge Report\n"
    report += "=" * 40 + "\n\n"
    
    # Calculate phase distances and list stops
    phase1_distance = 0
    phase2_distance = 0
    
    report += "Phase 1 (Before Recharge):\n"
    report += f"  Starting point: {path[0]}\n"
    report += "  Hospitals visited:\n"
    
    for i in range(1, recharge_index):
        report += f"    {i}. {path[i]}\n"
        
    report += f"  Return to: {path[recharge_index]} (for recharge)\n\n"
    
    report += "Phase 2 (After Recharge):\n"
    report += f"  Starting point: {path[recharge_index]}\n"
    report += "  Hospitals visited:\n"
    
    for i in range(recharge_index + 1, len(path) - 1):
        report += f"    {i-recharge_index}. {path[i]}\n"
        
    report += f"  Return to: {path[-1]}\n\n"
    
    # Segment details
    report += "Segment Details:\n"
    total_distance = 0
    
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i + 1]
        distance = calculate_distance(coordinates[start], coordinates[end])
        total_distance += distance
        
        phase_marker = ""
        if i == recharge_index:
            phase_marker = " (RECHARGE)"
        
        report += f"  {i+1}. {start} -> {end}: {distance:.2f} km{phase_marker}\n"
        
        # Add to appropriate phase total
        if i < recharge_index:
            phase1_distance += distance
        elif i == recharge_index:
            # The recharge segment belongs to phase 1
            phase1_distance += distance
        else:
            phase2_distance += distance
    
    # Summary
    report += "\nSummary:\n"
    report += f"  Phase 1 distance: {phase1_distance:.2f} km\n"
    report += f"  Phase 2 distance: {phase2_distance:.2f} km\n"
    report += f"  Total distance: {total_distance:.2f} km\n"
    
    return report

# Hospital coordinates
real_coordinates = {
    "VUB": (50.8222329, 4.3969074),
    "Edith Cavell": (50.8139343, 4.3578839),
    "Cliniques de l'Europe de Bruxelles, Sainte Elisabeth": (50.8050334, 4.3686235),
    "Epsylon ASBL - Clinique Fond'Roy": (50.7861456, 4.3666663),
    "Hôpital d'Etterbeek-Ixelles": (50.8252055, 4.3787444),
    "Clinique Saint-Jean": (50.8543172, 4.3603786),
    "Hôpitaux iris Ziekenhuizen": (50.8334341, 4.3559617),
}

def main():
    # Get user input for minimum stops before recharging
    while True:
        try:
            min_stops = int(input("How many hospitals to visit before recharging at VUB? (minimum 2): "))
            if min_stops < 2:
                print("Error: You must visit at least 2 hospitals before recharging.")
            elif min_stops > len(real_coordinates) - 1:
                print(f"Error: There are only {len(real_coordinates) - 1} hospitals besides VUB.")
            else:
                break
        except ValueError:
            print("Please enter a valid number.")
    
    # Define hospitals that cannot be visited immediately before recharging
    restricted_before_recharge = ["Hôpital d'Etterbeek-Ixelles"]
    print(f"\nFinding shortest path with {min_stops} stops before recharging...")
    print(f"Constraint: Cannot return to VUB for recharging from {', '.join(restricted_before_recharge)}")
    
    # Find the shortest path with recharge
    shortest_path, total_distance = find_shortest_path_with_recharge(
        real_coordinates, 
        min_stops,
        restricted_before_recharge
    )
    
    # Print basic results
    print("\nShortest Path with Recharge Stop:")
    print(" -> ".join(shortest_path))
    print(f"Total Distance: {total_distance:.2f} km\n")
    
    # Generate and print detailed report
    report = generate_text_report(real_coordinates, shortest_path)
    print(report)
    
    # Plot the path
    plot = plot_path_on_map(real_coordinates, shortest_path)
    plt.savefig('shortest_path_with_recharge.png', dpi=300, bbox_inches='tight')
    print("\nMap saved as 'shortest_path_with_recharge.png'")
    plt.show()

if __name__ == "__main__":
    main()3