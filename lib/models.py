import os
import sys

sys.path.append(os.getcwd)

from sqlalchemy import (create_engine, PrimaryKeyConstraint, Column, String, Integer, ForeignKey, Table)
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref


Base = declarative_base()
engine = create_engine('sqlite:///db/restaurants.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

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
    
    @classmethod
    def fanciest(cls):
        # Return the restaurant with the highest price
        return session.query(cls).order_by(cls.price.desc()).first()
    
    def all_reviews(self):
        reviews = session.query(Review).filter_by(restaurant_id=self.id).all()
        
        formatted_reviews = [
            f'Review for {self.name} by {review.customer.full_name()}: {review.star_rating} stars.'
            for review in reviews
        ]
        return formatted_reviews
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
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def favorite_restaurant(self):
        # check is any restaurant has any reviews
        if not self.reviews: 
            return None
        # Find the restaurant review with the highest rating and return the result
        max_rating_review = max(self.reviews, key=lambda review: review.star_rating)
        return max_rating_review.restuarant
    
    def add_review(self, restaurant, rating):
        # Creating a new review instance
        new_review = Review(
            star_rating=rating, 
            restaurant= restaurant
            )
        # Append the review to te customer's review list
        self.reviews.append(new_review)
        # Append the the review to the restaurant's review list
        restaurant.reviews.append(new_review)
        # Add new review and save
        session.add(new_review)
        session.commit()
    
    def delete_reviews(self, restaurant):
        # Get all the reviews for the customer and the restaurant
        reviews_to_be_deleted = [
            review for review in self.reviews if review.restaurant == restaurant
        ]
        # Delete reviews from the customer and the restaurant tables
        for review in reviews_to_be_deleted:
            self.reviews.remove(review)
            restaurant.reviews.remove(review)
        # Delete the reviews from the database
        for review in reviews_to_be_deleted:
            session.delete(review)
        # Save the changes
        session.commit()
    
class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))
        
    def __repr__(self):
        return f'Review(id={self.id},'+\
            f'Rating={self.star_rating},'+\
                f'Restaurant_id={self.restaurant_id}, '+\
                    f'Customer_id={self.customer_id})'
                    
    def review_customer(self):
        return self.customer
    
    def review_restaurant(self):
        return self.restaurant
    
    def full_review(self):
        return f'Review for {self.restaurant.name} by {self.customer.full_name()}: {self.star_rating} stars.'
