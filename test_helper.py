import datetime
import pytest
import helper

from main import app


@pytest.fixture(autouse=True)
def reset_items():
    helper.items.clear()
    yield
    helper.items.clear()


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_add_via_http_adds_item_transforms_b_and_sets_date(client):
    # Given
    text = "Bavub geht an die schbule"

    # When
    resp = client.post("/add", data={"text": text}, follow_redirects=False)

    # Then: redirect back to index
    assert resp.status_code in (301, 302, 303, 307, 308)

    # And: item persisted with transformation + date type
    assert len(helper.items) == 1
    item = helper.items[0]

    assert item.text == text.replace("b", "bbb").replace("B", "Bbb")
    assert isinstance(item.date, datetime.date)
    assert item.isCompleted is False


def test_index_renders_added_text(client):
    # Given
    client.post("/add", data={"text": "abc"}, follow_redirects=True)

    # When
    resp = client.get("/")

    # Then
    assert resp.status_code == 200
    html = resp.data.decode("utf-8")
    assert "abbbc" in html


def test_update_toggles_isCompleted(client):
    # Given
    client.post("/add", data={"text": "Task"}, follow_redirects=True)
    assert helper.items[0].isCompleted is False

    # When
    client.get("/update/0", follow_redirects=True)

    # Then
    assert helper.items[0].isCompleted is True

    # When
    client.get("/update/0", follow_redirects=True)

    # Then
    assert helper.items[0].isCompleted is False
