import database
from helper import string_from_words
from commands.command import Command


class Desc(Command):
	def respond(self):
		super().respond()

		# Handle incorrect usage
		try:
			todesc = string_from_words(self.args)
		except:
			return self.usage()

		# Handle cat breed not found
		try:
			result = database.query("""
				SELECT descr
				FROM Breed
				WHERE LOWER(name) = '{}';
				""".format(todesc.lower()))[0][0]
		except IndexError:
			# Handle food brand not found
			try:
				result = database.query("""
					SELECT descr
					FROM Brand
					WHERE LOWER(name) = '{}';
					""".format(todesc.lower()))[0][0]
			except IndexError:
				result = "I could not find any cat or food by the name of '{}'.".format(todesc)

		return result;
