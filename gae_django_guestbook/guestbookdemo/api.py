__author__ = 'NhatHV'

import json, logging

from google.appengine.api import users
from google.appengine.api.labs import taskqueue
from google.appengine.datastore.datastore_query import Cursor
from google.appengine.api import datastore_errors

from django.http import HttpResponse
from django.views.generic import FormView
from django.views.generic.detail import DetailView

from guestbookdemo.appconstants import AppConstants
from guestbookdemo.models import Guestbook, Greeting
from guestbookdemo.forms import GreetingForm, EditGreetingForm


class JSONResponseMixin(object):

    def render_to_json_response(self, context):
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        return HttpResponse(content,
                            content_type='application/json',
                            **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        return json.dumps(context)


class APIListGreeting(JSONResponseMixin, FormView):
    form_class = GreetingForm
    success_url = '/'

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

    def get(self, request, *args, **kwargs):
        try:
            Cursor(urlsafe=self.request.GET.get('cursor'))
        except datastore_errors.BadValueError:
            return HttpResponse(status=404)

        return super(APIListGreeting, self).get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        guestbook_name = self.kwargs.get('guestbook_name',
                                         AppConstants.get_default_guestbook_name())
        cursor_str = self.request.GET.get('cursor', None)

        # get list of Greeting, next_cursor, is_more
        greetings, next_cursor, is_more = self.get_queryset(guestbook_name, 20, cursor_str)

        greetings_dict = [greeting._to_dict() for greeting in greetings]

        data = {}
        data['greetings'] = greetings_dict
        if next_cursor:
            data['cursor']= next_cursor.urlsafe()
        data['is_more'] = is_more

        return data

    def get_queryset(self,
                     guestbook_name=AppConstants.get_default_guestbook_name(),
                     number_of_greeting=AppConstants.get_default_number_of_greeting(),
                     curs_str=None):

        greetings, nextcurs, more = Guestbook.get_page(guestbook_name, number_of_greeting, curs_str)

        return greetings, nextcurs, more

    def form_valid(self, form):
        new_greeting = form.save_greeting()
        if new_greeting:
            if users.get_current_user():
                user_email = users.get_current_user().email()
            else:
                user_email = "Anonymous"

            taskqueue.add(url='/send_email/',
                          method='GET',
                          params={'user_email': user_email})

            return HttpResponse(status=204)
        else:
            return HttpResponse(status=404)

    def form_invalid(self, form):

        return HttpResponse(status=404)


class APIGreetingDetail(JSONResponseMixin, DetailView, FormView):
    object = Greeting
    form_class = EditGreetingForm
    success_url = "/"

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

    def get_object(self, queryset=None):
        guestbook_name = self.kwargs.get('guestbook_name',
                                         AppConstants.get_default_guestbook_name())
        greeting_id = self.kwargs.get('greeting_id', -1)

        greeting = Guestbook.get_greeting_by_id(guestbook_name, greeting_id)
        if greeting:
            return greeting
        else:
            return None

    def get_context_data(self, **kwargs):
        if self.object:
            data = self.object._to_dict()
        else:
            data = {"error":"wrong greeting id"}

        return data

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        logging.warning("APIGreetingDetail - POST")
        super(APIGreetingDetail, self).post(self, request, *args, **kwargs)

    def form_valid(self, form):
        if form.update_greeting():
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=204)

    def form_invalid(self, form):
        return HttpResponse(status=404)