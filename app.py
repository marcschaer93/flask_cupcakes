"""Flask app for Cupcakes"""
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db 

# Create a FLASK instance
app = Flask(__name__)
# Add a DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
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

# #Create some users
# first_name = ['fluffy', 'stevie', 'carole', 'sira', 'sally', 'bella', 'lucy']
# last_name = ['hafer', 'wonder', 'baskin', 'baskin', 'struthers', 'ronder', 'ricardo']
# users = [User(first_name=first, last_name=last) for first, last in zip(first_name, last_name)]

# #Create some posts
# post1 = Post(title='My first post', content='This is my first post', user_id=1)
# post2 = Post(title='My second post', content='This is my second post', user_id=1)

# #Create some tags
# tag1 = Tag(name='funny')
# tag2 = Tag(name='sad')
# tag3 = Tag(name='happy')
# tag4 = Tag(name='angry')

# Drop and recreate tables
with app.app_context():
	db.drop_all()
	db.create_all()
	# for user in users:
	# 	existing_user = User.query.filter_by(first_name=user.first_name).first() and User.query.filter_by(last_name=user.last_name).first()
	# 	if not existing_user:
	# 		db.session.add(user)
            
	# db.session.commit()
	# db.session.add_all([post1, post2, tag1, tag2, tag3, tag4])
	# db.session.commit()

#----- ROUTES -----#
