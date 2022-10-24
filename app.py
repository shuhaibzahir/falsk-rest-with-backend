

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
app = Flask(__name__)


baseDir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///" + os.path.join(baseDir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False

# init db
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)
    
    def __init__(self, name, description, price, qty):
        self.name = name
        self.description= description
        self.price = price
        self.qty = qty

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id','name','description','price','qty')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)



# routes
@app.route("/", methods=["GET"])
def he():
    return jsonify({"ms":"welcom"})


@app.route("/product", methods=["POST"])

def create_product():
    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]
    qty = request.json["qty"]
    new_product = Product(name,description, price,qty)
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)

@app.route("/product",methods=["GET"])
def get_all_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)


@app.route("/product/<int:id>",methods=["GET"])
def get_product_by_id(id):
    get_product = Product.query.get(id)
    return product_schema.dump(get_product)

@app.route("/product/<int:id>",methods=["PUT"])
def update_product(id):
    product = Product.query.get(id)
    data = product_schema.dump(request.json)
    for key, value in data.items():
        setattr(product,key,value)
    db.session.commit()
    return product_schema.jsonify(product)
    

@app.route("/product/<int:id>",methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"msg":f"deleted successfully by id ={id}"})
    else :
        return jsonify({"msg":"not found"}),400


    
    

if __name__ == "__main__":
    app.run(debug=True)




