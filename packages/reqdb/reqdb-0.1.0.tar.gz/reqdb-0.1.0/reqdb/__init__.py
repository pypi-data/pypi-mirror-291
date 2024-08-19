from reqdb.api import API
from reqdb.schemas import BaseSchema, TagSchema, TopicSchema, \
    RequirementSchema, ExtraTypeSchema, ExtraEntrySchema, CatalogueSchema, CommentSchema
from reqdb.models import Base, Tag, Topic, \
    Requirement, ExtraType, ExtraEntry, Catalogue, Comment


class ReqDB:

    api = None

    def __init__(self, fqdn, bearer, insecure: bool = False) -> None:
        ReqDB.api = API(fqdn, bearer, insecure)

    class Entity:
        endpoint: str = None
        schema: BaseSchema = None
        model: Base = None

        @classmethod
        def get(cls, id):
            return ReqDB.api.get(f"{cls.endpoint}/{id}")

        @classmethod
        def all(cls):
            return ReqDB.api.get(f"{cls.endpoint}")

        @classmethod
        def update(cls, id, data: Base):
            if not isinstance(data, cls.model):
                raise TypeError(f"Data not the correct model ({cls.model.__name__})")
            return ReqDB.api.update(f"{cls.endpoint}/{id}", cls.schema.dump(data))

        @classmethod
        def delete(cls, id):
            return ReqDB.api.delete(f"{cls.endpoint}/{id}")

        @classmethod
        def add(cls, data: Base):
            if not isinstance(data, cls.model):
                raise TypeError(f"Data not the correct model ({cls.model.__name__})")
            r = ReqDB.api.add(f"{cls.endpoint}", cls.schema.dump(data))
            return r

    class Tags(Entity):
        endpoint = "tags"
        schema = TagSchema()
        model = Tag

    class Topics(Entity):
        endpoint = "topics"
        schema = TopicSchema()
        model = Topic

    class Requirements(Entity):
        endpoint = "requirements"
        schema = RequirementSchema()
        model = Requirement

    class ExtraTypes(Entity):
        endpoint = "extraTypes"
        schema = ExtraTypeSchema()
        model = ExtraType

    class ExtraEntries(Entity):
        endpoint = "extraEntries"
        schema = ExtraEntrySchema()
        model = ExtraEntry

    class Catalogues(Entity):
        endpoint = "catalogues"
        schema = CatalogueSchema()
        model = Catalogue

    class Comment(Entity):
        endpoint = "comments"
        schema = CommentSchema()
        model = Comment

    class Coffee(Entity):
        endpoint = "coffee"
        schema = None
        model = None
