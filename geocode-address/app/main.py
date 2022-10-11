import boto3
import os
import io


location_client = boto3.client('location')
INDEX_NAME = 'esri-demo-index'

running_locally = os.getenv('RUNING_LOCAL')


def lambda_handler(event, context):
    address_list = event['address_list']
    
    results = dict()
    for i, text in enumerate(address_list):
        response = geolocate(text)
        print(response)
        lon_lat = parse_lon_lat(response)
        results[i] = (text, lon_lat)
    print(results)
    return "success :)"


def geolocate(text):
    if isinstance(text, str):
        response = location_client.search_place_index_for_text(IndexName = INDEX_NAME, Text = text)
        return response
    return 'not-a-string: {}'.format(text)


def parse_lon_lat(response):
    #lon, lat = [-116.75641216799994, 33.033898143000044]
    lon_lat = response['Results'][0]['Place']['Geometry']['Point']
    return lon_lat
