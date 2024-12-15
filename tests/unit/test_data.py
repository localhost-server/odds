import pytest

@pytest.fixture
def data():
    with open('data/american-footbal/usa/nfl/new-orleans-saints-minnesota-vikings-E3C0Iu6A.html') as fp:
        result = fp.read()
    return result

def test_data(data):
    assert data