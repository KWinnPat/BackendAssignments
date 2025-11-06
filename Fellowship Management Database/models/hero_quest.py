from db import db

class HeroQuests(db.Model):
    __tablename__ = "HeroQuests"
    
    hero_id = db.Column(db.ForeignKey('Heroes.hero_id', ondelete='CASCADE'), primary_key=True)
    quest_id = db.Column(db.ForeignKey('Quests.quest_id', ondelete='CASCADE'), primary_key=True)
    date_joined = db.Column(db.DateTime(), nullable=True)