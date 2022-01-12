from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import requests
import time
import pandas as pd
import json
from pprint import pprint

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
# The ID of a sample document.
DOCUMENT_ID = '195j9eDD3ccgjQRttHhJPymLJUCOUjs-jmwTrekvdjFE'

def main():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('docs', 'v1', credentials=creds)

    # Retrieve the documents contents from the Docs service.
    document = service.documents().get(documentId=DOCUMENT_ID).execute()

    print('The title of the document is: {}'.format(document.get('title')))


def places(): 
    # search by place ID and retain all fields
    url = "https://maps.googleapis.com/maps/api/place/details/json?place_id=ChIJ_WSvdD72wokROnegxbxj37I&key=AIzaSyAp3LuAtLE4jxg2Ehoprg4zeg8gggq0bZ4"
       
    # search by place ID and restrict results to certain fields
    # url = "https://maps.googleapis.com/maps/api/place/details/json?place_id=ChIJN1t_tDeuEmsRUsoyG83frY4&fields=name%2Crating%2Cformatted_phone_number&key=AIzaSyAp3LuAtLE4jxg2Ehoprg4zeg8gggq0bZ4"
    
    # first page of text search "bars in Manhattan"    
    # url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=bars%20in%20Manhattan&key=AIzaSyAp3LuAtLE4jxg2Ehoprg4zeg8gggq0bZ4"
    
    # next page of text search "bars in Manhattan"
    # url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=bars%20in%20Manhattan&pagetoken=Aap_uED9dF7FNLrom5eJm0PZ034ioLpfyKozLRkg-SF8CpkUwIAOtMPxzREM4vnQ7iSCbZyMObDAVkqDLdXnIC6ya8vRtwj0tbiIQUGB3Sc20Vu-kLVPw4D0YknZlBvDedZ6SiKT-GlH643tkx0ZUSimaAebvAGm25NeFrJVQScNDDkyJD4oi8BVFXMFO8v2-byDcDTjdpDnxJ-kIzaUyEDIYz_Eg7oCci5VqFfutBAGoGO8TFENtBckQ1cffYe32UmlbGGCYUzcHAn6blPgOVcgBbHS7MNg9Snc7NJbut2_hXSHM8eX80asfMuiFD7bRYxjgFXW2KZcP4kPiNfNO37H2Mrmf-uxmWX-cr2sVX3havd_ZftTK7vOiICo_nPJYsqlgALiTELujET4gqr1aLYm&key=AIzaSyAp3LuAtLE4jxg2Ehoprg4zeg8gggq0bZ4"
    # pagetoken parameter allows us to specify which result is being displayed 
    # there are 20 results displayed per page 

    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.json())

def find_1000_bars(): 
    # first page of text search "bars in Manhattan"
    key = "AIzaSyAp3LuAtLE4jxg2Ehoprg4zeg8gggq0bZ4"
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=bars%20in%20Manhattan&key={}".format(key)
    response = requests.request("GET", url, headers={}, data={})
    store = response.json()
    next_page_token = store['next_page_token']
    next_page_token = str(next_page_token)
    next_page_token = next_page_token.strip()
    print(next_page_token)
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=bars%20in%20Manhattan&key=" + key + "&pagetoken="+next_page_token
    print(url)
    url2 = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=bars%20in%20Manhattan&pagetoken=Aap_uEBZMuxhlcmxaIH1h6fCQN48-qcMTWLlEPopT_FynFbQoXENETJuMXn4F2pn676kW_888fnDUQ4u1YHJeJnxxd3DjqPSXeg9Y6KLIQQH83RwthEQLLeWaGQEt5RO57i6DkdLt_4xhXINxLxPokNxx4DTctwepWEG9t4LGfTRzQVslX4wgoVCQfj_ucNfK-bCOH8Yv43ucI63BbAl0-lpQlm_iGfVnwkaV-UQduQtIPfj0eAJ2ukzdiO1iy0BibI4nKyDJ5tB0bV4kLH_r05x0hmqdi82X3eG4VFcSWRpf9Bim5OxJHTk-8U0XGS4UxZExDBOJz8F0REeWTQGxyGmT15f9UCF1wBqEJtDFq1GyOaDI4ku5CAt1YLP5NxGFj9m6enGWPRlGakStR_FrmbI&key=AIzaSyAp3LuAtLE4jxg2Ehoprg4zeg8gggq0bZ4"

    # keep finding next page as long as there exists a next page

    counter = 0
    while "next_page_token" in store and counter < 10: 
        next_page_token = store["next_page_token"]
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=bars%20in%20Manhattan&pagetoken={}&key={}".format(next_page_token, key)
        time.sleep(2)
        response = requests.request("GET", url, headers={}, data={})
        store = response.json()
        pprint(store)
        print(store.keys())
        print(len(store["results"]))
        counter += 1

# next_page_token will only return up to 60 additional results
# must use the ZIP code method 
# since we only have 12 zip codes (to prevent duplicates)
# we also need to employ the next_page_token method
# and possibly also use night_club as the type 
def find_1000_bars_zip(): 
    # df = pd.DataFrame()
    path = "data (1).json"
    # data = json.loads(path)
    data = pd.read_json(path)
    df = pd.DataFrame(data)
    print(df.head)
    print(set(df['business_status'].values))
    df = df[df.business_status != "CLOSED_TEMPORARILY"]
    print(df.head)

    key = "AIzaSyAp3LuAtLE4jxg2Ehoprg4zeg8gggq0bZ4"
    coords = [(40.824447,-73.947673), (40.806777,-73.961267), (40.789105,-73.946986), (40.786001,-73.977814),
                (40.770412,-73.959466), (40.768322,-73.994636), (40.755069,-73.974572), (40.749102,-74.002020),
                (40.736876,-73.980047), (40.730112,-74.006826), (40.718119,-73.986397), (40.709556,-74.011633)]
    extra_coords = [(40.740121, -73.993254), (40.723181, -73.999776), (40.721131, -74.010864), (40.742110, -74.003115),
                    (40.751900, -73.983896), (40.761483, -73.967199), (40.778345, -73.947807), (40.796964, -73.943207),
                    (40.763633, -73.984097), (40.766412, -73.991019), (40.763734, -73.996633), (40.731230, -73.987436)]
    coords = coords + extra_coords # now we need to be careful for duplicates
    latitudes, longitudes = [a[0] for a in coords], [a[1] for a in coords]
    for lat, long in zip(latitudes, longitudes): 
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat}%2C{long}&radius=1000&type=night_club&key={key}"
        time.sleep(2)
        response = requests.request("GET", url, headers={}, data={})
        store = response.json()
        df_ = pd.json_normalize(store["results"])
        df = pd.concat([df, df_])

        while "next_page_token" in store: 
            next_page_token = store["next_page_token"]
            url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat}%2C{long}&radius=1000&type=bar&key={key}&pagetoken={next_page_token}"
            time.sleep(2)
            response = requests.request("GET", url, headers={}, data={})
            store = response.json()
            df_ = pd.json_normalize(store["results"])
            df = pd.concat([df, df_])
    
    df_handle(df)

def df_handle(df): 
    print(df.head)
    df.set_index('place_id')
    df.drop_duplicates(subset="place_id", keep="first", inplace=True)
    df = df[df.business_status != "CLOSED_TEMPORARILY"]

    print(any(df["place_id"].duplicated()))
    result = df.to_json(orient="records")
    parsed = json.loads(result)
    with open("places.txt", "w") as of: 
        json.dump(parsed, of)

if __name__ == '__main__':
    find_1000_bars_zip()

