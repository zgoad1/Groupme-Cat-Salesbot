import database
import objects
from helper import string_from_words, prep_name
from commands.command import Command


class Cats(Command):
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

		# Get list of cat objects
		cats = database.query("""
			SELECT *
			FROM Cats
			WHERE owner = '{}'
			ORDER BY level DESC;
			""".format(target))
		for i in range(0, len(cats)):
			cats[i] = objects.Cat(*cats[i])

		# Handle no cats
		if len(cats) == 0:
			return "{} does not own any cats. How sad for them.".format(target_name)

		# Print cat list
		result = "{}'s cats:\n".format(target_name)
		for i in range(0, len(cats)):
			result += "{}\n".format(cats[i])

		return result
