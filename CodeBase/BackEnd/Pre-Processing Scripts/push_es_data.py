import json
import requests

domain_endpoint = "https://search-bars-yrxvtjgq3yv3v4qud7k7s4whx4.us-east-1.es.amazonaws.com"
index = "bars"
type = "Bar"

full_am_url = '/'.join([domain_endpoint, index, type]) + "/"
headers = {'Content-Type': 'application/json'}

file = open('final_places_data.json',)
data = json.load(file)
res_data = data['Bars']

def prepare_data(bar_data):
    filtered_data = dict()
    filtered_data['place_id'] = bar_data['place_id']
    filtered_data['price_level'] = bar_data['price_level']
    filtered_data['rating'] = bar_data['rating']
    filtered_data['name'] = bar_data['name']
    filtered_data['formatted_address'] = bar_data['formatted_address']
    filtered_data['zip_code'] = bar_data['formatted_address'][-10:-5]

    return filtered_data

for idx, dict_data in enumerate(res_data):
    print(f"Pushing Datapoint {str(idx)}")
    preprocessed_data = prepare_data(dict_data)
    response = requests.put(url = full_am_url + str(dict_data['place_id']), json=preprocessed_data, headers=headers, auth=('chandan', 'CCBD-bars21@'))
    print(response)