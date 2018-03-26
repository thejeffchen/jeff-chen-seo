from django.contrib import sitemaps
from django.urls import reverse
from votes.models import Profile


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['votes:index']

    def location(self, item):
        return reverse(item)


class ProfileSitemap(sitemaps.Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return Profile.objects.all()
