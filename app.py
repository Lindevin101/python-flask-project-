from peewee import *
import datetime

db = PostgresqlData('water', user='poowoo', password='123456', host='localhost', port=5432)

class BaseModel(Model):
    class Meta:
        database = db

class Bottle(BaseModel):
    brand = CharField()
    source = CharField()
    location = CharField()
    rating = FloatField()

db.connect()
db.drop_table([Bottle])
db.create_tables([Bottle])

app = Flask(__name__)

Bottle(brand='Arrowhead', source='Springwater', location='San Bernadino, CA', ph=7.93).save()
Bottle(brand='Poland Spring', source='Springwater', location='Poland Spring, ME', ph=6.4).save()
Bottle(brand='Sparkletts', source='Artesian', location='Various', ph=6.9).save()
Bottle(brand='Evian', source='Springwater', location='Evian, France', ph=7.2).save()

@app.route('/bottle/<int:id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def bottle_endpoint(id):
    bottle = Bottle.get_or_none(Bottle.id == id)
    if request.method == 'GET':
        if bottle:
            return jsonify(model_to_dict(bottle))
        else:
            return jsonify({'error': 'Bottle not found'}), 404
    elif request.method == 'POST':
        data = request.get_json()
        brand = data.get('brand')
        source = data.get('source')
        location = data.get('location')
        rating = data.get('rating')
        if not all([brand, source, location, rating]):
            return jsonify({'error': 'Invalid data'}), 400
        bottle = Bottle.create(brand=brand, source=source, location=location, rating=rating)
        return jsonify(model_to_dict(bottle)), 201
    elif request.method == 'PUT':
        data = request.get_json()
        brand = data.get('brand')
        source = data.get('source')
        location = data.get('location')
        rating = data.get('rating')
        if not all([brand, source, location, rating]):
            return jsonify({'error': 'Invalid data'}), 400
        bottle.brand = brand
        bottle.source = source
        bottle.location = location
        bottle.rating = rating
        bottle.save()
        return jsonify(model_to_dict(bottle)), 200
    elif request.method == 'DELETE':
        if bottle:
            bottle.delete_instance()
            return '', 204
        else:
            return jsonify({'error': 'Bottle not found'}), 404

# Run our application, by default on port 5000
app.run(debug=True)
