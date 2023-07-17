"""Flask app for Cupcakes"""
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import Cupcake, db, connect_db 
from seed import c1, c2 
from forms import NewCupcake
from flask_cors import CORS

# Create a FLASK instance
app = Flask(__name__)
 # This will enable CORS for all routes of your app.
CORS(app)
# Add a DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# SECRET KEY
app.config['SECRET_KEY'] = "hyptokrypo"
# DEBUG TOOLBAR
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# initializes the Flask Debug Toolbar
debug = DebugToolbarExtension(app)
# connect to DATABASE
connect_db(app)


with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.add_all([c1, c2])
    db.session.commit()

#----- ROUTES -----#
@app.route('/')
def homepage():
    """Show homepage"""
    return render_template('home.html')

@app.route('/cupcakes', methods=["GET", "POST"])
def create_new_cupcake():
    """Create a new cupcake"""
    form = NewCupcake()
	# form.validate_on_submit == checks if this is a POST request? AND is the TOKEN valid?
    if form.validate_on_submit():
        flavor = form.flavor.data
        size = form.size.data
        rating = form.rating.data
        image = form.image.data
        new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
        db.session.add(new_cupcake)
        db.session.commit()

        # flash(f"Added {flavor} cupcake", "success")
        return redirect('/')
    else:
        return render_template('new_cupcake.html', form=form)
 
@app.route('/api/cupcakes')
def show_cupcakes():
    """Show all cupcakes"""
    cupcakes = Cupcake.query.all()
    return jsonify(cupcakes=[cupcake.serialize() for cupcake in cupcakes])

@app.route('/api/cupcakes/<int:id>')
def show_cupcake(id):
    """Show a single cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Create a new cupcake"""
    new_cupcake = Cupcake(
        flavor=request.json["flavor"],
        size=request.json["size"],
        rating=request.json["rating"],
        image=request.json["image"]
    )
    db.session.add(new_cupcake)
    db.session.commit()
    response_json = jsonify(cupcake=new_cupcake.serialize())
    return (response_json, 201)

@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    """Update a cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    """Delete a cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")







