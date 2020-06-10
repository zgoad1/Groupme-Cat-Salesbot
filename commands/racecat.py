import database
import objects
from helper import string_from_words, prep_name
from commands.command import Command

class Racecat(Command):
	def respond(self):
		super().respond()

		# When supplied with no args, return the user's designated racecat,
		# or the usage if they have none
		if len(self.args) == 0:
			try:
				data_racecat = database.query("""
					SELECT *
					FROM Cats
					WHERE owner = '{}' AND is_racecat = True;
					""".format(self.uid))[0]
			except IndexError:
				# No racecat, return usage
				return self.usage() + "\n(You do not currently have a designated racecat.)"
			else:
				racecat = objects.Cat(*data_racecat)
				return "{}, your designated racecat is:\n{}".format(self.name, racecat)

		# Handle nonexistent cat / Get cat
		cat_name = string_from_words(self.args)
		try:
			data_cat = database.query("""
				SELECT *
				FROM Cats
				WHERE owner = '{}' AND LOWER(name) = '{}';
				""".format(self.uid, prep_name(cat_name)))[0]
		except IndexError:
			return "{}, you do not own a cat by the name of \"{}\"".format(
				self.name, cat_name
			)
		cat = objects.Cat(*data_cat)

		# Handle in betting period
		if database.get_metadata("bet_period"):
			return "Your tried to withdraw your cat from the race, but the officials wouldn't let you.\n(Racecats are locked in during betting period.)"

		# If this cat is their racecat, unset it UNLESS we're in the registration period
		if cat.is_racecat:
			if not database.get_metadata("reg_period"):
				cat.is_racecat = False
				cat.update_database()
				return "{}, who was previously your registered racecat, is no longer.".format(cat.name)
			else:
				return "{} is already your racecat!\n(Can't withdraw during registration period.)".format(cat.name)

		# Unset the cat who is their racecat
		try:
			data_racecat = database.query("""
				SELECT *
				FROM Cats
				WHERE owner = '{}' AND is_racecat = True;
				""".format(self.uid))[0]
		except IndexError:
			# ...unless they don't have one
			pass
		else:
			racecat = objects.Cat(*data_racecat)
			racecat.is_racecat = False
			racecat.update_database()

		# Set the specified cat as the user's racecat
		cat.is_racecat = True
		cat.update_database()

		return "{} is now your designated racecat, {}.".format(cat.name, self.name)
