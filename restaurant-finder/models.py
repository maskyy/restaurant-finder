import sys
from datetime import datetime
from uuid import uuid4

from peewee import (
    FloatField,
    ForeignKeyField,
    IntegerField,
    Model,
    TextField,
)
from playhouse.postgres_ext import (
    DateTimeTZField,
    JSONField,
    PostgresqlExtDatabase,
    UUIDField,
)

from .config import CONFIG
from .log import log

db = PostgresqlExtDatabase(
    CONFIG["POSTGRES_DB"],
    user=CONFIG["POSTGRES_USER"],
    password=CONFIG["POSTGRES_PASSWORD"],
    host=CONFIG["POSTGRES_HOST"],
    port=CONFIG["POSTGRES_PORT"],
)


def tznow() -> datetime:
    return datetime.astimezone(datetime.now())


class BaseModel(Model):
    class Meta:
        database = db
        only_save_dirty = True


class Query(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    name = TextField()
    latitude = FloatField()
    longitude = FloatField()
    created_at = DateTimeTZField(default=tznow)

    class Meta:
        table_name = "queries"


class NaturalQuery(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    user_query = TextField()
    parsed = JSONField(null=True)
    query = ForeignKeyField(Query, null=True)
    created_at = DateTimeTZField(default=tznow)

    class Meta:
        table_name = "natural_queries"


class Restaurant(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    query = ForeignKeyField(Query, backref="restaurants")
    name = TextField()
    latitude = FloatField()
    longitude = FloatField()
    url = TextField(null=True)
    rating = FloatField(null=True)
    review_count = IntegerField(null=True)
    created_at = DateTimeTZField(default=tznow)

    class Meta:
        table_name = "restaurants"


def create_tables():
    try:
        db.connect()
    except Exception as e:
        log.critical("Error connecting to database: %s %s", type(e), e)
        sys.exit(1)
    models = [
        NaturalQuery,
        Query,
        Restaurant,
    ]
    db.create_tables(models)
