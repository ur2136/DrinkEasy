import pandas as pd
import json
import requests
import time

def search_method(): 
    key="AIzaSyAp3LuAtLE4jxg2Ehoprg4zeg8gggq0bZ4"

    # jazz bars
    jazz_df = pd.DataFrame()
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=jazz%20bars%20in%20Manhattan&key={key}"
    response = requests.request("GET", url, headers={}, data={})
    store = response.json()
    df_ = pd.json_normalize(store["results"])
    jazz_df = pd.concat([jazz_df, df_])

    token = response.json()["next_page_token"]
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=jazz%20bars%20in%20Manhattan&pagetoken={token}&key={key}"
    time.sleep(2)
    response = requests.request("GET", url, headers={}, data={})
    store = response.json()
    df_ = pd.json_normalize(store["results"])
    jazz_df = pd.concat([jazz_df, df_])

    token = response.json()["next_page_token"]
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=jazz%20bars%20in%20Manhattan&pagetoken={token}&key={key}"
    time.sleep(2)
    response = requests.request("GET", url, headers={}, data={})
    store = response.json()
    df_ = pd.json_normalize(store["results"])
    jazz_df = pd.concat([jazz_df, df_])

    df_handle(jazz_df)

    # sports bars
    sports_df = pd.DataFrame()
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=sports%20bars%20in%20Manhattan&key={key}"
    response = requests.request("GET", url, headers={}, data={})
    store = response.json()
    df_ = pd.json_normalize(store["results"])
    sports_df = pd.concat([sports_df, df_])

    token = response.json()["next_page_token"]
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=sports%20bars%20in%20Manhattan&pagetoken={token}&key={key}"
    time.sleep(2)
    response = requests.request("GET", url, headers={}, data={})
    store = response.json()
    df_ = pd.json_normalize(store["results"])
    sports_df = pd.concat([sports_df, df_])

    token = response.json()["next_page_token"]
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=sports%20bars%20in%20Manhattan&pagetoken={token}&key={key}"
    time.sleep(2)
    response = requests.request("GET", url, headers={}, data={})
    store = response.json()
    df_ = pd.json_normalize(store["results"])
    sports_df = pd.concat([sports_df, df_])

    df_handle(sports_df)

def df_handle(df): 
    df.set_index('place_id')
    df.drop_duplicates(subset="place_id", keep="first", inplace=True)
    df = df[df.business_status != "CLOSED_TEMPORARILY"]

    print(any(df["place_id"].duplicated()))
    result = df.to_json(orient="records")
    parsed = json.loads(result)
    with open("sports.txt", "w") as of: 
        json.dump(parsed, of)

def test(): 
    df = pd.read_json("dynamo2.json")
    print(df.reviews)
    a = list(df.reviews)
    # print(a)
    # print([len(elem) for elem in a])
    counter = 0
    for establishment in a: 
        b = list(set([review["text"] for review in establishment]))
        for review in b: 
            # print("watch" in review)
            if "food" in review: 
                counter += 1
                print(review)
        # print(b)
    print(counter)


def compare_existing_with(path): 
    # given either jazz_df or sports_df 
    # determine which ones in the data corresponds to each category 
    category_df = pd.read_json(path)
    df = pd.read_json("dynamojazz.json")
    category_place_id = set(list(category_df["place_id"]))
    place_id = set(list(df["place_id"]))
    print(category_place_id.intersection(place_id))
    print(len(category_place_id.intersection(place_id)))
    intersection = category_place_id.intersection(place_id)

    # for every element in the intersection create a column which indicates (bool)
    ingredient = []
    for i, row in df.iterrows(): 
        if row["place_id"] in intersection: 
            ingredient.append(True)
        else: 
            ingredient.append(False)
    
    # create Series and append as column 
    ingredient = pd.Series(ingredient)
    print(ingredient)
    df["sports"] = ingredient
    print(df)

    result = df.to_json(orient="records")
    parsed = json.loads(result)
    with open("dynamosports.txt", "w") as of: 
        json.dump(parsed, of)

def add_nightclub(): 
    path = "dynamosports.json"
    df = pd.read_json(path)
    ingredient = []
    for i, row in df.iterrows(): 
        if "night_club" in row["types"]: 
            ingredient.append(True)
        else: 
            ingredient.append(False)
    
    ingredient = pd.Series(ingredient)
    print(ingredient)
    df["dancing"] = ingredient
    print(df)

    result = df.to_json(orient="records")
    parsed = json.loads(result)
    with open("dynamo3.txt", "w") as of: 
        json.dump(parsed, of)

if __name__ == "__main__": 
    jp = "jazz.json"
    sp = "sports.json"
    # compare_existing_with(sp)
    add_nightclub()
