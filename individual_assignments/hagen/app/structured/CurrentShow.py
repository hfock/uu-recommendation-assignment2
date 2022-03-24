class CurShow:

    index = None
    title = None
    desc = None

    img = None

    category = None
    adv_category = None

    channel = None

    def __init__(self, df):
        self.index = df['index']
        self.title = df['title']
        self.desc = df['description']
        self.category = df['category']
        self.channel = df['channel']
        self.adv_category = df['adv_category']
        self.img = df['img']


class CurShowJson:
    index = None
    title = None
    desc = None

    category = None

    channel = None

    release_year = None
    duration = None

    def __init__(self, json):
        self.index = json['Index']
        self.title = json['Title']
        self.desc = json['Description']
        self.category = json['Category']
        self.channel = json['Channel']
        self.release_year = json['Release Year']
        self.duration = json['Duration in Minutes']

