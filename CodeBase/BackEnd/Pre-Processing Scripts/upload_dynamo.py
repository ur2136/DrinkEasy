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
    aux = {"Bars": []}
    # print(df.head)
    # data = df.head # first 5 rows
    client = boto3.client("dynamodb")
    for i, d in df.iterrows():
        print('d', d)
        storage = d["opening_hours.periods"]
        formatted_hours = []
        for e in storage: 
            formatted_hours.append("open" + str(e["open"]["day"]) + e["open"]["time"])
            if "close" in e: 
                formatted_hours.append("close" + str(e["close"]["day"]) + e["close"]["time"])
            else: # just set to equal
                formatted_hours.append("close" + str(e["open"]["day"]) + e["open"]["time"])
        if d["photos"]: 
            formatted_photos = d["photos"][0]["photo_reference"]
        else: # photos is null
            formatted_photos = "N/A"
        # formatted_hours = ["open01100", "close01530", "open01700", "close02300", ...]

        copy = {
                    "formatted_address": {"S": d["formatted_address"]},
                    "zip": {"S": d["formatted_address"][-10:-5]}, # extract ZIP
                    "formatted_phone_number": {"S": d["formatted_phone_number"]},
                    "name": {"S": d["name"]},
                    "place_id": {"S": d["place_id"]},
                    "url": {"S": d["url"]},
                    "price_level": {"N": str(d["price_level"])}, 
                    "lgbtq_friendliness": {"N": str(d["lgbtq_friendliness"])},
                    "rating": {"N": str(d["rating"])}, 
                    "types": {"SS": d["types"]},
                    "reviews": {"SS": list(set([review["text"] for review in d["reviews"]]))},
                    "opening_hours_display": {"SS": d["opening_hours.weekday_text"]},
                    "opening_hours": {"SS": formatted_hours},
                    "photos": {"S": formatted_photos},
                    "jazz": {"N": str(int(d["jazz"]))},
                    "night_club": {"N": str(int(d["dancing"]))},
                    "sports": {"N": str(int(d["sports"]))}
                }
        aux["Bars"].append({"PutRequest": {"Item": copy}})
        aux2 = [{"PutRequest": {"Item": copy}}]
        for x in batch(aux2): 
            subbatch_dict = {"Bars": x}
            response = client.batch_write_item(RequestItems=subbatch_dict)

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

if __name__ == "__main__": 
    main()