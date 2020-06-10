import database
import objects
from commands.command import Command


class Shop(Command):
	def respond(self):
		super().respond()

		# Handle bad usage
		try:
			shop = self.args[0].lower()
			if shop != "cats" and shop != "food":
				raise ValueError("Invalid shop type")
		except:
			return self.usage()

		# Open the appropriate shop
		if shop == "cats":
			return shop_cats()
		else:
			return shop_food()


#
# Get a string representation of each cat from the shop, conCATenate them, and
# return the result
#
def shop_cats():

	print("Opening cat shop")

	# Get list of ShopCat objects
	cats = database.query("SELECT * FROM Shop_Cats ORDER BY index;")
	if cats is None or len(cats) == 0:
		return "Sorry, all my cats have been adopted. Wait until tomorrow!"
	shopcats = []
	for c in cats:
		shopcats.append(objects.ShopCat(c[0], c[1], c[2], c[3], c[4]))

	# Get string of ShopCats
	result = "Here are my available felines:\n\n"
	for i in range(0, len(shopcats) - 1):
		result += "{}\n= = = = = = = = = = = =\n".format(shopcats[i])
	result += str(shopcats[len(shopcats) - 1])

	return result


#
# Get a string representation of each food from the shop, concatenate them, and
# return the result
#
def shop_food():

	print("Opening food shop")

	# Get list of ShopFood objects
	foods = database.query("SELECT * FROM Shop_Food ORDER BY index;")
	shopfoods = []
	for f in foods:
		shopfoods.append(objects.ShopFood(f[0], f[1], f[2]))

	# Get string of ShopFoods
	result = "Here are my available foods:\n\n"
	for i in range(0, len(shopfoods) - 1):
		result += "{}\n= = = = = = = = = = = =\n".format(shopfoods[i])
	result += str(shopfoods[len(shopfoods) - 1])

	return result
