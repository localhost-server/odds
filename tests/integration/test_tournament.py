import datetime
import pytest
from oddsportal.tournament import Tournament
from oddsportal.match import Match
from oddsportal.team import Team

@pytest.fixture
def tournament():
    result = Tournament('/american-football/usa/nfl')
    return result 

def test_seasons(tournament):
    expected = [('https://www.oddsportal.com/american-football/usa/nfl/results/', '2023/2024'),
                ('https://www.oddsportal.com/american-football/usa/nfl-2022-2023/results/', '2022/2023'),
                ('https://www.oddsportal.com/american-football/usa/nfl-2021-2022/results/', '2021/2022'),
                ('https://www.oddsportal.com/american-football/usa/nfl-2020-2021/results/', '2020/2021'),
                ('https://www.oddsportal.com/american-football/usa/nfl-2019-2020/results/', '2019/2020'),
                ('https://www.oddsportal.com/american-football/usa/nfl-2018-2019/results/', '2018/2019'),
                ('https://www.oddsportal.com/american-football/usa/nfl-2017-2018/results/', '2017/2018'),
                ('https://www.oddsportal.com/american-football/usa/nfl-2016-2017/results/', '2016/2017'),
                ('https://www.oddsportal.com/american-football/usa/nfl-2015-2016/results/', '2015/2016'),
                ('https://www.oddsportal.com/american-football/usa/nfl-2014-2015/results/', '2014/2015'),
                ('https://www.oddsportal.com/american-football/usa/nfl-2013-2014/results/', '2013/2014'),
                ('https://www.oddsportal.com/american-football/usa/nfl-2012-2013/results/', '2012/2013'),
                ('https://www.oddsportal.com/american-football/usa/nfl-2011-2012/results/', '2011/2012'),
                ('https://www.oddsportal.com/american-football/usa/nfl-2010-2011/results/', '2010/2011'),
                ('https://www.oddsportal.com/american-football/usa/nfl-2009-2010/results/', '2009/2010'),
                ('https://www.oddsportal.com/american-football/usa/nfl-2008-2009/results/', '2008/2009'),]
    result = tournament.seasons
    assert result == expected

def test_all_matches_api_urls_fails_with_wrong_season(tournament):
    with pytest.raises(Exception) as err:
        result = tournament.all_matches_api_urls('2017')
    assert 'Season 2017 not found for /american-football/usa/nfl' in str(err)

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

def test_all_matches_api_data(tournament):
    result = tournament.all_matches_api_data('2019/2020')
    assert result['d']['total'] == len(result['d']['rows'])

def test_all_matches(tournament):
    expected = Match(id='/american-football/usa/nfl-2019-2020/kansas-city-chiefs-san-francisco-49ers-QNLis8yO/', 
                     event_id='QNLis8yO', 
                     sport_id=5, 
                     date=datetime.date(2020, 2, 2), 
                     home_team=Team(name='Kansas City Chiefs'), 
                     away_team=Team(name='San Francisco 49ers'),
                     event_stage = 'Finished')
    result = list(tournament.all_matches('2019/2020'))
    assert result[0] == expected

def test_matches_between(tournament):
    expected = [
        Match(id='/american-football/usa/nfl-2019-2020/kansas-city-chiefs-san-francisco-49ers-QNLis8yO/', 
              event_id='QNLis8yO', 
              sport_id=5, 
              date=datetime.date(2020, 2, 2), 
              home_team=Team(name='Kansas City Chiefs'), 
              away_team=Team(name='San Francisco 49ers'),
              event_stage = 'Finished'),
        Match(id='/american-football/usa/nfl-2019-2020/afc-nfc-OhIksAIi/', 
              event_id='OhIksAIi', 
              sport_id=5, 
              date=datetime.date(2020, 1, 26), 
              home_team=Team(name='AFC'), 
              away_team=Team(name='NFC'),
              event_stage = 'Finished')
    ]

    result = list(tournament.matches_between('2019/2020', datetime.date(2020, 1, 20), datetime.date.today()))

    assert result == expected