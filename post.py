import os.path

class Post(object):
    """Represents a single blog post.

    Properties (set by dbconvert.convert_post() are:

    - nid: node ID (integer)
    - title: string
    - created: datetime
    - timestamp: datetime
    - url: string
    - tags: list of strings
    - filter: string
    - body: string
    """

    def slug(self):
        """Return a string with the last part of the URL."""
        return os.path.basename(self.url)

