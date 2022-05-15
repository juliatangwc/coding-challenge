"""Models for inventory app for a logistic company."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Inventory(db.Model):
    """An item in the inventory."""

    __tablename__ = "inventory"

    sku = db.Column(db.Integer,
                    primary_key=True,
                    unique = True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouse.warehouse_id"))
    name = db.Column(db.String)
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer)
    unit = db.Column(db.String)
    unit_cost = db.Column(db.Numeric(18,2))

    warehouse = db.relationship('Warehouse', back_populates="inventory_item")
    
    def __repr__(self):
        return f"<Item SKU={self.sku} Name={self.name}>"
    
    @classmethod
    def create_inventory_item(cls, sku, warehouse_id, name, description, quantity, unit, unit_cost):
        """Create and return a new inventory item instance."""

        return cls(sku=sku, warehouse_id=warehouse_id, name=name, description=description,
                    quantity=quantity, unit=unit, unit_cost=unit_cost)

class Warehouse(db.Model):
    """A warehouse for inventory storage."""

    __tablename__ = "warehouse"

    warehouse_id = db.Column (db.Integer,
                                autoincrement=True,
                                primary_key=True)
    city_code = db.Column(db.String)
    city_name = db.Column(db.String)

    inventory_item = db.relationship('Inventory', back_populates="warehouse")

    def __repr__(self):
        return f"<Warehouse ID={self.warehouse_id} Location={self.location}"

    @classmethod
    def create_warehouse(cls, city_code, city_name):
        """Create and return a warehouse instance."""

        return cls(city_code=city_code, city_name=city_name)


def connect_to_db(flask_app, db_uri="postgresql:///inventory", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
