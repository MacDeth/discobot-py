import random
import re
import pickle
from disco.bot import Bot, Plugin
from disco.types.message import MessageEmbed
from datetime import datetime

class MainUtility(Plugin):
    # Plugins provide an easy interface for listening to Discord events
    @Plugin.listen('ChannelCreate')
    def on_channel_create(self, event):
        event.channel.send_message('Woah, a new channel huh!')

    @Plugin.command('about')
    def on_about_command(self, event):
        embed = MessageEmbed()
        embed.set_author(name='MacDeth#0420',
            url='https://github.com/MacDeth/discobot-py',
            icon_url='https://macdeth.keybase.pub/avatar.png')
        embed.title = 'About'
        embed.url = 'https://github.com/MacDeth/discobot-py'

        event.msg.reply(embed=embed)

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

    @Plugin.command('roll', '[amount:int] [value:int] [additions:int...]')
    def on_roll2_command(self, event, amount=1, value=20, additions=[]):
        sum = 0
        crits = 0
        fails = 0

        for i in range(amount):
            roll = random.randint(1, value)
            if roll == value:
                crits += 1
            elif roll == 1:
                fails += 1
            sum += roll

        for elem in additions:
            sum += elem

        event.msg.reply('You\'ve rolled {0:,} with {1:,} d{2:,}, plus {3}.'.
            format(sum, amount, value, additions))
        if crits > 0 or fails > 0:
            event.msg.reply('Crits: {0:,}, Fails: {1:,}'.format(crits, fails))

    @Plugin.command('8ball', '[query:str...]')
    def on_8ball_command(self, event, query=''):
        with open('8ball_messages.pickle', 'rb') as pickle_file:
            replies = pickle.load(pickle_file)
            event.msg.reply(replies[random.randint(0, len(replies) - 1)])

    @Plugin.command('initiative', '<content:str...>')
    def on_initiative_command(self, event, content):
        tokens = re.split(r'\s+', content)
        dellist = []
        for i in reversed(range(len(tokens) - 1)):
            if tokens[i].isidentifier() and \
                tokens[i + 1].replace(' ', '').isidentifier():
                    tokens[i] += ' ' + tokens[i + 1]
                    dellist.append(i + 1)
        for n in dellist:
            del tokens[n]

        order = dict()
        pretty = '```\n'

        for character, initiative in zip(tokens[::2], tokens[1::2]):
            if initiative not in order:
                order[initiative] = list()
            order[initiative].append(character)

        for i in sorted(order.keys(), key=lambda s: int(s), reverse=True):
            pretty += '{:>3}: {}\n'.format(i, order[i])

        pretty += '```'
        event.msg.reply(pretty)

    @Plugin.command('attribute', '<key:str> [value:str...]')
    def on_attribute_command(self, event, key, value=None):
        if value == None:
            try:
                event.msg.reply(key + ' = ' + self.user_attributes[\
                    str(event.msg.member.user.id)][key])
            except:
                event.msg.reply('That attribute does not exist.')
        else:
            try:
                self.user_attributes[str(event.msg.member.user.id)][key] = value
            except:
                self.user_attributes[str(event.msg.member.user.id)] = dict()
                self.user_attributes[str(event.msg.member.user.id)][key] = value
            event.msg.reply(key + ' = ' + self.user_attributes[\
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
                items = pickle.load(open(rarity + '_magic.pickle', 'rb'))
                event.msg.reply(items[random.randint(0, len(items) - 1)])
            except:
                event.msg.reply(pretty[rarity] +
                    ' magic items pickle not found.')
        else:
            event.msg.reply('Rarities: `common`, `uncommon`, `rare`, ' +
                '`veryrare`, `legendary`')
