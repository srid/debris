from google.appengine.ext import db
from debris import rst2html

class BasePage(object):
    
    def content_as_html(self):
        return rst2html(self.content)
    content_as_html = property(fget=content_as_html)


class Page(db.Model, BasePage):
    """Represent a webpage in database"""
    title           = db.StringProperty(multiline=False)
    path            = db.StringProperty(multiline=False)
    created_date    = db.DateTimeProperty(auto_now_add=True)
    content         = db.TextProperty()
    belongs_to_blog = db.BooleanProperty()
    draft           = db.BooleanProperty()

    @staticmethod
    def create_in_memory():
        "Create a new `Page' that is not persisted until `put()' is called"
        page = Page()
        page.draft = True
        page.belongs_to_blog = True
        page.title = page.path = page.content = "" # they cannot be None
        return page
        
    @staticmethod
    def get_latest():
        """Get the last 10 pages that were created recently"""
        return db.GqlQuery(
            "SELECT * FROM Page ORDER BY created_date DESC LIMIT 10")

    @staticmethod
    def get_by_path(path):
        return db.GqlQuery("SELECT * FROM Page WHERE path = :1",
                           path)[0]
    
        
class SpecialPage(BasePage):
    """Represent a special bliki page - not stored in DB, but act on
    the DB data, for example.
    """
    

    