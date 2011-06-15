from nose.tools import *
from cromwell.services import DataSource
from cromwell.parsers import DreamTeamParser

def test_parser():
    data_source = DataSource()
    data = data_source.read_file('d:/home/nick/dev/python/'
                                 'footyapp/source.html')
    dt_parser = DreamTeamParser()
    players = dt_parser.parse(data)

    assert(len(players) == 418)

    #dt_parser.print_player(players)
    dt_parser.add_players(players)
