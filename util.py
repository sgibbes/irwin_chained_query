import requests
import json
import pandas as pd
import csv
from urllib.parse import urlencode


def get_token(usr, pswd):
    'https://irwinoat.doi.gov/arcgis/tokens/generateToken?'
    # get a token in order to query the endpoint

    # # token_url = 'https://irwinoat.doi.gov/arcgis/tokens/generateToken?'
    token_url = 'https://www.arcgis.com/sharing/generatetoken?expiration=120&' \
                    'referer=localhost&f=json&username={}&password={}'.format(usr, pswd)

    # token_url = 'https://irwin.doi.gov/arcgis/tokens/'
    r = requests.post(token_url,
                      data={"username": usr,
                            "password": pswd,
                            'f': 'json'})

    response = r.json()

    return response['token']


def query_api(url, token, where):

    payload = urlencode({'f': 'json',
                         'token': token,
                         'where': where,
                         'outFields': '*'})

    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Referer': 'local', "x-ig-capabilities": "36oD"}

    r = requests.post(url=url, data=payload, headers=headers)

    try:
        response = r.content.decode('utf-8')
    except UnicodeDecodeError:
        response = r.content.decode('GB18030')

    response = response.replace(r'\n', ' ').replace(r'\t', ' ').replace(r'\r', ' ').replace(r'\\', '')

    x = json.loads(response)

    return x

def response_to_dict(feature_coll, csv_file):
    # put attributes into dictionary
    attributes = []

    for f in feature_coll['features']:

        try:
            # add geometry to the attributes as a new key
            f['attributes']['geometry'] = f['geometry']

        except:
            pass

        attributes.append(f['attributes'])

    df = pd.DataFrame(attributes)
    df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=[" ", " "], regex=True, inplace=True)

    df.to_csv(csv_file)


def response_to_dict_nopd(feature_coll, csv_file):
    # put attributes into dictionary
    attributes = []
    for f in feature_coll['features']:

        try:
            # add geometry to the attributes as a new key
            f['attributes']['geometry'] = f['geometry']

        except:
            pass

        attributes.append(f['attributes'])

    csv_columns = attributes[0].keys()

    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in attributes:
                writer.writerow(data)
    except IOError:
        print("I/O error")


def get_creds():
    with open('creds.json') as f:
        usr_data = json.load(f)
    return usr_data['username'], usr_data['password']
