#!/usr/bin/env python3
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.models import Restaurant,Customer, Review


if __name__ == '__main__':
    
    engine = create_engine('sqlite:///restaurants.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    import ipdb;ipdb.set_trace()

    
    