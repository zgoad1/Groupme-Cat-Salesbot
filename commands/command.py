command_prefix = "/"
commands = {
	"help": (
		"List commands.",		# Description
		"<topic>",				# Usage args
		"",						# Usage comments
		["basic"]				# Keyword tags (for /help <topic>)
		),
	"stats": (
		"View a user's stats.",
		"[user]",
		"",
		["basic", "user"]
		),
	"pay": (
		"Give someone Stuart Dollars™.",
		"<amount> <user>",
		"Note: Stuart Dollars™ cannot be split. <amount> must be a whole number.",
		["money"]
		),
	"calc": (
		"Do math.",
		"<math>",
		"",
		["basic"]
		),
	"mow": (
		"MOW",
		"",
		"",
		["basic"]
		),
	"shop": (
		"Shop for cats or food.",
		"<cats OR food>",
		"",
		["shop", "cat", "food"]
		),
	"desc": (
		"Describe a cat or food.",
		"<cat breed OR food type>",
		"",
		["shop", "cat", "food"]
		),
	"adopt": (
		"Adopt your very own feline.",
		"<cat #> <name>",
		"Use '/shop cats' to view adoptable felines.",
		["shop", "cat"]
		),
	"buy": (
		"Buy your very own cat food.",
		"<food #> <amount>",
		"Use '/shop food' to view all food for sale.",
		["shop", "food"]
		),
	"cats": (
		"View a user's cats.",
		"[user]",
		"",
		["cat", "user"]
		),
	"food": (
		"View a user's foods.",
		"[user]",
		"",
		["food", "user"]
		),
	"catstats": (
		"View a cat's stats.",
		"<cat name>",
		"",
		["cat"]
		),
	"feed": (
		"Feed a cat.",
		"<food #> <cat name>",
		"Use '/food' to view your available food and '/cats [user]' to view cats.",
		["food", "cat"]
		),
	"consume": (
		"Decrease your cat total.",
		"<cat name>",
		"WARNING: Using this command will delete a cat forever!",
		["cat"]
		),
	"racecat": (
		"Register a cat as your racecat.",
		"<cat name>",
		"",
		["race", "cat"]
		),
	"racers": (
		"View each user's designated racecat.",
		"",
		"",
		["race", "cat"]
		),
	"bet": (
		"Bet Stuart Dollars™ on a coin toss!",
		"<amount> <heads OR tails>",
		"",
		["money", "gambl"]
		),
	"race": (
		"Start a cat race between all racecats.",
		"",
		"Note: the existence of races is a myth.",
		["race", "gambl", "cat"]
		),
	"challenges": (
		"View incoming or outgoing challenge requests.",
		"<in OR out> [user]",
		"",
		["challenge", "gambl", "user"]
		),
	"battle": (
		"Send a cat battle request to a friend, betting Stuart Dollars™ that your cat will win.",
		"<cat 1> vs <cat 2>",
		"Note: the wager automatically increases with the win streaks between the two cats!",
		["battle", "challenge", "cat", "gambl"]
		),
	"accept": (
		"Accept a challenge request.",
		"<challenge ID>",
		"",
		["battle", "challenge"]
		),
	"reject": (
		"Reject a challenge request.",
		"<challenge ID>",
		"",
		["battle", "challenge"]
		),
	"cancel": (
		"Cancel a challenge you requested.",
		"<challenge ID>",
		"",
		["battle", "challenge"]
		),
	"dex": (
		"View accurate descriptions of Pokémon.",
		"<Pokémon>",
		"",
		["basic"]
		)
}


class Command:
	def __init__(self, command_name, args, uid, name = "", money = 0):
		self.args = args
		self.uid = uid
		self.name = name
		self.money = money
		self.command_name = command_name
		self.usage_desc, self.usage_args = commands[self.command_name][:2]
		try:
			self.usage_comments = commands[self.command_name][2]
		except:
			self.usage_comments = ""

	def usage(self):
		str = "{}\nUsage:\n{}{} {}\n{}".format(self.usage_desc, command_prefix,
			self.command_name, self.usage_args, self.usage_comments)
		return str

	def respond(self):
		print("Responding to '{}'.".format(self.command_name))
