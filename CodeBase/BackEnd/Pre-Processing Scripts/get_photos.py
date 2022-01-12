import json
import requests

file = open('final_places_data.json',)
data = json.load(file)
res_data = data['Bars']

for r_data in res_data:
    id = r_data['place_id']
    photos = r_data['photos']
    if photos is None or len(photos) == 0:
        continue
    photo_ref = photos[0]['photo_reference']
    request_query = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={photo_ref}&key=AIzaSyCltBNlR7imXi2UuZujzDUfR6LfqvsM6z8"
    response = requests.request("GET", request_query, headers={}, data={})
    with open(f"./photos/{id}.png", 'wb+') as image_file:
        for data in response:
            image_file.write(data)