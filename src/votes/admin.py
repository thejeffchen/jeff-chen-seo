from django.contrib import admin
from django.contrib.sessions.models import Session

from .models import Profile, Vote, Rank


class VotesInline(admin.TabularInline):
    model = Vote


class ProfileAdmin(admin.ModelAdmin):
    inlines = [VotesInline]
    list_display = ('id', 'name', 'profile_image', 'prof_id', 'city', 'state', 'job_title', 'company', )
    list_filter = ['state']
    search_fields = ['id', 'name', 'city', 'state', 'job_title', 'company']
    list_editable = ['name', 'profile_image', 'prof_id', 'city', 'state', 'job_title', 'company', ]


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']


class VoteAdmin(admin.ModelAdmin):
    list_display = ('voted_for', 'ip_address', 'dt_voted', 'vote_value')
    list_filter = ('dt_voted', 'voted_for', 'vote_value')
    search_fields = ['voted_for__name', 'voted_for__city', 'voted_for__state',
                     'voted_for__job_title', 'voted_for__company', 'ip_address']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Rank)
