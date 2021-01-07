from random import choice, randint
from time import time

from .. import db


#coinflip game
def coinflip(bot, user, side=None, *args):
	if side is None:
		bot.send_message("You need to guess which side the coin will land!")

	elif (side := side.lower()) not in (opt := ("h", "t", "heads", "tails")):
		bot.send_message("Enter one of the following as the side: " + ", ".join(opt))

	else:
		result = choice(("heads", "tails"))

		if side[0] == result[0]:
			bot.send_message(f"It landed on {result}! Nice job!")

		else:
			bot.send_message(f"Unlucky - it landed on {result}. Try again next time.")


def penis(bot, user, *args):
	
	penis_length = randint(1, 12)

	bot.send_message(f"{user['name']}'s penis is this big: " + "8{}D".format("=" * penis_length))



