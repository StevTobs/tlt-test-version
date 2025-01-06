from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError
from utils import get_lat_lon_geopy
import pandas as pd
from tabulate import tabulate

df = pd.read_pickle("./resources/data/df_volta_org_to24.pkl")



# Example usage:
if __name__ == "__main__":
    # province = "กรุงเทพมหานคร"
    # amphoe = "เขตคลองสาน"
    # tambon = "คลองต้นไทร"
    # print("------testing------")

    # print("province = ",province)
    # print("amphoe = ",amphoe)
    # print("tambon =",tambon)
    # lat, lon = get_lat_lon_geopy(province, amphoe, tambon)
    # if lat and lon:
    #     print(f"Latitude: {lat}, Longitude: {lon}")
    # else:
    #     print("Could not retrieve coordinates.")

    print(df.head())


    # Print DataFrame using tabulate
    # print(tabulate(df.head(), headers='keys', tablefmt='psql'))
    # print(df.head().to_markdown())
    print("--------------------")

    # lat, lon = get_lat_lon_geopy(province, amphoe, tambon )
    # print(lat, lon)
