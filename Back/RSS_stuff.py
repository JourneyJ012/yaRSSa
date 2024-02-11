import feedparser

def parse_url(url): #todo: make a toggle that allows the user to make whatever they want as a toggle
    feed = feedparser.parse(url)



    return feed.entries #Todo: make this into a toggle, then return a dict of what the people want.