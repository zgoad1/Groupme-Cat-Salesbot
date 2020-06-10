import random


cities = ["Baton Rouge", "New Orleans", "Lake Charles", "Tokyo", "London",
	"Beijing", "Orlando", "New York City", "San José", "Santiago", "Dakar",
	"Madrid", "Berlin", "Rome", "Paris", "Oslo", "Helsinki", "Mumbai",
	"Shanghai", "Sydney", "Newcastle", "Wellington", "Cat City", "Cat Forest"]
countries = ["Louisiana", "Texas", "Florida", "California", "China",
	"Australia", "England", "Greece", "Portugal", "France", "Antarctica",
	"Catland", "Senegal", "Egypt", "Brazil", "Canada", "Peru", "Greenland",
	"Germany", "South Africa", "Russia", "India", "Colorado", "Montana",
	"Norwegia", "Norway", "Sweden"]


def get_location():
    city = random.choice(cities)
    country = random.choice(countries)
    return "{}, {}".format(city, country)
