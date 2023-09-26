from redfin import Redfin


def get_current_price(address):
    client = Redfin()
    response = client.search(address)

    url = response['payload']['exactMatch']['url']
    initial_info = client.initial_info(url)

    property_id = initial_info['payload']['propertyId']
    mls_data = client.below_the_fold(property_id)

    listing_id = initial_info['payload']['listingId']
    avm_details = client.avm_details(property_id, listing_id)

    predict_val = avm_details['payload']['predictedValue']

    return predict_val

