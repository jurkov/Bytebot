#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from bytebot_config import BYTEBOT_PLUGIN_CONFIG
from plugins.plugin import Plugin
from urllib         import urlopen

import json

class spacestatus(Plugin):
    def onPrivmsg(self, irc, msg, channel, user):
        if msg.find('!status') != -1:
            try:
                response = urlopen(BYTEBOT_PLUGIN_CONFIG['spacestatus']['url'])
                data = json.loads(response.read())

                irc.msg(channel, 'Space status:')
                if data['state']['open']:
                    irc.msg(channel, '\tDer Space ist offen!')
                else:
                    irc.msg(channel, '\tDer Space ist geschlossen!')
            except Exception as e:
                irc.msg(channel, '\tFehler beim Abrufen des Status')