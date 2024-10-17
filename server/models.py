from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Relationship with Review
    reviews = db.relationship('Review', back_populates='customer', cascade='all, delete-orphan')

    # Association proxy to items via reviews
    items = association_proxy('reviews', 'item')

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

    def to_dict(self):
        customer_dict = {
            'id': self.id,
            'name': self.name,
            'reviews': [{'id': r.id, 'comment': r.comment, 'item_id': r.item_id} for r in self.reviews]
        }
        return customer_dict


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    # Relationship with Review
    reviews = db.relationship('Review', back_populates='item', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

    def to_dict(self):
        item_dict = {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'reviews': [{'id': r.id, 'comment': r.comment, 'customer_id': r.customer_id} for r in self.reviews]
        }
        return item_dict


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)

    # Foreign keys
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    # Relationships
    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

    def __repr__(self):
        return f'<Review {self.id}, {self.comment}>'

    def to_dict(self):
        review_dict = {
            'id': self.id,
            'comment': self.comment,
            'customer': {'id': self.customer.id, 'name': self.customer.name} if self.customer else None,
            'item': {'id': self.item.id, 'name': self.item.name, 'price': self.item.price} if self.item else None
        }
        return review_dict
