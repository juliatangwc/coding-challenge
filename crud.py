"""CRUD operations."""

from model import db, Inventory, connect_to_db


def create_inventory_item(sku, name, description, quantity, unit, location, unit_cost):
    """Create and return a new inventory item."""

    item = Inventory (sku=sku, name=name, description=description,
                        quantity=quantity, unit=unit, location=location,
                        unit_cost=unit_cost)

    return item

def get_all_inventory():
    """Make query and return a list of all inventory items."""

    return Inventory.query.all()

def get_item_by_sku(sku):
    """Return an item object by its SKU (Stock Keeping Unit)."""
    
    return Inventory.query.get(sku)



if __name__ == '__main__':
    from server import app
    connect_to_db(app)