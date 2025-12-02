import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db

class Users(db.Model):
    __tablename__ = "Users"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    temple_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Temples.temple_id'), nullable=False)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    force_rank = db.Column(db.String(), nullable=True)
    midi_count = db.Column(db.Integer(), nullable=True)
    joined_date = db.Column(db.DateTime())
    is_active = db.Column(db.Boolean(), default=True)

    temple = db.relationship('Temples', back_populates='users')
    auth = db.relationship('AuthTokens', back_populates='user')

    def __init__(self, temple_id, username, email, password, force_rank, midi_count, joined_date, is_active=True):
        self.temple_id = temple_id
        self.username = username
        self.email = email
        self.password = password
        self.force_rank = force_rank
        self.midi_count = midi_count
        self.joined_date = joined_date
        self.is_active = is_active

    def new_user_obj():
        return Users('', '', '', '', '', '', '', True)
    
class UsersSchema(ma.Schema):
    class Meta:
        fields = ['user_id', 'username', 'email', 'password', 'force_rank', 'midi_count', 'joined_date', 'is_active', 'temple']

    user_id = ma.fields.UUID()
    username = ma.fields.String(required=True)
    email = ma.fields.String(required=True)
    password = ma.fields.String(required=True)
    force_rank = ma.fields.String(allow_none=True)
    midi_count = ma.fields.Integer(allow_none=True)
    joined_date = ma.fields.DateTime(required=True)
    is_active = ma.fields.Boolean(required=True, dump_default=True)
    temple = ma.fields.Nested('TemplesSchema', exclude=['users'])

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)