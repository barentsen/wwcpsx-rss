"""Creates an RSS feed for the CPSX Western Worlds podcast.

Crafted with ♥ for Jon Kissi and Raymond Francis.
"""
try:
    from urllib import request  # Python 3
except ImportError:
    import urllib2 as request  # Legacy Python
import re
from feedgen import feed


PODCAST_URL = "http://cpsx.uwo.ca/outreach/western_worlds/western_worlds_episodes.html"


if __name__ == "__main__":
    fg = feed.FeedGenerator()
    fg.id(PODCAST_URL)
    fg.title("CPSX Western Worlds")
    fg.description("""Western Worlds offers bi-weekly podcast programming 
                      that features an interview with space-relevant
                      researchers, engineers, scientists, or advocates
                      representing the local, national and global planetary
                      science and exploration communities. Interview content
                      is designed to be accessible and interesting for a wide
                      range of listeners and will be followed by a round-table
                      discussion involving several Western Worlds co-hosts, who
                      have a wide-variety of educational and professional
                      backgrounds.""")
    fg.link(href=PODCAST_URL, rel='alternate')
    fg.load_extension('podcast')
    fg.podcast.itunes_category('Science & Medicine', 'Natural Sciences')

    html = request.urlopen(PODCAST_URL).readlines()
    for line in html:
        groups = re.search("<p>.*\.\./img(.*mp3).*\">(.*)</a><br/>(.*)</p>", str(line))
        if groups is not None:
            url = "http://cpsx.uwo.ca/img" + groups.group(1)
            title = groups.group(2)
            desc = groups.group(3)
            # Add to the feed
            fe = fg.add_entry()
            fe.id(url)
            fe.title(title)
            fe.description(desc)
            fe.enclosure(url, 0, 'audio/mpeg')

    fg.rss_file('wwcpsx-rss.xml', pretty=True)
