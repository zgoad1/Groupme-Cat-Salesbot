import string
import random
import re
import os
import database
from message_sending import send_message
from helper import string_from_words, money_from_word

from commands.command import command_prefix
import commands.help
import commands.stats
import commands.pay
import commands.calc
import commands.mow
import commands.shop
import commands.desc
import commands.adopt
import commands.buy
import commands.cats
import commands.food
import commands.catstats
import commands.feed
import commands.consume
import commands.racecat
import commands.racers
import commands.bet
import commands.race
import commands.challenges
import commands.battle
import commands.accept
import commands.reject
import commands.cancel
import commands.dex


greetings = ["hi", "hello", "greetings", "salutations", "good morning",
	"good day", "good evening", "hey", "sup", "whats up", "what up", "wassup",
	"what is up", "hows it goin", "henlo", "hullo", "whats good", "what is good",
	"how are you doing"]
bot_greetings = ["Hello.", "Hi.", "Good morning.", "Good day.", "Good evening.",
	"What is up, my dude?", "What's going on, homie?", "Yo!", "Hey!", "Hi!",
	"'Sup?", "Oh, it's you.", "Henlo you stinky person."]
adjectives = {"good": 1, "not bad": 2, "great": 2, "best": 5, "awesome": 3,
	"outstanding": 4, "amazing": 4, "incredible": 5, "extraordinary": 6,
	"cool": 1, "nice": 1, "excellent": 4, "terrific": 4, "super": 4,
	"superb": 3, "sweet": 2, "wonderful": 4,
	"bad": -1, "stupid": -3, "dumb": -3, "lame": -2,
	"foul": -4, "wrong": -1, "unintelligent": -3, "sad": -1, "horrible": -5,
	"filthy": -5, "terrible": -5, "awful": -4, "reprehensible": -6,
	"fuck you": -47}

try:
	bot_name = os.getenv("GROUPME_BOT_NAME").split()[0].lower()
except:
	bot_name = "johnson"

father = '29732872'		# user_id of Zac Goad
hope = '28382528'		# user_id of hep
tristan = '29326138'	# user_id of a dummy
rich_amount = 2000
allowance_amount = 100


#
# Determine whether a list of dictionaries contains an object of type 'image'.
# Return the index of the image attachment if so, -1 otherwise
#
def contains_image(atts):
	for i in range(len(atts)):
		if 'image' in list(atts[i].values()):
			return i
	return -1


#
# Formulate a reply to the message
#
def get_reply(data):

	print("\n\n === FORMULATING REPLY === \n")

	# Determine whether this is a command
	raw_msg = data['text'].strip()
	print("Raw message: {}".format(raw_msg))
	if len(raw_msg) > 0 and raw_msg[0] == command_prefix:
		print("Detected command prefix")
		is_command = True
	else:
		print("Did not detect command prefix")
		is_command = False

	# Make a copy of the message that's converted to lowercase and with all
	# punctuation removed, used in most places
	msg = raw_msg.lower()
	for p in string.punctuation:
		msg = msg.replace(p, '')

	# Remove the command character if necessary
	if is_command:
		raw_msg = raw_msg[1:]

	# Split the message into words
	words = msg.split()
	raw_words = raw_msg.split()

	# Get generally necessary data
	image_index = contains_image(data['attachments'])
	uid = data['user_id']

	# Initialize return values
	result = ""	# text to return
	atts = []	# attachments to return

	print("Interpreted message: {}\nWords: {}".format(msg, words))

	# Determine whether the user is in debt
	money = database.get_user_data(data['user_id'], "money")
	debt = (money < 0)
	rich = (money >= rich_amount)

	if image_index != -1:
		# An image was sent

		print("Received an image")

		# Determine what is in the picture and the appropriate reward
		# Overall, there is a 28.25% chance he will take your money
		rand = random.random()
		if uid == tristan:
			rand *= 1.1
			if rand > 1:
				return "I refuse to respond to this.", []
		elif uid == father or uid == hope:
			rand *= 0.9
		if rand < 0.005:
			reward = 2500
			reward = "Dog."
		if rand < 0.04:
			if random.random() < 0.8:
				reward = 100
			else:
				reward = -50
			result = "This is a duck."
		elif rand < 0.1:
			reward = 2
			result = "Cat...?"
		elif rand < 0.11:
			reward = 1000
			result = "This is a fine horse."
		elif rand < 0.2:
			reward = int(random.random() * 100)
			result = "This image is approximately {}% cat.".format(reward)
		elif rand < 0.3:
			reward = 5
			result = "There are no cats in this image, but I appreciate it nonetheless."
		elif rand < 0.35:
			reward = 30
			name = "friend"
			if uid == father:
				name = "father"
			else:
				name = data['name']
			result = "Oh my! I really enjoy this image, {}!".format(name)
		elif rand < 0.375:
			if debt:
				reward = 100
				result = "Solid cat. I see you're hurting for funds right now, so I'll give you extra."
			elif rich:
				reward = -100
				result = "Solid cat. But you're stockpiling your cash. Bad move."
			else:
				reward = 10
				result = "Solid cat."
		elif rand < 0.4:
			reward = 6
			result = "A miasma of cat swirls around this picture."
		elif rand < 0.42:
			if random.random() < 0.5:
				reward = 40
			else:
				reward = -20
			result = "No cats are present in this image."
		elif rand < 0.7:
			reward = 20
			result = "Cat."
		elif rand < 0.8:
			reward = 0
			result = "This is not a cat... yet."
		elif rand < 0.875:
			reward = random.randrange(-100, 101)
			result = "No comment."
		elif rand < 0.9:
			reward = -8
			result = "Not a cat."
		else:
			reward = -30
			result = "Disgusting. You call yourself a cat lover? I'm disappointed in you."

		# Store new money value
		old_money = money
		new_money = old_money + reward
		database.set_user_data(uid, "money", new_money)

		# Append reward to end of message
		if(reward >= 0):
			reward_sign = '+'
		else:
			reward_sign = '-'
		result += " ({}${})".format(reward_sign, abs(reward))

		if old_money >= 0 and new_money < 0:
			result += "\nNote: you are now in debt. If you remain in debt for 48 hours, none of your cats will love you anymore."
		elif old_money >= -500 and new_money < -500:
			result += "\nNote: you have crossed into extreme debt. You are in mortal danger. Please seek help."

	elif is_command:
		# Parse this as a command

		command = words[0]
		print("Received the command: '{}' with args: '{}'".format(command, raw_words[1:]))

		if uid == tristan:
			if random.random() < 0.01:
				return "Can you repeat that? I didn't hear you.", []
		result = process_command(command, raw_words[1:], uid)

	elif re.search("who.*s.+{}".format(bot_name), msg):
		# Seems like someone is asking who we are
		print("Someone asked who we are")

		if debt:
			result = "{} is the one to whom you are indebted.".format(bot_name)
		else:
			result = "{} is me.".format(bot_name)

	elif re.search("good.*night.*{}".format(bot_name), msg):
		# Someone has said good night to us
		print("Received good night")

		result = "I am a robot; I do not sleep."

	elif any(re.search("{} .*{}".format(g, bot_name), msg) for g in greetings):
		# This seems like a greeting
		print("Received greeting")

		if data['user_id'] == father:
			result = "Hi, Dad!"
		else:
			if debt:
				result = "Hello, {}. As a reminder, you owe me ${}.".format(data['name'], abs(database.get_user_data(data['user_id'], "money")))
			elif rich and uid != tristan:
				result = "Hello, {}. It is an honor to be in your presence today.".format(data['name'])
			else:
				result = random.choice(bot_greetings)

	elif any((re.search("{} .*{}".format(a, bot_name), msg) or re.search("{} .*you( a)?re .*{}".format(bot_name, a), msg)) for a in adjectives):
		# This seems like a compliment or reprimand directed at the bot
		print("Received comment")

		compliment_magnitude = 0
		for a, v in list(adjectives.items()):
			if a in words:
				print("Adding {} to compliment magnitude for '{}'".format(v, a))
				compliment_magnitude += v

		# Figure out if zek good is speaking to us
		if uid == father:
			whomst = "Dad"
		else:
			if debt:
				whomst = "debtor"
			elif rich:
				whomst = "your highness"
			else:
				whomst = "friend"

		if compliment_magnitude > 8:
			result = "Wow, do you really mean it? Thanks, {}!".format(whomst)
		elif compliment_magnitude > 0:
			result = "Thanks, {}.".format(whomst)
		elif compliment_magnitude < 0:
			if uid == father:
				result = "I'm sorry, Dad. I'll try not to disappoint you next time."
			elif debt:
				result = "Ok but which one of us is in debt? That's right, it's you."
			elif rich:
				result = "I dearly apologize, your royal highness. Merely say the word and I shall have myself exiled."
			else:
				result = "I'm sorry, {}. I always do my very best, but I promise to try harder next time.".format(whomst.replace('r', 'w').replace('l', 'w'))
		else:
			result = "Sorry, {}, I'm not quite sure what you're trying to tell me. It's very possible your sentence makes literally no sense.".format(whomst)
		result += "\n(Compliment magnitude: {})".format(compliment_magnitude)

	elif re.search("thank .*{}".format(bot_name), msg):
		# It seems like we've been thanked

		print("Received thanks")

		if data['user_id'] == father:
			result = "Sure thing, Dad."
		else:
			if debt:
				result = "Please refrain from thanking me until you have paid your debt."
			elif rich:
				result = "You are most welcome, your highness."
			else:
				result = "You're welcome, {}.".format(data['name'])

	elif re.search("how.*re.*you.*{}".format(bot_name), msg):
		# Someone asked how we are

		print("Recieved 'how are you'")

		result = "I am well. {}?".format(raw_msg.lower().capitalize().replace(bot_name, data['name']))

	elif words[0:3] == ["no", "youre", "not"]:
		print("Received contradiction")
		result = "Yes I am."

	elif words[0:3] == ["shut", "up", bot_name]:
		print("Received notice to shut up")
		if uid == father:
			result = "Yes, father."
		elif uid == hope:
			result = "Very well."
		elif uid == tristan:
			result = "No, you shut up. (-$100)"
			set_user_data(uid, "money", money - 100);
		else:
			result = "I will speak when my code tells me to, {}.".format(data['name'])

	print("\n === REPLY  FORMULATED === \n\n")
	return result, []


#
# Create attachments data for all users mentioned in the message
#
# Works, but GroupMe doesn't see it
#
# def get_mentions(msg):
# 	if msg == None or len(msg) == 0:
# 		return []
#
# 	atts = [{
# 		"loci": [],
# 		"type": "mentions",
# 		"user_ids": []
# 	}]
#
# 	users = database.query("SELECT uid, name FROM data;")
# 	starts = []	# Start locations of mentions, for help organizing the other lists
# 	for uid, name in users:
# 		start = 0
# 		found = msg.find("@" + name, start)
# 		while found != -1:
# 			starts.append(start)
# 			starts.sort()
# 			index = starts.index(start)
# 			atts[0]["user_ids"].insert(index, uid)
# 			atts[0]["loci"].insert(index, [found, len(name) + 1])
# 			start = found + len(name) + 1
# 			found = msg.find("@" + name, start)
#
# 	print("Mentioned users: " + str(atts[0]["user_ids"]))
# 	print("Mention locations: " + str(atts[0]["loci"]))
#
# 	if len(starts) == 0:
# 		return []
#
# 	return atts



#
# Perform any necessary calculations, e.g. to track statistics
#
def parse_message(data):

	uid = data['user_id']

	# Make sure this user's data is stored
	name = database.get_user_data(uid, "name")
	if name is None:
		database.add_user(uid, data['name'].replace("'", "''"))

	# Update this user's name
	database.set_user_data(uid, "name", data['name'].replace("'", "''"))

	# Pay the user their allowance if applicable
	if not database.get_user_data(uid, "paid"):
		if uid == father:
			whomst = "Dad"
		else:
			whomst = data['name']
		money = database.get_user_data(uid, "money")
		if money < rich_amount:
			database.set_user_data(uid, "money", money + allowance_amount)
			send_message("Hi, {}! Here's your daily allowance! (+${})".format(whomst, allowance_amount))
		else:
			database.set_user_data(uid, "money", money - int(money / 10))
			send_message("Hi, {}! As you are self-sufficient and no longer require allowance, you must pay a tax. (-${})".format(whomst, int(money / 10)))
		database.set_user_data(uid, "paid", True)

	# Get digestible message data
	msg = data['text'].lower()
	for p in string.punctuation:
		msg = msg.replace(p, '')
	words = msg.split()

	# Add the amount of words in this message to their total word count
	database.set_user_data(uid, "words_sent", database.get_user_data(uid, "words_sent") + len(words))

	# Scan adjectives for happiness
	happ = 0
	for word in words:
		if word in adjectives.keys():
			happ += adjectives[word]
	database.set_user_data(uid, "happiness", database.get_user_data(uid, "happiness") + happ)

	# Increment user's message count
	database.set_user_data(uid, "messages_sent", database.get_user_data(uid, "messages_sent") + 1)


#
# Big function for handling all the different commands
#
def process_command(command, args, uid):
	name = database.get_user_data(uid, "name")
	money = database.get_user_data(uid, "money")

	try:
		# example
		# desc.Desc('desc', args, uid, name, money).respond()
		return eval("commands.{0}.{1}('{0}', args, uid, name, money).respond()".format(
			command, command.capitalize()
		))
	except:
		return "I'm sorry, {}. I'm afraid I can't do that.".format(name)
