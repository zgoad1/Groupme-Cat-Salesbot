import database
import math
import random
from helper import prep_name
from message_sending import send_message


class User:
	def __init__(self, uid, name, messages_sent, words_sent, happiness, money):
		self.uid = uid
		self.name = name
		self.messages_sent = messages_sent
		self.words_sent = words_sent
		self.happiness = happiness
		self.money = money

class Cat:
	def __init__(self, name, owner, breed, is_racecat, level, exp = 0,
		speed = 0, power = 0, intel = 0, cool = 0, cute = 0, luck = 0,
		wins = 0, losses = 0, sex = 'F', times_fed = 0, battle_streak = 0):
		self.name = name
		self.owner = owner
		self.breed = breed
		self.sex = sex
		self.is_racecat = is_racecat
		self.level = level
		self.exp = exp
		self.speed = speed
		self.power = power
		self.intel = intel
		self.cool = cool
		self.cute = cute
		self.luck = luck
		self.wins = wins
		self.losses = losses
		self.times_fed = times_fed
		self.battle_streak = battle_streak

	def __str__(self):
		result = "{} the {}, {}, Level {}".format(
			self.name, self.breed, self.sex, self.level)
		if self.is_racecat:
			result += " (Racecat)"
		return result

	def breed_stats(self):
		return database.query("""
			SELECT speed, power, intel, cool, cute, luck
			FROM Breed
			WHERE name = '{}';
			""".format(self.breed))[0]

	def stats(self):
		bs = self.breed_stats()
		return (
			round(bs[0] * 10 + (self.level - 1) * 0.5 * bs[0] + self.speed),
			round(bs[1] * 10 + (self.level - 1) * 0.5 * bs[1] + self.power),
			round(bs[2] * 10 + (self.level - 1) * 0.5 * bs[2] + self.intel),
			round(bs[3] * 10 + (self.level - 1) * 0.5 * bs[3] + self.cool),
			round(bs[4] * 10 + (self.level - 1) * 0.5 * bs[4] + self.cute),
			round(bs[5] * 10 + (self.level - 1) * 0.5 * bs[5] + self.luck)
		)

	def stats_string(self):
		stats = self.stats()
		result = """{0}:
			{1:20}{2:>6d}

			{3:20}{4:>6d}
			{5:20}{6:>6d}
			{7:20}{8:>6d}
			{9:20}{10:>6d}
			{11:20}{12:>6d}
			{13:20}{14:>6d}

			{15:20}{16:>6d}
			{17:20}{18:>6d}""".format(
			self.name,
			"Level", self.level,
			"Speed", stats[0],
			"Power", stats[1],
			"Intelligence", stats[2],
			"Coolness", stats[3],
			"Cuteness", stats[4],
			"Luck", stats[5],
			"Competition Wins", self.wins,
			"Competition Losses", self.losses
			).replace(' ', '_')
		return result

	def eat(self, food):
		print("{} is consuming a food item".format(self.name))

		# Get exp yield from price
		exp = database.query("""
			SELECT price
			FROM Brand
			WHERE name = '{}';
			""".format(food.brand))[0][0]

		# Check for level up
		self.exp += exp
		level_gain = math.floor(self.exp / 100)
		self.exp %= 100

		# Get stat gains by food brand
		gains = database.query("""
			SELECT speed, power, intel, cool, cute, luck
			FROM Brand
			WHERE name = '{}';
			""".format(food.brand))[0]

		# Initialize output string
		result = "{} ate a bowl of {}.\n\n".format(self.name, food.brand)

		# Apply gains to stats & result string
		if gains[0] > 0:
			self.speed += gains[0]
			result += "+{} Speed\n".format(gains[0])
		if gains[1] > 0:
			self.power += gains[1]
			result += "+{} Power\n".format(gains[1])
		if gains[2] > 0:
			self.intel += gains[2]
			result += "+{} Intelligence\n".format(gains[2])
		if gains[3] > 0:
			self.cool += gains[3]
			result += "+{} Coolness\n".format(gains[3])
		if gains[4] > 0:
			self.cute += gains[4]
			result += "+{} Cuteness\n".format(gains[4])
		if gains[5] > 0:
			self.luck += gains[5]
			result += "+{} Luck\n".format(gains[5])

		# Remove that food from the database
		food.consume()

		self.times_fed += 1

		# Send comprehensive message
		send_message(result, [])

		# Update the cat's data with the new stats
		self.update_database()

		# Apply level-ups
		for i in range(0, level_gain):
			self.level_up()

	def level_up(self):
		stats_bef = self.stats()
		self.level += 1
		stats_aft = self.stats()

		result = """
		{0} leveled up to {1}!
		+{2} {3}
		+{4} {5}
		+{6} {7}
		+{8} {9}
		+{10} {11}
		+{12} {13}
		""".format(
		self.name, self.level,
		stats_aft[0] - stats_bef[0], "Speed",
		stats_aft[1] - stats_bef[1], "Power",
		stats_aft[2] - stats_bef[2], "Intelligence",
		stats_aft[3] - stats_bef[3], "Coolness",
		stats_aft[4] - stats_bef[4], "Cuteness",
		stats_aft[5] - stats_bef[5], "Luck")

		send_message(result, [])

		# Hatch eggs at level 10
		if self.level >= 10 and self.breed == "Egg":
			egg_rarity = database.query("""
				SELECT rarity
				FROM breed
				WHERE name = 'Egg';
				""")[0][0]
			breeds = [tuple[0] for tuple in database.query("""
				SELECT name
				FROM breed
				WHERE rarity >= {} AND name != '{}';
				""".format(egg_rarity, self.breed))]

			new_breed = random.choice(breeds)
			self.breed = new_breed
			send_message("Wow! The egg hatched into a {}! Congratulations!".format(
				new_breed
			))

		self.update_database()

	def update_database(self):
		database.query("""
			UPDATE Cats
			SET is_racecat = {}, breed = '{}', level = {}, exp = {},
				speed = {}, power = {}, intel = {}, cool = {}, cute = {}, luck = {},
				wins = {}, losses = {}, times_fed = {}, battle_streak = {}
			WHERE LOWER(name) = '{}';
			""".format(self.is_racecat, self.breed, self.level, self.exp,
			self.speed, self.power, self.intel, self.cool, self.cute, self.luck,
			self.wins, self.losses, self.times_fed, self.battle_streak,
			prep_name(self.name)))

	def add_to_database(self):

		# Make sure this cat isn't already in the database
		try:
			me = database.query("""
				SELECT *
				FROM Cats
				WHERE LOWER(name) = '{}';
				""".format(prep_name(self.name)))[0]
		except IndexError:
			pass
		else:
			print("Attempted to add a duplicate cat to Cats.\nThis is the cat that already exists: {}".format(me))
			return

		# Insert the cat
		database.query("""
			INSERT INTO Cats
			VALUES ('{}', '{}', '{}', {}, {}, {},
				{}, {}, {}, {}, {}, {}, {}, {}, '{}', {}, {});
			""".format(self.name.replace("'", "''"), self.owner, self.breed,
				self.is_racecat, self.level, self.exp, self.speed, self.power,
				self.intel, self.cool, self.cute, self.luck, self.wins,
				self.losses, self.sex, self.times_fed, self.battle_streak
		))

	def stat_score(self, x):
		# Get that stat's influence over an event, from 0 to 1
		return -(1 / ((x + 25 / 3) / 75 + 1)) + 1

	def pronouns(self):
		if self.sex == 'F':
			return ("she", "her", "her")
		elif self.sex == 'M':
			return ("he", "him", "his")
		else:
			# If this was a person I would use "they" but this seems more
			# natural to say for cats
			return ("it", "it", "its")

	def race_run(self):
		print("{} starting race".format(self.name))

		# Run 3 laps
		for lap in range(1, 4):
			send_race_message("{} begins lap {}!".format(self.name, lap))

			# Run the first third of the lap
			self.race_lap_third(lap)

			# Check if this cat encounters an obstacle
			if random.random() > self.stat_score(self.luck):
				# Randomly determine type of obstacle
				obstacle = list(race_obstacles.keys())[random.randrange(0, len(race_obstacles))]
				if random.random() < self.stat_score(self.intel):
					# Intelligently overcome the obstacle
					method = list(race_obstacles[obstacle].keys())[0]
					delay = race_obstacles[obstacle][method]
					send_race_message("Oh no! {} {} (+{} sec.)".format(obstacle.format(self.name), method.format(self.name), delay))
				else:
					# Attempt to brute force the obstacle
					method = list(race_obstacles[obstacle].keys())[1]
					# Initialize delay to attempt cost
					delay = race_obstacles[obstacle][method][0]
					send_race_message("Oh no! {} {} (+{} sec.)".format(obstacle.format(self.name), method.format(self.name), delay))
					wait(delay)
					if random.random() < self.stat_score(self.power):
						# Successfully brute-forced the obstacle
						send_race_message("{} succeeds and continues racing! (+{} sec.)".format(self.name, delay))
					else:
						# Add failure time to delay
						delay += race_obstacles[obstacle][method][1]
						send_race_message("{} fails, but pushes onward! (+{} sec.)".format(self.name, delay))
						wait(race_obstacles[obstacle][method][1])

			# Run the second third of the lap
			self.race_lap_third(lap)

			# Check if this cat does something illegal
			#if random.random() > self.stat_score(self.intel):
				# Cheat somehow
				# TODO: this

			# Run the final third of the lap
			self.race_lap_third(lap)

		# Cat finished the race!
		race_finishers.append(self)
		if len(race_finishers) == 1:
			place = "1st"
		elif len(race_finishers) == 2:
			place = "2nd"
		elif len(race_finishers) == 3:
			place = "3rd"
		else:
			place = "{}th".format(len(race_finishers))
		send_race_message("{} has crossed the finish line, taking {} place!".format(self.name, place))

class Food:
	def __init__(self, brand, owner, amount):
		self.brand = brand
		self.owner = owner
		self.amount = amount

	def __str__(self):
		if self.amount > 1:
			word = "bags"
		else:
			word = "bag"
		return "{} {} of {}".format(self.amount, word, self.brand)

	def add_to_database(self):
		try:
			food_amount = database.query("""
				SELECT amount
				FROM Food
				WHERE owner = '{}' AND brand = '{}';
				""".format(self.owner, self.brand))[0][0]
			# If the user already has this brand of food, just add to their amount
			database.query("""
				UPDATE Food
				SET amount = {}
				WHERE owner = '{}' AND brand = '{}';
				""".format(food_amount + self.amount, self.owner, self.brand))
		except IndexError:
			# The user does not own this type of food, add a row
			database.query("""
				INSERT INTO Food
				VALUES ('{}', '{}', {});
				""".format(self.brand, self.owner, self.amount))

	def consume(self):
		# Get the amount of remaining food after this one is consumed
		new_amount = database.query("""
			SELECT amount
			FROM Food
			WHERE brand = '{}' AND owner = '{}';
			""".format(self.brand, self.owner))[0][0] - 1

		if new_amount > 0:
			# If we still have food left, just decrement the amount
			database.query("""
				UPDATE Food
				SET amount = {}
				WHERE brand = '{}' AND owner = '{}';
				""".format(new_amount, self.brand, self.owner))
		else:
			# If the amount has reached 0, remove the entire row
			database.query("""
				DELETE FROM Food
				WHERE brand = '{}' AND owner = '{}';
				""".format(self.brand, self.owner))

class ShopCat:
	def __init__(self, index, breed, sex, level, price):
		self.index = index
		self.breed = breed
		self.sex = sex
		self.level = level
		self.price = price

	def __str__(self):
		return """Cat #{}
			Breed: {}
			Sex: {}
			Level: {}
			Price: ${}""".format(self.index, self.breed, self.sex, self.level, self.price)

class ShopFood:
	def __init__(self, index, brand, price):
		self.index = index
		self.brand = brand
		self.price = price

	def __str__(self):
		return """Food #{}
			Type: {}
			Price: ${}""".format(self.index, self.brand, self.price)
