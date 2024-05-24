from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from pytils.translit import slugify
from notes.models import Note
from notes.forms import WARNING

User = get_user_model()


class TestNoteCreation(TestCase):
    """Test case for creating a new note."""

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data.

        Creates a test author, a test note,
        and auth_client to simulate HTTP requests.
        """
        cls.form_data = {
            'title': 'Заметка',
            'text': 'Текст',
            'slug': 'slug',
        }
        cls.url = reverse('notes:add')
        cls.redirect_url = reverse('notes:success')
        cls.author = User.objects.create(username='anton')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.author)
        cls.form_data['author'] = cls.author
        cls.note = Note.objects.create(**cls.form_data)
        cls.test_notes_count = Note.objects.count()

    def test_different_user_create_note(self):
        """
        Test that different users can create a note.

        self.client - annonymous user, can't create a note
        self.auth_client - logged in user, can create a note
        """
        users = (self.client, self.auth_client)
        for user in users:
            with self.subTest(user=user):
                self.form_data['slug'] += 'new'
                response = user.post(self.url, data=self.form_data)
                if user == self.auth_client:
                    self.test_notes_count += 1
                    self.assertRedirects(response, self.redirect_url)
                notes_count = Note.objects.count()
                self.assertEqual(notes_count, self.test_notes_count)

    def test_note_without_slug(self):
        """
        Test creating a note without a slug.

        Simulates a request from an authenticated user.
        """
        self.test_notes_count += 1
        self.form_data.pop('slug')
        response = self.auth_client.post(self.url, data=self.form_data)
        self.assertRedirects(response, self.redirect_url)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, self.test_notes_count)
        note = Note.objects.last()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, slugify(self.form_data['title']))

    def test_user_cant_use_same_slug_for_several_notes(self):
        """
        Test that a user cannot use the same slug for multiple notes.

        Simulates a request from an authenticated user.
        """
        response = self.auth_client.post(self.url, data=self.form_data)
        self.assertFormError(
            response=response,
            form='form',
            field='slug',
            errors=(
                self.form_data['slug'] + WARNING
            )
        )
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, self.test_notes_count)

    def test_note_text_field_on_blank_is_false(self):
        """
        Test that the text field of a note cannot be blank.

        Simulates a request from an authenticated user.
        """
        self.form_data.pop('text')
        response = self.auth_client.post(self.url, data=self.form_data)
        self.assertFormError(
            response=response,
            form='form',
            field='text',
            errors=['Обязательное поле.']
        )
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, self.test_notes_count)


class TestNoteEditDelete(TestCase):
    """Test case for editing and deleting a note."""

    TITLE = 'Заметка'
    TEXT = 'Текст'
    SLUG = 'slug'

    NEW_TITLE = 'Новая заметка'
    NEW_TEXT = 'Новый текст'
    NEW_SLUG = 'new_slug'

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data.

        Creates a test author, a test reader, a test note,
        and clients to simulate HTTP requests.
        """
        cls.author = User.objects.create(username='anton')
        cls.reader = User.objects.create(username='test')
        cls.author_client = Client()
        cls.reader_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title=cls.TITLE,
            text=cls.TEXT,
            slug=cls.SLUG,
            author=cls.author,
        )
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.success_url = reverse('notes:success')
        cls.form_data = {
            'title': cls.NEW_TITLE,
            'text': cls.NEW_TEXT,
            'slug': cls.NEW_SLUG,
        }
        cls.test_notes_count = Note.objects.count()

    def test_author_can_delete_note(self):
        """
        Test that an author can delete a note.

        Simulates a request from an authenticated author.
        """
        self.test_notes_count -= 1
        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(response, self.success_url)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, self.test_notes_count)

    def test_reader_cant_delete_note(self):
        """
        Test that a reader cannot delete a note.

        Simulates a request from an authenticated reader.
        """
        response = self.reader_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, self.test_notes_count)

    def test_author_can_edit_note(self):
        """
        Test that an author can edit a note.

        Simulates a request from an authenticated author.
        """
        response = self.author_client.post(self.edit_url, data=self.form_data)
        self.assertRedirects(response, self.success_url)
        self.note.refresh_from_db()
        self.assertEqual(
            (self.note.title, self.note.text, self.note.slug),
            (self.NEW_TITLE, self.NEW_TEXT, self.NEW_SLUG),
        )

    def test_reader_cant_edit_note(self):
        """
        Test that a reader cannot edit a note.

        Simulates a request from an authenticated reader.
        """
        response = self.reader_client.post(self.edit_url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertEqual(
            (self.note.title, self.note.text, self.note.slug),
            (self.TITLE, self.TEXT, self.SLUG),
        )
