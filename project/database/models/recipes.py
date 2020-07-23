from sqlalchemy import Column, Integer, String
from database.database import Base

class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)
    type = Column(String)
    ingredients = Column(String)
    imageURL = Column(String)
    provider = Column(String)

    def __init__(self, name="", url="", type="", ingredients="", imageURL="", provider=""):
        self.name = name
        self.url = url
        self.type = type
        self.ingredients = ingredients
        self.imageURL = imageURL
        self.provider = provider

    def __repr__(self):
        return '<Recipe %r>' % (self.name)
"""
class RecipeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'url', 'type', 'ingredients', 'imageURL', 'provider')
"""
