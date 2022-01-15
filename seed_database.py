"""Script to seed database."""

import os
import json

import crud
import model
import server

os.system("dropdb inventory")
os.system('createdb inventory')

model.connect_to_db(server.app)
model.db.create_all()

# Load inventory data from JSON file
with open('data/inventory.json') as f:
    inventory_data = json.loads(f.read())

for item in inventory_data:
    sku = item['sku']
    name = item['name']
    description = item['description']
    quantity = item['quantity']
    unit = item['unit']
    location = item['location']
    unit_cost = item['unit_cost']
    image = item['image']

    new_item = crud.create_inventory_item (sku, name, description,
                                            quantity, unit, location,
                                            unit_cost, image)
    model.db.session.add(new_item)

model.db.session.commit()
    