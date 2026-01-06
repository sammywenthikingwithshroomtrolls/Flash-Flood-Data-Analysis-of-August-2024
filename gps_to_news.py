import math

def dms_to_decimal(degrees, minutes, seconds):
    """Convert degrees, minutes, seconds to decimal degrees"""
    return degrees + (minutes / 60.0) + (seconds / 3600.0)

def parse_dms_string(dms_str):
    """Parse a DMS string into decimal degrees"""
    # Remove double quotes and get direction
    dms_str = dms_str.replace('"', '')
    direction = dms_str[-1]
    
    # Split into components
    parts = dms_str[:-1].split('°')
    degrees = float(parts[0])
    
    # Handle minutes and seconds
    min_sec = parts[1].split("'")
    minutes = float(min_sec[0])
    seconds = float(min_sec[1].strip())
    
    decimal = dms_to_decimal(degrees, minutes, seconds)
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

def format_coordinates(value, direction):
    """
    Format coordinates into degrees with cardinal directions.
    
    Args:
        value (float): The coordinate value
        direction (str): Either 'NS' for latitude or 'EW' for longitude
    
    Returns:
        str: Formatted coordinate string
    """
    if direction == 'NS':
        cardinal = 'N' if value >= 0 else 'S'
    else:
        cardinal = 'E' if value >= 0 else 'W'
    
    return f"{abs(value):.6f}°{cardinal}"

def create_encompassing_grid(coordinates):
    """
    Create a grid that encompasses all given coordinates
    
    Args:
        coordinates (list): List of dictionaries containing lat/lon in decimal degrees
    """
    # Find the extremes
    lats = [coord['lat'] for coord in coordinates]
    lons = [coord['lon'] for coord in coordinates]
    
    north = max(lats)
    south = min(lats)
    east = max(lons)
    west = min(lons)
    
    # Calculate center point
    center_lat = (north + south) / 2
    center_lon = (east + west) / 2
    
    # Calculate grid size needed (with some padding)
    lat_size = north - south
    lon_size = east - west
    grid_size = max(lat_size, lon_size) * 1.1  # Add 10% padding
    
    # Round up to nearest 0.5 degree for cleaner grid
    grid_size = math.ceil(grid_size * 2) / 2
    
    return {
        'center': {'lat': center_lat, 'lon': center_lon},
        'boundaries': {
            'north': north + (grid_size - lat_size) / 2,
            'south': south - (grid_size - lat_size) / 2,
            'east': east + (grid_size - lon_size) / 2,
            'west': west - (grid_size - lon_size) / 2
        },
        'grid_size': grid_size
    }

def print_grid_box(grid_box):
    """
    Print grid box information in a formatted way.
    
    Args:
        grid_box (dict): The grid box dictionary
    """
    print("\nGrid Box Information:")
    print("=" * 50)
    print(f"Center Point: {format_coordinates(grid_box['center']['lat'], 'NS')}, "
          f"{format_coordinates(grid_box['center']['lon'], 'EW')}")
    print("\nBoundaries:")
    print(f"North: {format_coordinates(grid_box['boundaries']['north'], 'NS')}")
    print(f"East:  {format_coordinates(grid_box['boundaries']['east'], 'EW')}")
    print(f"West:  {format_coordinates(grid_box['boundaries']['west'], 'EW')}")
    print(f"South: {format_coordinates(grid_box['boundaries']['south'], 'NS')}")
    print(f"\nGrid Size: {grid_box['grid_size']:.3f}°")
    
    # Calculate box dimensions
    lat_distance = grid_box['boundaries']['north'] - grid_box['boundaries']['south']
    lon_distance = grid_box['boundaries']['east'] - grid_box['boundaries']['west']
    print(f"Box Dimensions: {lat_distance:.3f}° × {lon_distance:.3f}°")
    
    # Approximate distances in kilometers
    lat_km = lat_distance * 111  # 1 degree latitude ≈ 111 km
    lon_km = lon_distance * 111 * math.cos(math.radians(grid_box['center']['lat']))  # Adjust for latitude
    print(f"Approximate Box Size: {lat_km:.1f} km × {lon_km:.1f} km")

# Example usage
if __name__ == "__main__":
    # Your four coordinates
    coordinate_strings = [
        ("22° 6' 16.4412'' N", "89° 58' 7.0212'' E"),
        ("20° 40' 20.856'' N", "94° 6' 7.8372'' E"),
        ("26° 23' 25.7496'' N", "93° 58' 12.918'' E"),
        ("27° 8' 9.5748'' N", "89° 29' 5.6472'' E")
    ]
    
    # Convert to decimal degrees
    coordinates = []
    print("\nConverted Coordinates:")
    print("=" * 50)
    for lat_str, lon_str in coordinate_strings:
        lat = parse_dms_string(lat_str)
        lon = parse_dms_string(lon_str)
        coordinates.append({'lat': lat, 'lon': lon})
        print(f"Original: {lat_str}, {lon_str}")
        print(f"Decimal: {lat:.6f}°N, {lon:.6f}°E\n")
    
    # Create encompassing grid
    grid_box = create_encompassing_grid(coordinates)
    print_grid_box(grid_box)
