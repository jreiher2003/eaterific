# -*- coding: utf-8 -*-
from app import app, db
from flask import Blueprint, render_template, url_for, request, redirect, flash
from sqlalchemy import desc, asc
from .models import * 
from .forms import SearchForm

rest_blueprint = Blueprint("rest", __name__, template_folder="templates")

@rest_blueprint.route("/")
def index():
    """ front page of site has all the states listed """
    form = SearchForm()
    state = State.query.all()
    return render_template("front_page/index.html",state=state, form=form)

@rest_blueprint.route("/about")
def about():
    return "this is the about page"

@app.route("/<path:url_slug_state>/<int:state_id>/")
def state_page(url_slug_state,state_id):
    """ By State, within each state lists citys by county """
    form = SearchForm()
    county = County.query.filter_by(state_id=state_id).all()
    city_metro = City.query.filter_by(state_id=state_id, metro_area=False).order_by(desc(City.r_total)).all()
    canada = City.query.filter(City.state_id==state_id, City.county_id==None).order_by(desc(City.r_total)).all()
    state_name = State.query.filter_by(id=state_id).one()
    return render_template("state/state_page.html", 
        url_slug_state=url_slug_state,
        state_name=state_name.name, 
        state_id=state_id, 
        county=county, 
        city_metro=city_metro, 
        canada=canada,
        form=form)

@app.route("/<path:url_slug_state>/<int:state_id>/<path:url_slug_city>/<int:city_id>/<int:page>")
def city_page(url_slug_state,state_id,url_slug_city,city_id, page=1):
    """ Lists Restaurants in each City 50 per page """
    form = SearchForm()
    rest = Restaurant.query.filter_by(state_id=state_id, city_id=city_id).order_by(asc(Restaurant.rest_name)).paginate(page, 40, False)
    state_name = State.query.filter_by(id=state_id).one()
    city_name = City.query.filter_by(id=city_id).one()
    rest_cusine = db.session.query(Cusine).distinct()\
    .join(RestaurantCusine).filter(Cusine.id==RestaurantCusine.cusine_id)\
    .join(Restaurant).filter(Restaurant.id==RestaurantCusine.restaurant_id)\
    .filter(Restaurant.city_id==city_id).order_by(asc(Cusine.name)).all()
    return render_template('city/city_page.html', 
        url_slug_state=url_slug_state, 
        url_slug_city=url_slug_city, 
        state_name=state_name.name,
        state_id=state_id, 
        city_name=city_name.city_name, 
        city_id=city_id, 
        rest=rest, 
        rest_cusine=rest_cusine, 
        rest_total=city_name.r_total,
        form=form)


@app.route("/r/<path:url_slug_state>/<int:state_id>/<path:url_slug_city>/<int:city_id>/<path:url_slug_rest>/<path:rest_id>/")
def rest_page_city(url_slug_state, state_id, url_slug_city, city_id, url_slug_rest, rest_id):
    """ lists information and menu about each restaurant """
    form = SearchForm()
    rest = Restaurant.query.filter_by(id=rest_id).one()
    menu = Menu.query.filter_by(restaurant_id=rest_id).all()
    section = Section.query.filter_by(restaurant_id=rest_id).all()
    menu_items = MenuItem.query.filter_by(restaurant_id=rest_id).all()
    item_price = ItemPrice.query.filter_by(restaurant_id=rest_id).all()
    item_addon = ItemAddon.query.filter_by(restaurant_id=rest_id).all()
    return render_template("restaurant/rest_page.html", 
        rest=rest, 
        menu=menu, 
        section=section, 
        menu_items=menu_items, 
        item_price=item_price,
        item_addon=item_addon,
        form=form)

@app.route("/c/<path:url_slug_state>/<int:state_id>/<path:url_slug_city>/<int:city_id>/<path:url_slug_cusine>/<path:cusine_id>/")
def page_cusine_city(url_slug_state, state_id, url_slug_city, city_id, url_slug_cusine, cusine_id):
    form = SearchForm()
    rest_c = Restaurant.query.filter_by(state_id=state_id, city_id=city_id)\
    .join(RestaurantCusine)\
    .join(Cusine).filter(RestaurantCusine.cusine_id == cusine_id)\
    .order_by(asc(Restaurant.rest_name)).all()
    cusine_name = Cusine.query.filter_by(id=cusine_id).one()
    return render_template('page_cusine_city.html', 
         rest_c=rest_c,
         url_slug_state=url_slug_state, 
         state_id=state_id, 
         url_slug_city=url_slug_city, 
         city_id=city_id, 
         url_slug_cusine=url_slug_cusine, 
         cusine_id=cusine_id, 
         cusine_name=cusine_name.name,
         form=form)

@app.route("/searchbar", methods=["POST"])
def search_bar():
    """ searches the site for restaurants and brings back a result based on city state or zip criteria. """
    form = SearchForm()
    if request.method == 'POST':
        zip_ = request.form["search"]
        print zip_, type(zip_)
        rest = Restaurant.query.filter_by(zip_=int(zip_)).all()
        print len(rest)
        return "OK"
    else:
        return "NO"


