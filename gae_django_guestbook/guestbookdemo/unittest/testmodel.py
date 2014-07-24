__author__ = 'NhatHV'

from datetime import datetime

from google.appengine.ext import ndb

from guestbookdemo.models import Greeting, Guestbook
from guestbookdemo.appconstants import AppConstants

class TestModelGreeting:

    def test_get_key_from_name_with_right_app_name(self):
        x = ndb.Key('guestbookdemo',"1")
        assert x == Greeting.get_key_from_name("1")

    def test_get_key_from_name_with_wrong_app_name(self):
        x = ndb.Key('guestbook',"1")
        assert x != Greeting.get_key_from_name("1")

    def test_to_dict_with_right_data(self):
        greeting = Greeting()
        greeting.author = "author"
        greeting.content = "content"
        greeting.date = datetime.strptime('2014-07-14 01:11 +0000', "%Y-%m-%d %H:%M +0000")
        greeting.updated_by = "updated by"
        greeting.updated_date = datetime.strptime('2014-07-14 05:55 +0000', "%Y-%m-%d %H:%M +0000")

        greeting.put()

        test_dict = {
            'id' : greeting.key.id(),
            'author' : "author",
            'content' : "content",
            'date' : "2014-07-14 01:11 +0000",
            'updated_by' : "updated by",
            'updated_date' : "2014-07-14 05:55 +0000"
        }

        assert test_dict == greeting.to_dict()

    def test_to_dict_with_wrong_id(self):
        greeting = Greeting()
        greeting.author = "author"
        greeting.content = "content"
        greeting.date = datetime.strptime('2014-07-14 01:11 +0000', "%Y-%m-%d %H:%M +0000")
        greeting.updated_by = "updated by"
        greeting.updated_date = datetime.strptime('2014-07-14 05:55 +0000', "%Y-%m-%d %H:%M +0000")

        greeting.put()

        test_dict = {
            'id' : 111,
            'author' : "author",
            'content' : "content",
            'date' : "2014-07-14 01:11 +0000",
            'updated_by' : "updated by",
            'updated_date' : "2014-07-14 05:55 +0000"
        }

        assert test_dict != greeting.to_dict()

    def test_to_dict_with_wrong_author(self):
        greeting = Greeting()
        greeting.author = "author"
        greeting.content = "content"
        greeting.date = datetime.strptime('2014-07-14 01:11 +0000', "%Y-%m-%d %H:%M +0000")
        greeting.updated_by = "updated by"
        greeting.updated_date = datetime.strptime('2014-07-14 05:55 +0000', "%Y-%m-%d %H:%M +0000")

        greeting.put()

        test_dict = {
            'id' : greeting.key.id(),
            'author' : "wrong_author",
            'content' : "content",
            'date' : "2014-07-14 01:11 +0000",
            'updated_by' : "updated by",
            'updated_date' : "2014-07-14 05:55 +0000"
        }

        assert test_dict != greeting.to_dict()


class TestModelGuestbook:

    def test_put_greeting_with_data(self):
        greeting = Guestbook.put_greeting_with_data(AppConstants.get_default_guestbook_name(),
                                                    "author",
                                                    "content")

        assert greeting != None

    def test_get_lastest_greeting_with_undefine_guestbook_name(self):
        greeting = Guestbook.put_greeting_with_data(AppConstants.get_default_guestbook_name(),
                                                    "author",
                                                    "content")
        greetings = Guestbook.get_lastest_greeting("undefine_guesbook_name",
                                                   10)

        assert greetings != None and greetings == []

    def test_get_lastest_greeting_with_defined_guestbook_name(self):
        greeting = Guestbook.put_greeting_with_data(AppConstants.get_default_guestbook_name(),
                                                    "author",
                                                    "content")
        greetings = Guestbook.get_lastest_greeting(AppConstants.get_default_guestbook_name(),
                                                   10)

        assert greetings != None and greetings != []