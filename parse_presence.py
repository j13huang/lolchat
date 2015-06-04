import xml.etree.ElementTree as ElementTree
import summoner

PRESENCE_STATUS_KEY = 'show'
PRESENCE_INFO_KEY = 'status'

DATA_STATUS_KEY = 'chatStatus'

def from_string(name, string):
    root = ElementTree.fromstring(string)

    return parse_presence(name, root)

def parse_presence(name, presence):
    data = {}
    status = ''
    info = []
    #print presence.findall('*')
    #print presence.findall('*/*')
    #print presence.findall('*/*/*')

    for child in presence:
        if child.tag == PRESENCE_STATUS_KEY:
            status = child

        if child.tag == PRESENCE_INFO_KEY:
            info = child.findall('*/*')
    
    data[DATA_STATUS_KEY] = status
    for child in info:
        data[child.tag] = child.text

    return summoner.Summoner(name, data)

if __name__ == '__main__':
    with open('presence.txt', 'r') as f:
        data = f.read()
        summoner = from_string('test', data)
        print summoner.data
