import json
import boto3
import requests
from boto3.dynamodb.conditions import Key
from datetime import datetime

# Global variables
dynamodb_handler = boto3.resource('dynamodb',endpoint_url = 'https://dynamodb.us-east-1.amazonaws.com')
table_name_1 = 'Bars'
table_name_2 = 'Times'
region = 'us-east-1'

domain_endpoint = "https://search-bars-yrxvtjgq3yv3v4qud7k7s4whx4.us-east-1.es.amazonaws.com"
index = 'bars'
full_am_url = '/'.join([domain_endpoint, index, '_search?'])

filter_params = ['zip_code', 'day', 'time', 'rating', 'price_level','category','lgbtq_friendliness', 'crowdedness_level']

def retrieve_filter_params_data(event):
    params = event['queryStringParameters']
    req_attributes = {
        'zip_code' : params['zip_code'],
        'day' : params['day'],
        'time' : params['time'],
        'rating' : params['rating'],
        'price_level' : params['price_level'],
        'category': params['category'],
        'lgbtq_friendliness': params['lgbtq'],
        'crowdedness_level': params['crowd']
    }
    return req_attributes
    
def get_all_matches(req_attributes):
    zip_code = req_attributes[filter_params[0]]
    search_params_query={
    "from" :0,
    "size" :100,
    "query" : {
        "match" :{
            'zip_code' : zip_code
        }
        }
    }
    headers = {'Content-Type': 'application/json'}

    es_response = requests.get(url = full_am_url, data = json.dumps(search_params_query), 
                                headers = headers, auth=('chandan', 'CCBD-bars21@'))

    response = json.loads(es_response.text)
    print(response)
    return response
    
    
def get_explore_matches_from_es(req_attributes):
    zip_code = req_attributes[filter_params[0]]
    rating = req_attributes[filter_params[3]]
    price_level = req_attributes[filter_params[4]]
    lgbtq = req_attributes[filter_params[6]]



    # Random places will be returned when no filter has been specified...
    search_params_query = {
        "from": 0,
        "size": 100,
        "query": {
            "bool": {
              "must": [
                {
                  "match": {
                    "zip_code": zip_code
                  }
                }

                ]
                } 
            }
            }
            
    if rating != "none":
        rating_query =  {
                     "range":{
                         "rating":
                             {
                                 "gte": rating
                             }
                     }
                  }
    else:
        rating_query =  {
                     "range":{
                         "rating":
                             {
                                 "gte": "0"
                             }
                     }
                  }
    search_params_query["query"]["bool"]["must"].append(rating_query)
        
    if price_level != "none":
        price_query = {
                        "match": {
                    "price_level": int(price_level)
                  }
                 }
    
    else:
        price_query = {
                        "range": {
                    "price_level": {
                                 "gte": 0
                             }
                  }
                 }
        
    search_params_query["query"]["bool"]["must"].append(price_query)         

    headers = {'Content-Type': 'application/json'}
    es_response = requests.get(url = full_am_url, data = json.dumps(search_params_query), 
                                headers = headers, auth=('chandan', 'CCBD-bars21@'))
    response = json.loads(es_response.text)
    print(json.dumps(search_params_query))
    print(response)
    return response
    
def collate_recommendations(matched_data, req_attributes):
    bars_table = dynamodb_handler.Table(table_name_1)
    times_table = dynamodb_handler.Table(table_name_2)
    recommendations = []
    
    for bar_hit in matched_data.get('hits').get('hits'):
        print('Inside dynam oloop')
        format = "%Y-%m-%d"
        # convert from string format to datetime format
        date = req_attributes['day']
        datetime_date = datetime.strptime(date, format)
        day_key = str(datetime_date.weekday())

        times_data = times_table.query(KeyConditionExpression = Key('place_id').eq(bar_hit.get('_id')))
        crowdedness_levels_for_day = times_data['Items'][0][day_key]
        time_index = int(req_attributes['time'])
        crowd_level = req_attributes['crowdedness_level']
        if crowd_level != 'none':  
            crowd_level = int(crowd_level)
        crowdstring = crowdedness_levels_for_day.replace(' ','')
        retrieved_crowd = int(crowdstring[time_index])
        print('input crowd: ',crowd_level)
        print('crowdstring: ',crowdstring)
        print('retrieved_crowd: ',retrieved_crowd)
        
        if (crowd_level != 'none' and crowd_level != retrieved_crowd):
            continue
        
        bar_data = bars_table.query(KeyConditionExpression = Key('place_id').eq(bar_hit.get('_id')))
        bar_id_for_photo = bar_data['Items'][0]['place_id']
        bar_name = bar_data['Items'][0]['name']
        bar_address = bar_data['Items'][0]['formatted_address']
        bar_zip_code = str(bar_data['Items'][0]['zip'])
        bar_rating = str(bar_data['Items'][0]['rating'])
        bar_price_level = str(bar_data['Items'][0]['price_level'])
        bar_phone_number = bar_data['Items'][0]['formatted_phone_number']
        bar_lgbtq_status = str(bar_data['Items'][0]['lgbtq_friendliness'])
        bar_maps_url = bar_data['Items'][0]['url']
        bar_open_hours_to_display = list(bar_data['Items'][0]['opening_hours_display'])
        bar_jazz = int(bar_data['Items'][0]['jazz'])
        bar_sports =int(bar_data['Items'][0]['sports'])
        bar_night_club = int(bar_data['Items'][0]['night_club'])
        recommendations.append({
            'Id': bar_id_for_photo,
            'Name': bar_name,
            'Address': bar_address,
            'ZipCode': bar_zip_code,
            'Rating': bar_rating,
            'PriceLevel': bar_price_level,
            'PhoneNumber': bar_phone_number,
            'LGBTQ': bar_lgbtq_status,
            'Url': bar_maps_url,
            'OpenHours': bar_open_hours_to_display,
            'Sports':bar_sports,
            'Jazz':bar_jazz,
            'NightClub': bar_night_club,
            'Crowdedness': retrieved_crowd
        })
    return recommendations
    
def lambda_handler(event, context):
    # retrieve filter data from event
    req_attributes = retrieve_filter_params_data(event)
    if req_attributes['category'] == "none":
        print("no category")
        matched_data = get_explore_matches_from_es(req_attributes)
        init_recommendations = collate_recommendations(matched_data, req_attributes)
        print('Initial: ',init_recommendations)
        
        if req_attributes["lgbtq_friendliness"] == 'true':
            recommendations =  [x for x in init_recommendations if x['LGBTQ'] =='1']
        else:
            recommendations = init_recommendations
        print('Final: ',recommendations)
    else:
        print("category")
        matched_data = get_all_matches(req_attributes)
        init_recommendations = collate_recommendations(matched_data, req_attributes)
        
        print(req_attributes["category"])
        if req_attributes["category"] == '1':
            recommendations = [x for x in init_recommendations if x['Jazz'] ==1]
            print(recommendations)
        elif req_attributes["category"] == '2':
            recommendations = [x for x in init_recommendations if x['Sports'] ==1]
        elif req_attributes["category"] == '3':
            recommendations = [x for x in init_recommendations if x['LGBTQ'] =='1']
        elif req_attributes["category"] == '4':
            recommendations = [x for x in init_recommendations if x['NightClub'] ==1]
        else:
            recommendations = init_recommendations
            
            
    print("recomm: ",recommendations)
    response =  {
        'statusCode': 200,
        'headers':{
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(recommendations)
    }
    return response