import pytest
from oddsportal.tournament import Tournament
from pathlib import Path
from unittest import mock

@pytest.fixture
def tournament():
    url = 'https://www.oddsportal.com/ajax-sport-country-tournament-archive_'
    sid = '5'
    id = '69gXStto'
    bookiehash = 'X489013294X67133449X65536X0X134217984X0X0X0X0X0X0X0X10485760X134217729X512X1310722X2080X0X1024X16803840X135680X288'
    return_value = [
        f'{url}/{sid}/{id}/{bookiehash}/1/0/page/1',
        f'{url}/{sid}/{id}/{bookiehash}/1/0/page/2',
        f'{url}/{sid}/{id}/{bookiehash}/1/0/page/3',
        f'{url}/{sid}/{id}/{bookiehash}/1/0/page/4',
        f'{url}/{sid}/{id}/{bookiehash}/1/0/page/5',
        f'{url}/{sid}/{id}/{bookiehash}/1/0/page/6',
        f'{url}/{sid}/{id}/{bookiehash}/1/0/page/7',
    ]
    
    path = Path('data/ajax-sport-country-tournament-archive_/page')
    side_effect = []
    for file in path.glob('*.json'):
        data = open(file).read()
        side_effect.append(data)
    with (
        mock.patch('oddsportal.tournament.Tournament.all_matches_api_urls', return_value=return_value),
        mock.patch('oddsportal.tournament.get', side_effect=side_effect)):
        result = Tournament('/american-football/usa/nfl')
        yield result

def test_all_matches_api_data(tournament):
    result = tournament.all_matches_api_data('2019/2020')
    assert result['d']['total'] == len(result['d']['rows'])