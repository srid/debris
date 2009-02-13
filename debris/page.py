from google.appengine.ext import db
from google.appengine.ext import search
from debris import rst2html

from debris import SHELL


class BlikiPage(db.Model):
    """Represent a webpage in database"""
    title           = db.StringProperty(multiline=False)
    path            = db.StringProperty(multiline=False)
    created_date    = db.DateTimeProperty(auto_now_add=True)
    content         = db.TextProperty()
    tags            = db.StringListProperty()
    belongs_to_blog = db.BooleanProperty()
    draft           = db.BooleanProperty()
    
    def __form_set_tags__(self, tags_list_as_string):
        #SHELL()
        tags = tags_list_as_string.split(' ')
        tags = [tag.strip() for tag in tags]
        self.tags = tags
    
    def get_url(self):
        return self.path # abs url?
    
    @staticmethod
    def search(keywords):
        query = search.SearchableQuery('BlikiPage')
        query.Search(keywords)
        return query.Run()
    
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
        """Get all pages that were created recently and belongs to blog"""
        return db.GqlQuery(
            "SELECT * FROM BlikiPage WHERE belongs_to_blog = True ORDER BY created_date DESC"
        )
        
    @staticmethod
    def get_non_blog_pages():
        """Get all pages that do NOT belong to blog"""
        return db.GqlQuery(
            "SELECT * FROM BlikiPage WHERE belongs_to_blog = False ORDER BY path DESC"
        )
        
    @staticmethod
    def get_all_by_tag(tag):
        """Get all pages by tag"""
        return db.GqlQuery(
            "SELECT * FROM BlikiPage WHERE tags = :1", tag
        )
        
    @staticmethod
    def get_recent_entries():
        """Get the last 10 pages that were created recently"""
        return db.GqlQuery(
            "SELECT * FROM BlikiPage ORDER BY created_date DESC LIMIT 10"
        )

    @staticmethod
    def get_by_path(path):
        return db.GqlQuery("SELECT * FROM BlikiPage WHERE path = :1",
                           path)[0]
    
