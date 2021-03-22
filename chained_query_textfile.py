import util
import page_api
'''
Chains together multiple queries of IRWIN's hosted features services:
Start with a list of IrwinCRIDs, result in Resources on those requests
1. Query capability request using IrwinCRID from text file
2. Query resource capability table using IrwinCID
3. Query resource table using IrwinRID
'''


# reads credentials file
username = util.get_creds()[0]
password = util.get_creds()[1]

# get token
token = util.get_token(username, password)

# capability request table
capabilityrequest_url = 'https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/IRWIN_Resources/FeatureServer' \
                        '/5/query?resultOffset={}'

# result offset is the number of records to increment by each time. This matches AGOL limits
offset = 2000

# set up container for final list of data
feature_coll = {'features': []}

# open text file and loop through IrwinCRIDs
with open('irwincrid_list.txt') as thefile:
    for l in thefile:
        # strip out new line character
        irwincrid = l.strip('\n')

        # the where clause to narrow down results. Use to query the
        nested_where_1 = "IrwinCRID = '{}'".format(irwincrid)

        # return all results in a list of dictionaries
        first_result_features = page_api.page_api(token, capabilityrequest_url, nested_where_1, offset)

        # loop through irwin ids and query another table
        for f in first_result_features['features']:

            irwincid = f['attributes']['IrwinCID']

            if irwincid:

                resourcecapability_url = 'https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/IRWIN_Resources/FeatureServer' \
                               '/2/query?resultOffset={}'

                nested_where_2 = "IrwinCID = '{}'".format(irwincid)

                # return all results in a list of dictionaries
                second_result_features = page_api.page_api(token, resourcecapability_url, nested_where_2, offset)

                for f2 in second_result_features['features']:

                    irwinrid = f2['attributes']['IrwinRID']

                    resource_url = 'https://services1.arcgis.com/Hp6G80Pky0om7QvQ/arcgis/rest/services/IRWIN_Resources/FeatureServer' \
                                             '/0/query?resultOffset={}'

                    nested_where_3 = "IrwinRID = '{}'".format(irwinrid)

                    # return all results in a list of dictionaries
                    third_result_features = page_api.page_api(token, resource_url, nested_where_3, offset)

                    # append results to feature collection
                    feature_coll['features'].extend(third_result_features['features'])

# write the feature collection to a csv file
csv_file = 'test.csv'
util.response_to_dict_nopd(feature_coll, csv_file)
