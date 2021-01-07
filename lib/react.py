from collections import defaultdict
from re import search
from datetime import datetime, timedelta
from random import randint

from . import db

welcomed = []
messages = defaultdict(int)


# Processes reactions for welcome, bye, activity, and cheers
def process(bot, user, message):
	update_records(bot, user)

	if user["id"] not in welcomed:
		welcome(bot, user)

	elif "bye" in message:
		say_goodbye(bot, user)


	if user["id"] != "[user id]" or user["id"] != "[any other bot ids]":
		check_activity(bot, user)

	if(match := search(r'cheer[0-9]+', message)) is not None:
		thank_for_cheer(bot, user, match)



# Updates records in sql database for user and messages
def update_records(bot, user):
	db.execute("INSERT OR IGNORE INTO users (UserID) VALUES (?)",
		user["id"])

	db.execute("UPDATE users SET MessagesSent = MessagesSent + 1 WHERE UserID = ?", 
		user["id"])


# Command that welcomes user when a message is sent - resets when bot resets
def welcome(bot, user):
	bot.send_message(f"Welcome to the stream {user['name']}!")
	welcomed.append(user["id"])


# Command that says goodbye to the user based off the word bye
def say_goodbye(bot, user):
	bot.send_message(f"See ya later {user['name']}!")


# Command that thanks user at 75* messages sent 
def check_activity(bot, user):
	messages[user["id"]] += 1

	if(count := messages[user["id"]]) % 75 == 0:
		bot.send_message(f"Thanks for being active in the chat {user['name']} - you've sent {count:,} messages! Nice!")


# Command for thanking any cheers given
def thank_for_cheer(bot, user, match):
	bot.send_message(f"Thanks for the {match.string[5:]:,} bits, {user['name']}! I appreciate it!")

