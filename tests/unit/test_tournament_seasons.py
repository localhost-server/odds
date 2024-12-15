import pytest
from oddsportal.tournament import Tournament
from unittest import mock

@pytest.fixture
def tournament():
    html = open('data/american-footbal/usa/nfl/results.html').read()
    with mock.patch('oddsportal.tournament.get', return_value=html):    
        result = Tournament('/american-football/usa/nfl')
        yield result 

def test_seasons(tournament):
    expected = [('https://www.oddsportal.com/american-football/usa/nfl/results/', '2022/2023'),
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