import time
import random
import re
import pickle
from disco.bot import Bot, Plugin
from disco.types.message import MessageEmbed
from datetime import time as dttime

class MainUtility(Plugin):
    # Plugins provide an easy interface for listening to Discord events
    @Plugin.listen('ChannelCreate')
    def on_channel_create(self, event):
        event.channel.send_message('Woah, a new channel huh!')

    # They also provide an easy-to-use command component
    @Plugin.command('ping')
    def on_ping_command(self, event):
        event.msg.reply('Pong!')

    # Which includes command argument parsing
    @Plugin.command('echo', '<content:str...>')
    def on_echo_command(self, event, content):
        event.msg.reply(content)

    @Plugin.command('time')
    def on_time_command(self, event):
        pass

    @Plugin.listen('GuildCreate')
    def on_guild_create(self, event):
        pass

class DnDUtility(Plugin):
    user_attributes = dict()

    def load(self, ctx):
        try:
            self.user_attributes = pickle.load(\
                open('user_attributes.pickle', 'rb'))
        except:
            pickle.dump(\
                self.user_attributes, open('user_attributes.pickle', 'wb'))

    def unload(self, ctx):
        pickle.dump(self.user_attributes, open('user_attributes.pickle', 'wb'))

    @Plugin.command('roll', '<amount:int> <value:int> [additions:int...]')
    def on_roll2_command(self, event, amount, value, additions=[]):
        #values = re.split(r'\W+', values)
        sum = 0
        for i in range(amount):
            sum += random.randint(1, int(value))

        for elem in additions:
            sum += elem

        event.msg.reply('You\'ve rolled {0:,} with {1:,} d{2:,}, plus {3}.'.
            format(sum, amount, value, additions))

    @Plugin.command('')
    def on__command(self, event):
        event.msg.reply('test.')

    @Plugin.command('initiative', '<content:str...>')
    def on_initiative_command(self, event, content):
        tokens = re.split(r'\W+', content)
        order = list()
        while tokens != list():
            mx = max([int(x) for x in tokens[1:len(tokens):2]])
            tiers = list()
            while tokens.count(str(mx)) > 0:
                #event.msg.reply('Tie detected: '+str(mx))
                windex = tokens.index(str(mx))
                tiers.append(tokens[windex - 1])
                del tokens[windex]
                del tokens[windex - 1]
            order.append((tiers, mx))

        event.msg.reply('Order, ties are grouped: '+str(order))

    @Plugin.command('attribute', '<key:str> [value:str...]')
    def on_attribute_command(self, event, key, value=None):
        if value == None:
            try:
                event.msg.reply(key+' = '+self.user_attributes[\
                    str(event.msg.member.user.id)][key])
            except:
                event.msg.reply('That attribute does not exist.')
        else:
            try:
                self.user_attributes[str(event.msg.member.user.id)][key] = value
            except:
                self.user_attributes[str(event.msg.member.user.id)] = dict()
                self.user_attributes[str(event.msg.member.user.id)][key] = value
            event.msg.reply(key+' = '+self.user_attributes[\
                str(event.msg.member.user.id)][key])
        pickle.dump(self.user_attributes, open('user_attributes.pickle', 'wb'))

    @Plugin.command('clearattributes')
    def on_clearattributes_command(self, event):
        self.user_attributes[str(event.msg.member.user.id)] = dict()
        pickle.dump(self.user_attributes, open('user_attributes.pickle', 'wb'))

    @Plugin.command('removeattribute', '<attribute:str>')
    def on_removeattribute_command(self, event, attribute):
        self.user_attributes[str(event.msg.member.user.id)][attribute] = None
        pickle.dump(self.user_attributes, open('user_attributes.pickle', 'wb'))

    @Plugin.command('rollmagic', '<rarity:str>')
    def on_rollmagic_command(self, event, rarity):
        pretty = {
            'common':       'Common',
            'uncommon':     'Uncommon',
            'rare':         'Rare',
            'veryrare':     'Very rare',
            'legendary':    'Legendary'}
        if rarity in pretty:
            try:
                items = pickle.load(open(rarity+'_magic.pickle', 'rb'))
                event.msg.reply(items[random.randint(0, len(items) - 1)])
            except:
                event.msg.reply(pretty[rarity]+' magic items pickle not found.')
        else:
            event.msg.reply('Rarities: `common`, `uncommon`, `rare`, '+
                '`veryrare`, `legendary`')
