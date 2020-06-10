import database
import time
import random
from message_sending import send_message
from helper import money_from_word
from commands.command import Command


class Bet(Command):
	def respond(self):
		super().respond()

		# I'm making this a bet on a coin toss until I finish cat races

		# Handle incorrect usage
		try:
			amount = money_from_word(self.args[0])
			side = self.args[1][0].lower()
			if side != 'h' and side != 't':
				 raise ValueError("Invalid coin side")
		except:
			return self.usage()

		# Handle insufficient funds
		if amount > self.money:
			return "Sorry, {}, you can't afford to bet ${}!".format(self.name, amount)

		# Handle zero or negative amount
		if amount < 1:
			return "No, {}, it doesn't work that way.".format(self.name)

		# Execute the coin toss
		time.sleep(0.5)
		if side == 'h':
			side_string = "HEADS"
		else:
			side_string = "TAILS"
		send_message("{} bets ${} that the coin lands on {}.\nFlipping the coin...".format(self.name, amount, side_string))

		time.sleep(1 + random.randrange(1, 7))

		toss_result = random.random()
		if side == 'h':
			if toss_result < 0.6:
				# Correct
				database.set_user_data(self.uid, "money", self.money + amount)
				side_string = "HEADS"
				sign = "+"
			else:
				# Too bad
				database.set_user_data(self.uid, "money", self.money - amount)
				side_string = "TAILS"
				sign = "-"
		else:
			if toss_result > 0.4:
				# Correct
				database.set_user_data(self.uid, "money", self.money + amount)
				side_string = "TAILS"
				sign = "+"
			else:
				database.set_user_data(self.uid, "money", self.money - amount)
				# Too bad
				side_string = "HEADS"
				sign = "-"

		return "The result is {}! ({}${})".format(side_string, sign, amount)









		###############
		# CAT BETTING #
		###############


		# # Handle incorrect usage
		# try:
		# 	# Parse amount
		# 	amount = money_from_word(args[0])
		# except:
		# 	return "Bet money on a racecat.\nUsage:\n/bet <amount> <cat name>"
		#
		# # Withdraw bet if amount is 0
		# if amount == 0:
		# 	database.query("UPDATE Data SET bet_amount = 0, bet_cat = NULL WHERE uid = '{}';".format(uid))
		# 	return "{} withdraws their bet.".format(name)
		#
		# # Handle incorrect usage (1 arg is accepted if it's just 0, otherwise we need more args)
		# try:
		# 	# Parse cat name
		# 	cat_name = string_from_words(args[1:])
		# except:
		# 	return "Bet money on a racecat.\nUsage:\n/bet <amount> <cat name>"
		#
		# # Handle insufficient funds
		# if amount > money:
		# 	return "{}: You can't afford to bet ${}!".format(amount)
		#
		# # Handle negative amount
		# if amount < 0:
		# 	if uid == tristan:
		# 		# If it's Tristan, make him bet all his money.
		# 		amount = money
		# 	else:
		# 		return "No, {}, you can't do that.".format(name)
		#
		# # Handle nonexistent racecat / Get cat
		# data_cat = database.query("SELECT * FROM Cats WHERE name = '{}' AND is_racecat = True;".format(cat_name))
		# if data_cat is None:
		# 	return "{}: I couldn't place your bet because I couldn't find a racecat named \"{}\". Make sure you spelled it correctly.".format(name, cat_name)
		# cat = objects.get_cat(*data_cat)
		#
		# # TODO: Handle not in bet period
		#
		# # Determine if this user has already made a bet
		# current_amount = get_user_data(uid, "bet_amount")
		# if current_amount > 0:
		# 	already_bet = True
		# else:
		# 	already_bet = False
		#
		# # Store bet in database
		# database.query("UPDATE Data SET bet_amount = {}, bet_cat = '{}' WHERE uid = '{}';".format(amount, cat.name, uid))
		# if already_bet:
		# 	return "{} changes their bet to ${} on {}.".format(name, amount, cat.name)
		# else:
		# 	return "{} bets ${} on {}.".format(name, amount, cat.name)
