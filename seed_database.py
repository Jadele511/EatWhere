"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb eatwhere')
os.system('createdb eatwhere')

model.connect_to_db(server.app)
model.db.create_all()


for n in range(10):
    email = f'user{n}@test.com'
    password = 'test'

    user = crud.create_user(email, password)