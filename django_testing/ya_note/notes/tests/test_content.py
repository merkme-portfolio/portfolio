from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from notes.models import Note
from notes.forms import NoteForm

User = get_user_model()


class TestHomePage(TestCase):
    """Test case for the home page."""

    HOME_URL = reverse('notes:home')

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
        cls.slug = cls.note.slug,

    def test_only_you_can_see_your_notes(self):
        """
        Test that only the author can see their own notes.

        Simulates requests from an authenticated author
        and an authenticated reader.
        """
        list_url = reverse('notes:list')
        users_posts = (
            (self.author, 1),
            (self.reader, 0),
        )
        for user, posts in users_posts:
            self.client.force_login(user)
            response = self.client.get(list_url)
            object_list = response.context['object_list']
            all_posts = len(object_list)
            self.assertEqual(all_posts, posts)

    def test_pages_contains_form(self):
        """
        Test that pages contain a form.

        Tests the 'add' and 'edit' pages.

        Simulates a request from an authenticated author.
        """
        urls = (
            ('notes:add', None),
            ('notes:edit', self.slug),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                self.client.force_login(self.author)
                response = self.client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)

    def test_note_link_for_edit_or_delete_on_page(self):
        """
        Test that the note link for editing or deleting on the page.

        Simulates a request from an authenticated author.
        """
        self.client.force_login(self.author)
        url = reverse('notes:detail', args=self.slug)
        response = self.client.get(url)
        links_to_find = (
            'edit/',
            'delete/'
        )
        for link in links_to_find:
            with self.subTest(link=link):
                self.assertContains(response, link)
