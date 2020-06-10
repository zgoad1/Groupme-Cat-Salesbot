import database
import message_lib
from helper import money_from_word, string_from_words, prep_name
from commands.command import Command


class Pay(Command):
	def respond(self):
		# Handle incorrect usage
		try:
			# Parse args for amount and recipient
			amount = money_from_word(self.args[0])
			recipient = string_from_words(self.args[1:])
		except:
			return self.usage()

		# Get recipient's uid and funds, handle nonexistent recipient
		try:
			recipient_uid = database.query("""
				SELECT uid
				FROM Data
				WHERE LOWER(name) = '{}';
				""".format(prep_name(recipient)))[0][0]
		except IndexError:
			return "I could not find the human you call '{}'.".format(recipient)
		recipient_money = database.get_user_data(recipient_uid, "money")

		# Handle insufficient funds
		if amount > self.money:
			return "You do not have enough Stuart Dollars™ for this transaction."

		# Handle paying self
		if self.uid == recipient_uid:
			return "That's not how this works."

		# Handle negative amount
		if amount < 0:
			if self.uid == message_lib.tristan:
				database.set_user_data(self.uid, "money", self.money + amount)
				return "No Tristan, you can't steal money. (-${})".format(abs(amount))
			elif self.uid != message_lib.father:
				return "You're not my dad!"

		# Execute the transaction
		database.set_user_data(self.uid, "money", self.money - amount)
		database.set_user_data(recipient_uid, "money", recipient_money + amount)
		return "Sent ${} to {}.".format(amount, recipient)
