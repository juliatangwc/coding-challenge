"""Server for logistic inventory app."""

import os
from flask import Flask, render_template, redirect, request, flash, session
from model import connect_to_db, db, Inventory, Warehouse
import helper

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def show_homepage():
    """Show homepage with navigation buttons."""
    
    return render_template("homepage.html")

@app.route("/create-item")
def show_create_item_form():
    """Show form to create a new item in inventory."""

    #Get list of all warehouses to populate form
    warehouses = Warehouse.get_all_warehouses_by_city()

    return render_template("create_item.html", warehouses = warehouses)

@app.route("/create-item", methods=["POST"])
def create_item():
    """Create a new inventory item. Redirect to item page."""
    
    sku = request.form.get("sku")
    name = request.form.get("name")
    description = request.form.get("description")
    quantity = request.form.get("quantity")
    unit = request.form.get("unit")
    unit_cost = request.form.get("unit_cost")
    warehouse_id = request.form.get("warehouse")

    #Validate input fields
    if helper.validate_create_item_input(sku, name, quantity, unit, unit_cost, warehouse_id):
        if Inventory.get_item_by_sku(sku) is None: #Check if SKU is unique
            item = Inventory.create_inventory_item(sku, warehouse_id, name, description, 
                                                    quantity, unit, unit_cost)
            db.session.add(item)
            db.session.commit()
            flash ("New item created.")
            return redirect (f"/inventory/{sku}")
        else:
            flash ("New item cannot be created. SKU already in system.")
            return redirect(request.referrer)
    else:
        flash("Inaccurate/Incomplete information entered.")
        return redirect(request.referrer)

@app.route('/inventory')
def show_inventory():
    """Show all inventory"""

    inventory = Inventory.get_all_inventory()
    
    return render_template('inventory.html', inventory = inventory)

@app.route("/inventory/<sku>")
def show_item_details(sku):
    """Show details on a particular item"""
    
    item = Inventory.get_item_by_sku(sku)

    if item:
        return render_template("item_details.html", item=item)
    else:
        flash ("Item does not exist. Please see complete list of inventory.")
        return redirect("/inventory")

@app.route("/delete", methods=["POST"])
def delete_item():
    """Delete a particular item"""
    
    sku = request.form.get("sku")
    item = Inventory.get_item_by_sku(sku)
    db.session.delete(item)
    db.session.commit()
    flash ("Item deleted.")

    return redirect ("/inventory")

@app.route("/edit")
def show_edit_item_form():
    """Show form to edit a particular item"""
    
    sku = request.args.get("sku")
    item = Inventory.get_item_by_sku(sku)
    warehouses = Warehouse.get_all_warehouses_by_city()

    return render_template("item_edit.html", item=item, warehouses=warehouses)

@app.route("/edit", methods=["POST"])
def edit_item():
    """Edit a particular item"""
    
    sku = request.form.get("sku")
    name = request.form.get("name")
    description = request.form.get("description")
    quantity = request.form.get("quantity")
    unit = request.form.get("unit")
    unit_cost = request.form.get("unit_cost")
    warehouse = request.form.get("warehouse")

    item = Inventory.get_item_by_sku(sku)
    item.name = name
    item.description = description
    item.quantity = quantity
    item.unit = unit
    item.unit_cost = unit_cost
    item.warehouse_id = warehouse
    
    db.session.add(item)
    db.session.commit()
    
    flash ("Item updated.")
    return redirect(f"/inventory/{sku}")

@app.route("/search")
def show_search_form():
    """Show form to search for a particular item."""

    return render_template("search.html")

@app.route("/result")
def locate_item():
    """Locate a particular item."""
    
    sku = request.args.get("sku")
    
    if sku.isdigit():
        item = Inventory.get_item_by_sku(sku)
        if item:
            return redirect(f"/inventory/{sku}")
        else:
            flash("Invalid SKU. Try again.")
            return redirect("/search")
    else:
        flash("Please enter integers only.")
        return redirect("/search")

@app.route("/warehouse")
def show_warehouse_list():
    """Show a list of all warehouse."""
    warehouses = Warehouse.get_all_warehouses_by_id()
    return render_template("warehouse.html", warehouses=warehouses)

@app.route("/warehouse/<warehouse_id>")
def show_warehouse_details(warehouse_id):
    """Show details on a particular warehouse."""
    
    warehouse = Warehouse.get_warehouse_by_id(warehouse_id)

    if warehouse:
        return render_template("warehouse_details.html", warehouse=warehouse)
    else:
        flash ("Warehouse does not exist. Please see complete list of current warehouses.")
        return redirect("/warehouse")

@app.route("/add-warehouse")
def show_add_warehouse_form():
    """Show form to add a new warehouse."""
    return render_template("add_warehouse.html")

@app.route("/add-warehouse", methods=["POST"])
def add_warehouse():
    """Add a new warehouse to the database."""
    
    city_name = request.form.get("city_name").title()
    city_code = request.form.get("city_code").upper()

    #Validate add warehouse form input fields
    if helper.validate_add_warehouse_input(city_name, city_code):
        warehouse = Warehouse.create_warehouse(city_code, city_name)
        db.session.add(warehouse)
        db.session.commit()
        flash ("New warehouse added.")
        return redirect (f"/warehouse/{warehouse.warehouse_id}")
    else:
        flash("Inaccurate/Incomplete information entered.")
        return redirect(request.referrer)

@app.route("/delete-warehouse", methods=["POST"])
def delete_warehouse():
    """Delete a particular warehouse"""
    
    warehouse_id = request.form.get("warehouse_id")
    warehouse = Warehouse.get_warehouse_by_id(warehouse_id)
    db.session.delete(warehouse)
    db.session.commit()
    flash ("Warehouse deleted.")

    return redirect ("/warehouse")

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)