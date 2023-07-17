"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# Initialize the database
db = SQLAlchemy()

def connect_db(app):
    """Connect the database to the Flask app."""
    db.app = app
    db.init_app(app)

DEFAULT_IMG = 'https://tinyurl.com/demo-cupcake'

# MODELS GO HERE
class Cupcake(db.Model):
    '''Cupcake'''
    __tablename__ = 'cupcakes'

    def serialize(self):
        """Serialize a cupcake SQLAlchemy obj to dictionary."""

        return {
            "id": self.id,
            "flavor": self.flavor,
            "size": self.size,
            "rating": self.rating,
            "image": self.image or DEFAULT_IMG 
        }    

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.String, nullable=False)
    size = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.String, nullable=False, default=DEFAULT_IMG)
    

