import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db

class Realms(db.Model):
    __tablename__ = "Realms"

    realm_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    realm_name = db.Column(db.String(), nullable=False, unique=True)
    ruler = db.Column(db.String(), nullable=True)

    locations = db.relationship("Locations", back_populates='realm', cascade="all, delete")

    def __init__(self, realm_name, ruler=None):
        self.realm_name = realm_name
        self.ruler = ruler

    def new_realm_obj():
        return Realms('', None)
    
class RealmsSchema(ma.Schema):
    class Meta:
        fields = ['realm_id', 'realm_name', 'ruler', 'locations']
        
    realm_id = ma.fields.UUID()
    realm_name = ma.fields.String(required=True)
    ruler = ma.fields.String(allow_none=True)

    locations = ma.fields.Nested("LocationsSchema", many=True, exclude=['realm'])

realm_schema = RealmsSchema()
realms_schema = RealmsSchema(many=True)