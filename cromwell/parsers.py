from BeautifulSoup import BeautifulSoup 

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
            player_info[info] = tdTag.contents
            tdTag = tdTag.findNext('td')

        return player_info

    def print_player(self, players):
        """Print the player data."""
        for player_info in players:
            print player_info["pos"]
            print player_info["id"]

            soup = BeautifulSoup(str(player_info["name"]))
            aTag = soup.find('a')
            print aTag.contents

            print player_info["team"]
            print player_info["pts"]
