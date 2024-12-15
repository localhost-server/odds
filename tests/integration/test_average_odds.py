from oddsportal import Match

def test_average_odds():
    url = 'https://www.oddsportal.com/basketball/usa/ncaa-2021-2022/houston-cougars-butler-bulldogs-tISqbm1U'
    match = Match.from_url(url)
    print("HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRRRRRRRRRRRRRRREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
    result = match.handicap_with_tightest_spread(('over-under', 1))
    assert result == {'average_odds': [1.8590711746586537, 1.8643468225135493], 'handicap': '123.50', 'spread': -0.005275647854895649}