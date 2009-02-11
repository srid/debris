from __future__ import with_statement
import import_wrapper
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from PyRSS2Gen import RSS2, RSSItem, Guid

from debris.page import BlikiPage, AllPages
from debris      import template, form_to_db, rst2html, StringIO, SHELL


class MainPage(webapp.RequestHandler):
    def get(self):
        blog_pages = BlikiPage.get_recent_blog_entries()
        template(self.response, 'main.html', {'blog_pages': blog_pages})
        
class BlogPage(webapp.RequestHandler):
    def get(self):
        pages = BlikiPage.get_recent_blog_entries()
        template(self.response, 'recent.html', {'pages': pages})
        
class ViewBlikiPage(webapp.RequestHandler):
    def get(self, path):
        page = BlikiPage.get_by_path(path)
        template(self.response, 'blikipage.html',
                 {'page': page}) 

class ViewSpecialPage(webapp.RequestHandler):
    def get(self, path):
        page = AllPages()
        template(self.response, 'specialpage.html', {'page': page})
        
class ViewRSSPage(webapp.RequestHandler):
    def get(self, name):
        if name == "all":
            # RSS of  newly created pages
            pages = BlikiPage.get_recent_entries()
            rss_items = []
            for page in pages:
                rss_items.append(RSSItem(
                    title = page.title,
                    link = page.get_url(),
                    description = rst2html(page.content),
                    guid = Guid(page.get_url()),
                    pubDate = page.created_date
                ))
            
            rss = RSS2(
                title = 'Yet Another Debris Bliki',
                link = "http://www.google.com/", # XXX
                description = "Foo",
                items = rss_items
            )
            
            self.response.headers['Content-Type'] = 'application/rss+xml'
            with StringIO() as sio:
                rss.write_xml(sio)
                self.response.out.write(sio.getvalue())
        else:
            raise Exception, 'unknown RSS type "%s"' % name
        
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
     (r'/blog', BlogPage),
     (r'/-/admin/newpage', Admin_NewPage),
     (r'/-/admin/edit/([0-9a-zA-Z/]+)', Admin_EditPage),
     (r'/RSS/([0-9a-zA-Z]+)', ViewRSSPage),
     (r'/Special/([0-9a-zA-Z/]+)', ViewSpecialPage),
     (r'/([0-9a-zA-Z/]+)', ViewBlikiPage)],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
