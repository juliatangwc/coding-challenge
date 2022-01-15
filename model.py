"""Models for logistic app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Inventory(db.Model):
    """A item in the inventory."""

    __tablename__ = "inventory"

    sku = db.Column(db.Integer,
                    autoincrement=True,
                    primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer)
    unit = db.Column(db.String)
    location = db.Column(db.String)
    unit_cost = db.Column(db.Numeric(18,2))
    image = db.Column(db.String)
    


    def __repr__(self):
        return f"<Item SKU={self.sku} Name={self.name}>"


def connect_to_db(flask_app, db_uri="postgresql:///inventory", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
