"""Helper functions for CRUD operations."""

from model import db, Inventory, connect_to_db

def is_float(input_string):
    """Check if an input string is a float"""
    try:
        float(input_string)
        return True
    except ValueError:
        return False

def validate_create_item_input(sku, name, quantity, unit, unit_cost, warehouse):
    """Form input fields error handling"""
    # Check if fields are empty
    # Check if SKU is digit
    # Check if quantity is digit
    # Check if unit cost is is float

    if  sku == "" or \
        name == "" or \
        quantity == "" or \
        unit == "" or \
        unit_cost == "" or \
        warehouse == "" or \
        not sku.isdigit() or \
        not quantity.isdigit() or \
        not is_float(unit_cost):
            return False
    else:
        return True

def validate_add_warehouse_input(city_name, city_code):
    """Form input fields error handling"""
    # Check if fields are empty
    # Check if city_code consists of 3 alphabetical characters

    if  city_name == "" or \
        city_code == "" or \
        len(city_code) != 3:
            return False
    else:
        return True

if __name__ == '__main__':
    from server import app
    connect_to_db(app)