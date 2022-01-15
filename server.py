"""Server for logistic inventory app."""

from flask import Flask, render_template, redirect, request, flash, session
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def show_homepage():
    """Show homepage with navigation buttons."""
    
    return render_template("homepage.html")

@app.route("/create")
def show_form_create_item():
    """Show form to create a new item in inventory."""

    return render_template("create_item.html")

@app.route("/create", methods=["POST"])
def create_item():
    """Create a new inventory item."""
    
    sku = request.form.get("sku")
    name = request.form.get("name")
    description = request.form.get("description")
    quantity = request.form.get("quantity")
    unit = request.form.get("unit")
    unit_cost = request.form.get("unit_cost")
    location = request.form.get("location")
    
    item = crud.create_inventory_item(sku, name, description, 
                                    quantity, unit, location, 
                                    unit_cost)
    
    db.session.add(item)
    db.session.commit()

    return redirect (f"/inventory/{sku}")

@app.route('/inventory')
def show_inventory():
    """Show all inventory"""

    inventory = crud.get_all_inventory()
    
    return render_template('inventory.html', inventory = inventory)


@app.route("/inventory/<sku>")
def show_item_details(sku):
    """Show details on a particular item"""
    
    item = crud.get_item_by_sku(sku)

    return render_template("item_details.html", item=item)

@app.route("/delete", methods=["POST"])
def delete_item():
    """Delete a particular item"""
    
    sku = request.form.get("sku")
    item = crud.get_item_by_sku(sku)
    db.session.delete(item)
    db.session.commit()

    return redirect ("/inventory")

@app.route("/edit")
def show_edit_item_form():
    """Show form to edit a particular item"""
    
    sku = request.args.get("sku")
    item = crud.get_item_by_sku(sku)

    return render_template("item_edit.html", item=item)

@app.route("/edit", methods=["POST"])
def edit_item():
    """Edit a particular item"""
    
    sku = request.form.get("sku")
    name = request.form.get("name")
    description = request.form.get("description")
    quantity = request.form.get("quantity")
    unit = request.form.get("unit")
    unit_cost = request.form.get("unit_cost")
    location = request.form.get("location")

    item = crud.update_item(sku, name, description, quantity,
                            unit, unit_cost, location)
    
    db.session.add(item)
    db.session.commit()
    

    return redirect(f"/inventory/{sku}")

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)