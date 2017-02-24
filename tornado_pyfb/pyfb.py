"""
    This is an Easy to Use Python Interface to the Facebook Graph API

    It gives you methods to access your data on facebook and
    provides objects instead of json dictionaries!
"""
from tornado import gen
from .client import FacebookClient, PyfbException
__all__ = ['Pyfb', 'PyfbException']


class Pyfb(object):
    """
        This class is Facade for FacebookClient
    """

    def __init__(self, app_id, access_token=None, raw_data=False,
                 permissions=None):
        self._client = FacebookClient(app_id, access_token=access_token,
                                      raw_data=raw_data,
                                      permissions=permissions)

    def get_auth_url(self, redirect_uri=None):
        """
            Returns the authentication url
        """
        return self._client.get_auth_token_url(redirect_uri)

    def get_auth_code_url(self, redirect_uri=None, state=None):
        """
            Returns the url to get a authentication code
        """
        return self._client.get_auth_code_url(redirect_uri, state=state)

    @gen.coroutine
    def get_access_token(self, app_secret_key, secret_code, redirect_uri=None):
        """
            Gets the access token
        """
        token = yield self._client.get_app_access_token(
            app_secret_key, secret_code, redirect_uri
        )
        return token

    @gen.coroutine
    def exchange_token(self, app_secret_key, exchange_token):
        """
             Exchanges a short-lived access token (like those obtained from
             client-side JS api) for a longer-lived access token
        """
        res = yield self._client.exchange_token(app_secret_key, exchange_token)
        return res

    def get_dialog_url(self, redirect_uri=None):
        """
            Returns a url inside facebook that shows a dialog allowing
            users to publish contents.
        """
        return self._client.get_dialog_url(redirect_uri)

    def set_access_token(self, token):
        """
            Sets the access token. Necessary to make the requests that
            requires autenthication
        """
        self._client.access_token = token

    def set_permissions(self, permissions):
        """
            Sets a list of data access permissions that the user must give to
            the application
            e.g:
                permissions = [auth.USER_ABOUT_ME, auth.USER_LOCATION,
                               auth.FRIENDS_PHOTOS, ...]
        """
        self._client.permissions = permissions

    @gen.coroutine
    def get_myself(self):
        """
            Gets myself data
        """
        res = yield self._client.get_one("me", "FBUser")
        return res

    @gen.coroutine
    def get_user_by_id(self, id=None):
        """
            Gets an user by the id
        """
        if id is None:
            id = "me"
        res = yield self._client.get_one(id, "FBUser")
        return res

    @gen.coroutine
    def get_friends(self, id=None):
        """
            Gets a list with your friends
        """
        res = yield self._client.get_list(id, "Friends")
        return res

    @gen.coroutine
    def get_statuses(self, id=None):
        """
            Gets a list of status objects
        """
        res = yield self._client.get_list(id, "Statuses")
        return res

    @gen.coroutine
    def get_photos(self, id=None):
        """
            Gets a list of photos objects
        """
        res = yield self._client.get_list(id, "Photos")
        return res

    @gen.coroutine
    def get_comments(self, id=None):
        """
            Gets a list of photos objects
        """
        res = yield self._client.get_list(id, "Comments")
        return res

    @gen.coroutine
    def publish(self, message, id=None, **kwargs):
        """
            Publishes a message on the wall
        """
        res = yield self._client.push(id, "feed", message=message, **kwargs)
        return res

    @gen.coroutine
    def publish_picture(self, message, id=None, **kwargs):
        """
            Publish picture
        """
        res = yield self._client.push(id, "photos", message=message, **kwargs)
        return res

    @gen.coroutine
    def comment(self, message, id=None, **kwargs):
        """
            Publishes a message on the wall
        """
        res = yield self._client.push(
            id, "comments", message=message, **kwargs
        )
        return res

    @gen.coroutine
    def get_likes(self, id=None):
        """
            Get a list of liked objects
        """
        res = yield self._client.get_list(id, "likes")
        return res

    @gen.coroutine
    def get_pages(self, id=None):
        """
            Get a list of Facebook Pages user has access to
        """
        res = yield self._client.get_list(id, 'accounts', 'FBPage')
        return res

    @gen.coroutine
    def like(self, id):
        """
            LIKE: It Doesn't work. Seems to be a bug on the Graph API
            http://bugs.developers.facebook.net/show_bug.cgi?id=10714
        """
        print(self.like.__doc__)
        res = yield self._client.push(id, "likes")
        return res

    @gen.coroutine
    def delete(self, id):
        """
            Deletes a object
        """
        res = yield self._client.delete(id)
        return res

    @gen.coroutine
    def fql_query(self, query):
        """
            Executes a FBQL query
        """
        res = yield self._client.execute_fql_query(query)
        return res
