"""Server for logistic inventory app."""

from flask import Flask, render_template, redirect, request, flash, session
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def show_homepage():
    return render_template('homepage.html')

@app.route('/inventory')
def show_inventory():
    """Show all inventory"""

    inventory = crud.get_all_inventory()
    
    return render_templates('inventory.html', inventory = inventory)


@app.route("/inventory/<sku>")
def show_item_details(sku):
    """Show details on a particular item"""
    
    item = crud.get_item_by_sku(sku)

    return render_template("item_details.html", item=item)



if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)