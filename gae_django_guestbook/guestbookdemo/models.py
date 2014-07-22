import logging, datetime

from google.appengine.ext import ndb
from google.appengine.api import memcache

from guestbookdemo.appconstants import AppConstants


class Greeting(ndb.Model):
    author = ndb.StringProperty()
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    updated_by = ndb.StringProperty()
    updated_date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def get_key_from_name(cls, guestbook_name=None):
        return ndb.Key('guestbookdemo', guestbook_name or AppConstants.get_default_guestbook_name())


class Guestbook:

    @classmethod
    def get_lastest_greeting(cls, guestbook_name, number_of_greeting):
        greetings = memcache.get('%s:greetings' % guestbook_name)
        if greetings is None:
            guestbook_key = Greeting.get_key_from_name(guestbook_name)
            greetings_query = Greeting.query(
                ancestor=guestbook_key).order(-Greeting.date)
            greetings = greetings_query.fetch(number_of_greeting)

            if not memcache.add('%s:greetings' % guestbook_name, greetings,
                                AppConstants.get_default_cache_time()):
                logging.error('Memcache set failed.')

        return greetings

    @classmethod
    def put_greeting_with_data(cls, guestbook_name, greeting_author, greeting_content):
        guestbook_key = Greeting.get_key_from_name(guestbook_name)

        @ndb.transactional
        def put_greeting_to_db():
            greeting = Greeting(parent=guestbook_key)
            greeting.author = greeting_author
            greeting.content = greeting_content

            # save object
            greeting.put()

            # clear cache
            memcache.delete('%s:greetings' % guestbook_name)

            return greeting

        new_greeting = put_greeting_to_db()

        return new_greeting

    @classmethod
    def delete_greeting_by_id(cls, guestbook_name, greeting_id):
        key = ndb.Key('guestbookdemo', guestbook_name, Greeting, int(greeting_id))
        if key:
            greeting = key.get()

            if greeting:
                key.delete()

                # clear cache
                memcache.delete('%s:greetings' % guestbook_name)
                return True
            else:
                return False

    @classmethod
    def get_greeting_by_id(cls, guestbook_name, greeting_id):
        key = ndb.Key('guestbookdemo', guestbook_name,
                      Greeting, int(greeting_id))
        if key:
            greeting = key.get()
            return greeting
        else:
            return None

    @classmethod
    def update_greeting_by_id(cls, guestbook_name, greeting_id, greeting_content, updated_by):
        key = ndb.Key('guestbookdemo', guestbook_name,
                      Greeting, int(greeting_id))
        if key:
            @ndb.transactional
            def update_greeting(greeting_content):
                greeting = key.get()
                greeting.content = greeting_content
                greeting.updated_by = updated_by
                greeting.updated_date = datetime.datetime.now()

                greeting.put()

                # clear cache
                memcache.delete('%s:greetings' % guestbook_name)

                return greeting

            updated_greeting = update_greeting(greeting_content)

            return updated_greeting
        else:
            return None
