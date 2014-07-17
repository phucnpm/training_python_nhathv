import logging

from google.appengine.ext import ndb
from google.appengine.api import memcache

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'
DEFAULT_CACHE_TIME = 3600 * 24 * 30


class Greeting(ndb.Model):
    author = ndb.StringProperty()
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def get_key_from_name(cls, guestbook_name=None):
        return ndb.Key('guestbook', guestbook_name or DEFAULT_GUESTBOOK_NAME)


class Guestbook:

    @classmethod
    def get_lastest_greeting(cls, guestbook_name, number_of_greeting):
        greetings = memcache.get('%s:greetings' % guestbook_name)
        if greetings is None:
            guestbook_key = Greeting.get_key_from_name(guestbook_name)
            greetings_query = Greeting.query(
                ancestor=guestbook_key).order(-Greeting.date)
            greetings = greetings_query.fetch(number_of_greeting)

            if not memcache.add('%s:greetings' % guestbook_name, greetings, DEFAULT_CACHE_TIME):
                logging.error('Memcache set failed.')


        return greetings

    @classmethod
    def put_greeting_with_data(cls, guestbook_name, greeting_author, greeting_content):
        guestbook_key = Greeting.get_key_from_name(guestbook_name)

        greeting = Greeting(parent=guestbook_key)
        greeting.author = greeting_author
        greeting.content = greeting_content

        # save object
        greeting.put()

        # clear cache
        memcache.delete('%s:greetings' % guestbook_name)

    @classmethod
    def get_default_name(cls):
        return DEFAULT_GUESTBOOK_NAME