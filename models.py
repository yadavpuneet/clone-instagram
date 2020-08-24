from google.appengine.ext import ndb


class Reaction(ndb.Model):
    text = ndb.StringProperty()
    member = ndb.KeyProperty(kind="Member")
    datetime = ndb.DateTimeProperty()


class Post(ndb.Model):
    image = ndb.BlobKeyProperty()
    text = ndb.StringProperty()
    reactions = ndb.KeyProperty(Reaction, repeated=True)
    datetime = ndb.DateTimeProperty()


class Member(ndb.Model):
    name = ndb.StringProperty()
    following = ndb.KeyProperty(kind="Member", repeated=True)
    followers = ndb.KeyProperty(kind="Member", repeated=True)
    posts = ndb.KeyProperty(Post, repeated=True)
