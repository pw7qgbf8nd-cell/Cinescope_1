import pytest

pytestmark = pytest.mark.skip(reason="Тесты временно  отключены ил-за нестабильности")

@pytest.mark.smoke
def test_addition():
    assert 1 + 1 == 2


@pytest.mark.regression
def test_subtraction():
    assert 5 - 3 == 2

@pytest.mark.api
def test_multiplication():
    assert 2 * 3 == 6

@pytest.mark.slow
def test_division():
    assert 10 / 2 == 5

@pytest.mark.db
def test_db():
    assert 9 / 3 == 3

@pytest.mark.ui
def test_ui():
    assert 20 / 2 == 10