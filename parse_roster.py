import xml.etree.ElementTree as ElementTree
JID_KEY = 'jid'
NAME_KEY = 'name'

def from_string(string):
    root = ElementTree.fromstring(data)

    return parse_roster(root)

def parse_roster(root):
    jid_summoner = {}

    items = root.findall('*/*')
    for item in items:
        jid = item.attrib[JID_KEY]
        summoner = item.attrib[NAME_KEY]
        jid_summoner[jid] = summoner
    return jid_summoner

if __name__ == '__main__':
    with open('roster.txt', 'r') as f:
        data = f.readline()
        jid_summoner = from_string(data)
        print jid_summoner
