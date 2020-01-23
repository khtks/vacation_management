import pytest
from application.models.post import *
from application.tests.model.test_category import *


@pytest.fixture
def post(category):
    post = Post(title="test title", body="test body", category=category)
    db.session.add(post)
    db.session.commit()
    return post


def test_create_post_in_db(post):
    post_in_db = Post.query.get(post.id)

    assert post_in_db
    assert post_in_db.title == post.title


def test_get_title(post):
    assert post.title == post.get_title()
