"""Server for logistic inventory app."""

import os
from flask import Flask, render_template, redirect, request, flash, session
from werkzeug.utils import secure_filename
from PIL import Image
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
    image = ""
    thumbnail = ""

    if sku.isdigit():
        item = crud.create_inventory_item(sku, name, description, 
                                        quantity, unit, location, 
                                        unit_cost, image, thumbnail)
        db.session.add(item)
        db.session.commit()
        flash ("New item created.")
        return redirect (f"/inventory/{sku}")
    else:
        flash("Please enter a valid SKU (Integers only).")
        return redirect("/create")

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
    flash ("Item deleted.")

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
    
    flash ("Item updated.")
    return redirect(f"/inventory/{sku}")

@app.route("/search")
def show_search_form():
    """Show form to search for a particular item."""

    return render_template("search.html")

@app.route("/result")
def locate_item():
    """Locate a particular item"""
    
    sku = request.args.get("sku")
    
    if sku.isdigit():
        item = crud.get_item_by_sku(sku)
        if item:
            return redirect(f"/inventory/{sku}")
        else:
            flash("Invalid SKU. Try again.")
            return redirect("/search")
    else:
        flash("Please enter integers only.")
        return redirect("/search")

def allowed_file(filename):
    return ('.' in filename and
            filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS)

@app.route("/image", methods=["GET", "POST"])
def upload_image_():
    """Allow user to upload a product image.
        Create a thumbnail and update database with path."""
    
    if request.method == 'POST':

        if 'file' not in request.files:
            flash("Cannot locate file. Please try again.")
            return redirect(request.url)
        sku = request.form.get("sku")
        file = request.files["file"]

        if file.filename == "":
            flash("No selected file. Please try again.")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(path)
            
            image = Image.open(file)
            image.thumbnail((100,100))
            thumbpath = os.path.join(app.config["UPLOAD_FOLDER"], f"thumb{filename}")
            image.save(thumbpath)
            
            item = crud.update_image(sku, f"/static/uploads/{filename}", f"/static/uploads/thumb{filename}")
            db.session.add(item)
            db.session.commit()

            flash("Success! Image uploaded.")
            return redirect(request.url)
    
    return redirect ("/inventory")

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)