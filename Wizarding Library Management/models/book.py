import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db

class Books(db.Model):
    __tablename__ = "Books"

    book_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(), nullable=False, unique=True)
    author = db.Column(db.String())
    subject = db.Column(db.String())
    rarity_level = db.Column(db.Integer())
    magical_properties = db.Column(db.String())
    available = db.Column(db.Boolean(), default=True)

    school_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Magical_Schools.school_id"), nullable=False)


    def __init__(self, title, school_id, author, subject, rarity_level, magical_properties, available=True):
        self.title = title
        self.school_id = school_id
        self.author = author
        self.subject = subject
        self.rarity_level = rarity_level
        self.magical_properties = magical_properties
        self.available = available