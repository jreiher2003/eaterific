from app import app
import requests 

@app.template_filter()
def format_phone(phone):
    return "+1"+''.join(e for e in phone if e.isalnum())

@app.template_filter()
def yelp_city_filter(phone):
    API_KEY="HBzCfvnKwiYpxHuFGfqrrsvRejSpav3xe61P8_ZG7Tvj5M9vEPTL-OyN0YEOnajXvpsVMEAxYQfmTJsKfl3F5C0tn-AUDwIHvR5F812dKpGAV9zue1tFsnH7j6XPWnYx"
    headers = {
        'Authorization': 'Bearer %s' % API_KEY,
    }
    params={"phone": phone}
    r = requests.get("https://api.yelp.com/v3/businesses/search/phone", headers=headers, params=params)
    yield r.json()