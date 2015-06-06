class Summoner(object):
    DATA_SHOW_KEY = 'show'
    DATA_RESOURCE_KEY = 'resource'

    def __init__(self, name, data):
        self.name = name
        self.data = data

    def get_show(self):
        return self.data[self.DATA_SHOW_KEY] if self.DATA_SHOW_KEY in self.data else ''
