# -*- coding: utf-8 -*-
import os
from app import db
from slugify import slugify


class State(db.Model):
    __tablename__ = "state"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    abbr = db.Column(db.String)
    counties = db.relationship("County")
    cities = db.relationship("City")
    restaurants = db.relationship("Restaurant")

    @property 
    def url_slug_state(self):
        return slugify(self.name)
        
class County(db.Model):
    __tablename__ = "county"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    state_id = db.Column(db.Integer, db.ForeignKey("state.id"), index=True)
    cities = db.ForeignKey("City")
    restaurants = db.ForeignKey("Restaurant")
     
    @property 
    def url_slug_county(self):
        return slugify(self.name)
        
class City(db.Model):
    __tablename__ = "city" 
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String)
    neighborhood_name = db.Column(db.String)
    metro_area = db.Column(db.Boolean)
    r_total = db.Column(db.Integer)
    state_id = db.Column(db.Integer, db.ForeignKey("state.id"), index=True)
    county_id = db.Column(db.Integer, db.ForeignKey("county.id"), index=True)
    restaurants = db.ForeignKey("Restaurant")
    
    @property 
    def url_slug_city(self):
        return slugify(self.city_name)
        
class Restaurant(db.Model):
    __tablename__ = "restaurant"
    id = db.Column(db.Integer, primary_key=True)
    rest_name = db.Column(db.String)
    rest_link = db.Column(db.String)
    thumbnail_img = db.Column(db.String) # cdn link to img for later download 
    menu_available = db.Column(db.Boolean)
    text_menu_available = db.Column(db.Boolean)
    city_name = db.Column(db.String)
    neighborhood_name = db.Column(db.String)  
    phone = db.Column(db.String)
    address = db.Column(db.String)
    city_ = db.Column(db.String)
    state_ = db.Column(db.String)
    zip_ = db.Column(db.String)
    website = db.Column(db.String)
    description = db.Column(db.String)
    hours = db.Column(db.String)
    delivery = db.Column(db.Boolean)
    wifi = db.Column(db.Boolean)
    alcohol = db.Column(db.String)
    price_point = db.Column(db.String)
    attire = db.Column(db.String)
    payment = db.Column(db.String)
    parking = db.Column(db.String)
    outdoor_seats = db.Column(db.Boolean) 
    reservations = db.Column(db.Boolean)
    good_for_kids = db.Column(db.Boolean)
    menu_url_id = db.Column(db.String)
    menu_link_pdf = db.Column(db.String)

    state_id = db.Column(db.Integer, db.ForeignKey("state.id"), index=True)
    state = db.relationship('State')
    county_id = db.Column(db.Integer, db.ForeignKey("county.id"), index=True)
    county = db.relationship('County')
    city_id = db.Column(db.Integer, db.ForeignKey("city.id"), index=True)
    city = db.relationship('City')
    cusine = db.relationship('Cusine', secondary='restaurant_cusine', backref=db.backref('restaurant', lazy='dynamic', cascade="all, delete-orphan", single_parent=True))
    menu = db.relationship("Menu")
    
    @property 
    def url_slug_rest(self):
        if self.neighborhood_name is not None:
            return slugify(self.neighborhood_name)
        return slugify(self.rest_name)
        
class Cusine(db.Model):
    __tablename__ = "cusine"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    @property 
    def url_slug_cusine(self):
        return slugify(self.name)

class RestaurantCusine(db.Model):
    __tablename__ = "restaurant_cusine"
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id', ondelete='CASCADE'), index=True)
    cusine_id = db.Column(db.Integer, db.ForeignKey('cusine.id', ondelete='CASCADE'), index=True)

class RestaurantCoverImage(db.Model):
    __tablename__ = "restaurant_cover_image"
    id = db.Column(db.Integer, primary_key=True)
    cover_photo = db.Column(db.String)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id', ondelete='CASCADE'), index=True)

class RestaurantImages(db.Model):
    __tablename__ = "restaurant_images"
    id = db.Column(db.Integer, primary_key=True)
    photos = db.Column(db.String)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id', ondelete='CASCADE'), index=True)

class Menu(db.Model):
    __tablename__ = "menu"
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id', ondelete='CASCADE'), index=True)
    menu_section = db.relationship("Section")

class Section(db.Model):
    __tablename__ = "section"
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String)
    description = db.Column(db.String)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id', ondelete='CASCADE'), index=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id', ondelete='CASCADE'), index=True)
    items = db.relationship("MenuItem")
 
class MenuItem(db.Model):
    __tablename__ = "menu_item"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id', ondelete='CASCADE'), index=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id', ondelete='CASCADE'), index=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id', ondelete='CASCADE'), index=True)
    price_items = db.relationship("ItemPrice")
    addon_items = db.relationship("ItemAddon")

class ItemPrice(db.Model):
    __tablename__ = "item_price"
    id = db.Column(db.Integer, primary_key=True)
    price_title = db.Column(db.String)
    price_value = db.Column(db.String)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id', ondelete='CASCADE'), index=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id', ondelete='CASCADE'), index=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id', ondelete='CASCADE'), index=True)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id', ondelete='CASCADE'), index=True) 

class ItemAddon(db.Model):
    __tablename__ = "item_addon"
    id = db.Column(db.Integer, primary_key=True)
    addon_title = db.Column(db.String)
    addon_value = db.Column(db.String)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id', ondelete='CASCADE'), index=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id', ondelete='CASCADE'), index=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id', ondelete='CASCADE'), index=True)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id', ondelete='CASCADE'), index=True) 


