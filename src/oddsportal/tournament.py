import datetime
from bs4 import BeautifulSoup
from functools import cached_property, cache
from .utils import get
from .match import Match
from .team import Team
from urllib.parse import urlparse
import json
import re
import math
import logging

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"

logger = logging.getLogger(__name__)

class Tournament():
    def __init__(self, tournament):
        """
        URL path to tournament in the form of /sport/country/tournament such as:
        
        >>> tournament = Tournament('/american-football/usa/nfl')
        """
        self.host = 'https://www.oddsportal.com'
        self.tournament = tournament
        # the bookiehash comes from the pageVar javascript variable defined in oddsportal.com/sport/country/tournament when logged in
        self.bookiehash = 'X489013294X67133449X65536X0X134217984X0X0X0X0X0X0X0X10485760X134217729X512X1310722X2080X0X1024X16803840X135680X288'

    def __repr__(self):
        return f'{self.tournament}'

    @cached_property
    def seasons(self):
        """
        Retrieve all avaiable seasons in https://www.oddsportal.com/sport/country/tournament/results/
        """
        url = f'{self.host}{self.tournament}/results'
        soup = BeautifulSoup(get(url), 'lxml')
        seasons_select = [tag for tag in soup.find_all(name = 'select') if tag.get('id') != 'sign-up-country'][0]
        
        result = [
            (elem['value'], elem.string.strip()) 
            for elem in seasons_select.find_all(name = 'option')
        ]

        return result

    @cache
    def season_url(self, season):
        """
        Retrieve the season url from the available seasons
        """
        url = [u for u, s in self.seasons if s == season]
        if not url:
            raise Exception(f'Season {season} not found for {self}')
        return url[0]

    @cache
    def season_results_html(self, season):
        """
        Retrieve the season results html page
        """
        url = self.season_url(season)
        result = get(url)
        return result
    
    @cached_property
    def next_matches_urls(self):
        """
        Download the links for upcoming matches available in https://www.oddsportal.com/sport/country/tournament for the current season

        The data is extracted from the table with id="tournamentTable" and saved in the data/ directory.
        """
        url = f'{self.host}{self.tournament}'
        soup = BeautifulSoup(get(url), 'lxml')
        tag = soup.find('next-matches')
        if tag:
            result = json.loads(tag.get(':comp-data'))
            result = [f'{self.host}{match["url"]}' for match in result['d']['rows']]
        else:
            result = None
        return result

    @cache
    def all_matches_api_urls(self, season):
        logger.info(f'Indexing all matches for {season} season')
        soup = BeautifulSoup(self.season_results_html(season), 'html.parser')
        scripts = [
            elem.string
            for elem in soup.find_all('script') 
            if elem.string and 'var pageOutrightsVar' in elem.string
        ][0]
        
        script = re.search(r'var pageOutrightsVar = \'(.+)\';', scripts.string)
        page_outrights_var = json.loads(script.group(1).removeprefix("\'").removesuffix("\'"))
        
        url = f"https://www.oddsportal.com/ajax-sport-country-tournament-archive_/{page_outrights_var['sid']}/{page_outrights_var['id']}/{self.bookiehash}/1/0/"

        data = json.loads(get(url, xhr=True))

        total_rows = data['d']['total']
        if total_rows == 0:
            result = None
        else:
            rows_per_page = data['d']['onePage']
            pages = range(1, math.ceil(total_rows / rows_per_page)+1)
            result = [f'{url}page/{page}' for page in pages]
        return result

    @cache
    def all_matches_api_data(self, season):
        """
        Download the links for previous matches of a given season available in https://www.oddsportal.com/sport/country/tournament-season/results/

        >>> tournament.all_matches_api_data('2019/2020')
        """
        urls = self.all_matches_api_urls(season)
        if not urls:
            result = None
            logger.info(f'No match indexed')
        else:
            result = json.loads(get(urls[0], xhr=True))
            for url in urls[1:]:
                tmp = json.loads(get(url, xhr=True))
                result['d']['rows'].extend(tmp['d']['rows'])
            logger.info(f'Indexed {len(result["d"]["rows"])} matches')
        return result

    def all_matches(self, season):
        data = self.all_matches_api_data(season)
        if not data:
            return []
        else:
            for row in data['d']['rows']:
                yield Match(id = urlparse(row['url']).path,
                            event_id = row['encodeEventId'],
                            sport_id = row['sport-id'],
                            date = datetime.datetime.fromtimestamp(row['date-start-timestamp']).date(),
                            home_team = Team(name = row['home-name']),
                            away_team = Team(name = row['away-name']),
                            event_stage = row['event-stage-name'],)
    
    def matches_between(self, season, start_date, end_date):
        """
        Download the links for previous matches of a given season between two dates
        """
        for match in self.all_matches(season):
            if start_date <= match.date <= end_date:
                yield match
