import os, glob, sys, logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from debris.page import BlikiPage, AllPages
from debris      import template, form_to_db, SHELL

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
     (r'/Special/([0-9a-zA-Z/]+)', ViewSpecialPage),
     (r'/([0-9a-zA-Z/]+)', ViewBlikiPage)],
    debug=True)

def main():
    root = os.path.dirname(__file__)
    for ziplib in glob.glob(os.path.join(root, '3rdparty', '*.zip')):
        logging.info("Adding 3rdparty library '%s' to sys.path" % ziplib)
        sys.path.insert(0, ziplib)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
