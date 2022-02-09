from send_email.jounal_feed_parsers import parse_physical_review_feed
from send_email.jounal_feed_parsers import RSS_feed_parsers

journal = 'Physical Review Physics'
feed_parser, URL = RSS_feed_parsers[journal]
result = feed_parser(URL, journal)
for elem in result:
    print(elem.date)
    print(elem)
