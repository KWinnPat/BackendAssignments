import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db

class Quests(db.Model):
    __tablename__ = "Quests"

    quest_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location_id = db.Column(db.ForeignKey('Realms.realm_id', ondelete='SET NULL'), nullable=True)
    quest_name = db.Column(db.String(), nullable=False, unique=True)
    difficulty = db.Column(db.String(), nullable=True)
    reward_gold = db.Column(db.Integer, nullable=True)
    is_completed = db.Column(db.Boolean, default=False)

    location = db.relationship("Realms", foreign_keys='[Quests.location_id]', back_populates='quests')
    heroes = db.relationship("Heroes", secondary="HeroQuests", back_populates='quests')

    def __init__(self, location_id, quest_name, difficulty=None, reward_gold=None, is_completed=False):
        self.location_id = location_id
        self.quest_name = quest_name
        self.difficulty = difficulty
        self.reward_gold = reward_gold
        self.is_completed = is_completed
        
    def new_quest_obj():
        return Quests(None, '', None, None, False)
    
class QuestsSchema(ma.Schema):
    class Meta:
        fields = ['quest_id', 'location', 'quest_name', 'difficulty', 'reward_gold', 'is_completed', 'heroes']

    quest_id = ma.fields.UUID()
    quest_name = ma.fields.String(required=True)
    difficulty = ma.fields.String(allow_none=True)
    reward_gold = ma.fields.Integer(allow_none=True)
    is_completed = ma.fields.Boolean() 

    location = ma.fields.Nested("RealmsSchema", exclude=['quests'])
    heroes = ma.fields.Nested("HeroesSchema", many=True, exclude=['quests'])

quest_schema = QuestsSchema()
quests_schema = QuestsSchema(many=True)