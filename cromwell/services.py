import urllib2

class DataSource(object):
    def read_url(self, url):
        """Read a url as a data source."""
        response = urllib2.urlopen(url)
        html = response.read()
        response.close()

        return html

    def read_file(self, filename):
        """Reads a file as a data source."""
        f = open(filename)
        data = f.read()
        f.close()

        return data

    def set_proxy(self, proxy):
        """Setup proxy authentication."""
        proxy_url = proxy
        proxy_support = urllib2.ProxyHandler({"http":proxy_url})
        opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler)
        urllib2.install_opener(opener)

if __name__ == '__main__':
    ds = DataSource()
    data = ds.read_file('D:/home/nick/dev/python/footyapp/source.html')

    from parsers import DreamTeamParser
    dtp = DreamTeamParser()
    players = dtp.parse(data)

    dtp.print_player(players)
