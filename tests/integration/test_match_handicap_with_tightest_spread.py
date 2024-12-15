from oddsportal import Match

def test_handicap_with_tightest_spread():
    match = Match.from_url(url = 'https://www.oddsportal.com/american-football/usa/nfl/new-orleans-saints-minnesota-vikings-E3C0Iu6A')
    result = match.handicap_with_tightest_spread(('ah', 1))
    assert result == {'average_odds': [1.9132917122992668, 1.9096451032103572], 'handicap': '4.00', 'spread': 0.0036466090889095693}