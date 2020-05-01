"""Flask app for Cupcakes"""

from flask import Flask, request, redirect, render_template, flash, jsonify
from models import db, connect_db, Cupcake
from forms import AddCupcakeForm

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:41361@localhost/cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route("/")
def home():
    """Render homepage with cupcake form"""
    form = AddCupcakeForm()
    return render_template("home.html", form=form)

@app.route("/api/cupcakes")
def get_cupcakes():
    """Get data about all cupcakes"""
    cupcakes = [c.serialize() for c in Cupcake.query.all()]

    return jsonify(cupcakes=cupcakes)

@app.route("/api/cupcakes/<int:id>")
def get_cupcake(id):
    """Get data about one cupcake"""
    cupcake = Cupcake.query.get_or_404(id).serialize()

    return jsonify(cupcake=cupcake)

@app.route("/api/cupcakes", methods=['POST'])
def add_cupcake():
    """Add a new cupcake"""
    
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image'] if request.json['image'] else None

    cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=cupcake.serialize()), 201)

@app.route("/api/cupcakes/<int:id>", methods=['PATCH'])
def edit_cupcake(id):
    """Edit a cupcake"""
    cupcake = Cupcake.query.get_or_404(id)

    cupcake.flavor = request.json['flavor']
    cupcake.size = request.json['size']
    cupcake.rating = request.json['rating']
    cupcake.image = request.json['image'] if request.json['image'] else None

    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())

@app.route("/api/cupcakes/<int:id>", methods=['DELETE'])
def delete_cupcake(id):
    """Delete a cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")