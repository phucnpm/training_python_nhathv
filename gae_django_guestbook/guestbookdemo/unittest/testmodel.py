__author__ = 'NhatHV'

from datetime import datetime

from google.appengine.ext import ndb
from guestbookdemo.models import Greeting


class TestModelGreeting:

    def test_get_key_from_name_one(self):
        x = ndb.Key('guestbookdemo',"1")
        assert x == Greeting.get_key_from_name("1")

    def test_get_key_from_name_two(self):
        x = ndb.Key('guestbook',"1")
        assert x != Greeting.get_key_from_name("1")

    def test_to_dict_one(self):
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

        assert test_dict == greeting._to_dict()

    def test_to_dict_two(self):
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

        assert test_dict != greeting._to_dict()