#!/usr/bin/python3
# Slightly modified version of https://gitlab.com/juergens/reddit_bot_base

import os, traceback, shutil, re, time, sys
from decouple import RepositoryIni
import praw, prawcore
from praw.exceptions import APIException

from . helper import s2b
from . helper import PicnicException
from . helper import MyLog
import logging
l = MyLog(stream=sys.stdout,#filename='logFile.log',
          format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
          level=logging.INFO)


class RedditBotBase(object):
    sleep_time_s = 10
    settingsFile = '.settings.ini'
    #RepositoryIni(settingsFile).__getitem__('DRYRUN')
    #RepositoryIni(settingsFile).__getitem__('DEBUG')
    #RepositoryIni(settingsFile).__getitem__('INCLUDE_OLD_MENTIONS')
    dry_run = s2b(None, True)
    debug = s2b(None, False)
    include_old_mentions = s2b(None, False)
    working_path = os.path.abspath("./data/working")

    def process_summon(self, mention):
        """
        this is how your bot will deal with requests.
        throw picnic-exceptions if you want to let "handle_user_error" handle it.
        @:return text for your reply (in reddit-markdown format)
        """
        raise NotImplementedError()

    def handle_user_error(self, mention, text):
        """
        This is how your bot will notify you of problems.
        This will be called whenever something happens, that the caller can deal with (e.g. bot is banned in the
        target-sub).
        some suggestions:
        * post in a thread made by automod (this is what stabbot does)
        * PM the dev
        * PM the user
        * log to console
        @:param text: the text of the error
        @:param metion: the summon, that caused the error
        """
        raise NotImplementedError()

    def __init__(self, user_agent, reddit_client_id, reddit_client_secret, reddit_user, reddit_password):

        self.reddit = praw.Reddit(client_id=reddit_client_id,
                                  client_secret=reddit_client_secret,
                                  username=reddit_user,
                                  password=reddit_password,
                                  user_agent=user_agent)
        l("config:"
          + f"\n\tdryrun: {self.dry_run}"
          + f"\n\tdebug: {self.debug}"
          + f"\n\told_mentions: {self.include_old_mentions}")

        l(f"reddit user: {self.reddit.user.me().name}")

    def __call__(self, *args, **kwargs):
        self.main_loop()

    def clear_env(self):
        if os.path.exists(self.working_path):
            shutil.rmtree(self.working_path)
        os.makedirs(self.working_path)
        os.chdir(self.working_path)

    def get_next_job(self):
        for mention in self.reddit.inbox.mentions(limit=50):
            if not mention.new and not self.include_old_mentions:
                continue
            if not self.dry_run:
                mention.mark_read()
            else:
                l("dryrun: " + str(self.dry_run))

            return mention

    def post_reply(self, reply_md, mention):
        l("post_reply... ")
        if self.dry_run:
            l(f"reply would be: {reply_md}")
            return

        for i in range(0, 5):
            try:
                mention.reply(reply_md)
                l('Reply sent')
                return

            except prawcore.exceptions.RequestException:
                l("RequestException... trying again")

            except APIException as e:
                if e.error_type == 'RATELIMIT':
                    l.w(f"I was posting too fast. Error-Message: {e}")
                    wait_time_m = int(re.search(r'\d+', str(e)).group()) + 1
                    if wait_time_m > 10:
                        wait_time_m = 10
                    l.w(f"going to sleep for {wait_time_m} minutes.")
                    time.sleep(wait_time_m * 60)
                else:
                    raise e
        l.e("post_reply... failed")

    def main_loop(self):
        l("starting...")
        while True:
            mention = None
            reply_md = None
            try:
                try:
                    self.clear_env()
                    mention = self.get_next_job()
                    if mention is None:
                        time.sleep(self.sleep_time_s)
                        continue

                    reply_md = self.process_summon(mention)

                    try:
                        self.post_reply(reply_md, mention)
                    except praw.exceptions.APIException as e:
                        if str(e) == 'DELETED_COMMENT':
                            # sometimes reddit does this for no apparent reason
                            # Wait and try once more
                            l.w("executing workaround for DELETED_COMMENT")
                            time.sleep(self.sleep_time_s)
                            self.post_reply(reply_md, mention)
                        else:
                            raise

                except praw.exceptions.APIException as e:
                    if str(e) == 'DELETED_COMMENT':
                        # if the comment really was deleted, tell the summoner about it
                        self.handle_user_error(mention, "I could not reply to [your comment](" + str(
                            mention.context) + "), because it has been deleted. \n___\n" + reply_md)
                    else:
                        tb = traceback.format_exc()
                        debug_info = str(e.__class__) + ", " + str(e.__doc__) + ", " + str(e) + "\n\n " + tb
                        l.e(debug_info)
                        self.handle_user_error(mention, "An unexpected error occurred in [your request](" + str(mention.context)
                                               + "). \n___\nHere are some debug-infos: \n\n" + debug_info)
                except prawcore.exceptions.Forbidden:
                    l.w("Error: prawcore.exceptions.Forbidden")
                    self.handle_user_error(mention, "I could not reply to [your comment](" + str(
                        mention.context) + "), because I have been banned in this community. \n___\n" + reply_md)

                except PicnicException as e:
                    l.e("Error")
                    self.handle_user_error(mention, "There was something wrong with [your request](" + str(mention.context)
                                           + "): \n\n" + str(e))
                except Exception as e:
                    tb = traceback.format_exc()
                    debug_info = str(e.__class__) + ", " + str(e.__doc__) + ", " + str(e) + "\n\n " + tb
                    l.e(debug_info)
                    self.handle_user_error(mention, "An unexpected error occurred in [your request](" + str(mention.context)
                                           + "). \n___\nHere are some debug-infos: \n\n" + debug_info)
            except Exception as e:
                l.e("fatal error")
                tb = traceback.format_exc()
                debug_info = str(e.__class__) + ", " + str(e.__doc__) + ", " + str(e) + "\n\n " + tb
                l.e(debug_info)
