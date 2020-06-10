import os
import datetime
import random
import psycopg2	as db	# Postgres integration
from helper import multi_split


cursor = None		# Handle by which we access the current position in the database
connection = None	# Handle by which we access the database as a whole


#
# Establish a connection to the database.
# Extract the credentials from the URL and return a connection.
#
def open_connection():
	global cursor
	global connection

	# Split the database URI into digestible parts
	uri = os.getenv("DATABASE_URL")
	split_uri = multi_split(uri, ['://', '@', ':', '/'])
	print(split_uri)

	# Use the data from the URI to connect
	connection = db.connect(dbname = split_uri[5], user = split_uri[1],
		password = split_uri[2], host = split_uri[3])
	cursor = connection.cursor()
	return connection


#
# Close the database connection. Must be called after open_connection().
#
def close_connection():
	cursor.close()
	connection.close()


#
# Execute a query on the database and print some helpful information.
# 'one' determines whether it should return a single row of data or a list
# of rows.
#
def query(query):

	# Execute query
	print("\nExecuting query:\n{}".format(query))
	cursor.execute(query)
	connection.commit()

	if query.split()[0].upper() == "SELECT":
		# If it was a SELECT query, return the result
		result = cursor.fetchall()
	else:
		# Otherwise not a SELECT query, so no result
		result = None

	print("Query result:\n{}".format(result))
	return result


#
# Get the value of a single attribute of one user from the Data table.
#
def get_user_data(uid, attribute):
	try:
		return query("""
			SELECT {}
			FROM Data
			WHERE uid = '{}';
			""".format(attribute, uid))[0][0]
	except IndexError:
		print("Tried to access nonexistent user attribute!")
		return None


#
# Set arbitrary data in the table.
#
def set_user_data(uid, attribute, value):
	if type(value) == type(""):
		# Value is a string, add quotes around it in the query
		query_string = """
			UPDATE Data
			SET {} = '{}'
			WHERE uid = '{}';
			""".format(attribute, value, uid)
	else:
		# Attribute is not a string, do not add quotes
		query_string = """
			UPDATE Data
			SET {} = {}
			WHERE uid = '{}';
			""".format(attribute, value, uid)
	query(query_string)


#
# Get a value from the Metadata table.
#
def get_metadata(attribute):
	return query("SELECT {} FROM Metadata;".format(attribute))[0][0]


#
# Set a value in the Metadata table.
#
def set_metadata(attribute, value):
	query("UPDATE Metadata SET {} = {};".format(attribute, value))


#
# Add an entire row to the Data table.
#
def add_user(uid, name):
	query_string = """
		INSERT INTO Data
		VALUES ('{}', '{}', 0, 0, 0, 0, False, 0, NULL);
		""".format(uid, name)
	query(query_string)


#
# Determine if today is later than the date that Metadata.shop_update was last
# updated. If so, set Metadata.shop_update to today.
#
def update_day():
	print("Updating date")

	try:
		# Throws TypeError when shop_update has never been set
		last_update = get_metadata("shop_update")

		# Finish if it's not a new day
		if last_update == datetime.date.today():
			return

	except IndexError:
		# If it has never been updated, add the current date
		query("INSERT INTO Metadata VALUES (NOW());");

	# It's a new day
	print("Updating day-based events")

	# Update the shop
	query("UPDATE Metadata SET shop_update = NOW();")
	update_shop()

	# Reset hunger for all cats
	query("UPDATE Cats SET times_fed = 0;")

	# Reset has_raced for all users
	query("UPDATE Data SET has_raced = False;")

	# Update allowance boolean
	query("UPDATE Data SET paid = False;")


#
# If the cat & food shops must be updated, do so.
# Updating the shops involves choosing randomly from all possible foods and cats
# and placing the chosen ones in the shop.
#
def update_shop():

	# Clear the shop
	query("DELETE FROM Shop_Cats;")
	query("DELETE FROM Shop_Food;")

	# Choose 3 to 6 random cats to put in the shop
	breeds = query("SELECT * FROM Breed;")
	amount = random.randrange(3, min(6, len(breeds)) + 1)
	chosen = []
	while len(chosen) < amount:

		cat = random.choice(breeds)

		# If our random number is greater than its rarity, put it in
		if random.randrange(1, 11) >= cat[8]:

			# Randomly determine sex
			if random.random() < 0.5:
				sex = 'M'
			else:
				sex = 'F'

			# Randomly determine level
			lvl_rand = random.random()
			if lvl_rand < 0.5:
				lvl = 1
			elif lvl_rand < 0.75:
				lvl = 2
			elif lvl_rand < 0.875:
				lvl = 3
			elif lvl_rand < 0.95:
				lvl = 4
			else:
				lvl = 5

			# Determine price
			new_price = round(cat[9] + (lvl - 1) * cat[9] * 0.25)

			# Create a ShopCat and add it to the list
			chosen.append([len(chosen) + 1, cat[0], sex, lvl, new_price])

	for cat in chosen:
		query("""
			INSERT INTO Shop_Cats
			VALUES ({}, '{}', '{}', {}, {});
			""".format(*cat))

	# Choose 5 random foods to put in the shop
	foods = query("SELECT * FROM Brand;")
	amount = 5
	chosen = []
	while len(chosen) < amount:
		food = random.choice(foods)
		# If our random number is greater than its rarity, put it in
		if random.randrange(1, 11) >= food[8]:
			chosen.append([len(chosen) + 1, food[0], food[9]])
			# Remove the food from the list since we can't have duplicates here
			foods.remove(food)

	for food in chosen:
		query("""
		INSERT INTO Shop_Food
		VALUES ({}, '{}', {});
		""".format(*food))
