from BeautifulSoup import BeautifulSoup 
import sqlite3

class DreamTeamParser(object):
    
    def parse(self, html):
        """Parse the dream team html."""
        html = self.find_player_list(html)

        return self.parse_players(html)

    def find_player_list(self, html):
        """Strips the html down to just the <tbody>...</tbody> tags."""
        soup = BeautifulSoup(html)
        html = soup.find('tbody')

        # cast into a string
        html = str(html)

        return html

    def parse_players(self, html):
        """Parse a html table of players.

        Each player's information is contained within <tr>...</tr> tags.
        This method simply passes each <tr> section to the parse_player
        method.
        """
        soup = BeautifulSoup(html)
        html = soup.find('tr')

        players = []

        while html <> None:
            players.append(self.parse_player(str(html)))
            html = html.findNext('tr')

        return players

    def parse_player(self, html):
        """Extract the player information."""
        soup = BeautifulSoup(html)
        tdTag = soup.find('td')

        info_tags = ("pos", "id", "name", "team", "pts")

        player_info = {}

        for info in info_tags:
            player_info[info] = tdTag.contents[0]
            tdTag = tdTag.findNext('td')

        return player_info

    def print_player(self, players):
        """Print the player data."""
        for player_info in players:
            print player_info["pos"]
            print player_info["id"]

            soup = BeautifulSoup(str(player_info["name"]))
            aTag = soup.find('a')
            print aTag.contents[0]

            print player_info["team"]
            print player_info["pts"]

    def connect_db(self):
        return sqlite3.connect('./tmp/cromwell.db')

    def add_players(self, players):
        db = self.connect_db()

        for player in players:
            id = player['id']
            pos = self.translate_position(player['pos'])

            soup = BeautifulSoup(str(player['name']))
            aTag = soup.find('a')
            name = aTag.contents[0]

            club = self.translate_club(player['team'])
            pts = player['pts']

            db.execute('insert into players (id, name, pos, club, pts) values (?, ?, ?, ?, ?)',
                    [int(id), str(name), str(pos), str(club), float(pts)])
            db.commit()

    def translate_position(self, position):
        """Translate a position to a common name."""
        translate = {
                'GK': 'Keeper',
                'DEF': 'Defender',
                'MID': 'Midfielder',
                'STR': 'Striker',
                }
        return translate[position]

    def translate_club(self, club):
        """Translate a club to a common name."""
        translate = {
                'Arsenal': 'ars',
                'Aston Villa': 'ast',
                'Birmingham': 'bir',
                'Blackburn': 'blb',
                'Blackpool': 'blp',
                'Bolton': 'bol',
                'Chelsea': 'che',
                'Everton': 'eve',
                'Fulham': 'ful',
                'Liverpool': 'liv',
                'Man City': 'manc',
                'Man Utd': 'manu', 
                'Newcastle': 'new',
                'Stoke': 'sto',
                'Sunderland': 'sun',
                'Tottenham': 'tot',
                'West Brom': 'wesb',
                'West Ham': 'wesh',
                'Wigan': 'wig',
                'Wolves': 'wol',
                }
        return translate[club]
