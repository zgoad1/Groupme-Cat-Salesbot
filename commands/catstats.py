import database
import objects
from helper import string_from_words, prep_name
from commands.command import Command


class Catstats(Command):
	def respond(self):
		super().respond()

		# Handle incorrect usage
		try:
			cat_name = string_from_words(self.args)
		except:
			return self.usage()

		# Handle nonexistent cat
		try:
			cat = database.query("""
				SELECT *
				FROM Cats
				WHERE LOWER(name) = '{}';
				""".format(prep_name(cat_name)))[0]
		except IndexError:
			return "No one owns a cat named \"{}\".".format(cat_name)

		# Print the cat's stats
		return objects.Cat(*cat).stats_string()
