from oddsportal import Match

def test_init_from_url():    
    match = Match.from_url(url = 'https://www.oddsportal.com/basketball/usa/nba-2020-2021/new-york-knicks-washington-wizards-OGhiTcvM')
    result = match.handicap_with_tightest_spread(('over-under', 1))
