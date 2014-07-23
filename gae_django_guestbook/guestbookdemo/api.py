__author__ = 'NhatHV'

import json

from google.appengine.datastore.datastore_query import Cursor

from django.http import HttpResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import DetailView

from guestbookdemo.appconstants import AppConstants
from guestbookdemo.models import Guestbook, Greeting


class JSONResponseMixin(object):

    def render_to_json_response(self, context):
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        return HttpResponse(content,
                            content_type='application/json',
                            **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        return json.dumps(context)


class APIListGreeting(JSONResponseMixin, BaseListView):

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        guestbook_name = self.kwargs.get('guestbook_name',
                                         AppConstants.get_default_guestbook_name())
        cursor_str = self.request.GET.get('cursor', None)

        # get list of Greeting, next_cursor, is_more
        greetings, next_cursor, is_more, error = self.get_queryset(guestbook_name, 20, cursor_str)

        if error:
            return {'error':404}

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

        greetings, nextcurs, more, error = Guestbook.get_page(guestbook_name, number_of_greeting, curs_str)

        return greetings, nextcurs, more, error


class APIGreetingDetail(JSONResponseMixin, DetailView):
    object = Greeting

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
            data = {"error":404}

        return data
