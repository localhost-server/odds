import pytest
import datetime
from oddsportal import Match

@pytest.fixture()
def match():
    result = Match.from_url(url = 'https://www.oddsportal.com/hockey/usa/nhl/new-york-rangers-winnipeg-jets-trGRhSUH')
    yield result


def test_init_from_url(match):    
    assert match.date == datetime.date(2023, 2 , 20)

def test_match_date():
    match = Match.from_url(url = 'https://www.oddsportal.com/basketball/usa/wnba/los-angeles-sparks-indiana-fever-4l3sN3f1')
    assert match.date == datetime.date(2023, 7 , 25)