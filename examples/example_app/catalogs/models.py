from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from fastapi_crud_kit.models import BaseModel


class Category(BaseModel):
    __tablename__ = "categories"

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # One-to-many: a category has many articles
    articles = relationship("Article", back_populates="category")

    def __repr__(self) -> str:
        return f"<Category {self.name}>"


class Tag(BaseModel):
    __tablename__ = "tags"

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # Many-to-many: a tag can be associated with many articles
    articles = relationship("Article", secondary="article_tag", back_populates="tags")

    def __repr__(self) -> str:
        return f"<Tag {self.name}>"
