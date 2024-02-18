import os
import sys

sys.path.append(os.getcwd)

from sqlalchemy import (create_engine, PrimaryKeyConstraint, Column, String, Integer, ForeignKey, Table)
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref


Base = declarative_base()
engine = create_engine('sqlite:///db/restaurants.db', echo=True)

restaurant_customer=Table(
    'restaurant_customers',
    Base.metadata,
    Column('id', Integer(), primary_key=True),
    Column('restaurant_id', ForeignKey('restaurants.id')),
    Column('customer_id', ForeignKey('customers.id')),
    extend_existing=True,
)

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String())
    price = Column(Integer)
    customers=relationship('Customer', secondary=restaurant_customer, back_populates='restaurants')
    reviews=relationship('Review', backref=backref('restaurant'))

    def __repr__(self):
        return f'Restaurant: {self.name}, Price: {self.price} dollars'

    def restaurant_reviews(self):
        return self.reviews
    
    def restaurant_customers(self):
        return [review.customer for review in self.reviews]

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    restaurants=relationship('Restaurant', secondary=restaurant_customer, back_populates='customers')
    reviews=relationship('Review', backref=backref('customer'))
    
    def __repr__(self):
        return f'Customer: {self.first_name}'

    def customer_reviews(self):
        return self.reviews
    
    def customer_restaurants(self):
        return [review.restaurant for review in self.reviews]
    
class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))
    # restaurant=relationship("Restaurant", back_populates='reviews')
    # customer=relationship("Customer", back_populates='reviews')
    
    def __repr__(self):
        return f'Review(id={self.id},'+\
            f'Rating={self.star_rating},'+\
                f'Restaurant_id={self.restaurant_id}, '+\
                    f'Customer_id={self.customer_id})'
                    
    def review_customer(self):
        return self.customer
    
    def review_restaurant(self):
        return self.restaurant
    
    