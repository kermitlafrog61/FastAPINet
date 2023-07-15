from core.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Post(Base):
    """
    Post table
    """
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
