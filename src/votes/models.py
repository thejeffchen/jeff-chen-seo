from django.db import models
from django.db.models import Count

from .documents import ProfileDocument

# Create your models here.


class Profile(models.Model):
    name = models.CharField(max_length=150)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    job_title = models.CharField(max_length=200, null=True, blank=True)
    company = models.CharField(max_length=200, null=True, blank=True)
    profile_image = models.ImageField()
    votes = models.IntegerField(default=0)
    prof_id = models.IntegerField(null=True, blank=True)
    added_by = models.GenericIPAddressField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s, %s, %s' % (self.name, self.state, self.company)

    def ranking(self):
        aggregate = Profile.objects.filter(votes__gt=self.votes)\
            .aggregate(ranking=Count('votes'))
        return aggregate['ranking'] + 1

    def indexing(self):
        obj = ProfileDocument(
            meta={'id': self.id},
            name=self.name,
            city=self.city,
            state=self.state,
            country=self.country,
            job_title=self.job_title,
            company=self.company,
            id=self.id
        )
        obj.save()
        return obj.to_dict(include_meta=True)

    def get_absolute_url(self):
        return '/jeff-chen-'+str(self.id)


class Vote(models.Model):
    voted_for = models.ForeignKey(Profile)
    ip_address = models.GenericIPAddressField()
    dt_voted = models.DateTimeField('date/time voted', auto_now_add=True)
    vote_value = models.IntegerField()

    def __str__(self):
        return '%s, %s' % (self.voted_for, self.ip_address)


class Rank(models.Model):
    profile_id = models.OneToOneField(Profile)
    rank = models.IntegerField()



