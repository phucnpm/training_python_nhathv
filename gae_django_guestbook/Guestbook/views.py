import urllib

from google.appengine.api import users

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from guestbook.models import Guestbook

DEFAULT_NUMBER_OF_GREETING = 10


class MainPageView(TemplateView):
    template_name = "guestbook/main_page.html"

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)

        # get guestbook_name
        guestbook_name = self.request.GET.get('guestbook_name', Guestbook.get_default_name())

        # get list of Greeting
        greetings = self.get_queryset(DEFAULT_NUMBER_OF_GREETING)

        # create login/logout url
        if users.get_current_user():
            url = users.create_logout_url(self.request.get_full_path())
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.get_full_path())
            url_linktext = 'Login'

        context['guestbook_name'] = guestbook_name
        context['greetings'] = greetings
        context['url'] = url
        context['url_linktext'] = url_linktext

        return context

    def get_queryset(self, number_of_greeting):
        guestbook_name = self.request.GET.get('guestbook_name', Guestbook.get_default_name())
        greetings = Guestbook.get_lastest_greeting(guestbook_name, number_of_greeting)

        return greetings

    def post(self, request):
        guestbook_name = request.POST.get('guestbook_name')
        if users.get_current_user():
            greeting_author = users.get_current_user().nickname()
        else:
            greeting_author = None
        greeting_content = request.POST.get('content')

        Guestbook.put_greeting_with_data(guestbook_name, greeting_author, greeting_content)

        return HttpResponseRedirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))