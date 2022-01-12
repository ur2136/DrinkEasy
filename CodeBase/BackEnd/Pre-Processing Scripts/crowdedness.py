# given the place IDs from googleplaces.py stored in dynamo3.json
# we get the crowdedness levels for each time bucket (7 days a week, 24 hours each day)
# and insert the results into DynamoDB
import pandas as pd
import boto3
import random
import numpy as np
from pprint import pprint
import requests

# each place_id will have 7 columns corresponding to the 7 days of the week
# each day will have 24 integer values stored in them
# 0 if closed, 1 to 5 otherwise 
def main(): 
    path = "dynamo3.json"
    data = pd.read_json(path)
    df = pd.DataFrame(data)

    client = boto3.client("dynamodb")
    for i, d in df.iterrows():
        storage = d["opening_hours.periods"]
        storage = sorted(storage, key=lambda x: (x["open"]["day"]-1) % 7)
        formatted_hours = []
        twenty_four_seven_table = [[False for j in range(24)] for i in range(7)] # Monday to Sunday
        for e in storage: 
            if "close" not in e: # [{'open': {'day': 0, 'time': '0000'}}], i.e. open 24/7
                twenty_four_seven_table = [[True for j in range(24)] for i in range(7)]
                break 
            else: 
                open_day = (e["open"]["day"]-1) % 7
                open_time = e["open"]["time"][:2] # keep only the hour
                close_day = (e["close"]["day"]-1) % 7
                close_time = e["close"]["time"][:2] # keep only the hour
                # we keep only the hours because of the 1-hour bucket system
                # we don't support granularity anyway
                # modify times in e[open_day] and e[close_day] as necessary 
                if open_day == close_day: # close and open in the same day so just modify one
                    for time in range(int(open_time), int(close_time)): 
                        twenty_four_seven_table[open_day][time] = True # must insert value later
                else: # open today and close tomorrow so modify both 
                    for time in range(int(open_time), 24): 
                        twenty_four_seven_table[open_day][time] = True
                    for time in range(0, int(close_time)): 
                        twenty_four_seven_table[close_day][time] = True

        # false must be converted to 0 and true must be converted to some crowdedness value
        result = convert(d["place_id"], twenty_four_seven_table)
        # pprint(result)
        copy = {
            "place_id": {"S": d["place_id"]},
            "0": {"S": result[0]}, 
            "1": {"S": result[1]}, 
            "2": {"S": result[2]}, 
            "3": {"S": result[3]}, 
            "4": {"S": result[4]}, 
            "5": {"S": result[5]}, 
            "6": {"S": result[6]}
        } 

        # 7 columns and 24 elements each (but single string separated by spaces) approach
        # 0 is Monday 6 is Sunday 
        aux2 = [{"PutRequest": {"Item": copy}}]
        for x in batch(aux2): 
            subbatch_dict = {"Times": x}
            response = client.batch_write_item(RequestItems=subbatch_dict)

def convert(place_id, table): 
    for day in range(0, 7): 
        for hour in range(0, 24): 
            if table[day][hour] == False: 
                table[day][hour] = 0 
            else: 
                table[day][hour] = get_crowdedness(place_id, day, hour)
    return [" ".join([str(e) for e in t]) for t in table]

# return integer in {1, 2, 3, 4, 5} depending on day and hour 
def get_crowdedness(place_id, day, hour): 
    url = "https://besttime.app/api/v1/forecasts/busy"

    params = {
        'api_key_public': 'pub_e11661721b084d36b8f469a2c012e754',
        'venue_id': place_id,
        'day_step': day,
        'hour_step': hour
    }

    response = requests.request("GET", url, params=params)
    data = response.json().analysis
    crowdedness = int(data.busy_hours.info.hour_rank)
    return crowdedness
    
def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

if __name__ == "__main__": 
    main()