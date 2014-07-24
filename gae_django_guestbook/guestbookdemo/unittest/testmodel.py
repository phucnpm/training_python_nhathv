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

        assert greeting is not None and greeting.author == "author"

    def test_get_lastest_greeting_with_defined_guestbook_name(self):
        greeting = Guestbook.put_greeting_with_data(AppConstants.get_default_guestbook_name(),
                                                    "author",
                                                    "content")
        greetings = Guestbook.get_lastest_greeting(AppConstants.get_default_guestbook_name(),
                                                   10)

        assert greetings is not None and greetings != []

    def test_get_lastest_greeting_with_undefined_guestbook_name(self):
        greeting = Guestbook.put_greeting_with_data(AppConstants.get_default_guestbook_name(),
                                                    "author",
                                                    "content")
        greetings = Guestbook.get_lastest_greeting("undefine_guesbook_name",
                                                   10)

        assert greetings is not None and greetings == []

    def test_get_page_with_no_cursor(self):
        greeting = Guestbook.put_greeting_with_data(AppConstants.get_default_guestbook_name(),
                                                    "author",
                                                    "content")
        items, nextcurs, more = Guestbook.get_page(AppConstants.get_default_guestbook_name(),
                                                   10,
                                                   None)
        assert items is not None and nextcurs is not None and more is False

    def test_get_page_with_right_cursor(self):
        greeting = Guestbook.put_greeting_with_data(AppConstants.get_default_guestbook_name(),
                                                    "author",
                                                    "content")
        greeting_2 = Guestbook.put_greeting_with_data(AppConstants.get_default_guestbook_name(),
                                                    "author",
                                                    "content")
        items_tmp, nextcurs_tmp, more_tmp = Guestbook.get_page(AppConstants.get_default_guestbook_name(),
                                                   1,
                                                   None)

        items, nextcurs, more = Guestbook.get_page(AppConstants.get_default_guestbook_name(),
                                                   10,
                                                   nextcurs_tmp.urlsafe())

        assert items is not None and nextcurs is not None and more is False

    def test_get_page_with_wrong_cursor(self):
        greeting = Guestbook.put_greeting_with_data(AppConstants.get_default_guestbook_name(),
                                                    "author",
                                                    "content")
        items, nextcurs, more = Guestbook.get_page(AppConstants.get_default_guestbook_name(),
                                                   10,
                                                   "wrong_cursor")
        assert items is None and nextcurs is None and more is None

    def test_get_page_with_right_page_size(self):
        greeting = Guestbook.put_greeting_with_data(AppConstants.get_default_guestbook_name(),
                                                    "author",
                                                    "content")
        greeting_2 = Guestbook.put_greeting_with_data(AppConstants.get_default_guestbook_name(),
                                                    "author",
                                                    "content")
        items, nextcurs, more = Guestbook.get_page(AppConstants.get_default_guestbook_name(),
                                                   10,
                                                   None)
        assert items is not None and len(items) == 2

    def test_get_page_with_wrong_page_size(self):
        greeting = Guestbook.put_greeting_with_data(AppConstants.get_default_guestbook_name(),
                                                    "author",
                                                    "content")
        greeting_2 = Guestbook.put_greeting_with_data(AppConstants.get_default_guestbook_name(),
                                                    "author",
                                                    "content")
        items, nextcurs, more = Guestbook.get_page(AppConstants.get_default_guestbook_name(),
                                                   10,
                                                   None)
        assert items is not None and len(items) != 3

    def test_get_lastest_greeting_with_number_over_size(self):
        for i in range(0, 3, 1):
            greeting = Guestbook.put_greeting_with_data(AppConstants.get_default_guestbook_name(),
                                                    "author",
                                                    "content")
        greetings = Guestbook.get_lastest_greeting(AppConstants.get_default_guestbook_name(),
                                                   10)
        assert len(greetings) == 3

    def test_get_lastest_greeting_with_number_in_size(self):
        for i in range(0, 20, 1):
            greeting = Guestbook.put_greeting_with_data(AppConstants.get_default_guestbook_name(),
                                                    "author",
                                                    "content")
        greetings = Guestbook.get_lastest_greeting(AppConstants.get_default_guestbook_name(),
                                                   10)
        assert len(greetings) == 10

    def test_get_lastest_greeting_with_wrong_guestbook_name(self):
        for i in range(0, 20, 1):
            greeting = Guestbook.put_greeting_with_data("Undefined_guestbook_name",
                                                    "author",
                                                    "content")
        greetings = Guestbook.get_lastest_greeting(AppConstants.get_default_guestbook_name(),
                                                   10)
        assert len(greetings) == 0

    def test_get_greeting_by_id(self):
        greeting_tmp = Guestbook.put_greeting_with_data(AppConstants.get_default_guestbook_name(),
                                                    "author",
                                                    "content")
        id_tmp = greeting_tmp.key.id()

        greeting = Guestbook.get_greeting_by_id(AppConstants.get_default_guestbook_name(),
                                                id_tmp)

        assert greeting is not None and greeting == greeting_tmp

    def test_get_greeting_by_id_with_wrong_greeting_id(self):
        greeting_tmp = Guestbook.put_greeting_with_data(AppConstants.get_default_guestbook_name(),
                                                    "author",
                                                    "content")

        greeting = Guestbook.get_greeting_by_id(AppConstants.get_default_guestbook_name(),
                                                123456789)

        assert greeting is None