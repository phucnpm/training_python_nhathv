from google.appengine.ext import ndb


class Greeting(ndb.Model):
    author = ndb.StringProperty()
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def get_key_from_name(cls, guestbook_name=None):
        return ndb.Key('guestbook', guestbook_name or 'default_guestbook')

class Guestbook:

    @classmethod
    def get_lastest_greeting(cls, guestbook_name, numberOfGreeting):
        guestbook_key = Greeting.get_key_from_name(guestbook_name)
        greetings_query = Greeting.query(
            ancestor=guestbook_key).order(-Greeting.date)
        greetings = greetings_query.fetch(numberOfGreeting)

        return greetings

    def put_greeting_with_data(cls, guestbook_name, greeting_author, greeting_content):
        guestbook_key = Greeting.get_key_from_name(guestbook_name)

        greeting = Greeting(parent=guestbook_key)
        greeting.author = greeting_author
        greeting.content = greeting_content

        # save object
        greeting.put()