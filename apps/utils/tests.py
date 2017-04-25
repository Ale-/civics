from django.test import TestCase
from .template_tags import utils
from civics import settings

class FiltersTestCase(TestCase):

    def CssTagFilterTest(self):
        uri = 'test.css'
        self.assertEqual( utils.css(context_url), settings.BASE_DIR + '/static/civics/css/' + uri )

    def JsTagFilterTest(self):
        uri = 'test.js'
        self.assertEqual( utils.css(context_url), settings.BASE_DIR + '/static/civics/js/' + uri )

    def ImgTagFilterTest(self):
        uri = 'test.jpg'
        self.assertEqual( utils.css(context_url), settings.BASE_DIR + '/static/civics/img/' + uri )
