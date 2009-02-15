from __future__ import with_statement
import import_wrapper
import meta
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from PyRSS2Gen import RSS2, RSSItem, Guid

from debris.page import BlikiPage
from debris      import template, form_to_db, site_url, rst2html, StringIO, SHELL


class MainPage(webapp.RequestHandler):
    def get(self):
        pages = BlikiPage.get_all_pages()
        template(self.response, 'main.html', {'pages': pages})
        
class ViewBlikiPage(webapp.RequestHandler):
    def get(self, path):
        page = BlikiPage.get_by_path(path)
        template(self.response, 'blikipage.html',
                 {'page': page})
        
class ViewTagPage(webapp.RequestHandler):
    def  get(self, tag):
        pages = BlikiPage.get_all_by_tag(tag)
        template(self.response, 'tag.html', {
            'tag': tag,
            'pages': pages,
            'messages': ["You are viewing pages tagged '<b>%s</b>'" % tag]
        })

class ViewRSSPage(webapp.RequestHandler):
    def get(self, name):
        if name == "all":
            # RSS of  newly created pages
            pages = BlikiPage.get_all_rss_worthy_pages()
            rss_items = []
            for page in pages:
                rss_items.append(RSSItem(
                    title = page.title,
                    link = site_url(self.request, page.path),
                    author = meta.SITE_AUTHOR,
                    description = rst2html(page.content),
                    guid = Guid(page.get_url()),
                    pubDate = page.created_date
                ))
            
            rss = RSS2(
                title = meta.SITE_TITLE,
                link = site_url(self.request),
                description = meta.SITE_DESCRIPTION,
                items = rss_items
            )
            
            self.response.headers['Content-Type'] = 'application/rss+xml'
            with StringIO() as sio:
                rss.write_xml(sio)
                self.response.out.write(sio.getvalue())
        else:
            raise Exception, 'unknown RSS type "%s"' % name
        
class SearchPage(webapp.RequestHandler):
    def get(self):
        q = self.request.get('q')
        results = BlikiPage.search(q)
        template(self.response, 'search.html', {'results': results, 'q': q})
        
class Admin_NewPage(webapp.RequestHandler):
    def get(self):
        page = BlikiPage.create_in_memory()
        template(self.response, 'edit.html', {'page': page})

    def post(self):
        page = BlikiPage.create_in_memory()
        form_to_db(self.request, page)
        page.put()
        logging.info('New BlikiPage "%s" created' % page.path) 
        self.redirect('/')
        
class Admin_EditPage(webapp.RequestHandler):
    def get(self, path):
        page = BlikiPage.get_by_path(path)
        template(self.response, 'edit.html', {'page': page})
        
    def post(self, path):
        page = BlikiPage.get_by_path(path)
        form_to_db(self.request, page)
        page.put()
        logging.info('BlikiPage "%s" modified' % page.path) 
        self.redirect('/' + page.path)


application = webapp.WSGIApplication(
    [(r'/', MainPage),
     (r'/-/admin/newpage', Admin_NewPage),
     (r'/-/admin/edit/([0-9a-zA-Z/]+)', Admin_EditPage),
     (r'/Search', SearchPage),
     (r'/RSS/([0-9a-zA-Z]+)', ViewRSSPage),
     (r'/tag/([0-9a-zA-Z]+)', ViewTagPage),
     (r'/([0-9a-zA-Z/]+)', ViewBlikiPage)],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
