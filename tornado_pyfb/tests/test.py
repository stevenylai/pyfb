import unittest
import os
from tornado import testing
from ..pyfb import Pyfb


class PyfbTests(testing.AsyncTestCase):

    pyfb_args = {}

    def setUp(self):
        super().setUp()
        app_id = os.getenv('FACEBOOK_APP_ID')
        user_token = os.getenv('FACEBOOK_USER_TOKEN')
        if app_id is None or user_token is None:
            try:
                from .test_data import config
                app_id = config["FACEBOOK_APP_ID"]
                user_token = config["FACEBOOK_USER_TOKEN"]
            except (ImportError, KeyError):
                print(
                    "\nERROR! You must have a test_data.py file "
                    "providing the facebook app id and the access token."
                    "\nExample:"
                    '\tconfig = {\n\t\t"FACEBOOK_APP_ID": "your_app_id",\n'
                    '\t\t"FACEBOOK_USER_TOKEN": "your_token"\n\t}\n'
                )
        self.pyfb = Pyfb(app_id, **self.pyfb_args)
        self.pyfb.set_access_token(user_token)
        self.me = self.io_loop.run_sync(self.pyfb.get_myself)

    def test_auth(self):
        self.assertEqual(type(self.me.name), str)
        self.assertEqual(type(self.me.id), str)

    @testing.gen_test
    def test_get_friends(self):
        friends = yield self.pyfb.get_friends(self.me.id)
        self.assertTrue(isinstance(friends, list))

    @testing.gen_test
    def test_get_photos_paging(self):
        photos = yield self.pyfb.get_photos()
        if photos.has_next():
            more_photos = yield photos.next()
        else:
            more_photos = None
        if more_photos is not None and more_photos.has_next():
            more_more_photos = yield more_photos.next()
        else:
            more_more_photos = None

        if len(photos) < 25 and more_photos is not None and \
           len(more_photos) > 0:
            raise Exception()

        if len(photos) == 25 and more_photos is not None and \
           len(more_photos) < 25 and more_more_photos is not None and \
           len(more_more_photos) > 0:
            raise Exception()

        self.assertTrue(isinstance(photos, list))
        self.assertTrue(isinstance(more_photos, (list, type(None))))
        self.assertTrue(isinstance(more_more_photos, (list, type(None))))

        if more_photos is not None:
            previous = yield more_photos.previous()
            self.assertEqual(len(photos), len(previous))
        self.assertEqual(photos.has_previous(), False)


class PyfbTestRawDataTests(PyfbTests):

    pyfb_args = {"raw_data": True}

    def test_auth(self):
        self.assertEqual(type(self.me["name"]), str)

    @testing.gen_test
    def test_get_friends(self):
        friends = yield self.pyfb.get_friends(self.me["id"])
        self.assertTrue(isinstance(friends, list))
        for friend in friends:
            self.assertTrue(isinstance(friend, dict))

    def test_get_photos_paging(self):
        """
            pagination is not supported by raw data since it returns a
            dictionary instead of an object.
        """
        pass


if __name__ == "__main__":

    unittest.main()
