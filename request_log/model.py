from mongoengine import Document, ListField, StringField, DateTimeField, EmbeddedDocument, EmbeddedDocumentField, BinaryField
from datetime import datetime
from flask_mongoengine import MongoEngine

db = MongoEngine()

class Base(db.Document):
    ip = StringField(required=True)
    datetime = DateTimeField(default=datetime.utcnow)

    meta = {'allow_inheritance': True}

class KeyValue(EmbeddedDocument):
    key = StringField(required=True)
    value = StringField(required=True)

class HTTP(Base):
    method = StringField(required=True)
    url = StringField(required=True)
    query_string = StringField()
    query = ListField(EmbeddedDocumentField(KeyValue))
    headers = ListField(EmbeddedDocumentField(KeyValue))
    data = BinaryField()