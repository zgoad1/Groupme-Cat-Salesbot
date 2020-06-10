import database
import objects
from helper import string_from_words, prep_name
from commands.command import Command


food_per_day = 3	# How many times per day a cat may be fed


class Feed(Command):
	def respond(self):
		super().respond()

		# Handle usage
		try:
			food_index = int(self.args[0]) - 1	# Subtract 1 to convert to array indexing
			cat_name = string_from_words(self.args[1:])
		except:
			return self.usage()

		# Handle nonexistent food / Get food
		try:
			data_food = database.query("""
				SELECT brand, owner, amount
				FROM Food
				WHERE owner = '{}'
				ORDER BY brand;
				""".format(self.uid))[food_index]
		except:
			return "{}, your food #{} does not exist.".format(self.name, food_index + 1)
		food = objects.Food(*data_food)

		# Handle nonexistent cat / Find cat
		try:
			data_cat = database.query("""
				SELECT *
				FROM Cats
				WHERE lower(name) = '{}';
				""".format(prep_name(cat_name)))[0]
		except IndexError:
			return "No one owns a cat named \"{}\".".format(cat_name)
		cat = objects.Cat(*data_cat)

		# Handle full cat
		if cat.times_fed >= food_per_day:
			return "{} isn't hungry. Wait until tomorrow!".format(cat_name)

		# Feed the specified food to the cat
		cat.eat(food)
		return
