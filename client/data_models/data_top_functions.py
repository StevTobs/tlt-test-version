
import pandas as pd
import numpy as np
from decimal import Decimal
import json
def near_stations(lat, lng):
    """
    Finds nearby stations based on latitude, longitude, and a distance threshold.

    Args:
        lat: Latitude of the reference point.
        lng: Longitude of the reference point.

    Returns:
        A list of dictionaries containing the names and distances of nearby stations, or None if no stations are found.
    """
    # Read the data model
    data_model = pd.read_csv("./client/data_models/ext-data-model/tlt_model.csv")

    # Ensure the required columns exist in the data model
    if not all(col in data_model.columns for col in ['lat', 'lng', 'stationName']):
        print("Data model must contain 'lat', 'lng', and 'stationName' columns.")
        return None

    # Convert latitude and longitude columns to numeric types if they are not already
    for col in ['lat', 'lng']:
        if not pd.api.types.is_numeric_dtype(data_model[col]):
            try:
                data_model[col] = pd.to_numeric(data_model[col], errors='coerce')
            except Exception as e:
                print(f"Error converting '{col}' column to numeric: {e}")
                return None
    
    # Remove rows with invalid lat/lng values
    data_model = data_model.dropna(subset=['lat', 'lng'])
    
    if data_model.empty:
        print("No valid station data found after removing invalid coordinates.")
        return None

    # Ensure lat and lng are float values
    lat = float(lat) if isinstance(lat, Decimal) else lat
    lng = float(lng) if isinstance(lng, Decimal) else lng

    # Calculate distances using the Euclidean approximation (could also use Haversine formula)
    data_model['distance'] = np.sqrt((data_model['lat'] - lat)**2 + (data_model['lng'] - lng)**2) * 111.32  # Approximate distance in km
    
    # Set a threshold distance (e.g., 10 km)
    threshold_distance = 30

    # Filter stations within the threshold distance
    nearby_stations = data_model[data_model['distance'] <= threshold_distance]

    if nearby_stations.empty:
        print("No stations found within the specified distance.")
        return None

    # Convert to list of dictionaries
    stations_list = nearby_stations.to_dict(orient='records')

    # Save the filtered stations to a CSV file
    stations_list_save = pd.DataFrame(stations_list)
    stations_list_save.to_csv("./client/data_models/ext-data-model/tlt_model_nearby.csv", index=False)

        # 1. Export the dictionary to a JSON file
    json_file_path = './client/data_models/ext-data-model/tlt_model_nearby.json'

    # Use 'w' for writing to the file
    with open(json_file_path, 'w') as json_file:
        json.dump(stations_list, json_file, indent=4)  # Use indent for pretty printing

    # print(f"Data has been written to {json_file_path}")


    # Return both the column names and the list of stations
    return {'columns': nearby_stations.columns.tolist(), 'info': stations_list}


# def location_analysis(request):
#     # Example latitude and longitude (replace with actual values or user-specific data)
#     my_lat = 14.073777
#     my_lng = 100.642301

#     # Get nearby stations based on latitude and longitude
#     result = near_stations(my_lat, my_lng)

#     # Send the result to the template
#     context = {
#         'locations': result.get('columns', []),
#         'stations': result.get('info', []),  # result['info'] contains the station data
#     }

#     return render(request, 'client/location_analysis.html', context)

if __name__ == "__main__":
    # Example usage (replace with your actual latitude and longitude)
    my_lat = 14.073777
    my_lng = 100.642301

    result = near_stations(my_lat, my_lng)
    print(result[ 'columns'])
    print(result[ 'info'])
    
    # 2. Read the JSON file back into a dictionary
    # json_file_path = './client/data_models/ext-data-model/tlt_model_nearby.json'

    # with open(json_file_path, 'r') as json_file:
    #     loaded_data = json.load(json_file)

    # print("Data loaded from JSON file:")
    # print(loaded_data[0])

    avg = []
                
    for station in result['info']:
        # Check if the 'avg_ev_num_weekly_66' value is not NaN
        avg_ev_value = station.get('avg_ev_num_weekly_66', None)
        if avg_ev_value is not None and not isinstance(avg_ev_value, str):  # Ensure it's a valid number
            avg.append(float(avg_ev_value))

    # Convert the list of averages to a numpy array
    avg = np.array(avg)

    # Filter out NaN values using numpy
    avg = avg[~np.isnan(avg)]

    # Calculate and print the average of valid numbers
    if len(avg) > 0:
        print("average: ", avg.mean())
    else:
        print("No valid data to calculate average.")
        