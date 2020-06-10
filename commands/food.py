import database
import objects
from helper import string_from_words, prep_name
from commands.command import Command


class Food(Command):
	def respond(self):
		super().respond()

		# Get target UID
		if len(self.args) == 0:
			target = self.uid
			target_name = self.name
		else:
			# Handle nonexistent target
			target_name = string_from_words(self.args)
			try:
				target = database.query("""
					SELECT uid
					FROM Data
					WHERE LOWER(name) = '{}';
					""".format(prep_name(target_name)))[0][0]
			except IndexError:
				return "I could not find the human you call \"{}\".".format(target_name)

		# Get list of food objects
		foods = database.query("""
			SELECT brand, owner, amount
			FROM Food
			WHERE owner = '{}'
			ORDER BY brand;
			""".format(target))
		for i in range(0, len(foods)):
			foods[i] = objects.Food(*foods[i])

		# Handle no foods
		if len(foods) == 0:
			return "{} currently does not own any food.".format(target_name)

		# Print food list
		result = "{}'s foods:\n".format(target_name)
		for i in range(0, len(foods)):
			result += "(#{}) {}\n".format(i + 1, foods[i])

		return result
