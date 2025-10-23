import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db

class Companies(db.Model):
  __tablename__ = "Companies"

  company_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
company_name = db.Column(db.String(), nullable=False)