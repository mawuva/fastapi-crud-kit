from sqlalchemy import Column, String, Text, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from fastapi_crud_kit.models import BaseModel
from fastapi_crud_kit.database.base import Base

# Association table for the many-to-many relationship between Article and Tag
article_tag = Table(
    "article_tag",
    Base.metadata,
    Column("article_id", Integer, ForeignKey("articles.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


class Article(BaseModel):
    __tablename__ = "articles"

    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)

    # Many-to-one: an article belongs to one category
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    category = relationship("Category", back_populates="articles")

    # Many-to-many: an article has many tags
    tags = relationship("Tag", secondary="article_tag", back_populates="articles")
