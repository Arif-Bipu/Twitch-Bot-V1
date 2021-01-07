"""
	COPYRIGHT INFORMATION
	---------------------

Python Twitch Bot (bot.py)


Some code in this file is licensed under the Apache License, Version 2.0.
    http://aws.amazon.com/apache2.0/


Copyright © Arif-Bipu 2020

    """

from irc.bot import SingleServerIRCBot
from requests import get

from lib import db, cmds, react


NAME = "[bot name]"
OWNER = "[twitch user]"


class Bot(SingleServerIRCBot):
	def __init__(self):
		# Setting up general items
		self.HOST = "irc.chat.twitch.tv"
		self.PORT = 6667
		self.USERNAME = NAME.lower()
		self.CLIENT_ID = ""
		self.TOKEN = ""
		self.CHANNEL = f"#{OWNER}"

		# Allows us to get the channel ID
		url = f"https://api.twitch.tv/kraken/users?login={self.USERNAME}"
		headers = {'Client-ID': self.CLIENT_ID, "Accept": "application/vnd.twitchtv.v5+json"}
		resp = get(url, headers=headers).json()
		self.channel_id = resp["users"][0]["_id"]

		# Runs the init function
		super().__init__([(self.HOST, self.PORT, f"oauth:{self.TOKEN}")], self.USERNAME, self.USERNAME)

	# When it joins the channel
	def on_welcome(self, cxn, event):
		for req in ("membership", "tags", "commands"):
			cxn.cap("REQ", f":twitch.tv/{req}")

		cxn.join(self.CHANNEL)
		db.build()
		self.send_message("Now online.")

	@db.with_commit
	def on_pubmsg(self, cxn, event):
		tags = {kvpair["key"]: kvpair["value"] for kvpair in event.tags}
		user = {"name": tags["display-name"], "id": tags["user-id"]}
		message = event.arguments[0]


		if user["name"] != NAME or user["id"] == 19264788:
			react.process(bot, user, message)
			cmds.process(bot, user, message)

	# Command to send messages with the bot
	def send_message(self, message):
		self.connection.privmsg(self.CHANNEL, message)

# Actual start
if __name__ == "__main__":
	bot = Bot()
	bot.start()

