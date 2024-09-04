#!/usr/bin/env python3

from crypt import methods
from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(  bakeries,   200  )

@app.route('/baked_goods', methods=['POST'])
def baked_goods():
    if request.method == 'POST':
        new_bg = BakedGood(
            bakery_id = request.form.get('bakery_id'),
            name = request.form.get('name'),
            price = request.form.get('price'),
        )
        db.session.add(new_bg)
        db.session.commit()

        newbg_dict = new_bg.to_dict()
        result = make_response( newbg_dict, 201  )
        return result

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def baked_goods_by_id(id):
    if request.method == 'DELETE':
        bg = BakedGood.query.filter_by(id=id).first()
        if not bg:
            return make_response( 'Baked good not found', 404  )

        db.session.delete(bg)
        db.session.commit()
        response_body = {
                "delete_successful": True,
                "message": "Baked good deleted."
            }

        return make_response( response_body, 200  )
    
@app.route('/bakeries/<int:id>', methods=['GET','PATCH', 'DELETE'])
def bakery_by_id(id):
    if request.method == 'GET':
        bakery = Bakery.query.filter_by(id=id).first()
        bakery_serialized = bakery.to_dict()
        return make_response ( bakery_serialized, 200  )
    elif request.method == 'PATCH':
        bakery = Bakery.query.filter_by(id=id).first()
        if not bakery:
            return make_response( 'Bakery not found', 404  )

        bakery.name = request.form.get('name')
        db.session.commit()

        bakery_updated_serialized = bakery.to_dict()
        return make_response( bakery_updated_serialized, 200  )
        
    
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    return make_response( baked_goods_by_price_serialized, 200  )
   

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return make_response( most_expensive_serialized,   200  )

if __name__ == '__main__':
    app.run(port=5555, debug=True)