"""Script to seed database."""

import os
import json

from model import connect_to_db, db, Inventory, Warehouse

os.system("dropdb inventory")
os.system('createdb inventory')

connect_to_db(server.app)
db.create_all()

# Load inventory data from JSON file
with open('data/inventory.json') as f:
    inventory_data = json.loads(f.read())

#Create new instance of inventory item in database
for item in inventory_data:
    sku = item['sku']
    warehouse_id = item['warehouse_id']
    name = item['name']
    description = item['description']
    quantity = item['quantity']
    unit = item['unit']
    unit_cost = item['unit_cost']

    new_item = Inventory.create_inventory_item (sku, warehouse_id, name, description,
                                                quantity, unit, unit_cost)
    model.db.session.add(new_item)

model.db.session.commit()
    