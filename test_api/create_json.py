import requests
import json

# URL of the raw JSON data
url = "https://raw.githubusercontent.com/kongvut/thai-province-data/master/api_province_with_amphure_tambon.json"

# Fetch the data from the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON data
    provinces_data = response.json()

    # Save the JSON data to a local file
    with open('api_province_with_amphure_tambon.json', 'w', encoding='utf-8') as file:
        json.dump(provinces_data, file, ensure_ascii=False, indent=4)

    print("The provinces.json file has been created successfully.")

else:
    print("Failed to fetch data. Status code:", response.status_code)
