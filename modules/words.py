

class Module(object):
    def __init__(self, bot):
        self.bot = bot
        bot.events.on("received").on("message").on("channel"
            ).hook(self.channel_message)
        bot.events.on("received").on("command").on("words"
            ).hook(self.words, channel_only=True,
            usage="<nickname>", help=
            "See how many words you or the given nickname have used")
        bot.events.on("received").on("command").on("trackword"
            ).hook(self.track_word, min_args=1,
            help="Start tracking a word", usage="<word>",
            permission="track-word")
        bot.events.on("received").on("command").on("wordusers"
            ).hook(self.word_users, min_args=1,
            help="Show who has used a tracked word the most",
            usage="<word>")

    def channel_message(self, event):
        words = list(filter(None, event["message_split"]))
        word_count = len(words)

        user_words = event["user"].get_setting("words", {})
        if not event["channel"].name in user_words:
            user_words[event["channel"].name] = 0
        user_words[event["channel"].name] += word_count
        event["user"].set_setting("words", user_words)

        tracked_words = set(event["server"].get_setting(
            "tracked-words", []))
        for word in words:
            if word.lower() in tracked_words:
                setting = "word-%s" % word
                word_count = event["user"].get_setting(setting, 0)
                word_count += 1
                event["user"].set_setting(setting, word_count)

    def words(self, event):
        if event["args_split"]:
            target = event["server"].get_user(event["args_split"
                ][0])
        else:
            target = event["user"]
        words = target.get_setting("words", {})
        this_channel = words.get(event["target"].name, 0)
        total = 0
        for channel in words:
            total += words[channel]
        event["stdout"].write("%s has used %d words (%d in %s)" % (
            target.nickname, total, this_channel, event["target"].name))

    def track_word(self, event):
        word = event["args_split"][0].lower()
        tracked_words = event["server"].get_setting("tracked-words", [])
        if not word in tracked_words:
            tracked_words.append(word)
            event["server"].set_setting("tracked-words", tracked_words)
            event["stdout"].write("Now tracking '%s'" % word)
        else:
            event["stderr"].wrote("Already tracking '%s'" % word)

    def word_users(self, event):
        word = event["args_split"][0].lower()
        if word in event["server"].get_setting("tracked-words", []):
            word_users = event["server"].get_all_user_settings(
                "word-%s" % word, [])
            items = [(word_user[0], word_user[2]) for word_user in word_users]
            word_users = dict(items)

            top_10 = sorted(word_users.keys())
            top_10 = sorted(top_10, key=word_users.get, reverse=True)[:10]
            top_10 = [event["server"].get_user(nickname
                ).nickname for nickname in top_10]
            top_10 = ", ".join("%s (%d)" % (nickname, word_users[
                nickname.lower()]) for nickname in top_10)
            event["stdout"].write("Top '%s' users: %s" % (word, top_10))
        else:
            event["stderr"].write("That word is not being tracked")
