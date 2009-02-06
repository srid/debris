from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from debris.db import Page
from debris    import template, form_to_db, SHELL


class MainPage(webapp.RequestHandler):
    def get(self):
        pages = Page.get_latest()
        template(self.response, 'recent.html', {'pages': pages})

class Admin_NewPage(webapp.RequestHandler):
    def get(self):
        SHELL()
        template(self.response, 'new-page.html', {})
    def post(self):
        page = Page()
        form_to_db(self.request, page)
        page.put()
        self.redirect('/')

class Admin_ViewEditPage(webapp.RequestHandler):
    def get(self, path, edit):
        if edit == None:
            template(self.response, 'recent.html',
                     {'pages': [Page.get_by_path(path)]})
        else:
            raise

application = webapp.WSGIApplication(
    [('/', MainPage),
     ('/([a-zA-Z/]+)/(\+edit)?', Admin_ViewEditPage),
     ('/-/admin/newpage', Admin_NewPage)],
    debug=True)

if __name__ == "__main__":
    run_wsgi_app(application)
