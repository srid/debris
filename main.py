import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from debris.page import BlikiPage, AllPages
from debris      import template, form_to_db, SHELL


class MainPage(webapp.RequestHandler):
    def get(self):
        pages = BlikiPage.get_latest()
        template(self.response, 'recent.html', {'pages': pages})

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
        

class Admin_ViewPage(webapp.RequestHandler):
    def get(self, path):
        page = BlikiPage.get_by_path(path)
        template(self.response, 'blikipage.html',
                 {'page': page}) 

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
        
class Admin_ViewSpecialPage(webapp.RequestHandler):
    def get(self, path):
        page = AllPages()
        template(self.response, 'specialpage.html', {'page': page})

application = webapp.WSGIApplication(
    [(r'/', MainPage),
     (r'/-/admin/newpage', Admin_NewPage),
     (r'/-/admin/edit/([a-zA-Z/]+)', Admin_EditPage),
     (r'/Special/([a-zA-Z/]+)', Admin_ViewSpecialPage),
     (r'/([a-zA-Z/]+)', Admin_ViewPage)],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
