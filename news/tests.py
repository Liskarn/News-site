from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Post

class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create_user(username='testuser', password='12345')
        test_user = User.objects.get(username='testuser')
        Post.objects.create(title='Test Title', description='Test Description', author=test_user)

    def test_title_content(self):
        post = Post.objects.get(id=1)
        expected_object_name = f'{post.title}'
        self.assertEqual(expected_object_name, 'Test Title')

    def test_description_content(self):
        post = Post.objects.get(id=1)
        expected_object_name = f'{post.description}'
        self.assertEqual(expected_object_name, 'Test Description')


class PostListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_posts = 5

        test_user = User.objects.create_user(username='testuser', password='12345')
        for post_num in range(number_of_posts):
            Post.objects.create(
                title=f'Post {post_num}',
                description='Test Description',
                author=test_user,
            )
    
    def setUp(self):
        # Log in.
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_view_url_exists_at_desired_location(self): 
        resp = self.client.get('') 
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'post_list.html')

    def test_pagination_is_five(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['post_list']) == 5)