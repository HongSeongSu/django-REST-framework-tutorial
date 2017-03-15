import random

from django.contrib.auth import get_user_model

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APILiveServerTestCase

from snippets.models import Snippet

User = get_user_model()


class SnippetsTest(APILiveServerTestCase):

    test_title = 'Test Snippet[{}] Title'
    test_code = 'print("Hello, world{}")'
    default_linenos = False
    default_languages = 'python'
    default_style = 'friendly'

    test_username = 'test_username'
    test_password = 'test_password'

    def create_user(self):
        user = User.objects.create_user(
            username=self.test_username,
            password=self.test_password,
        )
        return user

    def create_snippet(self, num=1):

        for i in range(num):
            test_title = self.test_title.format(i + 1)
            test_code = self.test_code.format('!' * (i + 1))
            url = reverse('snippet:list')
            data = {
                'title': test_title,
                'code': test_code,
            }
            response = self.client.post(url, data, format='json')
            if num == 1:
                return response

    def test_snippet_list(self):
        self.create_user()
        self.client.login(username=self.test_username, password=self.test_password)

        num = random.randrange(1, 20)
        self.create_snippet(num)
        self.assertEqual(Snippet.objects.count(), num)
        for index, snippet_value_tuple in enumerate(Snippet.objects.value_list('title', 'code')):
            self.assertEqual(snippet_value_tuple[0], self.test_title.format(index + 1))
            self.assertEqual(snippet_value_tuple[1], self.test_code.format('!' * (index + 1)))

        for index, snippet in enumerate(Snippet.objects.all().iterator()):
            self.assertEqual(snippet.title, self.test_title.format(index + 1))
            self.assertEqual(snippet.code, self.test_code.format('!' * (index + 1)))

    def test_snippet_create(self):
        self.create_user()
        self.client.login(username=self.test_username, password=self.test_password)

        response = self.create_snippet()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('title'), self.test_title.format(1))
        self.assertEqual(response.data.get('code'), self.test_code.format('!'))
        self.assertEqual(response.data.get('linenos'), self.default_linenos)
        self.assertEqual(response.data.get('languages'), self.default_languages)
        self.assertEqual(response.data.get('style'), self.default_style)

    def test_snippet_retrieve(self):
        pass

    def test_snippet_update_partial(self):
        pass

    def test_snippet_update(self):
        pass

    def test_snippet_delete(self):
        pass
