
import pandas as pd
import numpy as np
from decimal import Decimal
from client.models import CalcostAc 
import json

def reset_db():

    # Save data to the database
    costtotal_addon = CalcostAc()
    costtotal_addon.cal_costtotal_addon = 0
    costtotal_addon.costtotal = 0
    costtotal_addon.addon_total = 0
    costtotal_addon.numev = 0
    costtotal_addon.size_tr = 0
    costtotal_addon.disthvtotr = 0
    costtotal_addon.packageadd = 0
    costtotal_addon.distrtomdb = 0
    costtotal_addon.distmdbtoev = 0
    costtotal_addon.price_ev_7kw = 0
    costtotal_addon.roi = 0
    costtotal_addon.cap_kwh_thb = 3.7
    costtotal_addon.sell_kwh_thb = 6.5
    costtotal_addon.save()

def near_stations(lat, lng):
    
    # reset_db()
    data_model = pd.read_csv("./client/data_models/ext-data-model/tlt_model.csv")

    if not all(col in data_model.columns for col in ['lat', 'lng', 'stationName']):
        print("Data model must contain 'lat', 'lng', and 'stationName' columns.")
        return None

    for col in ['lat', 'lng']:
        if not pd.api.types.is_numeric_dtype(data_model[col]):
            try:
                data_model[col] = pd.to_numeric(data_model[col], errors='coerce')
            except Exception as e:
                print(f"Error converting '{col}' column to numeric: {e}")
                return None
    
    data_model = data_model.dropna(subset=['lat', 'lng'])
    
    if data_model.empty:
        print("No valid station data found after removing invalid coordinates.")
        return None

    lat = float(lat) if isinstance(lat, Decimal) else lat
    lng = float(lng) if isinstance(lng, Decimal) else lng

    data_model['distance'] = np.sqrt((data_model['lat'] - lat)**2 + (data_model['lng'] - lng)**2) * 111.32  # Approximate distance in km
    
    # Set a threshold distance (e.g., 50 km)
    threshold_distance = 50

    nearby_stations = data_model[data_model['distance'] <= threshold_distance]

    if nearby_stations.empty:
        print("No stations found within the specified distance.")
        return None

    

    stations_list = nearby_stations.to_dict(orient='records')

        # Sort stations by distance (ascending order)
    nearby_stations = nearby_stations.sort_values(by='distance')


    # Select the top 3 nearest stations
    tops_stations = nearby_stations.head(6)


    # Assuming calculation of averages from available data for the top 3
    num_ev_avg = tops_stations['avg_ev_num_weekly_66'].max() if 'avg_ev_num_weekly_66' in tops_stations else np.nan
    num_res_ev_avg = tops_stations['avg_res_ev_num_weekly_66'].max() if 'avg_res_ev_num_weekly_66' in tops_stations else np.nan
    num_tra_ev_avg = tops_stations['avg_trav_ev_num_weekly_66'].max() if 'avg_trav_ev_num_weekly_66' in tops_stations else np.nan

    kwh_ev_avg = tops_stations['avg_kwh'].max() if 'avg_kwh' in tops_stations else np.nan
    hr_ev_avg = tops_stations['avg_hr'].max() if 'avg_hr' in tops_stations else np.nan
    kwh_ev_avg = float(kwh_ev_avg)
    hr_ev_avg  = float(hr_ev_avg )


    cost_total_data = CalcostAc.objects.last()
 
    thb_cap = 3.7
    thb_sell = 6.5

    thb_margin = thb_sell - thb_cap 
    week_income_app = kwh_ev_avg * thb_sell
    week_income_app = "{:,.0f}".format(week_income_app) 
    month_income_app = "{:,.0f}".format(kwh_ev_avg * thb_sell * 4) 
    year_income_app = "{:,.0f}".format(kwh_ev_avg * thb_sell * 4 * 12) 

    week_bene_app = kwh_ev_avg * thb_margin
    week_bene_app = "{:,.0f}".format(week_bene_app) 
    month_bene_app = "{:,.0f}".format(kwh_ev_avg * thb_margin * 4) 
    year_bene_app = "{:,.0f}".format(kwh_ev_avg * thb_margin * 4 * 12) 

    # Return both the column names and the list of stations
    return {'columns': nearby_stations.columns.tolist(), 
                    'info': stations_list, 
                    'num_ev_avg': num_ev_avg, 
                    'num_res_ev_avg': num_res_ev_avg,
                    'num_tra_ev_avg': num_tra_ev_avg,
                    'kwh_ev_avg':kwh_ev_avg,
                    'hr_ev_avg':hr_ev_avg,
                    'week_income_app':week_income_app,
                    'month_income_app':month_income_app,
                    'year_income_app': year_income_app,
                    'week_bene_app':week_bene_app,
                    'month_bene_app':month_bene_app,
                    'year_bene_app':year_bene_app}

if __name__ == "__main__":
    # Example usage (replace with your actual latitude and longitude)
    my_lat = 14.073777
    my_lng = 100.642301

    result = near_stations(my_lat, my_lng)
    print(result[ 'columns'])
    # print(result[ 'info'])
