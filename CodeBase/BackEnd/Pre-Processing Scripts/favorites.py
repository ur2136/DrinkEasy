# given the place IDs from googleplaces.py stored in places.txt
# we search for the detailed data 
# and insert the results into DynamoDB
import json
import pandas as pd
import requests
import boto3

KEY = "AIzaSyAp3LuAtLE4jxg2Ehoprg4zeg8gggq0bZ4"

def main(): 
    path = "dynamo3.json"
    data = pd.read_json(path)
    df = pd.DataFrame(data)
    client = boto3.client("dynamodb")
    
    for i, d in df.iterrows():
        print('d', d)
        copy = {
                    "place_id": {"S": d["place_id"]},
                    "fav": {"S": str(0)} # boolean false 
                }

        aux2 = [{"PutRequest": {"Item": copy}}]
        for x in batch(aux2): 
            subbatch_dict = {"Favorites": x}
            response = client.batch_write_item(RequestItems=subbatch_dict)

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

if __name__ == "__main__": 
    main()