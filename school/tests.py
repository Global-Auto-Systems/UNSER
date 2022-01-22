from unicodedata import name
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Reason
class BlogTests(TestCase):
    def setUp(self):
        # self.user = get_user_model().objects.create_user(
        #     username='testuser',
        #     email='test@email.com',
        #     password='secret'
        #     ) 
        self.reason = Reason.objects.create(name='Sickness')
    def test_string_representation(self):
        reason = Reason(name='Sickness')
        self.assertEqual(str(reason), reason.name)
    def test_reason_content(self):
        self.assertEqual(f'{self.reason.name}', 'Sickness')
    # def test_reason_list_view(self):
    #     response = self.client.get(reverse('home'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'Nice body content')
    #     self.assertTemplateUsed(response, 'home.html')
    # def test_post_detail_view(self):
    #     response = self.client.get('/post/1/')
    #     no_response = self.client.get('/post/100000/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(no_response.status_code, 404)
    #     self.assertContains(response, 'A good title')
    #     self.assertTemplateUsed(response, 'post_detail.html')
