import pytest
from oddsportal.tournament import Tournament
from unittest import mock

@pytest.fixture
def tournament():
    html = open('data/american-footbal/usa/nfl/nfl-2019-2020-results.html').read()
    json = open('data/ajax-sport-country-tournament-archive_/5-69gXStto-1-0.json').read()
    with (
        mock.patch('oddsportal.tournament.Tournament.season_results_html', return_value=html),
        mock.patch('oddsportal.tournament.get', return_value=json)
    ):
        result = Tournament('/american-football/usa/nfl')
        yield result 

def test_all_matches_api_urls(tournament):
    url = 'https://www.oddsportal.com/ajax-sport-country-tournament-archive_'
    sid = '5'
    id = '69gXStto'
    bookiehash = 'X489013294X67133449X65536X0X134217984X0X0X0X0X0X0X0X10485760X134217729X512X1310722X2080X0X1024X16803840X135680X288'
    expected = [
        f'{url}/{sid}/{id}/{bookiehash}/1/0/page/1',
        f'{url}/{sid}/{id}/{bookiehash}/1/0/page/2',
        f'{url}/{sid}/{id}/{bookiehash}/1/0/page/3',
        f'{url}/{sid}/{id}/{bookiehash}/1/0/page/4',
        f'{url}/{sid}/{id}/{bookiehash}/1/0/page/5',
        f'{url}/{sid}/{id}/{bookiehash}/1/0/page/6',
        f'{url}/{sid}/{id}/{bookiehash}/1/0/page/7',
    ]
    result = tournament.all_matches_api_urls('2019/2020')
    assert result == expected