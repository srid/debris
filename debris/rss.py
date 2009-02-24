# Manage creation of site RSS

from PyRSS2Gen   import RSS2, RSSItem, Guid

import meta
from debris.html import site_url, rst2html
from debris.page import BlikiPage
from debris.util import file_write_to_string


def rss_worthy_pages_xml(request, pages):
    """Return the rss xml content containing all newly created pages
    that are 'rss worthy'
    """
    rss_items = []
    
    for page in pages:
        rss_items.append(
            RSSItem(
                title = page.title,
                link = site_url(request, page.path),
                author = meta.SITE_AUTHOR,
                description = rst2html(page.content),
                guid = Guid(site_url(request, page.path)),
                pubDate = page.created_date
            )
        )
   
    rss = RSS2(
        title = meta.SITE_TITLE,
        link = site_url(request),
        description = meta.SITE_DESCRIPTION,
        items = rss_items
    )
    
    return file_write_to_string(rss.write_xml)
        
