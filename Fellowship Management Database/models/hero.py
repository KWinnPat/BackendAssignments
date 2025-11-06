import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db

class Heroes(db.Model):
    __tablename__ = "Heroes"

    hero_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    race_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Races.race_id'), nullable=False)
    hero_name = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=True)
    health_points = db.Column(db.Integer, nullable=True)
    is_alive = db.Column(db.Boolean, default=True)

    race = db.relationship("Races", foreign_keys='[Heroes.race_id]', back_populates='heroes')
    quests = db.relationship("Quests", secondary="HeroQuests", back_populates='heroes')
    abilities = db.relationship("Abilities", foreign_keys='[Abilities.hero_id]', back_populates='hero', cascade="all")

    def __init__(self, race_id, hero_name, age=None, health_points=None, is_alive=True):
        self.race_id = race_id
        self.hero_name = hero_name
        self.age = age
        self.health_points = health_points
        self.is_alive = is_alive

    def new_hero_obj():
        return Heroes('', '', None, None, True)
    
class HeroesSchema(ma.Schema):
    class Meta:
        fields = ['hero_id', 'race', 'hero_name', 'age', 'health_points', 'abilities', 'is_alive', 'quests']
    hero_id = ma.fields.UUID()
    hero_name = ma.fields.String(required=True)
    age = ma.fields.Integer(allow_none=True)
    health_points = ma.fields.Integer(allow_none=True)
    abilities = ma.fields.Nested("AbilitiesSchema", many=True, exclude=['hero'])
    is_alive = ma.fields.Boolean() 
    race = ma.fields.Nested("RacesSchema", exclude=['heroes'])
    quests = ma.fields.Nested("QuestsSchema", many=True, exclude=['heroes'])


hero_schema = HeroesSchema()
heroes_schema = HeroesSchema(many=True)