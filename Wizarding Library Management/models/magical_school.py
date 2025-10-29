import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db

class Magical_Schools(db.Model):
    __tablename__ = "Magical_Schools"

    school_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    school_name = db.Column(db.String(), nullable=False, unique=True)
    location = db.Column(db.String())
    founded_year = db.Column(db.Integer())
    headmaster = db.Column(db.String())

    wizards = db.relationship('Wizards',  back_populates='school', cascade="all, delete")

    def __init__(self, school_name, location, founded_year, headmaster):
        self.school_name = school_name
        self.location = location
        self.founded_year = founded_year
        self.headmaster = headmaster