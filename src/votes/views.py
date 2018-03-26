from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from ipware.ip import get_real_ip, get_ip
from send_email.forms import ContactForm

from .documents import ProfileDocument
from .forms import JeffChenForm
from .models import Profile, Vote


def index(request, profile_id=None):
    query = request.GET.get('q')
    list_of_jeff_chens = Profile.objects.all().order_by(
        '-votes', '-country', 'profile_image')
    popular_jeff_chens = []
    form = JeffChenForm()
    contact_us_form = ContactForm()
    single_profile = False
    message = False
    error = False
    search_hits = 0
    count_all_jeff_chens = len(list_of_jeff_chens)

    if request.GET.get('message') == 'sent-email':
        message = 'Email Sent!'
    if request.GET.get('message') == 'not-valid-email':
        error = 'Unfortunately your email address did not work! Can you check again?'
    if request.GET.get('added-jeff-chen') == 'true':
        message = 'Jeff Chen Successfully Added!'
    if request.GET.get('added-jeff-chen') == 'false':
        error = ('Can you make sure all fields are filled out, including uploading an image?'
                 'Unfortunately we could not add this Jeff Chen :(')

    if profile_id:
        single_profile = True
        list_of_jeff_chens = Profile.objects.all().filter(
            id=profile_id)

        popular_jeff_chens = Profile.objects.all().order_by(
            '-votes', '-country', 'profile_image')

        paginator = Paginator(popular_jeff_chens, 10)
        page = request.GET.get('page', 1)

        try:
            popular_jeff_chens = paginator.page(page)
        except PageNotAnInteger:
            popular_jeff_chens = paginator.page(1)
        except EmptyPage:
            popular_jeff_chens = paginator.page(paginator.num_pages)

    if query:
        elastic_search_query = ProfileDocument.search().query("multi_match",
                                                              query=query,
                                                              fields=[
                                                                  'name',
                                                                  'city',
                                                                  'state',
                                                                  'country',
                                                                  'job_title',
                                                                  'company',
                                                              ])
        hit_array = []
        for each_hit in elastic_search_query.scan():
            hit_array.append(each_hit.id)

        list_of_jeff_chens = Profile.objects.all().filter(
            pk__in=hit_array).order_by(
            '-votes', '-country', 'profile_image')

        popular_jeff_chens = Profile.objects.all().order_by(
            '-votes', '-country', 'profile_image')

        paginator = Paginator(popular_jeff_chens, 10)
        page = request.GET.get('page', 1)

        try:
            popular_jeff_chens = paginator.page(page)
        except PageNotAnInteger:
            popular_jeff_chens = paginator.page(1)
        except EmptyPage:
            popular_jeff_chens = paginator.page(paginator.num_pages)

    search_hits = len(list_of_jeff_chens)

    paginator = Paginator(list_of_jeff_chens, 10)
    page = request.GET.get('page', 1)

    try:
        list_of_jeff_chens = paginator.page(page)
    except PageNotAnInteger:
        list_of_jeff_chens = paginator.page(1)
    except EmptyPage:
        list_of_jeff_chens = paginator.page(paginator.num_pages)

    if settings.DEBUG:
        ip = str(get_ip(request))
    else:
        ip = str(get_real_ip(request))

    list_of_every_jeff_chen_ip_has_voted = Profile.objects.all().filter(
        vote__ip_address=ip)

    context = {
        'list_of_jeff_chens': list_of_jeff_chens,
        'list_of_every_jeff_chen_ip_has_voted': list_of_every_jeff_chen_ip_has_voted,
        'popular_jeff_chens': popular_jeff_chens,
        'form': form,
        'google_maps_api_key': 'AIzaSyD4xHCrwMPa32MNNRR7EjbqCTEnJSThHPo',
        'single_profile': single_profile,
        'contact_us_form': contact_us_form,
        'message': message,
        'error': error,
        'query': query,
        'search_hits': search_hits,
        'count_all_jeff_chens': count_all_jeff_chens,
    }

    return render(request, 'votes/index.html', context)


def vote(request, profile_id):
    if settings.DEBUG:
        ip = str(get_ip(request))
    else:
        ip = str(get_real_ip(request))

    profile = get_object_or_404(Profile, pk=profile_id)
    votes = Vote.objects.filter(ip_address=ip, voted_for=profile_id)

    context = {
        'profile': profile,
        'error_message': "You did not select a Jeff Chen to vote for",
        'ip': ip,
        'votes': votes,
    }

    if votes.count() == 0:
        try:
            selected_jeff_chen = Profile.objects.get(pk=request.POST['vote'])
        except (KeyError, Profile.DoesNotExist):
            return render(request, 'votes/index.html', context)

        if ip is not None:
            v = Vote(voted_for=profile, ip_address=ip, vote_value=1)
            v.save()

            new_key = ip + ":" + profile_id
            cache.set(new_key, "True")

        else:
            v = Vote(voted_for=profile, vote_value=1)
            v.save()

        selected_jeff_chen.votes = F('votes') + 1
        selected_jeff_chen.save()

    else:
        print("You have already voted for " + str(profile_id))

    if request.GET.get('page'):
        print('hello')
        page = request.GET.get('page')
        return HttpResponseRedirect(
            reverse('votes:index') + '?page=' + page)

    return HttpResponseRedirect(reverse('votes:index'))


def add(request):
    if settings.DEBUG:
        ip = str(get_ip(request))
    else:
        ip = str(get_real_ip(request))

    if request.method == "POST":
        form = JeffChenForm(request.POST, request.FILES)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.added_by = ip
            profile.save()
            return HttpResponseRedirect(
                reverse('votes:index') + '?added-jeff-chen=true')

    return HttpResponseRedirect(
        reverse('votes:index') + '?added-jeff-chen=false')
