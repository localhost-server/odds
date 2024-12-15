import pytest
from oddsportal.tournament import Tournament
from unittest import mock

@pytest.fixture
def tournament():
    with mock.patch('oddsportal.tournament.Tournament.all_matches_api_data', return_value=None):
        result = Tournament('/american-football/usa/xfl')
        yield result 

def test_all_matches(tournament):
    expected = []
    result = list(tournament.all_matches('2023'))
    assert result == expected