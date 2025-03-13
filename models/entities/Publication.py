class Publication:
    def __init__(self, id_post, content, date, username=None):
        self.id = id_post
        self.content = content
        self.date = date
        self.username = username