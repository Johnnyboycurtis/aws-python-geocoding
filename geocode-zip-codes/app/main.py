import pandas as pd
import boto3
import os
import io
#from tqdm import tqdm
#tqdm.pandas()

INDEX_NAME = 'esri-demo-index'
location_client = boto3.client('location')

running_locally = os.getenv('RUNING_LOCAL')


def handler(event, context):
    start = event.get('start')
    stop = event.get('stop')
    df = load_zip_county_data()
    n = df.shape[0]
    if n < stop:
        stop = n
    print("df.loc[{}:{}]".format(start, stop))
    df = df.loc[start:stop]
    print("Dataframe size: ", df.shape)
    print("-- geocoding -- ")
    df['response'] = df.apply(geolocate, axis=1)
    print("-- getting lon and lat --")
    df['lon_lat'] = df['response'].apply(parse_results)
    print("-- Geocoding complete --")
    print(df.head())
    if running_locally:
        df.to_csv("us-zipcode-county-locations.csv")
    else:
        bucket = 'aclaimant-datascience-insights-non-prod-non-prod'
        key = 'geolocation/us-zipcode-county-locations_{}_{}.csv'.format(start, stop)
        upload_to_s3(df, bucket, key)
        print("-- results uploaded --")
    return "success :)"


def upload_to_s3(df_chunk, bucket, key):
    s3_client = boto3.client('s3')
    csv_buffer = io.StringIO()
    df_chunk.to_csv(csv_buffer, index=False)
    s3_client.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())
    print(f'file written to {bucket} --{key}')
    return True



def load_zip_county_data():
    df = pd.read_csv("county-zip-huduser.csv", dtype=str)
    print(df.head())
    return df

def geolocate(row):
    zip_code = row['zip_code']
    usps_zip_pref_city = row['usps_zip_pref_city']
    usps_zip_pref_state = row['usps_zip_pref_state']
    text = f"{zip_code}, {usps_zip_pref_city}, {usps_zip_pref_state}"
    response = location_client.search_place_index_for_text(IndexName = INDEX_NAME, Text = text)
    return response


def parse_results(response):
    try:
        #lon, lat = [-116.75641216799994, 33.033898143000044]
        lon_lat = response['Results'][0]['Place']['Geometry']['Point']
        return lon_lat
    except:
        return ''

if __name__ == "__main__":
    print("Geocoding app")
