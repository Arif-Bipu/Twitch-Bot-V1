# Inializes the bot and the defining commands
from time import time

from . import misc, games

PREFIX = "!"

class Cmd(object):
	def __init__(self, callables, func, cooldown=0):
		self.callables = callables
		self.func = func
		self.cooldown = cooldown
		self.next_use = time()



#cmds = {
#	"hello": misc.hello, 
#}

cmds = [
	#	Misc
	Cmd(["hello", "hi", "hey"], misc.hello, cooldown=5),
	Cmd(["about"], misc.about),
	Cmd(["uptime"], misc.uptime),
	Cmd(["userinfo", "ui"], misc.userinfo),
	Cmd(["shutdown"], misc.shutdown),

	#	Games
	Cmd(["coinflip", "flip"], games.coinflip, cooldown=5),
	Cmd(["penis"], games.penis, cooldown = 5),



]

# Processes the messages from the user and removes the prefix
def process(bot, user, message):
	if message.startswith(PREFIX):
		cmd = message.split(" ")[0][len(PREFIX):]
		args = message.split(" ")[1:]
		perform(bot, user, cmd, *args)

# Performs the actual command with the func command
def perform(bot, user, call, *args):
	if call in ("help", "commands", "cmds"):
		misc.help(bot, PREFIX, cmds)

	# Allows callables to be used for object oriented programming
	else:
		for cmd in cmds:
			if call in cmd.callables:
				if time()> cmd.next_use:
					cmd.func(bot, user, *args)
					cmd.next_use = time() + cmd.cooldown

				else:
					bot.send_message(f"Cooldown still in effect. Try again in {cmd.next_use-time():,.0f} seconds.")

				return

		bot.send_message(f"{user['name']}, \"{call}\" isn't a registered command.")



