import constant as c


class Show:
    index = None
    title = None
    desc = None

    preview_img = None
    full_scale_img = None

    category = None
    adv_category = None

    channel = None

    # series = None
    # episode = None

    def __init__(self, df):
        self.index = df['index']
        self.title = df['title']
        self.desc = df[c.DF_DESCRIPTION]
        self.category = df[c.DF_CATEGORY]
        self.channel = df['channel']
        self.adv_category = df['k_means']
        self.preview_img = df[c.DF_IMAGE_PREVIEW]
        self.full_scale_img = df[c.DF_IMAGE_LARGE]
        # self.series = df['series']
        # self.episode = df['episode']


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
