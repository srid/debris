from google.appengine.ext import db
from google.appengine.ext import search


class BlikiPage(db.Model):
    """Represent a webpage in database"""
    title           = db.StringProperty(multiline=False)
    path            = db.StringProperty(multiline=False)
    content         = db.TextProperty()
    tags            = db.StringListProperty()
    draft           = db.BooleanProperty()
    created_date    = db.DateTimeProperty(auto_now_add=True)    
    rss_worthy      = db.BooleanProperty()
    has_comments    = db.BooleanProperty()
    
    def __form_set_tags__(self, tags_list_as_string):
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
        page.rss_worthy = True
        page.title = page.path = page.content = "" # they cannot be None
        return page
        
    @staticmethod
    def get_all_rss_worthy_pages():
        return db.GqlQuery(
            "SELECT * FROM BlikiPage WHERE rss_worthy = True ORDER BY created_date DESC"
        )
        
    @staticmethod
    def get_all_pages():
        return db.GqlQuery(
            "SELECT * FROM BlikiPage ORDER BY created_date DESC"
        )
        
    @staticmethod
    def get_all_by_tag(tag):
        """Get all pages by tag"""
        return db.GqlQuery(
            "SELECT * FROM BlikiPage WHERE tags = :1", tag
        )
        
    @staticmethod
    def get_by_path(path):
        q = db.GqlQuery("SELECT * FROM BlikiPage WHERE path = :1", path)
        if q.count() > 0:
            return q[0]
        else:
            return None # none found
    
