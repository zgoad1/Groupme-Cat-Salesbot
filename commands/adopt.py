import database
import objects
from helper import string_from_words
from commands.command import Command


class Adopt(Command):
	def respond(self):
		super().respond()

		# Handle incorrect usage
		try:
			cat_index = int(self.args[0])
			cat_name = string_from_words(self.args[1:])
		except:
			return self.usage()

		# Handle index not found
		try:
			shopcat = database.query("""
				SELECT breed, sex, level
				FROM Shop_Cats
				WHERE index = {};
				""".format(cat_index))[0]
		except IndexError:
			return "Cat #{} does not exist.".format(cat_index)

		# Handle insufficient funds
		price = database.query("""
			SELECT price
			FROM Shop_Cats
			WHERE index = {};
			""".format(cat_index))[0][0]
		if self.money < price:
			return "Sorry, but you can't afford ${} for that cat. Try posting pictures of cats or betting on cat races to earn more money.".format(price)

		# Handle too long name
		if len(cat_name) > 32:
			return "Do you really want to type that out every time you refer to your cat? (Pick a shorter name!)"

		# Handle name containing symbols
		if ' vs ' in cat_name:
			return "You can't have the string ' vs ' in your cat's name, because then it would confuse me if you tried to battle it! Pick another name!"

		# Handle duplicate name
		try:
			print("Attempted to give a cat a non-unique name")
			dupe_owner = database.query("""
				SELECT owner
				FROM Cats
				WHERE LOWER(name) = '{}'
				""".format(cat_name.lower().replace("'", "''")))[0][0]
			username = database.get_user_data(dupe_owner, "name")
			return "Cat names must be unique! {} already has a cat named \"{}\".".format(username, cat_name)
		except IndexError:
			print("Successfully named the cat")

		# Handle too many cats
		numcats = len(database.query("""
			SELECT *
			FROM Cats
			WHERE owner = '{}';
			""".format(self.uid)))
		if numcats >= 8:
			return "Sorry, {}, but I can't give you another cat. You have too many!\n(Use /consume to decrease your cat total!)".format(self.name)

		# Transfer the cat to the new owner
		# Remove from Shop_Cats and decrement any indices past this one
		database.query("""
			DELETE FROM Shop_Cats
			WHERE index = {};
			""".format(cat_index))
		database.query("""
			UPDATE Shop_Cats
			SET index = index - 1
			WHERE index > {};
			""".format(cat_index))
		# Insert into Cats
		newcat = objects.Cat(cat_name, self.uid, shopcat[0], False,
			shopcat[2], sex = shopcat[1])
		newcat.add_to_database()

		# Deduct funds from the new owner
		database.set_user_data(self.uid, "money", self.money - price)

		# Add happiness to the new owner
		database.set_user_data(self.uid, "happiness",
			database.get_user_data(self.uid, "happiness") + 25)

		return "Congratulations, {}! You have adopted {} the {}! (-${})".format(
			self.name, cat_name, shopcat[0], price)
