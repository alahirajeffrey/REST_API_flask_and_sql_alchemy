from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
import os

##init app
app = Flask(__name__)

##app config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

##init dbs
db = SQLAlchemy(app)

##init marshmellow
ma = Marshmallow(app)

#create product taclassclble
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200) )
    price = db.Column(db.Float)
    qty = db.Column(db.String(50))
    category = db.Column(db.String(50))

    def __init__(self, name, description, price, qty, category):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty
        self.category = category

##define output format
class ProductSchema(ma.Schema):
    class Meta:
        # Fields in product table to expose
        fields = ("id","name", "description","price","qty","category")

##initialize product schema
product_schema = ProductSchema()
product_schemas = ProductSchema(many = True)

#create product
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']
    category = request.json['category']

    #instantiate product class and save to database
    new_product = Product(name, description, price, qty, category)
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

#get all products
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = product_schemas.dump(all_products)
    
    db.session.commit()

    return jsonify(result.data)

#update product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)

    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']
    category = request.json['category']

    product.name = name
    product.description= description
    product.price = price
    product.qty = qty
    product.category = category

    db.session.commit()

    result = product_schema(product)
    return jsonify(result)  

#delete product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    
    db.session.delete(product)
    db.session.commit()

    return jsonify(result)


##run server
if __name__ == "__main__":
    app.run(debug=True)

