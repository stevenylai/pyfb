import unittest
import os
import json
from tornado import testing
from ..pyfb import Pyfb


class PyfbTests(testing.AsyncTestCase):

    pyfb_args = {}

    def setUp(self):
        super().setUp()
        app_id = os.getenv('FACEBOOK_APP_ID')
        app_token = os.getenv('FACEBOOK_TOKEN')
        if app_id is None or app_token is None:
            try:
                from .test_data import config
                app_id = config["FACEBOOK_APP_ID"]
                app_token = config["FACEBOOK_TOKEN"]
            except (ImportError, KeyError):
                print(
                    "\nERROR! You must have a test_data.py file "
                    "providing the facebook app id and the access token."
                    "\nExample:"
                    '\tconfig = {\n\t\t"FACEBOOK_APP_ID": "your_app_id"\n'
                    '\t\t"FACEBOOK_TOKEN": "your_token"\n\t}\n'
                )
        self.pyfb = Pyfb(app_id, **self.pyfb_args)
        self.pyfb.set_access_token(app_token)
        self.me = self.io_loop.run_sync(self.pyfb.get_myself)

    def test_auth(self):
        self.assertEquals(type(self.me.name), type(unicode()))

    def test_get_friends(self):
        self.assertTrue(isinstance(self.pyfb.get_friends(self.me.id), list))

    @testing.gen_test
    def test_get_photos_paging(self):
        photos = yield self.pyfb.get_photos()
        more_photos = photos.next()
        more_more_photos = more_photos.next()

        if len(photos) < 25 and len(more_photos) > 0:
            raise Exception()

        if len(photos) == 25 and len(more_photos) < 25 and len(more_more_photos) > 0:
            raise Exception()

        self.assertTrue(isinstance(photos, list))
        self.assertTrue(isinstance(more_photos, list))
        self.assertTrue(isinstance(more_more_photos, list))

        self.assertEquals(len(photos), len(more_photos.previous()))
        self.assertEquals(photos.previous(), [])


class PyfbTestRawDataTests(PyfbTests):

    pyfb_args = {"raw_data": True }

    def test_auth(self):
        self.assertEquals(type(self.me["name"]), type(unicode()))

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
