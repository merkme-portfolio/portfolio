from django.conf import settings
import pytest
from pytest_lazyfixture import lazy_fixture as fixture
from news.forms import CommentForm

pytestmark = pytest.mark.usefixtures('news_test_list')


@pytest.mark.django_db
def test_news_count_on_home_page(home_page_object_list):
    """Test that the home page displays the correct number of news objects."""
    assert len(home_page_object_list) == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(home_page_object_list):
    """Test that news on home page is sorted in reverse order."""
    all_dates = [news.date for news in home_page_object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
@pytest.mark.usefixtures('comments_test_list')
def test_comments_order(client, detail_url):
    """Test that comments on news page is sorted in reverse order."""
    response = client.get(detail_url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.django_db
@pytest.mark.parametrize(
    'client_chosen, have_form',
    (
        (fixture('author_client'), True),
        (fixture('client'), False)
    )
)
def test_different_client_has_form(client_chosen, have_form, detail_url):
    """
    Test that different clients have access to the comment form.

    Check form is displayed on the news detail page.
    Author_client is logged in, can send comment, means have form.
    Client is used for annonymous user, can't send comment, means haven't form.
    """
    response = client_chosen.get(detail_url)
    assert ('form' in response.context) is have_form
    if client_chosen == 'author_client':
        assert isinstance(response.context['form'], CommentForm)
