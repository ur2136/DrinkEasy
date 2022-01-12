# given the place IDs from googleplaces.py stored in places.txt
# we search for the detailed data 
# and insert the results into DynamoDB
import json
import pandas as pd
import requests

KEY = "AIzaSyAp3LuAtLE4jxg2Ehoprg4zeg8gggq0bZ4"

def main(): 
    path = "places.json"
    data = pd.read_json(path)
    df = pd.DataFrame(data)
    aux = {"yelp-restaurants": []}
    
    final_df = pd.DataFrame()

    # first pull the detailed data
    for i, row in df.iterrows(): 
        place_id = row["place_id"]
        url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={KEY}"
        response = requests.request("GET", url, headers={}, data={})
        store = response.json()
        df_ = pd.json_normalize(store["result"])
        final_df = pd.concat([final_df, df_])
    
    final_df.set_index('place_id')
    result = final_df.to_json(orient="records")
    parsed = json.loads(result)
    with open("dynamo.txt", "w") as of: 
        json.dump(parsed, of)

# "opening_hours":{
#       "open_now":false,
#       "periods":[
#          {
#             "close":{
#                "day":0,
#                "time":"1530"
#             },
#             "open":{
#                "day":0,
#                "time":"1100"
#             }
#          },
#          {
#             "close":{
#                "day":0,
#                "time":"2300"
#             },
#             "open":{
#                "day":0,
#                "time":"1700"
#             }
#          },
#          {
#             "close":{
#                "day":1,
#                "time":"2300"
#             },
#             "open":{
#                "day":1,
#                "time":"1700"
#             }
#          },
#          {
#             "close":{
#                "day":2,
#                "time":"2300"
#             },
#             "open":{
#                "day":2,
#                "time":"1700"
#             }
#          },
#          {
#             "close":{
#                "day":3,
#                "time":"2300"
#             },
#             "open":{
#                "day":3,
#                "time":"1700"
#             }
#          },
#          {
#             "close":{
#                "day":4,
#                "time":"2300"
#             },
#             "open":{
#                "day":4,
#                "time":"1700"
#             }
#          },
#          {
#             "close":{
#                "day":5,
#                "time":"2300"
#             },
#             "open":{
#                "day":5,
#                "time":"1700"
#             }
#          },
#          {
#             "close":{
#                "day":6,
#                "time":"1530"
#             },
#             "open":{
#                "day":6,
#                "time":"1100"
#             }
#          },
#          {
#             "close":{
#                "day":6,
#                "time":"2300"
#             },
#             "open":{
#                "day":6,
#                "time":"1700"
#             }
#          }
#       ],
#       "weekday_text":[
#          "Monday: 5:00 – 11:00 PM",
#          "Tuesday: 5:00 – 11:00 PM",
#          "Wednesday: 5:00 – 11:00 PM",
#          "Thursday: 5:00 – 11:00 PM",
#          "Friday: 5:00 – 11:00 PM",
#          "Saturday: 11:00 AM – 3:30 PM, 5:00 – 11:00 PM",
#          "Sunday: 11:00 AM – 3:30 PM, 5:00 – 11:00 PM"
#       ]
#    },


if __name__ == "__main__": 
    main()