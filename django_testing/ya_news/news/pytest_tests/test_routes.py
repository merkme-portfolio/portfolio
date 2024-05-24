from http import HTTPStatus
import pytest
from pytest_lazyfixture import lazy_fixture as fixture
from pytest_django.asserts import assertRedirects
from django.urls import reverse


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:home', None),
        ('news:detail', fixture('news_pk')),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
    ),
)
@pytest.mark.usefixtures('news')
@pytest.mark.django_db
def test_annonymous_user_can_access(client, name, args):
    """Trying to get pages and check status code. Expected is OK (code:200)."""
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'client_chosen, expected_status_code',
    (
        (fixture('author_client'), HTTPStatus.OK),
        (fixture('admin_client'), HTTPStatus.NOT_FOUND),
    )
)
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:edit', fixture('comment_pk')),
        ('news:delete', fixture('comment_pk')),
    ),
)
def test_diff_clients_acess_edit_and_delete_comment(
    client_chosen, name, args, expected_status_code
):
    """
    Trying to get pages using different clients.

    Author_client - logged in, as news author.
    admin_client - logged in, as reader.
    """
    url = reverse(name, args=args)
    response = client_chosen.get(url)
    assert response.status_code == expected_status_code


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:edit', fixture('comment_pk')),
        ('news:delete', fixture('comment_pk')),
    ),
)
@pytest.mark.django_db
def test_annonymous_user_redirect_to_login_page(client, name, args):
    """
    Testing redirect for annonymous client.

    Using in-build client fixture.
    Do check with assertRedirects from pytest_django.asserts
    Expected code is 302. Checking route with ?next=.
    """
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
