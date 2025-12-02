import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db

class AuthTokens(db.Model):
    __tablename__ = "AuthTokens"

    auth_token_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Users.user_id'), nullable=False)
    expiration = db.Column(db.DateTime(), nullable=False)

    user = db.relationship('Users', back_populates='auth')

    def __init__(self, user_id, expiration):
        self.user_id = user_id
        self.expiration = expiration

class AuthTokenSchema(ma.Schema):
    class Meta:
        fields = ['auth_token_id', 'expiration', 'user']

    auth_token_id = ma.fields.UUID()
    expiration = ma.fields.DateTime(required=True)
    user = ma.fields.Nested('UsersSchema', only=('user_id', 'email', 'first_name', 'last_name', 'role', 'active'))

auth_token_schema = AuthTokenSchema()