import random
import helper
import database
from commands.command import Command


race_comments = ["the weather here is just perfect for cat racing!", "the audience is absolutely riled!", "I can't believe just how many people are here!", "gee, is it cold here!", "I'm sweating up a storm in this heat!", "I can feel the true essence of racing coursing through the air!", "I can't wait to see who wins this one!"]
				# {Obstacle description: { Intelligent solution: cost, Unintelligent solution: (attempt cost, fail cost) }, ... }
race_obstacles = {
	"A boulder has crashed onto the track, falling straight in front of {}!": {"{} maneuvers around the huge rock!": 5, "{} tries to dig through the boulder!": (3, 10)},
	"{}'s boat approaches a massive iceberg!": {"{} climbs over the mountain of ice!": 7, "{} attempts to swim under the iceberg!": (5, 20)},
	"A large dog has run onto the track, locking eyes with {}!": {"{} hides behind a human, unseen by the canine!": 8, "{} attempts to beat up the dog!": (3, 25)},
	"A kraken has rises out of the sea and attacks {}!": {"Luckily, {} suspected this might happen and brought anti-tank weaponry! The kraken is defeated!": 2, "{} attempts to swim past the kraken!": (2, 45)},
	"Somebody has thrown a molotov cocktail at {}, who is now on fire!": {"{} remembers to stop, drop, and roll, and continues the race unscathed!": 6, "{} attempts to power through it!": (0, 20)},
	"A flock of ducks flies overhead, conspiring to distract {}!": {"{} only looks at the ducks for a second, and pushes onward!": 1, "{} attempts to leap into the sky to catch a duck!": (4, 8)},
	"A nearby volcano spews molten lava directly in front of {}!": {"{} stays well away from the lava and continues safely!": 3, "{} attempts to run straight through the lava!": (0, 30)},
	"A downpur of acid rain begins directly above {}!": {"But {} checked the weather forecast beforehand and remembered to bring an umbrella!": 3, "{} attempts to power through it!": (0, 20)},
	"Lord Voldemort apparates onto the track and casts a spell of slowness on {}!": {"{} casts Protego and deflects the bulk of the spell!": 5, "{} attempts to beat up Voldemort to nullify the spell!": (4, 10)},
	"Darth Vader approaches, claiming to be {}'s father!": {"But {} searched its feelings and knew it not to be true!": 5, "{} grabs its lightsaber and duels Vader!": (10, 10)}
}
race_finishers = []
race_messages = ""
min_racers = 3		# Minimum number of cats in order to start a race


class Race(Command):
	def respond(self):
		super().respond()

		return "Hold your cats! I'm still constructing the racetracks! Come back in a few days/weeks/never."

		# Handle race already in progress
		# if any(database.query("SELECT reg_period, bet_period, count_period, race_period FROM Metadata;")):
		# 	return "Can't start a new race - race already in progress!"
		#
		# # Handle user already did /race today
		# if get_user_data(uid, "has_raced"):
		# 	return "Sorry, {}, you've already used your daily Stuart's Cat Races Token™ to start a race!".format(name)
		#
		# # Handle not enough racecats (at least 3)
		# data_cats = database.query("SELECT * FROM Cats WHERE is_racecat = True;", False)
		# if len(data_cats) < min_racers:
		# 	return "Only {} cats are registered for the race. At least {} must be registered to start a race.".format(len(data_cats), min_racers)

		# Set this user's has_raced to true
		# set_user_data(uid, "has_raced", True)

		# # Begin registration period
		# set_metadata("reg_period", True)
		#
		# # Start a race
		# start_race()


#
# Begin a cat race.
#
def start_race():
	print("Starting a cat race...")

	# Announce race start
	start_announcement = """
= = = = = = = = = = = =
{}'S CAT RACES™ #{}
= = = = = = = = = = = =

Welcome, one and all! I'm {} and I'll be your announcer today!
I'm here for today's cat races in {}, {}, and {}
Without further ado, let's start the registration period!

Everyone gets 5 minutes to register their racecats using "/racecat", \
starting now! If you've already registered a racecat, it will automatically \
be registered for this race, but you are still allowed to change your \
designated racecat. Note: during the registration period, you CANNOT withdraw \
your cat from the race, but you CAN swap it out for another one of your cats.

	BEGIN REGISTRATION PERIOD
	""".format(
	bot_name.upper(),
	database.get_metadata("race_number"),
	bot_name.capitalize(),
	random.choice(race_cities),
	random.choice(race_countries),
	random.choice(race_comments)
	)
	message_lib.send_message(start_announcement, [])

	# Wait 4 minutes
	wait(4 * 60)

	message_lib.send_message("Only one minute remaining to register your cats! After this, \
	your racecats are locked in!", [])

	# Wait 1 minute
	wait(60)

	# Begin betting period
	databse.set_metadata("reg_period", False)
	databse.set_metadata("bet_period", True)

	message_lib.send_message("""Your racecats are now locked in and are on their way to the \
starting gates! While our expert cat handlers prepare the racecats, let's \
place some bets!

Use "/racers" to see who's racing, and "/bet <amount> <cat name>" to place a \
bet on who you think will win the race! The race starts in 5 minutes, so bet \
fast!

	BEGIN BETTING PERIOD""", [])

	# Wait 4 minutes
	wait(4 * 60)

	message_lib.send_message("We're down to the last minute before the race starts! If you \
	still need to place a bet, hurry up and get it in!")

	# Wait 1 minute
	wait(60)

	# End betting period
	databse.set_metadata("bet_period", False)
	databse.set_metadata("count_period", True)

	# Get racecats
	data_cats = database.query("SELECT * FROM Cats WHERE is_racecat = True;", False)
	racecats = []
	for dc in data_cats:
		racecats.append(Cat(*dc))

	# Begin actual race
	race(racecats)


#
# The actual body of the race, from countdown to finish
#
def race(cats):

	message_lib.send_message("The bets are locked in and the racecats are ready!\n\nBEGIN COUNTDOWN", [])
	wait(2)

	# Begin race for any early starters
	for cat in cats:
		cat.race_wait_to_start()

	# send_message("10, 9, 8...")
	# wait(3)
	# send_message("7, 6, 5, 4...")
	# wait(4)
	# send_message("3, 2, 1...")
	# wait(3 + random.randrange(0, 8))
	message_lib.send_message("GO!")

	# Update race period
	databse.set_metadata("count_period", False)
	databse.set_metadata("race_period", True)

	# Start race for fair starters
	threads = []
	for cat in cats:
		threads.append(threading.Thread(target = cat.race_run()))

	# Simultaneously start all the cats
	for thread in threads:
		thread.start()

	# Wait until all the cats are done
	for thread in threads:
		thread.join()

	end_race()


def end_race():

	flush_race_messages()

	message_lib.send_message("dats it son")

	# Update race period to false
	databse.set_metadata("race_period", False)


#
# Consider pooling race messages here so the chat doesn't get spammed too much
#
def send_race_message(msg):
	message_lib.send_message(msg, [])

	global race_messages

	if len(race_messages) + len(msg) > 450:
		message_lib.send_message(race_messages)
		race_messages = msg
	else:
		race_messages += "\n\n{}".format(msg)


#
# Send anything left in race_messages
#
def flush_race_messages():
	if len(race_messages) > 0:
		send_message(race_messages)
