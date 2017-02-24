Tornado_pyfb - A fork of pyfb which supports Tornado with Python 3
==================================================================

This is an Easy to Use Python Interface to the Facebook Graph API
-----------------------------------------------------------------

It gives you methods to access your data on facebook and
provides objects instead of json dictionaries!

To run the tests
----------------

1. Set environment variable FACEBOOK_APP_ID to your app ID
2. Set environment variable FACEBOOK_USER_TOKEN to the testing user token.
   You may get one from https://developers.facebook.com/tools/accesstoken/

Tornado Facebook Example Using Pyfb
-----------------------------------

.. code-block:: python

    class Facebook(object):
        app_id = '1234324'
        @gen.coroutine
        def sign_in(self, db_conn, access_token, sign_up=False):
            """Sign up or sign in. Return user"""
            rows = yield User.by_login_method(
                db_conn, 'facebook_access_token', access_token
            )
            if len(rows) > 0:
                return rows[0]
            pyfb = tornado_pyfb.Pyfb(self.app_id)
            pyfb.set_access_token(access_token)
            user_info = yield pyfb.get_myself()
            rows = yield User.by_login_method(
                db_conn, 'facebook_id', facebook_id
            )
            if len(rows) > 0:
                rows[0].facebook_access_token = access_token
                yield rows[0].store(db_conn)
                return rows[0]
            if sign_up:
                user_acct = User()
                user_acct.facebook_access_token = access_token
                user_acct.facebook_id = user_info.id
                yield user_acct.store(db_conn)
                return user_acct
