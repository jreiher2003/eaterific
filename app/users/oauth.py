import json
import random
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
            return None, None, None
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()}, decoder=json.loads
        )
        me = oauth_session.get('me?fields=id,email,name,gender,age_range,picture').json()
        print me['name'], me['gender'],me['age_range'],me['picture']['data']['url']
        return (
            'facebook$' + me['id'],
            me.get('name'),  # Facebook does not provide
                                            # username, so the email's user
                                            # is used instead
            me.get('email')
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
            return None, None, None
        oauth_session = self.service.get_auth_session(
            request_token[0],
            request_token[1],
            data={'oauth_verifier': request.args['oauth_verifier']}
        )
        me = oauth_session.get('account/verify_credentials.json').json()
        social_id = 'twitter$' + str(me.get('id'))
        username = me.get('screen_name')
        return social_id, username, None   # Twitter does not provide email


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
            return None, None, None#, None#, None, None
        data = {'code': request.args['code'],
                      'grant_type': 'authorization_code',
                      'redirect_uri': self.get_callback_url()}
        json_decoder = json.loads
        params = {'decoder': json_decoder,
                  'bearer_auth': False}
        session = self.service.get_auth_session(data=data, **params)
        r = session.get('people/~:(id,email-address,first-name,last-name)', params={
                        'format': 'json',
                        'oauth2_access_token': session.access_token}, bearer_auth=False)
        me = r.json()
        email = me['emailAddress']
        first_name = me['firstName']
        last_name = me['lastName']
        return (
            # 'linkedin',
            'linkedin$' + str(me['id']),
            first_name + ' ' + last_name,
            email,
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
            return None, None, None#, None#, None, None
        oauth_session = self.service.get_auth_session(
                data={'code': request.args['code'],
                      'grant_type': 'authorization_code',
                      'redirect_uri': self.get_callback_url()})
        me = oauth_session.get('user?fields=email,name,login').json()
        return (
            # 'github',
            'github$' + str(me['id']),
            me.get('name'),
            me.get('email'),
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
        first_name = me.get('given_name')
        last_name = me.get('family_name')
        return (
            # 'google',
            'google$' + str(me['id']),
            me.get('name'),
            me.get('email'),
            # first_name,
            # last_name,
            # None
        )