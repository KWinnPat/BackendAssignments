import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db

class Wizards(db.Model):
    __tablename__ = "Wizards"

    wizard_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    wizard_name = db.Column(db.String(), nullable=False, unique=True)
    house = db.Column(db.String())
    year_enrolled = db.Column(db.Integer())
    magical_power_level = db.Column(db.Integer())
    active = db.Column(db.Boolean(), default=True)

    school_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Magical_Schools.school_id", ondelete='CASCADE'), nullable=False)
    
    school = db.relationship("Magical_Schools", back_populates='wizards')

    def __init__(self, wizard_name, school_id, house, year_enrolled, magical_power_level, active=True):
        self.wizard_name = wizard_name
        self.school_id = school_id
        self.house = house
        self.year_enrolled = year_enrolled
        self.magical_power_level = magical_power_level
        self.active = active