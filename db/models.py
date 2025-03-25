from sqlalchemy import BigInteger, Column, String, Boolean
from sqlalchemy.orm import declarative_base, validates

Base = declarative_base()

class Register(Base):
    __tablename__ = "registrations"

    id = Column(BigInteger, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, index=True)
    phone = Column(String, index=True)
    telegram = Column(String, index=True)
    company = Column(String, index=True, nullable=True)
    agree_personal_data = Column(Boolean, index=True)
    agree_terms = Column(Boolean, index=True)

    @validates('agree_personal_data', 'agree_terms')
    def validate_agreements(self, key, value):
        if not value:
            raise ValueError("Необходимо согласиться с условиями")
        return value


