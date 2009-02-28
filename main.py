from __future__ import with_statement
import import_wrapper
import meta
import logging

from google.appengine.api             import users
from google.appengine.ext             import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import debris.filters # load and register the filters
from debris.page      import BlikiPage
from debris.html      import template, site_url, form_to_db, error_404
from debris.rss       import rss_worthy_pages_xml

def draft_filter(pages):
    """Filter the list of `pages' by removing 'draft' pages if admin is not logged in
    """
    if not users.is_current_user_admin():
        return (page for page in pages if page.draft == False)
    else:
        return pages

class MainPage(webapp.RequestHandler):
    def get(self):
        pages = BlikiPage.get_all_pages()
        pages = draft_filter(pages)
        template(self.response, 'main.html', {'pages': pages})
        
class ViewBlikiPage(webapp.RequestHandler):
    def get(self, path):
        page = BlikiPage.get_by_path(path)
        if page is None:
            error_404(self)
        else:
            template(self.response, 'blikipage.html', {'page': page, 'single': True})
        
class ViewTagPage(webapp.RequestHandler):
    def  get(self, tag):
        pages = BlikiPage.get_all_by_tag(tag)
        pages = draft_filter(pages)
        template(self.response, 'tag.html', {
            'tag': tag,
            'pages': pages,
            'messages': ["You are viewing pages tagged '<b>%s</b>'" % tag]
        })

class ViewRSSPage(webapp.RequestHandler):
    def get(self):
        pages = BlikiPage.get_all_rss_worthy_pages()
        pages = draft_filter(pages)
        self.response.headers['Content-Type'] = 'application/rss+xml'
        self.response.out.write(rss_worthy_pages_xml(self.request, pages))
        
class SearchPage(webapp.RequestHandler):
    def get(self):
        q = self.request.get('q')
        results = BlikiPage.search(q)
        results = draft_filter(results)
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
     (r'/rss', ViewRSSPage),
     (r'/tag/([0-9a-zA-Z]+)', ViewTagPage),
     (r'/([0-9a-zA-Z/]+)', ViewBlikiPage)],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
