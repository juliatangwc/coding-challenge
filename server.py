"""Server for logistic inventory app."""

from flask import Flask, render_template, redirect

app = Flask(__name__)


@app.route('/')
def show_inventory():
    """Show all inventory"""
    
    return render_templates('inventory.html')


if __name__ == "__main__":
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0", debug=True)