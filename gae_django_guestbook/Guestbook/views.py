import logging
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from google.appengine.api import users

from guestbook.models import Greeting

import urllib

class MainPageView(TemplateView):
    model = Greeting
    template_name = "guestbook/main_page.html"

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        context['greetings'] = self.get_queryset()
        context['guestbook_name'] = self.request.GET.get('guestbook_name', 'default_guestbook')
        if users.get_current_user():
            url = users.create_logout_url(self.request.get_full_path())
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.get_full_path())
            url_linktext = 'Login'
        context['url'] = url
        context['url_linktext'] = url_linktext

        return context

    def get_queryset(self):
        guestbook_name = self.request.GET.get('guestbook_name', 'default_guestbook')
        guestbook_key = Greeting.get_key_from_name(guestbook_name)
        greetings_query = Greeting.query(
            ancestor=guestbook_key).order(-Greeting.date)
        greetings = greetings_query.fetch(10)
        logging.warning("%s", greetings)

        return greetings

def sign_post(request):
    if request.method == 'POST':
        guestbook_name = request.POST.get('guestbook_name')
        guestbook_key = Greeting.get_key_from_name(guestbook_name)
        greeting = Greeting(parent=guestbook_key)

        if users.get_current_user():
            greeting.author = users.get_current_user().nickname()

        greeting.content = request.POST.get('content')
        greeting.put()
        return HttpResponseRedirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))
    return HttpResponseRedirect('/')
