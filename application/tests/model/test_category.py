import pytest
from application.models.category_model import Category


@pytest.fixture
def category(session):
    category = Category(name="test name")
    session.add(category)
    session.commit()
    return category


def test_create_category_in_db(category):
    category_in_db = Category.query.get(category.id)

    assert category_in_db
    assert category_in_db.name == category.name


def test_get_name(category):
    assert category.name == category.get_name()
