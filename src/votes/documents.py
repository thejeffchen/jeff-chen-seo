from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Integer


connections.create_connection()

class ProfileDocument(DocType):
    name = Text()
    city = Text()
    state = Text()
    country = Text()
    job_title = Text()
    company = Text()
    id = Integer()

    class Meta:
        index = 'profile'
