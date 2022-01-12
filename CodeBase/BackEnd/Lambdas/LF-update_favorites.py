import json
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime

# Global variables
dynamodb_handler = boto3.resource('dynamodb',endpoint_url = 'https://dynamodb.us-east-1.amazonaws.com')
table_name_1 = 'Bars'
table_name_2 = 'Times'
table_name_3 = 'Favorites'
region = 'us-east-1'

domain_endpoint = "https://search-bars-yrxvtjgq3yv3v4qud7k7s4whx4.us-east-1.es.amazonaws.com"
index = 'bars'
full_am_url = '/'.join([domain_endpoint, index, '_search?'])

filter_params = ['zip_code', 'day', 'time', 'rating', 'price_level','category','lgbtq_friendliness', 'crowdedness_level']

def lambda_handler(event, context):
    client = boto3.client('dynamodb')
    favorites_table = dynamodb_handler.Table(table_name_3)
    bar_table = dynamodb_handler.Table(table_name_1)
    times_table = dynamodb_handler.Table(table_name_2)
    # read the event to retrieve place_id 
    params = event['queryStringParameters']
    recommendations = []
    if params is None:
        response = favorites_table.scan(FilterExpression= Key('fav').eq('1'))#favorites_table.query(KeyConditionExpression = Key('fav').eq('1'))
        print(response)
        place_ids = [item['place_id'] for item in response['Items']]
        for id in place_ids:
            bar_data= bar_table.query(KeyConditionExpression = Key('place_id').eq(id))
            times_data = times_table.query(KeyConditionExpression = Key('place_id').eq(id))
            today = str(datetime.today().weekday())
            print(times_data)
            crowdedness_levels_for_day = times_data['Items'][0][today]
            crowdstring = crowdedness_levels_for_day.replace(' ','')
            time_index = 21
            crowd_level = crowdstring[time_index]
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
            'Crowdedness': crowd_level
            })
            
                
        response =  {
        'statusCode': 200,
        'headers':{
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(recommendations)
        }
        return response
                       
    place_id = params['Id']
    current_value = params['isfavorite']
    current_value = int(current_value)
    value = str(current_value)
    print('v', value)
    response = client.update_item(
        TableName = 'Favorites', 
        AttributeUpdates = {
            'fav': {
            'Value': {
                'S': value
            },
            'Action': 'PUT'
            }
        },
        Key = {
            "place_id": {
                "S": place_id
            }
        }
    )
    rr = response

    response =  {
        'statusCode': 200,
        'headers':{
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps("Hello from Dynamo-Lambda!")
    }
    
    return response