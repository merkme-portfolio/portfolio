from datetime import timedelta
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
import pytest
from news.models import News, Comment


@pytest.fixture
def author(django_user_model):
    """Create author user."""
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    """Authenticate author in client."""
    client.force_login(author)
    return client


@pytest.fixture
def news():
    """Fixture that creates a news object."""
    return News.objects.create(
        title='Заголовок',
        text='Текст',
    )


@pytest.fixture
def news_test_list():
    """List with test news."""
    today = timezone.now()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Текст',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)
    return all_news


@pytest.fixture
def home_page_object_list(client, home_page_url):
    """Object list from home page."""
    response = client.get(home_page_url)
    return response.context['object_list']


@pytest.fixture
def comment(news, author):
    """Fixture that creates comment objetct."""
    return Comment.objects.create(
        news=news,
        author=author,
        text='Коммент',
    )


@pytest.fixture
def comments_test_list(news, author):
    """List with test comments."""
    now = timezone.now()
    comment_list = []
    for index in range(2):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Текст {index} комментария.'
        )
        comment.created = now + timedelta(days=index)
        comment.save()
        comment_list.append(comment)
    return comment_list


@pytest.fixture
def home_page_url():
    """Return home page using reverse function."""
    return reverse('news:home')


@pytest.fixture
def detail_url(news_pk):
    """
    Return news page using reverse function.

    Args used from news_pk fixture.
    """
    return reverse('news:detail', args=news_pk)


@pytest.fixture
def comment_delete_url(comment_pk):
    """
    Return delete page for comment using reverse function.

    Args used from comment_pk fixture.
    """
    return reverse('news:delete', args=comment_pk)


@pytest.fixture
def comment_edit_url(comment_pk):
    """
    Return edit page for comment using reverse function.

    Args used from comment_pk fixture.
    """
    return reverse('news:edit', args=comment_pk)


@pytest.fixture
def comment_add_url():
    return reverse('news:add')


@pytest.fixture
def news_pk(news):
    """
    Get tuple with pk-key from Comment model.

    Need it for use as args in requests.
    """
    return news.pk,


@pytest.fixture
def comment_pk(comment):
    """
    Get tuple with pk-key from Comment model.

    Need it for use as args in requests.
    """
    return comment.pk,


@pytest.fixture
def form_data(news, author):
    """Text value for use as a data for HTTP request."""
    return {
        'news': news,
        'text': 'Комментарий',
        'author': author,
    }


@pytest.fixture
def comments_expected_result():
    """Need to calculate number of test news created."""
    return Comment.objects.count()


@pytest.fixture
def last_comment_created():
    """Need to get last comment object."""
    return Comment.objects.last


@pytest.fixture
def comments_url(detail_url):
    """Return page with news and pull it to comments block."""
    return detail_url + '#comments'
