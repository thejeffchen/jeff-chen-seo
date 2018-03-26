from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import ContactForm


def email(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            subject = 'Jeff Chen SEO: ' + subject
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            message = from_email + ': \n' + message
            try:
                send_mail(subject, message, 'contact@email.jeffchenseo.com', ['thejeffchen@gmail.com'], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect(reverse('votes:index') + '?message=sent-email')
    return HttpResponseRedirect(reverse('votes:index') + '?message=not-valid-email')


def success(request):
    return HttpResponse('Success! Thank you for your message.')