import os
import requests
from app import cache

def format_phone(phone):
    return "+1"+''.join(e for e in phone if e.isalnum())

# @cache.cached(timeout=60*60*24, key_prefix='yelp_reviews')
def yelp_reviews(_id):
    API_KEY=os.environ["YELP_API"]
    headers = {
        'Authorization': 'Bearer %s' % API_KEY,
    }
    r = requests.get("https://api.yelp.com/v3/businesses/"+_id+"/reviews", headers=headers)
    return r.json()

# @cache.cached(timeout=60*60*24, key_prefix='yelp_phone_search')
def yelp_api_phone_search(phone):
    API_KEY=os.environ["YELP_API"]
    headers = {
        'Authorization': 'Bearer %s' % API_KEY,
    }
    params={"phone": phone}
    r = requests.get("https://api.yelp.com/v3/businesses/search/phone", headers=headers, params=params)
    return r.json()
    # "+14157492060"