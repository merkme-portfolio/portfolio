from http import HTTPStatus
import pytest
from pytest_django.asserts import assertRedirects, assertFormError
from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db


def test_annonymous_user_cant_create_comment(
    client, detail_url, form_data, comments_expected_result
):
    """Test that an anonymous user cannot create a comment."""
    client.post(detail_url, data=form_data)
    assert Comment.objects.count() == comments_expected_result


def test_user_can_create_comment(
    author_client, detail_url, form_data,
    comments_expected_result, last_comment_created
):
    """Test that an authenticated user can create a comment."""
    comments_expected_result += 1
    response = author_client.post(detail_url, data=form_data)
    assertRedirects(response, f'{detail_url}#comments')
    assert Comment.objects.count() == comments_expected_result
    last_comment = last_comment_created()
    assert last_comment.text == form_data['text']
    assert last_comment.news == form_data['news']
    assert last_comment.author == form_data['author']


def test_user_cant_use_bad_words(
    author_client, detail_url, comments_expected_result
):
    """Test that a user cannot use bad words in a comment."""
    response = author_client.post(detail_url, data={'text': BAD_WORDS[0]})
    assertFormError(response, form='form', field='text', errors=WARNING,)
    assert Comment.objects.count() == comments_expected_result


@pytest.mark.usefixtures('comment')
def test_author_can_delete_comment(
    author_client, comment_delete_url, comments_url, comments_expected_result
):
    """Test that an author can delete their own comment."""
    comments_expected_result -= 1
    response = author_client.delete(comment_delete_url)
    assertRedirects(response, comments_url)
    assert Comment.objects.count() == comments_expected_result


@pytest.mark.usefixtures('comment')
def test_reader_cant_delete_comment(
    admin_client, comment_delete_url, comments_expected_result
):
    """Test that a reader cannot delete a comment."""
    response = admin_client.delete(comment_delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == comments_expected_result


def test_author_can_edit_comment(
    author_client, comment_edit_url, form_data,
    comments_url, comment
):
    """Test that an author can edit their own comment."""
    response = author_client.post(comment_edit_url, data=form_data)
    assertRedirects(response, comments_url)
    comment.refresh_from_db()
    assert comment.text == form_data['text']
    assert comment.news == form_data['news']
    assert comment.author == form_data['author']


def test_reader_cant_edit_comment(
    admin_client, comment_edit_url,
    form_data, comment
):
    """Test that a reader cannot edit a comment."""
    initial_text = comment.text
    response = admin_client.post(comment_edit_url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == initial_text
