import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db

class Temples(db.Model):
    __tablename__ = "Temples"

    temple_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    temple_name = db.Column(db.String(), nullable=False, unique=True)
    planet = db.Column(db.String(), nullable=False)
    master_count = db.Column(db.Integer(), nullable=True)
    padawan_limit = db.Column(db.Integer(), nullable=True)
    is_active = db.Column(db.Boolean(), default=True)

    users = db.relationship("Users", foreign_keys="[Users.temple_id]", back_populates='temple', cascade="all")

    def __init__(self, temple_name, planet, master_count, padawan_limit, is_active=True):
        self.temple_name = temple_name
        self.planet = planet
        self.master_count = master_count
        self.padawan_limit = padawan_limit
        self.is_active = is_active

    def new_temple_obj():
        return Temples('', '', '', '', True)

class TemplesSchema(ma.Schema):
    class Meta:
        fields = ['temple_id', 'temple_name', 'planet', 'master_count', 'padawan_limit', 'is_active', 'users']

    temple_id = ma.fields.UUID()
    temple_name = ma.fields.String(required=True)
    planet = ma.fields.String(required=True)
    master_count = ma.fields.Integer(allow_none=True)
    padawan_limit = ma.fields.Integer(allow_none=True)
    is_active = ma.fields.Boolean(required=True, dump_default=True)
    users = ma.fields.Nested('UsersSchema', exclude=['temple'])

temple_schema = TemplesSchema()
temples_schema = TemplesSchema(many=True)