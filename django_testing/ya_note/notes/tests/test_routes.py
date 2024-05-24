from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):
    """Test case for routes."""

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data.

        Creates a test author, a test reader, and a test note.
        """
        cls.author = User.objects.create(username='anton')
        cls.reader = User.objects.create(username='test')
        cls.note = Note.objects.create(
            title='Заметка',
            text='Текст',
            author=cls.author
        )

    def test_pages_availability_without_auth(self):
        """
        Test that pages are available without authentication.

        Tests the home page, login page, logout page, and signup page.
        """
        urls = (
            ('notes:home'),
            ('users:login'),
            ('users:logout'),
            ('users:signup'),
        )

        for name in urls:
            with self.subTest(name=name):
                url = reverse(name, args=None)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_notes_access(self):
        """
        Test that only the author can access note pages.

        Tests the note detail page, edit page, and delete page.

        Simulates requests from an authenticated
        author and an authenticated reader.
        """
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        urls = (
            'notes:detail',
            'notes:edit',
            'notes:delete',
        )

        for user, status in users_statuses:
            self.client.force_login(user)
            for name in urls:
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.note.slug,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_without_auth(self):
        """
        Test that unauthenticated users are redirected to the login page.

        Tests the add page, list page, success page,
        note detail page, edit page, and delete page.
        """
        login_url = reverse('users:login')
        slug = (self.note.slug,)
        urls = (
            ('notes:add', None),
            ('notes:list', None),
            ('notes:success', None),
            ('notes:detail', slug),
            ('notes:edit', slug),
            ('notes:delete', slug)
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_auth_user_acess_pages(self):
        """
        Test that authenticated users can access certain pages.

        Tests the list page, success page, and add page.
        Simulates a request from an authenticated author.
        """
        self.client.force_login(self.author)
        urls = (
            'notes:list',
            'notes:success',
            'notes:add',
        )
        for name in urls:
            url = reverse(name)
            response = self.client.get(url)
            self.assertEqual(response.status_code, HTTPStatus.OK)
