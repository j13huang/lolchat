import xml.etree.ElementTree as ElementTree
from sleekxmpp.stanza.presence import Presence
import summoner

PRESENCE_SHOW_KEY = 'show'
PRESENCE_STATUS_KEY = 'status'

DATA_SHOW_KEY = 'show'

def from_string(name, string):
    root = ElementTree.fromstring(string)
    stanza = Presence(xml=root)

    #doesn't work
    #return parse_presence(name, stanza)

def parse_presence(name, presence):
    data = {}
    show = presence[PRESENCE_SHOW_KEY]
    data[DATA_SHOW_KEY] = show

    #import pdb; pdb.set_trace()
    #for stanza in presence.get_payload():
        #print stanza
    #print presence

    """
    for child in presence.get_payload():
        print child.name
        #if child.name == PRESENCE_SHOW_KEY:
            #show = child.text

        if child.name == PRESENCE_STATUS_KEY:
            status = child.findall('*/*')
    
    data[DATA_SHOW_KEY] = show
    for child in status:
        data[child.tag] = child.text

    return summoner.Summoner(name, data)
    """
    status = presence[PRESENCE_STATUS_KEY].encode('utf-8')
    #print status
    root = ElementTree.fromstring(status)
    #import pdb; pdb.set_trace()
    status_xml = root.findall('*')

    for child in status_xml:
        data[child.tag] = child.text.encode('utf-8') if child.text else child.text

    #print status.encode('utf-8')

    return summoner.Summoner(name, data)

if __name__ == '__main__':
    with open('presence.txt', 'r') as f:
        data = f.read()
        summoner = from_string('test', data)
        print summoner.data
