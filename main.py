from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from debris.db import Page
from debris    import template, form_to_db, SHELL, rst2html


class MainPage(webapp.RequestHandler):
    def get(self):
        pages = Page.get_latest()
        template(self.response, 'recent.html', {'pages': pages, 'rst2html': rst2html})

class Admin_NewPage(webapp.RequestHandler):
    def get(self):
        page = Page.create_in_memory()
        template(self.response, 'edit-page.html', {'page': page})
    def post(self):
        page = Page.create_in_memory()
        form_to_db(self.request, page)
        page.put()
        self.redirect('/')

class Admin_ViewPage(webapp.RequestHandler):
    def get(self, path):
        page = Page.get_by_path(path)
        template(self.response, 'recent.html',
                 {'pages': [page], 'rst2html': rst2html}) 

class Admin_EditPage(webapp.RequestHandler):
    def get(self, path):
        page = Page.get_by_path(path)
        template(self.response, 'edit-page.html', {'page': page})
        
    def post(self, path):
        page = Page.get_by_path(path)
        form_to_db(self.request, page)
        page.put()
        self.redirect('/' + page.path)

application = webapp.WSGIApplication(
    [('/', MainPage),
     ('/-/admin/newpage', Admin_NewPage),
     ('/-/admin/edit/([a-zA-Z/]+)', Admin_EditPage),
     ('/([a-zA-Z/]+)', Admin_ViewPage)],
    debug=True)

if __name__ == "__main__":
    run_wsgi_app(application)
