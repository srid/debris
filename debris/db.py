from google.appengine.ext import db


class Page(db.Model):
    """Represent a webpage in database"""
    title           = db.StringProperty(multiline=False)
    path            = db.StringProperty(multiline=False)
    created_date    = db.DateTimeProperty(auto_now_add=True)
    content         = db.TextProperty()
    belongs_to_blog = db.BooleanProperty()

    @staticmethod
    def get_latest():
        """Get the last 10 pages that were created recently"""
        return db.GqlQuery(
            "SELECT * FROM Page ORDER BY created_date DESC LIMIT 10")

    @staticmethod
    def get_by_path(path):
        return db.GqlQuery("SELECT * FROM Page WHERE path = :1",
                           path)[0]
        
