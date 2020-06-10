import database
from helper import string_from_words, prep_name
from commands.command import Command

class Stats(Command):
	def respond(self):
		super().respond()

		# Get target
		if len(self.args) == 0:
			# If called with no args, use self
			target_name = database.get_user_data(self.uid, "name")
			uid = self.uid
		else:
			# If called with args, parse args for name of target
			target_name = string_from_words(self.args)

			# Make sure we have data on that name
			try:
				uid = database.query("""
					SELECT uid
					FROM Data
					WHERE LOWER(name) = '{}';
					""".format(prep_name(target_name)))[0][0]
			except IndexError:
				return "I have no data on the human you call '{}'.".format(target_name)

		# Print stats
		money = database.get_user_data(uid, "money")
		result = "{}:".format(target_name)
		result += """
			{0:20}{1:>6d}
			{2:20}{3:>6d}
			{4:20}{5:>6d}
			{6:20}{7:>6d}
			""".format(
				"Messages Sent", database.get_user_data(uid, "messages_sent"),
				"Words Sent", database.get_user_data(uid, "words_sent"),
				"Happiness", database.get_user_data(uid, "happiness"),
				"Money", money).replace(' ', '_')
		if money < 0:
			result += "(Note: you owe me money. Please post cat pictures to earn money.)"

		return result
