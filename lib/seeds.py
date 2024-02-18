from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Restaurant,Customer, Review, Base

if __name__ == '__main__':
    
    engine = create_engine('sqlite:///restaurants.db')
    Base.metadata.create_all(engine) 
    Session = sessionmaker(bind=engine)
    session = Session()
    
    session.query(Restaurant).delete()
    session.query(Customer).delete()
    session.query(Review).delete()
    
    fake=Faker()
        
    restaurant_names = [fake.company() for _ in range(20)]
        
    restaurants =[]
    for i in range(10):
        restaurant=Restaurant(
            name=random.choice(restaurant_names),
            price=random.randint(1,20)
        )
        
        session.add(restaurant)
        session.commit()
        
        restaurants.append(restaurant)
    
    customers=[]
    for i in range(20):
        customer=Customer(
            first_name=fake.name(),
            last_name=fake.name(),
        )
        session.add(customer)
        session.commit()
        
        customers.append(customer)
    
    reviews=[]
    for restaurant in restaurants:
        for i in range(random.randint(1,20)):
            customer=random.choice(customers)
            if restaurant not in customer.restaurants:
                customer.restaurants.append(restaurant)
                session.add(customer)
                session.commit()
                
            review=Review(
                star_rating=random.randint(1, 20),
                restaurant_id=restaurant.id,
                customer_id=customer.id,
            )
            
            reviews.append(review)
    session.bulk_save_objects(reviews)
    session.commit()
    session.close()