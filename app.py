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

@app.route('/')
def index():
    return "Hello, world!"

Bottle(brand='Arrowhead', source='Springwater', location='San Bernadino, CA', ph=7.93).save()
Bottle(brand='Poland Spring', source='Springwater', location='Poland Spring, ME', ph=6.4).save()
Bottle(brand='Sparkletts', source='Artesian', location='Various', ph=6.9).save()
Bottle(brand='Evian', source='Springwater', location='Evian, France', ph=7.2).save()
# Run our application, by default on port 5000
app.run(debug=True)
