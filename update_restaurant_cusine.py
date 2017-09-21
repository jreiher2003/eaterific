from app import app, db 
from app.rest.models import RestaurantLinks, Cusine, RestaurantLinksCusine 

def populate_rlc(_id):
    i = RestaurantLinksCusine.query.filter_by(id=_id).one()
    print i.id, i.restaurant_links_id
    rc = RestaurantLinks.query.filter_by(id=i.restaurant_links_id).one()
    # print rc.id, rc.state_id, rc.county_id, rc.city_metro_id
    i.state_id = rc.state_id
    i.county_id = rc.county_id
    i.city_metro_id = rc.city_metro_id
    # nn = RestaurantLinksCusine(state_id=rc.state_id, county_id=rc.county_id, city_metro_id=rc.city_metro_id)
    db.session.add(i)
    db.session.commit()

if __name__ == "__main__":
    for i in range(25, 3092017):#13001 
        populate_rlc(i)