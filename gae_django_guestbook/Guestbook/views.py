import logging
import urllib

from google.appengine.api import users, memcache

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from guestbook.models import Guestbook


class MainPageView(TemplateView):
    template_name = "guestbook/main_page.html"

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)

        # get guestbook_name
        guestbook_name = self.request.GET.get('guestbook_name', 'default_guestbook')
        context['guestbook_name'] = guestbook_name

        # get list of Greeting
        greetings = memcache.get('%s:greetings' % guestbook_name)
        if greetings is None:
            greetings = self.get_queryset()
            if not memcache.add('%s:greetings' % guestbook_name, greetings, 3600 * 24 * 30):
                logging.error('Memcache set failed.')

        context['greetings'] = greetings

        # create login/logout url
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
        guestbook = Guestbook()
        greetings = guestbook.get_lastest_greeting(guestbook_name, 10)

        return greetings

    def post(self, request):
        guestbook_name = request.POST.get('guestbook_name')
        if users.get_current_user():
            greeting_author = users.get_current_user().nickname()
        else:
            greeting_author = None
        greeting_content = request.POST.get('content')

        guestbook = Guestbook()
        guestbook.put_greeting_with_data(guestbook_name, greeting_author, greeting_content)

        # clear cache
        memcache.delete('%s:greetings' % guestbook_name)

        return HttpResponseRedirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))