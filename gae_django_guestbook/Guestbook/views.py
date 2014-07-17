from google.appengine.api import users

from django.views.generic.edit import FormView

from guestbook.models import Guestbook
from guestbook.forms import GreetingForm
from guestbook.appconstants import AppConstants


class MainPageView(FormView):
    template_name = "guestbook/main_page.html"
    form_class = GreetingForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)

        # get guestbook_name
        guestbook_name = self.request.GET.get('guestbook_name',
                                              AppConstants.get_default_guestbook_name())

        # get list of Greeting
        greetings = self.get_queryset()

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

    def get_queryset(self, number_of_greeting=AppConstants.get_default_number_of_greeting()):
        guestbook_name = self.request.GET.get('guestbook_name',
                                              AppConstants.get_default_guestbook_name())
        greetings = Guestbook.get_lastest_greeting(guestbook_name, number_of_greeting)

        return greetings

    def form_valid(self, form):

        form.save_greeting()

        return super(MainPageView, self).form_valid(form)