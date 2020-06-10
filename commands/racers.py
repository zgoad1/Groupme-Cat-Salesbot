import database
import objects
from helper import print_list
from commands.command import Command


class Racers(Command):
	def respond(self):
		super().respond()

		# Show list of all racecats, sorted by descending wins
		# (using the string representation of cats)

		data_cats = database.query("""
			SELECT *
			FROM Cats
			WHERE is_racecat = True
			ORDER BY wins DESC;
			""")

		# Handle no racecats
		if len(data_cats) == 0:
			return "Nobody currently owns a registered racecat."

		# Get list of racecats
		racecats = [objects.Cat(*cat) for cat in data_cats]

		# Get result string
		header = "Cats participating in the next race:"
		strings = []
		for rc in racecats:
			rc_owner = database.get_user_data(rc.owner, "name")
			strings.append("{}:\n\t{}\n\tWins: {}".format(rc_owner, rc, rc.wins))
		return print_list(strings, header)
