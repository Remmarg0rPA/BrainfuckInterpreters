#!/usr/bin/python3

from brainfuck_bot import BrainFuckBot
from decouple import RepositoryIni

if __name__ == "__main__":
    getItem = lambda key: RepositoryIni('./brainfuck_bot/.settings.ini').__getitem__(key)
    b = BrainFuckBot(reddit_client_id = getItem('client_id'),
                reddit_client_secret = getItem('client_secret'),
                reddit_user = getItem('username'),
                reddit_password = getItem('password'),
                user_agent = getItem('user_agent'))
    b.dry_run = True
    b.debug = False
    b.include_old_mentions = False
    b()
