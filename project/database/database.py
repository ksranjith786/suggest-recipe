from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, and_, or_

engine = None
Base = declarative_base()
db_session = None

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

Session = sessionmaker(bind=engine)
ses = Session()

def initDB():
    global engine, db_session
    engine = create_engine('sqlite:///' + 'hebbars_recipes.db', convert_unicode=True, connect_args={'check_same_thread': False})
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    return db_session
# end initDB

def createRecipeDB():
    initDB()
    global Base
    Base.metadata.bind = engine
    Base.metadata.create_all(bind=engine)
# end createRecipeDB

def addRecipeToDB(name="", url="", type="", ingredients="", imageURL="", provider=""):
    recipe1 = Recipe(name=name, url=url, type=type, ingredients=ingredients, imageURL=imageURL, provider=provider)

    if db_session == None:
        initDB()
    try:
        db_session.add(recipe1)
        db_session.commit()
    except:
        print("Exception caught while adding recipe")
        return False
    return True
# end addRecipeToDB

def queryRecipeFromDB(name=""):
    #print(name)
    if db_session == None:
        initDB()
    
    #noOfRecords = 0

    try:
        look_for = '%{0}%'.format(name)
        rs = db_session.query(Recipe).filter(Recipe.name.ilike(look_for))
        #print(rs)
        #for recipe in rs:
            #print(repr(recipe))
            #noOfRecords += 1

    except:
        print("Exception caught while querying recipe")
        return None

    #print("No.of Records matched:", noOfRecords)
    return rs
# end queryRecipeFromDB

def queryIngredientsFromDB(ingredients="", combination="all"):
    #print(ingredients, combination)
    if db_session == None:
        initDB()
    
    try:
        ids = []
        for ingredient in ingredients.split(";"):
            #print(ingredient)
            look_for = '%{0}%'.format(ingredient)
            if len(ids) == 0:
                rs = db_session.query(Recipe).filter(Recipe.ingredients.ilike(look_for))
                
            else:
                rs = db_session.query(Recipe).filter(
                    and_(
                        Recipe.id.in_(ids),
                        Recipe.ingredients.ilike(look_for)                    
                        )
                    )
            
            if combination == "all":
                if len(rs) == 0:
                    print("No such recipe combination to look out for")
                    rs = None
                    break
                ids = []
                for result in rs:
                    ids.append(result.id)
            else:
                for result in rs:
                    if ids.count(result.id) == 0:
                        ids.append(result.id)
                                
        #print(ids)
        #print(rs)

    except:
        print("Exception caught while querying ingredients")
        return None

    #print("No.of Records matched:", noOfRecords)
    return rs
# end queryRecipeFromDB

def deleteRecipeFromDB(id=""):
    if db_session == None:
        initDB()
    try:
        for recipe in db_session.query(Recipe).filter(
                Recipe.id.__eq__(id)
            ).all():
                db_session.delete(recipe)
    except:
        print("Exception caught while deleting recipe")
        return False

    return True
# end  deleteRecipeFromDB