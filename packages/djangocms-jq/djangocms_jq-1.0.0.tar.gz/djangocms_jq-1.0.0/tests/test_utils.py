from django.test import SimpleTestCase

from djangocms_jq.utils import get_cache_key


class UtilsTest(SimpleTestCase):

    def test_get_cache_key(self):
        self.assertEqual(get_cache_key("https://example.com/"), "djangocms_jq_src:https://example.com/")
