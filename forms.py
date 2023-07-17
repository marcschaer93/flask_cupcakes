from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SelectField, IntegerRangeField
from wtforms.validators import InputRequired, Length, NumberRange, URL, Optional

class NewCupcake(FlaskForm):
    """Add a new cupcake"""
    flavor = StringField("Flavor", validators=[InputRequired(), Length(max=50)])
    rating = IntegerRangeField("Rating", validators=[InputRequired(), NumberRange(min=1, max=10)])
    size = SelectField("Size", choices=[("small", "Small"), ("medium", "Medium"), ("large", "Large")])
    image = StringField("Image URL", validators=[Optional(), URL()])