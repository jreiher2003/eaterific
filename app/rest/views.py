from app import app, db
from flask import Blueprint, render_template, url_for
from sqlalchemy import desc, asc
from .models import * 

rest_blueprint = Blueprint("rest", __name__, template_folder="templates")

@rest_blueprint.route("/")
def index():
    state = State.query.all()
    return render_template("front_page/front_page_index.html",state=state)

@rest_blueprint.route("/about")
def about():
    return "this is the about page"

@app.route("/<path:url_slug_state>/<int:state_id>/")
def state_page(url_slug_state,state_id):
    county = County.query.filter_by(state_id=state_id).all()
    city_metro = City.query.filter_by(state_id=state_id, metro_area=False).order_by(desc(City.r_total)).all()
    canada = City.query.filter(City.state_id==state_id, City.county_id==None).order_by(desc(City.r_total)).all()
    state_name = State.query.filter_by(id=state_id).one()
    return render_template("state_page.html", url_slug_state=url_slug_state,state_name=state_name.name, state_id=state_id, county=county, city_metro=city_metro, canada=canada)

@app.route("/<path:url_slug_state>/<int:state_id>/<path:url_slug_city>/<int:city_id>/<int:page>")
def city_page(url_slug_state,state_id,url_slug_city,city_id, page=1):
    # rest = RestaurantLinks.query.filter_by(state_id=state_id, city_metro_id=city_metro_id).all()
    rest = Restaurant.query.filter_by(state_id=state_id, city_id=city_id).order_by(asc(Restaurant.rest_name)).paginate(page, 40, False)
    state_name = State.query.filter_by(id=state_id).one()
    city_name = City.query.filter_by(id=city_id).one()
    rest_cusine=None
    # rest_cusine = db.session.query(
    #     Cusine, Restaurant, RestaurantCusine)\
    #     .join(Restaurant)\
    #     .join(RestaurantCusine)\
    #     .filter(Cusine.id==RestaurantCusine.cusine_id)\
    #     .filter(Restaurant.id==RestaurantCusine.restaurant_id)\
    #     .filter(Restaurant.city_id==city_id, Restaurant.state_id==state_id).all()
    # for r in rest_cusine:
    #     print r.name
    # rc = Restaurant.query.filter_by(state_id=state_id, city_id=city_id).all()
    # rest_cusine1 = []      
    # for r in rc:
    #     for j in r.rlc:
    #         pass
    #     for x in r.cusine:
    #         rest_cusine1.append([x.name, x.url_slug_cusine, x.id]) 
    # k = sorted(rest_cusine1)
    # rest_cusine = [k[i] for i in range(len(k)) if i == 0 or k[i] != k[i-1]]# removes dups 
    return render_template('city_page.html', 
        url_slug_state=url_slug_state, 
        url_slug_city=url_slug_city, 
        state_name=state_name.name,
        state_id=state_id, 
        city_name=city_name.city_name, 
        city_id=city_id, 
        rest=rest, 
        rest_cusine=rest_cusine, 
        rest_total=city_name.r_total)

@app.route("/<path:url_slug_state>/<int:state_id>/<path:url_slug_city>/<int:city_id>/<path:url_slug_rest>/<path:rest_id>/")
def rest_page_city(url_slug_state, state_id, url_slug_city, city_id, url_slug_rest, rest_id):
    rest = Restaurant.query.filter_by(id=rest_id).one()
    return render_template("rest_page.html", rest=rest)

# @app.route("/r/<path:url_slug_state>/<int:state_id>/<path:url_slug_city>/<int:city_metro_id>/<path:url_slug_rest>/<path:rest_id>/")
# def rest_page_city(url_slug_state, state_id, url_slug_city, city_metro_id, url_slug_rest, rest_id):
#     rest = RestaurantLinks.query.filter_by(id=rest_id).one()
#     menu_name = Menu.query.filter_by(restaurant_links_id=rest_id).one_or_none()
#     cats = Menu.query.filter_by(restaurant_links_id=rest.id).join(RestaurantMenuCategory).join(Category).join(RestaurantMenuCategoryItem).filter(RestaurantMenuCategory.restaurant_links_id==rest.id and RestaurantMenuCategory.category_id==Category.id).all()
#     return render_template("rest_page.html", rest=rest, menu_name=menu_name, cats=cats)

# @app.route("/c/<path:url_slug_state>/<int:state_id>/<path:url_slug_city>/<int:city_metro_id>/<path:url_slug_cusine>/<path:cusine_id>/")
# def page_cusine_city(url_slug_state, state_id, url_slug_city, city_metro_id, url_slug_cusine, cusine_id):
#     rest_c = RestaurantLinks.query.filter_by(state_id=state_id, city_metro_id=city_metro_id).join(RestaurantLinksCusine).join(Cusine).filter(RestaurantLinksCusine.cusine_id == cusine_id).order_by(asc(RestaurantLinks.rest_name)).all()
#     cusine_name = Cusine.query.filter_by(id=cusine_id).one()
#     return render_template('page_cusine_city.html', rest_c=rest_c, url_slug_state=url_slug_state, state_id=state_id, url_slug_city=url_slug_city, city_metro_id=city_metro_id, url_slug_cusine=url_slug_cusine, cusine_id=cusine_id, cusine_name=cusine_name.name)

