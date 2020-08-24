import operator
import os
import re
from datetime import datetime

import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.api.images import get_serving_url
from google.appengine.ext import ndb
from google.appengine.ext.ndb import blobstore
from google.appengine.ext.webapp import blobstore_handlers

from models import Member, Post, Reaction

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

JINJA_ENVIRONMENT.globals['get_serving_url'] = get_serving_url


def timeline(member):
    posts = []
    for post in Post.query().fetch():
        for m in [member.key] + member.following:
            if post.key in m.get().posts:
                posts.append(post)
    print posts
    posts = sorted(posts, key=operator.attrgetter("datetime"), reverse=True)
    print posts
    return posts[:50]


JINJA_ENVIRONMENT.globals['timeline'] = timeline


def initialize(request):
    user = users.get_current_user()
    if user:
        url = users.create_logout_url('/')
        url_string = 'logout'
        email = user.email().strip()
        member_key = ndb.Key('Member', email)
        member = member_key.get()
        if member is None:
            name = re.sub('\W+', ' ', email.split('@')[0]).title()
            member = Member(id=email, name=name)
            member.put()
    else:
        url = users.create_login_url()
        url_string = 'login'
        member = None
    template_values = {
        'url': url,
        'url_string': url_string,
        'user': user,
        'member': member,
        'upload': blobstore.create_upload_url('/upload')
    }

    return template_values


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template_values = initialize(self.request)
        for x in self.request.params:
            template_values[str(x)] = str(self.request.params[x])

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


class NewPostHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        params = self.request
        template_values = initialize(self.request)
        member = template_values['member']
        post = Post(text=params.get('new_post_text'), image=self.get_uploads()[0].key(), datetime=datetime.now(),
                    parent=member.key)
        post.put()
        member.posts.insert(0, post.key)
        member.put()
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


class ProfileViewHandler(webapp2.RequestHandler):
    def get(self):
        params = self.request
        template_values = initialize(self.request)
        if not template_values['user']:
            self.redirect('/')
            return
        try:
            profile = ndb.Key(urlsafe=params.get('id')).get()
            template_values['profile'] = profile
        except:
            pass
        template = JINJA_ENVIRONMENT.get_template('profile.html')
        self.response.write(template.render(template_values))


class SearchProfileHandler(webapp2.RequestHandler):
    def post(self):
        params = self.request
        template_values = initialize(self.request)
        if not template_values['user']:
            self.redirect('/')
            return
        try:
            result = []
            search = params.get('search').strip().lower()
            print search
            for m in Member.query().fetch():
                print m
                if search in m.name.lower():
                    result.append(m)
            template_values['result'] = result
        except:
            pass
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


class FollowProfileHandler(webapp2.RequestHandler):
    def get(self):
        params = self.request
        template_values = initialize(self.request)
        if not template_values['user']:
            self.redirect('/')
            return
        try:
            profile = ndb.Key(urlsafe=params.get('id')).get()
            member = template_values['member']
            member.following.append(profile.key)
            profile.followers.append(member.key)
            member.put()
            profile.put()
            template_values['profile'] = profile
        except:
            pass
        template = JINJA_ENVIRONMENT.get_template('profile.html')
        self.response.write(template.render(template_values))


class UnFollowProfileHandler(webapp2.RequestHandler):
    def get(self):
        params = self.request
        template_values = initialize(self.request)
        if not template_values['user']:
            self.redirect('/')
            return
        try:
            profile = ndb.Key(urlsafe=params.get('id')).get()
            member = template_values['member']
            member.following.remove(profile.key)
            profile.followers.remove(member.key)
            member.put()
            profile.put()
            template_values['profile'] = profile
        except:
            pass
        template = JINJA_ENVIRONMENT.get_template('profile.html')
        self.response.write(template.render(template_values))


class ShowFollowingHandler(webapp2.RequestHandler):
    def get(self):
        params = self.request
        template_values = initialize(self.request)
        if not template_values['user']:
            self.redirect('/')
            return
        try:
            profile = ndb.Key(urlsafe=params.get('id')).get()
            template_values['profile'] = profile
        except:
            pass
        template = JINJA_ENVIRONMENT.get_template('following.html')
        self.response.write(template.render(template_values))


class ShowFollowersHandler(webapp2.RequestHandler):
    def get(self):
        params = self.request
        template_values = initialize(self.request)
        if not template_values['user']:
            self.redirect('/')
            return
        try:
            profile = ndb.Key(urlsafe=params.get('id')).get()
            template_values['profile'] = profile
        except:
            pass
        template = JINJA_ENVIRONMENT.get_template('followers.html')
        self.response.write(template.render(template_values))


class PostCommentHandler(webapp2.RequestHandler):
    def post(self):
        params = self.request
        template_values = initialize(self.request)
        if not template_values['user']:
            self.redirect('/')
            return
        try:
            post = ndb.Key(urlsafe=params.get('id')).get()
            member = template_values['member']
            reply = params.get('reply').strip()
            reaction = Reaction(text=reply, member=member.key, datetime=datetime.now())
            reaction.put()
            post.reactions.insert(0, reaction.key)
            post.put()
            template_values['highlight'] = post
            print self.request.uri
        except:
            pass
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


class PostReactHandler(webapp2.RequestHandler):
    def post(self):
        params = self.request
        template_values = initialize(self.request)
        if not template_values['user']:
            self.redirect('/')
            return
        try:
            post = ndb.Key(urlsafe=params.get('id')).get()
            member = template_values['member']
            reply = params.get('reply').strip()
            reaction = Reaction(text=reply, member=member.key, datetime=datetime.now())
            reaction.put()
            post.reactions.insert(0, reaction.key)
            post.put()
            template_values['highlight'] = post
            template_values['profile'] = post.key.parent().get()
        except:
            pass
        template = JINJA_ENVIRONMENT.get_template('profile.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/upload', NewPostHandler),
    ('/profile', ProfileViewHandler),
    ('/search', SearchProfileHandler),
    ('/follow', FollowProfileHandler),
    ('/unfollow', UnFollowProfileHandler),
    ('/followers', ShowFollowersHandler),
    ('/following', ShowFollowingHandler),
    ('/comment', PostCommentHandler),
    ('/react', PostReactHandler),

], debug=True)
