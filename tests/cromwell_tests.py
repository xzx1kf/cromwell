from nose.tools import *
from cromwell.services import DataSource 

def test_read_url():
    data_source = DataSource()
    data_source.set_proxy("http://internetemea.eds.com:8080")
    html = data_source.read_url('http://www.dreamteamfc.com/'
                                'fantasyfootball/1011/ViewPlayerList.aspx')
    assert(len(html) > 0)
    
def test_read_file():
    data_source = DataSource()
    data = data_source.read_file('d:/home/nick/dev/python/'
                                 'footyapp/source.html')
    assert(len(data) > 0)

