from db import db

class Wizard_Specializations(db.Model):
    __tablename__ = "Wizard_Specializations"
    
    wizard_id = db.Column(db.ForeignKey('Wizards.wizard_id', ondelete='CASCADE'), primary_key=True)
    spell_id = db.Column(db.ForeignKey('Spells.spell_id', ondelete='CASCADE'), primary_key=True)
    proficiency_level = db.Column(db.Float(), nullable=False, default=1)
    date_learned = db.Column(db.DateTime())
    
    def __init__(self, wizard_id, spell_id, proficiency_level, date_learned):
        self.wizard_id = wizard_id
        self.spell_id = spell_id
        self.proficiency_level = proficiency_level
        self.date_learned = date_learned
    