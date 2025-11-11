import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db

class Locations(db.Model):
    __tablename__ = "Locations"

    location_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    realm_id = db.Column(db.ForeignKey('Realms.realm_id', ondelete='CASCADE'), nullable=False)
    location_name = db.Column(db.String(), nullable=False, unique=True)
    danger_level = db.Column(db.Integer, nullable=True)

    realm = db.relationship("Realms", foreign_keys='[Locations.realm_id]', back_populates='locations')
    quests_available = db.relationship("Quests", back_populates='location', cascade="all, delete")

    def __init__(self, realm_id, location_name, danger_level=None):
        self.realm_id = realm_id
        self.location_name = location_name
        self.danger_level = danger_level    

    def new_location_obj():
        return Locations('', '', None)
    
class LocationsSchema(ma.Schema):
    class Meta:
        fields = ['location_id', 'realm', 'location_name', 'danger_level', 'quests_available']

    location_id = ma.fields.UUID()
    location_name = ma.fields.String(required=True)
    danger_level = ma.fields.Integer(allow_none=True)

    realm = ma.fields.Nested("RealmsSchema", exclude=['locations'])
    quests_available = ma.fields.Nested("QuestsSchema", many=True, exclude=['location'])

location_schema = LocationsSchema()
locations_schema = LocationsSchema(many=True)