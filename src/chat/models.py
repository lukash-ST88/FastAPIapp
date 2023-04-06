from database import Base
from sqlalchemy import Column, String, Integer


class Messages(Base):
    __tablename__ = 'messanges'

    id = Column(Integer, primary_key=True)
    message = Column(String)

    def as_dict(self):
        print(self.__table__.columns)
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
