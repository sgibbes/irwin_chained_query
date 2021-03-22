import util


def page_api(token, endpoint_url, where, offset):

    # use the REST api's resultOffset parameter, start at 0, increment by "offset" var, which here is 2,000
    result_offset = 0

    # create empty list to store each record
    feature_coll = {'features': []}

    # set this to True to start the while loop
    limit_exceeded = True

    itnum = 0

    while limit_exceeded:
        # can keep track of iteration number and print/log if need.
        itnum += 1

        next_batch = util.query_api(endpoint_url.format(result_offset), token, where)

        # catch any errors returned by API
        if 'error' in next_batch.keys():
            print(next_batch['error'])
            continue

        # append results to feature collection
        feature_coll['features'].extend(next_batch['features'])

        # increment result offset to get the next n records (probably 2,000)
        result_offset += offset

        # set the value for limit_exceeded
        if 'exceededTransferLimit' in next_batch.keys():
            limit_exceeded = next_batch['exceededTransferLimit']

        else:
            limit_exceeded = False

    return feature_coll
