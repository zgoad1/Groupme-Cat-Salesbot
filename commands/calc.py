import random
import re
from helper import string_from_words
from commands.command import Command


class Calc(Command):
	def respond(self):
		super().respond()

		# Check usage
		if len(self.args) == 0:
			return self.usage()

		# Prevent SQL injection
		if re.search("[a-zA-Z]", string_from_words(self.args)):
			return "Ahem.\nUsage:\n/calc < M A T H >"

		# If the user is in debt, respond with their debt amount
		if self.money < 0:
			return self.money

		# Provide the correct calculation result unless the input is '9 + 10'
		# or the bot feels like saying '69'
		if random.random() < 0.069:
			return 69
		if len(self.args) == 3 and self.args[0] == '9' and self.args[1] == '+' and self.args[2] == '10':
			return 21
		result = eval(''.join(str(i) for i in self.args))
		return result
