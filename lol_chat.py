import logging
import argparse
import getpass
import parse_roster
import parse_presence

from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout

DOMAIN = 'pvp.net'
RESOURCE = 'xiff'
PASSWORD_PREFIX = 'AIR_'

STANZA_ATTRIBUTE_TIMESTAMP = 'stamp'

class LoLChat(ClientXMPP):

    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message_received)
        #self.add_event_handler("presence_available", self.presence_available)
        #self.add_event_handler("presence_unavailable", self.presence_unavailable)
        #self.add_event_handler("presence_form", self.presence_form)
        #self.add_event_handler("sent_presence", self.sent_presence)
        self.add_event_handler("changed_status", self.changed_status)
        #self.add_event_handler("roster_update", self.roster_update)
        self.add_event_handler("got_online", self.got_online)
        self.add_event_handler("got_offline", self.got_offline)
        # xep_0030 dunno if you can use
        #self.add_event_handler("disco_info", self.disco_info)
        #self.add_event_handler("disco_items", self.disco_items)
        self.jid_summoner_name = {}
        self.summoners = {}
        self.online = []
        self.offline = []
        # jid, name
        self.current_user = ('','')

        # If you wanted more functionality, here's how to register plugins:
        # self.register_plugin('xep_0030') # Service Discovery
        # self.register_plugin('xep_0199') # XMPP Ping

        # Here's how to access plugins once you've registered them:
        # self['xep_0030'].add_feature('echo_demo')

        # If you are working with an OpenFire server, you will
        # need to use a different SSL version:
        # import ssl
        # self.ssl_version = ssl.PROTOCOL_SSLv3

    def run(self):
        xmpp.connect(address=('chat.na2.lol.riotgames.com',5223), use_tls=False, use_ssl=True)
        #xmpp.connect(address=('chat.na2.lol.riotgames.com',5223))
        #xmpp.process(block=True)
        xmpp.process(block=False)

    def session_start(self, event):
        presence = self.send_presence()
        roster = self.get_roster()
        self.jid_summoner_name = parse_roster.parse_roster(roster)
        self.offline = self.jid_summoner_name.keys()
        #print self.jid_summoner_name
        #import pdb; pdb.set_trace()

        # Most get_*/set_* methods from plugins use Iq stanzas, which
        # can generate IqError and IqTimeout exceptions
        #
        # try:
        #     self.get_roster()
        # except IqError as err:
        #     logging.error('There was an error getting the roster')
        #     logging.error(err.iq['error']['condition'])
        #     self.disconnect()
        # except IqTimeout:
        #     logging.error('Server is taking too long to respond')
        #     self.disconnect()

    def presence_available(self, presence):
        print 'available', presence.findall('*/*/*')

    def presence_unavailable(self, presence):
        print 'unavailable', presence.findall('*/*/*')

    def presence_form(self, presence):
        print 'form', presence.findall('*/*/*')

    def sent_presence(self, data):
        print 'sent_presence', data

    def changed_status(self, presence):
        from_jid = self.stanza_jid_from(presence)
        #print 'changed_status', from_jid, presence.findall('*')
        #print 'changed_status', from_jid, presence.findall('*/*')
        #print 'changed_status', from_jid, presence.findall('*/*/*')

    def roster_update(self, roster):
        print 'roster_update', roster.findall('*/*')

    def got_online(self, presence):
        #print presence
        from_jid = self.stanza_jid_from(presence)
        if from_jid in self.boundjid.full:
            summoner = parse_presence.parse_presence('Self', presence)
            print from_jid, summoner.name, summoner.data
            return

        if from_jid not in self.online:
            self.online.append(from_jid)

        if from_jid in self.offline:
            self.offline.remove(from_jid)

        name = self.jid_summoner_name[from_jid]
        summoner = parse_presence.parse_presence(name, presence)
        self.summoners[name] = summoner
        print 'online', from_jid, summoner.name, summoner.data
        #import pdb; pdb.set_trace()

    def got_offline(self, presence):
        from_jid = self.stanza_jid_from(presence)
        if from_jid not in self.jid_summoner_name:
            print 'offline from_jid {} doesn\'t exist'.format(from_jid)
            return

        if from_jid not in self.offline:
            self.offline.append(from_jid)

        if from_jid in self.online:
            self.online.remove(from_jid)

        if self.current_user[0] == from_jid:
            print 'current_user went offline'
            self.current_user = ('', '')

        name = self.jid_summoner_name[from_jid]
        summoner = self.summoners[name]
        print 'offline', from_jid, summoner.name, summoner.data
        #import pdb; pdb.set_trace()

    def message_received(self, message_stanza):
        print message_stanza
        from_jid = self.stanza_jid_from(message_stanza)
        name = 'Unknown'
        if from_jid in self.jid_summoner_name:
            name = self.jid_summoner_name[from_jid]

        timestamp = ''
        if STANZA_ATTRIBUTE_TIMESTAMP in message_stanza:
            timestanp = message_stanza[STANZA_ATTRIBUTE_TIMESTAMP]

        message = message_stanza['body'].text
        print '\n{} {}: {}\n{}>'.format(timestamp, name, message, self.current_user[0])
        #if msg['type'] in ('chat', 'normal'):
            #msg.reply("Thanks for sending\n%(body)s" % msg).send()

    def list_online(self):
        print 0, 'Nobody'
        for i, jid in enumerate(self.online):
            name = self.jid_summoner_name[jid]
            summoner = self.summoners[name]
            print i + 1, name, summoner.data

    def select_user(self, user_index):
        if user_index == 0:
            self.current_user = ('', '')
            return

        if not self.online:
            print 'select_user: no users online'
            return

        index = user_index - 1
        if index < 0 or index > len(self.online):
            print 'select_index: index {}, has to be between 0 and {}'.format(index, len(self.online))
            return

        jid = self.online[index]
        name = self.jid_summoner_name[jid] if jid in self.jid_summoner_name else ''
        self.current_user = (jid, name)

    def send_message_current_user(self, message):
        if not message:
            return

        if not self.boundjid.full:
            print 'no jid for self'
            return

        if not self.current_user:
            print 'no user selected for message'
            return

        self.send_message(self.current_user[0], message, mtype='chat', mfrom=self.boundjid)
        #print 'send_message', self.current_user[0], self.boundjid, message
        #print 'send_message: "{}"'.format(message)

    def stanza_jid_from(self, stanza):
        full_jid = stanza.get_from()
        return '{}@{}'.format(full_jid.username, full_jid.domain)

if __name__ == '__main__':
    # Ideally use optparse or argparse to get JID,
    # password, and log level.
    parser = argparse.ArgumentParser(description='connect to league of legends chat')
    parser.add_argument('username', type=str, nargs=1, help='LoL login name.')
    parser.add_argument('log_level', type=str, nargs='?', default='INFO', help='[INFO|WARNING|DEBUG|ERROR] default is INFO')

    args = parser.parse_args()

    logging.basicConfig(level=args.log_level,
                        format='%(levelname)-8s %(message)s')

    username = args.username[0]
    password = getpass.getpass()
    xmpp = LoLChat('{}@{}/{}'.format(username, DOMAIN, RESOURCE), '{}{}'.format(PASSWORD_PREFIX,password))
    #import pdb; pdb.set_trace()
    xmpp.run()
    try:
        while True:
            message = raw_input('{}>'.format(xmpp.current_user[1]))
            if message == '!exit' or message == '!q':
                break
            elif message == '!list' or message == '!l':
                xmpp.list_online()
            elif message == '!select':
                xmpp.list_online()

                while True:
                    message = raw_input('Select user (q to exit):'.format(xmpp.current_user[1]))
                    if message.isdigit() or message == 'q':
                        break

                    print 'invalid input (pick a number)'

                if message == 'q':
                    continue

                index = int(message)
                xmpp.select_user(index)
            elif message == '!status':
                pass
            else:
                if not xmpp.current_user[0]:
                    print 'use !select to select a current user first'
                    continue

                xmpp.send_message_current_user(message)
    except Exception as e:
        print e
    finally:
        print 'disconnecting'
        xmpp.disconnect(wait=False)
        exit()
