import xml.etree.ElementTree as ElementTree
from sleekxmpp.xmlstream import stanzabase
JID_KEY = 'jid'
NAME_KEY = 'name'

def from_string(string):
    root = ElementTree.fromstring(string)
    stanza = stanzabase.StanzaBase(xml=root)

    return parse_roster(stanza)

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
        data = f.read()
        jid_summoner = from_string(data)
        print jid_summoner
