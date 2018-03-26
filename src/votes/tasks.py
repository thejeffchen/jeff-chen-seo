from .models import Profile
from .documents import ProfileDocument

from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch


def bulk_indexing():
    ProfileDocument.init()
    es = Elasticsearch()
    bulk(client=es,
         actions=(p.indexing() for p in Profile.objects.all().iterator()))

def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)