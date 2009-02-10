from google.appengine.ext import db
from debris import rst2html


class BlikiPage(db.Model):
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
        page = BlikiPage()
        page.draft = True
        page.belongs_to_blog = True
        page.title = page.path = page.content = "" # they cannot be None
        return page
        
    @staticmethod
    def get_recent_blog_entries():
        """Get the last 10 pages that were created recently and belongs to blog"""
        return db.GqlQuery(
            "SELECT * FROM BlikiPage WHERE belongs_to_blog = True ORDER BY created_date DESC LIMIT 10")

    @staticmethod
    def get_by_path(path):
        return db.GqlQuery("SELECT * FROM BlikiPage WHERE path = :1",
                           path)[0]
    

class SpecialPage(object):

    @property    
    def title(self):
        return 'Special/%s' % self.__class__.__name__
    
    
class AllPages(SpecialPage):
    
    @property
    def content(self):
        return 'Foo'
    