import database
from helper import string_from_words, prep_name
from message_sending import send_message
from commands.command import Command
from commands.cancel import Cancel
from commands.reject import Reject


class Consume(Command):
	def respond(self):
		super().respond()

		# Handle incorrect arguments
		try:
			cat_name = string_from_words(self.args)
		except:
			return self.usage()

		# Handle no cat
		try:
			wins = database.query("""
				SELECT wins
				FROM Cats
				WHERE owner = '{}' AND LOWER(name) = '{}';
				""".format(self.uid, prep_name(cat_name)))[0][0]
		except IndexError:
			return "{}, you do not have a cat by the name of \"{}\".".format(self.name, cat_name)

		# Handle cat currently battling
		battles = database.query("""
			SELECT *
			FROM challenges
			WHERE (LOWER(challenger) = '{0}' OR LOWER(challengee) = '{0}')
				AND in_progress = 'True';
			""".format(prep_name(cat_name)))
		if len(battles) > 0:
			return "You must wait for {} to finish its challenge before you can eat it, you hungry imbecile!"

		# Calculate compensation for cat consumption
		reward = wins * 100

		# Cancel any challenges where this cat is the challenger
		try:
			id = database.query("""
				SELECT index
				FROM challenges
				WHERE LOWER(challenger) = '{0}';
				""".format(prep_name(cat_name)))[0][0]
		except IndexError:
			pass
		else:
			send_message(Cancel("cancel", [id], self.uid, "Stuart", 0).respond())

		# Reject any challenges where this cat is the challengee
		try:
			id = database.query("""
				SELECT index
				FROM challenges
				WHERE LOWER(challengee) = '{0}';
				""".format(prep_name(cat_name)))[0][0]
		except IndexError:
			pass
		else:
			send_message(Reject("reject", [id], self.uid, "Stuart", 0).respond())

		# Consume the cat
		database.query("""
			DELETE FROM Cats
			WHERE owner = '{}' AND LOWER(name) = '{}';
			""".format(self.uid, prep_name(cat_name)))

		# Add reward money
		database.set_user_data(self.uid, "money", self.money + reward)

		# Remove happiness
		database.set_user_data(self.uid, "happiness", database.get_user_data(self.uid, "happiness") - 25)

		# Output consumption feedback
		result = "Nom."
		if reward > 0:
			result += " (+${})".format(reward)
		return result
