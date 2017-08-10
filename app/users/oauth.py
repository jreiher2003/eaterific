import json
import random
from string import letters
import requests
from rauth import OAuth1Service, OAuth2Service
from flask import current_app, url_for, request, redirect, session


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('users.oauth_callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class FacebookSignIn(OAuthSignIn):
    def __init__(self):
        super(FacebookSignIn, self).__init__('facebook')
        self.service = OAuth2Service(
            name='facebook',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://graph.facebook.com/oauth/authorize',
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com/'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        if 'code' not in request.args:
            return None, None, None, None
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()}, decoder=json.loads
        )
        me = oauth_session.get('me?fields=id,email,name,picture').json()
        print me['name'],me['picture']['data']['url']
        return (
            'facebook$' + me['id'],
            me.get('name'),  # Facebook does not provide
            me.get('email'),
            me['picture']['data']['url'],                   # username, so the email's user
                                            # is used instead
        )


class TwitterSignIn(OAuthSignIn):
    def __init__(self):
        super(TwitterSignIn, self).__init__('twitter')
        self.service = OAuth1Service(
            name='twitter',
            consumer_key=self.consumer_id,
            consumer_secret=self.consumer_secret,
            request_token_url='https://api.twitter.com/oauth/request_token',
            authorize_url='https://api.twitter.com/oauth/authorize',
            access_token_url='https://api.twitter.com/oauth/access_token',
            base_url='https://api.twitter.com/1.1/'
        )

    def authorize(self):
        request_token = self.service.get_request_token(
            params={'users.oauth_callback': self.get_callback_url()}
        )
        session['request_token'] = request_token
        return redirect(self.service.get_authorize_url(request_token[0]))

    def callback(self):
        request_token = session.pop('request_token')
        if 'oauth_verifier' not in request.args:
            return None, None, None, None
        oauth_session = self.service.get_auth_session(
            request_token[0],
            request_token[1],
            data={'oauth_verifier': request.args['oauth_verifier']}
        )
        me = oauth_session.get('account/verify_credentials.json').json()
        print me
        social_id = 'twitter$' + str(me.get('id'))
        avatar = me.get("profile_image_url_https")
        username = me.get('screen_name')
        return social_id, username, None, avatar   # Twitter does not provide email


class LinkedinLogin(OAuthSignIn):
    def __init__(self):
        super(LinkedinLogin, self).__init__('linkedin')
        self.service = OAuth2Service(
                name='linkedin',
                client_id=self.consumer_id,
                client_secret=self.consumer_secret,
                authorize_url='https://www.linkedin.com/uas/oauth2/authorization',
                access_token_url='https://www.linkedin.com/uas/oauth2/accessToken',
                base_url='https://api.linkedin.com/v1/'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
                scope='r_emailaddress r_basicprofile',
                response_type='code',
                state=''.join(str(random.randrange(9)) for _ in range(24)),
                redirect_uri=self.get_callback_url()
        ))

    def callback(self):
        if 'code' not in request.args:
            return None, None, None, None#, None, None
        data = {'code': request.args['code'],
                      'grant_type': 'authorization_code',
                      'redirect_uri': self.get_callback_url()}
        json_decoder = json.loads
        params = {'decoder': json_decoder,
                  'bearer_auth': False}
        session = self.service.get_auth_session(data=data, **params)
        r = session.get('people/~:(id,email-address,first-name,last-name,picture-url)', params={
                        'format': 'json',
                        'oauth2_access_token': session.access_token}, bearer_auth=False)
        me = r.json()
        print me
        email = me['emailAddress']
        first_name = me['firstName']
        last_name = me['lastName']
        avatar = me['pictureUrl']
        return (
            # 'linkedin',
            'linkedin$' + str(me['id']),
            first_name + ' ' + last_name,
            email,
            avatar,
            # first_name,
            # last_name,
        )

class GithubLogin(OAuthSignIn):
    def __init__(self):
        super(GithubLogin, self).__init__('github')
        self.service = OAuth2Service(
                name='github',
                client_id=self.consumer_id,
                client_secret=self.consumer_secret,
                authorize_url='https://github.com/login/oauth/authorize',
                access_token_url='https://github.com/login/oauth/access_token',
                base_url='https://api.github.com'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
                scope='user',
                response_type='code',
                redirect_uri=self.get_callback_url()
        ))

    def callback(self):
        if 'code' not in request.args:
            return None, None, None, None#, None, None
        oauth_session = self.service.get_auth_session(
                data={'code': request.args['code'],
                      'grant_type': 'authorization_code',
                      'redirect_uri': self.get_callback_url()})
        me = oauth_session.get('user?fields=email,name,login,avatar_url').json()
        return (
            # 'github',
            'github$' + str(me['id']),
            me.get('name'),
            me.get('email'),
            me.get("avatar_url")
            # me.get('login')
            # me.get('name').split()[0],
        )

class GoogleLogin(OAuthSignIn):
    def __init__(self):
        super(GoogleLogin, self).__init__('google')
        self.service = OAuth2Service(
                name='google',
                client_id=self.consumer_id,
                client_secret=self.consumer_secret,
                authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
                access_token_url='https://www.googleapis.com/oauth2/v4/token',
                base_url='https://www.googleapis.com'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
                scope='email profile',
                response_type='code',
                redirect_uri=self.get_callback_url()
        ))

    def callback(self):
        if 'code' not in request.args:
            return None, None, None#, None
        data = {'code': request.args['code'],
                      'grant_type': 'authorization_code',
                      'redirect_uri': self.get_callback_url()}
        response = self.service.get_raw_access_token(data=data)
        response = response.json()
        oauth2_session = self.service.get_session(response['access_token'])
        me = oauth2_session.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
        return (
            'google$' + str(me['id']),
            me.get('name'),
            me.get('email'),
            me.get('picture')
        )

class FourSquareLogin(OAuthSignIn):
    def __init__(self):
        super(FourSquareLogin, self).__init__('foursquare')
        self.service = OAuth2Service(
                name='foursquare',
                client_id=self.consumer_id,
                client_secret=self.consumer_secret,
                authorize_url='https://foursquare.com/oauth2/authenticate',
                access_token_url='https://foursquare.com/oauth2/access_token',
                base_url='https://api.foursquare.com/v2'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
                client_id= self.consumer_id,
                response_type='code',
                redirect_uri=self.get_callback_url()
        ))

    def callback(self):
        if 'code' not in request.args:
            return None, None, None, None
        data = {'code': request.args['code'],
                      'grant_type': 'authorization_code',
                      'redirect_uri': self.get_callback_url()}
        print data
        response = self.service.get_raw_access_token(data=data)
        response = response.json()
        print response
        # oauth2_session = self.service.get_session(response['access_token'])
        me = requests.get('https://api.foursquare.com/v2/users/self?oauth_token=%s&v=20170725' % response['access_token']).json()
        fr = me['response']['user']
        print fr 
        avatar = fr['photo']['prefix']+ '64x64' +fr['photo']['suffix']
        return (
            "foursquare$" + str(fr['id']), 
            fr['firstName'] + " " + fr['lastName'], 
            fr['contact']['email'],
            avatar
            )

class RedditLogin(OAuthSignIn):
    def __init__(self):
        super(RedditLogin, self).__init__('reddit')
        self.service = OAuth2Service(
                name='reddit',
                client_id=self.consumer_id,
                client_secret=self.consumer_secret,
                authorize_url='https://ssl.reddit.com/api/v1/authorize',
                access_token_url='https://ssl.reddit.com/api/v1/access_token',
                base_url='https://oauth.reddit.com'
        )

    def random_string(self):
        return "".join(random.choice(letters) for x in xrange(16))


    def authorize(self):
        state = self.random_string()
        return redirect(self.service.get_authorize_url(
                client_id=self.consumer_id,
                response_type='code',
                state=state,
                redirect_uri=self.get_callback_url(),
                user_agent='j3ffrey_',
                duration='permanent',
                scope='identity'
        ))

    def callback(self):
        if 'code' not in request.args:
            return None, None, None#, None
        data = {'code': request.args['code'],
                      'grant_type': 'authorization_code',
                      'redirect_uri': self.get_callback_url()}
        print data
        response = self.service.get_raw_access_token(data=data)
        response = response.json()
        print response
        headers = {"Authorization": "bearer" + response['access_token']}
        me = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers).json()
        return (me["id"], me["name"], me["email"])