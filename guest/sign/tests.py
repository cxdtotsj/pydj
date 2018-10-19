from django.test import TestCase
from sign.models import Event,Guest
from django.test import Client
from django.comtrib.auth.models import User

# Create your tests here.

class ModelTest(TestCase):

    def setUp(self):
        Event.objects.create(id=1, name="oneplus 3 event", status=True, limit=2000,
                address='shenzhen', start_time='2016-08-31 02:18:22')
        Guest.objects.create(id=1,event_id=1,realname='alen',phone='13711001101',
                email='alen@mail.com', sign=False)

    def test_event_models(self):
        result = Event.objects.get(name="oneplus 3 event")
        self.assertEqual(result.address,"shenzhen")
        self.assertTrue(result.status)
    
    def test_guest_models(self):
        result = Guest.objects.get(phone='13711001101')
        self.assertEqual(result.realname, "alen")
        self.assertFalse(result.sign)


class IndexPageTest(TestCase):
    ''' 测试index登录首页 '''

    def test_index_page_renders_index_template(self):
        '''测试 index 视图'''
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'index.html')