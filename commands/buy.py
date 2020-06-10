import objects
import database
from commands.command import Command


class Buy(Command):
	def respond(self):
		super().respond()

		# Handle incorrect usage
		try:
			# Parse arguments
			index = int(self.args[0])
			amount = int(self.args[1])
		except:
			return self.usage()

		# Handle nonexistent food
		try:
			shopfood = database.query("""
				SELECT brand, price
				FROM Shop_Food
				WHERE index = '{}';
				""".format(index))[0]
			price = shopfood[1]
			brand = shopfood[0]
		except IndexError:
			return "Food #{} does not exist.".format(index)

		# Handle insufficient funds
		total = price * amount
		if total > self.money:
			return "You cannot afford ${} worth of food.".format(total)

		# Handle 0 amount
		if amount == 0:
			return "{} leaves the food store empty-handed.".format(self.name)

		# Give the food to the user
		newfood = objects.Food(brand, self.uid, amount)
		newfood.add_to_database()

		# Deduct funds from the new owner
		database.set_user_data(self.uid, "money", self.money - total)

		return "{} bought {} bag(s) of {}. (-${})".format(self.name, amount, brand, total)
