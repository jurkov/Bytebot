#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import json
#i use old version of requests
import requests0 as requests

from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from plugins.plugin import Plugin
from time import time

from bytebot_config import BYTEBOT_HTTP_TIMEOUT, BYTEBOT_HTTP_MAXSIZE
from bytebot_config import BYTEBOT_PLUGIN_CONFIG

class issue(Plugin):

    def __init__(self):
        pass

    def registerCommand(self, irc):
        irc.registerCommand('!issue', 'Create GitHub Issue')
    
    #https://gist.github.com/JeffPaine/3145490
    def make_github_issue(self, title, body=None, assignee=None, labels=None):
        '''Create an issue on github.com using the given parameters.'''
        # Our url to create issues via POST
        url = 'https://api.github.com/repos/%s/%s/issues' % (
            BYTEBOT_PLUGIN_CONFIG["issue"]["owner"], 
            BYTEBOT_PLUGIN_CONFIG["issue"]["name"]
        )
        # Create an authenticated session to create the issue
        session = requests.session(
            auth=(
                BYTEBOT_PLUGIN_CONFIG["issue"]["username"], 
                BYTEBOT_PLUGIN_CONFIG["issue"]["password"])
                )
        # Create our issue
        issue = {
                  "title": title,
                  "body": body,
                  "assignee": assignee,
                  "labels": labels
                }
        # Add the issue to our repository
        r = session.post(url, json.dumps(issue))
        if r.status_code == 201:
            #print 'Successfully created Issue "%s"' % title
            j = json.loads(r.content)
            return j['html_url']
        else:
            #print 'Could not create Issue "%s"' % title
            #print 'Response:', r.content
            return FALSE

    def onPrivmsg(self, irc, msg, channel, user):
        if msg.find('!issue') == -1:
            return

        self.irc = irc
        self.channel = channel

        try:
            last_iss = irc.last_iss
        except Exception as e:
            last_iss = 0

        if last_iss < (time() - 60):
            
            try:
                if(msg[0]=='!'):
                    soup = BeautifulSoup(
                        "<"+msg[1:]+">", 
                        'html.parser'
                    )
                    issue = self.make_github_issue(
                        soup.issue['t'], 
                        soup.issue['b'], 
                        "", 
                        ['irc']
                    )
                    print_str = "See: " + issue
                else:
                    print_str = "false syntax"
                    
                irc.msg(
                    channel, 
                        print_str.encode(
                            "utf-8", 
                            "ignore")
                    )

                irc.last_iss = time()

            except Exception as e:
                print(e)
                irc.msg(channel, 'Error while doing.')
        else:
            irc.msg(channel, "Don't overdo it ;)")
