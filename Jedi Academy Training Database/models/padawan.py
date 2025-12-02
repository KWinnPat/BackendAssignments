import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db

class Padawans(db.Model):
    __tablename__ = "Padawans"

    padawan_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    master_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Masters.master_id'), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Users.user_id'), nullable=False)
    species_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Species.species_id'), nullable=False)
    padawan_name = db.Column(db.String(), nullable=False, unique=True)
    age = db.Column(db.Integer(), nullable=True)
    training_level = db.Column(db.Integer(), nullable=True)
    graduation_date = db.Column(db.DateTime())

    master = db.relationship("Masters", foreign_keys='[Masters.master_id]', back_populates='padawans')
    species = db.relationship("Species", foreign_keys='[Species.species_id]', back_populates='users')

    def __init__(self, master_id, user_id, species_id, padawan_name, age, training_level, graduation_date):
        self.master_id = master_id
        self.user_id = user_id
        self.species_id = species_id
        self.padawan_name = padawan_name
        self.age = age
        self.training_level = training_level
        self.graduation_date = graduation_date

    def new_padawan_obj():
        return Padawans('', '', '', '', '', '', '')
    
class PadawansSchema(ma.schema):
    class Meta:
        fields = ['padawan_id', 'user_id', 'padawan_name', 'age', 'training_level', 'graduation_date', 'master', 'species']

    padawan_id = ma.fields.UUID()
    user_id = ma.fields.UUID()
    padawan_name = ma.fields.String(required=True)
    age = ma.fields.Integer(allow_none=True)
    training_level = ma.fields.Integer(allow_none=True)
    graduation_date = ma.fields.DateTime(allow_none=True)
    master = ma.fields.Nested('MastersSchema', exclude=['padawans'])
    species = ma.fields.Nested('SpeciesSchema', exclude=['users'])

padawan_schema = PadawansSchema()
padawans_schema = PadawansSchema(many=True)