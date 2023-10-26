import pandas as pd
import zipfile
import os

def get_filtered_feed(path: str, output_directory: str):
    # Extract the GTFS data from the ZIP file
    with zipfile.ZipFile(path, 'r') as z:
        # Read the routes, trips, stop_times, and stops data frames
        routes = pd.read_csv(z.open('routes.txt'))
        trips = pd.read_csv(z.open('trips.txt'))
        stop_times = pd.read_csv(z.open('stop_times.txt'))
        stops = pd.read_csv(z.open('stops.txt'))
        shapes = pd.read_csv(z.open('shapes.txt'))
        pathways = pd.read_csv(z.open('pathways.txt'))

    # Filter the routes file for trams and subways
    is_tram_or_subway = routes['route_type'].isin([0, 1])
    filtered_routes = routes[is_tram_or_subway]

    # Filter trips
    route_ids = filtered_routes['route_id'].tolist()
    filtered_trips = trips[trips['route_id'].isin(route_ids)]

    # Filter stop_times
    trip_ids = filtered_trips['trip_id'].tolist()
    filtered_stop_times = stop_times[stop_times['trip_id'].isin(trip_ids)]

    # Filter stops
    stop_ids = filtered_stop_times['stop_id'].tolist()
    filtered_stops = stops[stops['stop_id'].isin(stop_ids)]

    #filter shapes
    shape_ids = filtered_trips['shape_id'].tolist()
    filtered_shapes = shapes[shapes['shape_id'].isin(shape_ids)]

    #filter pathways
    filtered_pathways = pathways[pathways['from_stop_id'].isin(stop_ids)&pathways['to_stop_id'].isin(stop_ids)]

    # Save the filtered dataframes as .txt files
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    filtered_routes.to_csv(os.path.join(output_directory, 'routes.txt'), index=False)
    filtered_trips.to_csv(os.path.join(output_directory, 'trips.txt'), index=False)
    filtered_stop_times.to_csv(os.path.join(output_directory, 'stop_times.txt'), index=False)
    filtered_stops.to_csv(os.path.join(output_directory, 'stops.txt'), index=False)
    filtered_shapes.to_csv(os.path.join(output_directory, 'shapes.txt'), index=False)
    filtered_pathways.to_csv(os.path.join(output_directory, 'pathways.txt'), index=False)

# Usage:
output_dir = "export"
get_filtered_feed("budapest_gtfs.zip", output_dir)